from selenium.webdriver.common.by import By
from common.stopwatch import Stopwatch
from selenium.common.exceptions import StaleElementReferenceException,\
    WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
from time import sleep
from common.constant import Platform, Browser
from core.webdriver.exceptions import ElementIsNone


class ElementBase(object):
    _current_action = ""
    
    """ Properties """
    @property
    def text(self):
        """
        @summary: this method will return the text of element
        @return: text of element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Get text"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                return elem.text
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except ElementIsNone:
                return None
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()

    @property
    def native_element(self):
        return self._get_element(self._timeout)
    
    @property
    def location(self):
        return self.native_element.location
    
    @property
    def size(self):
        return self.native_element.size
    
    @property
    def mid_point(self):
        """
        @summary: this method will return mid point of element
        @return: mid point of element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        height = pyautogui.size()[1]
        window_size = self._driver.get_window_size()
        body_location = self._driver.find_element(By.XPATH, "//html").location
        viewport_h = self._driver.execute_script("return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);")
        if self._driver.driverSetting.platform == Platform.WINDOWS:
            viewport_gap = window_size["height"] - viewport_h - body_location["y"] - (height - window_size["height"])
        elif self._driver.driverSetting.platform == Platform.MAC:
            viewport_gap = window_size["height"] - viewport_h - body_location["y"] + 15
             
        mid_x = self.location["x"] + self.size["width"] / 2
        mid_y = (self.location["y"] + viewport_gap) + self.size["height"] / 2
        return {"x": mid_x, "y": mid_y}
    
    """ Methods """
    def __init__(self, driver, by=By.XPATH, value=None):        
        self._by = by
        self._value = value
        self._driver = driver        
        self._timeout = self._driver.driverSetting.element_wait_timeout
        self._element = None
        self._locator = "{{By: {}, Value: {}}}".format(by, value)
    
    
    def _get_element(self, timeout=None):
        _elem = self._driver.find_element(self._by, self._value, timeout)
        if not _elem:
            raise ElementIsNone(self._driver, self._current_action, self._locator)
        
        return _elem
    
    
    def _print_action(self):
        separator = "                              "
        print(" " + (self._current_action + separator)[:27] + ">>  " + self._locator)
        
        
    def click_element(self):
        """
        @summary: handle for click an element on mac or another
        @author: Thanh Le
        @created_date: August 5, 2016
        """
        if self._driver._driverSetting.browser_name == Browser.Safari:
            self.jsclick()
        else:
            self.click()


    def click(self):
        """
        @summary: click element by selenium
        @author: Thanh Le
        @created_date: August 5, 2016
        """
        self._current_action = "Click"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        message = []
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                elem.click()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except WebDriverException as wdex:
                if ("Element is obscured" in str(wdex)) or ("Other element would receive the click" in str(wdex)):
                    self.wait_until_clickable(2)
                else:
                    message.append(wdex)
            except Exception as ex:
                message.append(ex)
                raise ex
                
            timeleft -= sw.elapsed().total_seconds()
             
        if message:
            self._driver.save_screenshot()
            print(message)
                
    
    def jsclick(self):
        """
        @summary: click element by js
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Java-script Click"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                self._driver.execute_script("arguments[0].click();", elem)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
        
    def pyautogui_click(self):
        """
        @summary: click element by pyautogui
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "PyAutoGui Click"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                pyautogui.click(self.mid_point["x"], self.mid_point["y"])
                sleep(0.5)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
                
  
    def mouse_to(self):
        """
        @summary: move mouse by selenium
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Mouse to"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(self._timeout)
                ActionChains(self._driver.wrapped_driver).move_to_element(elem).perform()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
            
    def jsmouse_to(self):
        """
        @summary: use js to move mouse
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Java-script Mouse to"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(self._timeout)
                mouseOverScript = "if(document.createEvent){var evObj = document.createEvent('MouseEvents');evObj.initEvent('mouseover', true, false); arguments[0].dispatchEvent(evObj);} else if(document.createEventObject) { arguments[0].fireEvent('onmouseover');}"
                self._driver.execute_script(mouseOverScript, elem)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
    
    def pyautogui_mouse_to(self):
        """
        @summary: move mouse to element by pyautogui
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "PyAutoGui Mouse to"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                pyautogui.moveTo(self.mid_point["x"], self.mid_point["y"], 0.1)
                sleep(0.5)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
    
    def scroll_to(self):
        self._current_action = "Java-script Scroll to"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(self._timeout)
                self._driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
              
        return self       
    
    
    def drag_and_drop_by_js(self, xoffset, yoffset):
        self._current_action = "Java-script Drag and drop"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(self._timeout)
                self._driver.execute_script('''
                return(function simulate(elemDrag, xoffset, yoffset) {
                    var fireMouseEvent = function (type, elem, centerX, centerY) {
                      var evt = document.createEvent('MouseEvents');
                      evt.initMouseEvent(type, true, true, window, 1, 1, 1, centerX, centerY, false, false, false, false, 0, elem);
                      elem.dispatchEvent(evt);
                    };
                    var pos = elemDrag.getBoundingClientRect();
                    var center1X = Math.floor((pos.left + pos.right) / 2);
                    var center1Y = Math.floor((pos.top + pos.bottom) / 2);
                    var center2X = center1X + xoffset;
                    var center2Y = center1Y + yoffset;
                    
                    fireMouseEvent('mousemove', elemDrag, center1X, center1Y);
                    fireMouseEvent('mouseenter', elemDrag, center1X, center1Y);
                    fireMouseEvent('mouseover', elemDrag, center1X, center1Y);
                    fireMouseEvent('mousedown', elemDrag, center1X, center1Y);
                    
                    fireMouseEvent('dragstart', elemDrag, center1X, center1Y);
                    fireMouseEvent('drag', elemDrag, center1X, center1Y);
                    fireMouseEvent('mousemove', elemDrag, center1X, center1Y);
                    fireMouseEvent('drag', elemDrag, center2X, center2Y);
                    fireMouseEvent('mousemove', elemDrag, center2X, center2Y);
                    
                    fireMouseEvent('mouseenter', elemDrag, center2X, center2Y);
                    fireMouseEvent('dragenter', elemDrag, center2X, center2Y);
                    fireMouseEvent('mouseover', elemDrag, center2X, center2Y);
                    fireMouseEvent('dragover', elemDrag, center2X, center2Y);
                    
                    fireMouseEvent('drop', elemDrag, center2X, center2Y);
                    fireMouseEvent('dragend', elemDrag, center2X, center2Y);
                    fireMouseEvent('mouseup', elemDrag, center2X, center2Y);
                    return true;
                    })(arguments[0], arguments[1], arguments[2]);
            ''', elem, xoffset, yoffset)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
              
        return self
        
        
    def find_element(self, by=By.XPATH, value=None):
        """
        @summary: find element
        @param by: by values below
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        @param value: value of element
        @return: element if element exists, None if element not exists
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Find child element"
        self._print_action()
        
        
        if(self._by == By.XPATH):
            return self._driver.find_element(self._by, self._value + value, self._timeout)
        else:
            sw = Stopwatch()
            sw.start()
            timeleft = self._timeout
            
            while(timeleft > 0):
                try:
                    elem = self._get_element(self._timeout)
                    return elem.find_element(by, value)
                except StaleElementReferenceException:
                    self.wait_until_clickable(2)
                except Exception as ex:
                    self._driver.save_screenshot()
                    raise ex
                timeleft -= sw.elapsed().total_seconds()
            
        return None
    
    
    def is_enabled(self, wait_time_out=None):
        """
        @summary: This method allows check element is enable
        @return: True if element is enable, False if element None
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Is enabled"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        sw = Stopwatch()
        sw.start()
        
        while(sw.elapsed().total_seconds() < self._timeout):
            try:
                elem = self._get_element(wait_time_out)
                return elem.is_enabled()
            except ElementIsNone:
                return False
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            
                
    def is_clickable(self, wait_time_out=None):
        """
        @summary: this method allows check element is clickable
        @param wait_time_out: time to waiting for element
        @return: True if element is clickable, False if element is not clickable
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Is clickable"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        return self._driver.is_element_clickable(self._by, self._value, wait_time_out)
        
    
    def is_displayed(self, wait_time_out=None):
        """
        @summary: this method allows check element displays
        @param wait_time_out: time to waiting for element
        @return: True if element displays, False if element does not display
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Is displayed"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        return self._driver.is_element_visible(self._by, self._value, wait_time_out)

    
    def is_disappeared(self, wait_time_out=None):
        """
        @summary: this method allows check element is disappeared
        @param wait_time_out: time to waiting for element
        @return: True if element disappear, False if element does not disappear
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Is disappeared"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        return self._driver.is_element_invisible(self._by, self._value, wait_time_out)
    
     
    def wait_until_displayed(self, wait_time_out=None):
        """
        @summary: wait until element displays
        @param wait_time_out: time to waiting for element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Wait until displayed"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        self._driver.wait_for_element_visible(self._by, self._value, wait_time_out)
        return self
    
      
    def wait_until_disappeared(self, wait_time_out=None):
        """
        @summary: wait until element is disappeared
        @param wait_time_out: time to waiting for element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Wait until disappeared"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        self._driver.wait_for_element_invisible(self._by, self._value, wait_time_out)
    
    
    def wait_until_clickable(self, wait_time_out=None):
        """
        @summary: wait until element is clickable
        @param wait_time_out: time to waiting for element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Wait until clickable"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._timeout
        
        self._driver.wait_for_element_clickable(self._by, self._value, wait_time_out)
        return self

