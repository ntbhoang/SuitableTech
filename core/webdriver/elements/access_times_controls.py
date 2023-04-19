from selenium.webdriver.common.by import By
from data_test.dataobjects.enum import AccessTimesEventType, WeekDays
from core.webdriver.elements.element_list import ElementList
from core.utilities.utilities import Utilities
from common.application_constants import ApplicationConst


class AccessTimesEventAttributes(object):
    
    def __init__(self, title, style):
        self._title = title
        self._attributes = {}
        
        if style:
            style_items = style.split(";")        
            for item in style_items:
                entry = item.split(":")
                if len(entry) > 1:
                    self._attributes[entry[0].strip()] = entry[1].strip()

    def get_attributes(self):
        return self._attributes
    
    def get_attribute(self, attr_name):
        return self._attributes[attr_name] if attr_name in self._attributes else None


class WeekviewEvent(object):
    
    def __init__(self):
        self._is_all_day = False
        self._time_range = ""
        self._is_valid = False
        self._event_type = AccessTimesEventType.AllMembers
        self._access_days = []
        
    def parse_event_data(self, web_elem_list, dict_header_info):
        if not web_elem_list:
            return
        
        title = web_elem_list[0]._title
        if ApplicationConst.LBL_ALL_MEMBERS in title:
            self._event_type = AccessTimesEventType.AllMembers                
            if web_elem_list[0]._title == ApplicationConst.LBL_ALL_MEMBERS:
                self._is_all_day = True
            else:
                self._is_all_day = False
                self._time_range = title.split("|")[0].strip()
        else:    
            self._event_type = AccessTimesEventType.Member
            if title.find("|") > 0:
                self._is_all_day = False
                self._time_range = title.split("|")[0].strip()
            else:
                self._is_all_day = True
                    
        access_day = []
        for web_elem in web_elem_list:
            left_offset = self.__find_left_offset(web_elem) + 4
            day = self.__find_week_day(left_offset, dict_header_info)
            if day:
                access_day.append(day)
        
        self._access_days = sorted(access_day, key=lambda c: c.value)
    
    def __find_left_offset(self, web_elem):
        val = web_elem.get_attribute("left")
        if val:
            _left = val.replace("px", "")
            if Utilities.is_number(_left):
                return int(float(_left))
        return 0
        
    def __find_week_day(self, left_offset, dict_header_info):
        for key in dict_header_info:
            left = dict_header_info[key][0]
            right = dict_header_info[key][1]
            if left <= left_offset <= right:
                return self.__find_week_day_by_name(key)
        return None
                
    def __find_week_day_by_name(self, day_title):
        for day in WeekDays:
            if day.name == day_title or ApplicationConst.get_date_time_label(day.name) == day_title:
                return day
        return None    
    
    def is_all_day(self):
        return self._is_all_day
    
    def is_valid(self):
        return self._is_valid
    
    def get_access_days(self):
        return self._access_days
    
    def get_label(self):
        if self._event_type == AccessTimesEventType.AllMembers:
            item_type = None
            if self.is_all_day():
                item_type = ApplicationConst.get_date_time_label("All day")
            elif self._time_range:
                item_type = ApplicationConst.get_date_time_label(self._time_range)
                
            if len(self._access_days) == 7:
                lbl = ApplicationConst.get_date_time_label("every day")
            else:
                lbl = ', '.join((ApplicationConst.get_date_time_label(d.name) for d in self._access_days))
            
            item_label = "{} {}".format(item_type, lbl)
            
            return item_label
        else:
            return "Not defined"

 
class WeekviewAllEvents(ElementList):
    
    def __init__(self, driver, by=By.XPATH, locator=None):
        ElementList.__init__(self, driver, by, locator)
    
    def parse_events(self, dict_header_info, event_title):
        elements = self._get_elements()
        
        if elements is None:
            raise Exception("Element list is not found!")
        
        # sort all event item by 'top' attribute to detect all related event
        by_top_dictionary = {}    
        for elem in elements:
            style = elem.get_attribute("style")
            
            try:    
                span = elem.find_element(By.XPATH, ".//span")
                if span:
                    title = span.text
                else:
                    title = "Unknown"
                
                # check expected event title
                if event_title and title.strip() != event_title:
                    continue
            except:
                try:
                    div_time = elem.find_element(By.XPATH, ".//div[@class='fc-event-time']")
                    div_title = elem.find_element(By.XPATH, ".//div[@class='fc-event-title']")
                    if div_time and div_title:
                        title = "{} | {}".format(div_time.text, div_title.text)
                    # check expected event title
                    if event_title and div_title.text.strip() != event_title:
                        continue
                except:
                    continue
            
            web_elem = AccessTimesEventAttributes(title, style)
            top_attr = web_elem.get_attribute("top")

            if not (top_attr and title):
                continue
            
            key = "{}-{}".format(title, top_attr)
            if key in by_top_dictionary:
                event_list = by_top_dictionary[key]
            else:
                event_list = []
                
            event_list.append(web_elem)
            # update dictionary
            by_top_dictionary[key] = event_list
        
        events = []
        for i in by_top_dictionary:
            web_elem_array = by_top_dictionary[i]
            if web_elem_array:
                event = WeekviewEvent()
                event.parse_event_data(web_elem_array, dict_header_info)
                events.append(event)
                
        return events


class WeekviewEventHeader(ElementList):
    
    def __init__(self, driver, by=By.XPATH, locator=None):
        ElementList.__init__(self, driver, by, locator)
        self._columns = {}
    
    def __find_width_attribute(self, web_element):
        width = 0
        try:
            style = web_element.get_attribute("style")
            style_items = style.split(";")
                   
            for item in style_items:
                entry = item.split(":")
                if len(entry) > 1 and entry[0].strip() == "width":
                    txt_width = entry[1].strip().replace('px', '')
                    if Utilities.is_number(txt_width):
                        width = int(txt_width)
                        break
        except:
            width = 0
            
        return width
                
    def parse_header_info(self):
        elements = self._get_elements()
        if elements is None:
                raise Exception("Element list is not found!")
        
        if len(elements) == 9:
            current_left = self.__find_width_attribute(elements[0])
        
            prev_width = 0
            last = (len(elements) - 1)
            for i in range(1, last):
                text = elements[i].text.split()[0]
                width = self.__find_width_attribute(elements[i])
                if width <= 0:
                    width = prev_width
                else:
                    prev_width = width
                
                self._columns[text] = [current_left, current_left + width]
                current_left += width
                
    def get_header_column_info(self):
        return self._columns
