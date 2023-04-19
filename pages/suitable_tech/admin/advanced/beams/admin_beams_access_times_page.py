from selenium.webdriver.common.by import By
from common.application_constants import ApplicationConst
from core.utilities.utilities import Utilities
from core.webdriver.elements.access_times_controls import WeekviewEventHeader, WeekviewAllEvents
from core.webdriver.elements.dropdownlist import DropdownList
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_base import ElementBase
from core.webdriver.elements.element_list import ElementList
from core.webdriver.exceptions import FunctionNotSupportedException
from data_test.dataobjects.enum import WeekDays
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from core.suitabletechapis.user_api import UserAPI
from time import sleep
from common.constant import Platform


class _AdminBeamAccessTimesPageLocator(object):
    
    _pnlAccessTimesSideBar = (By.XPATH, "//div[@class='row ng-scope']/div[1]")
    _pnlAccessTimesCalendar = (By.XPATH, "//div[@class='row ng-scope']/div[2]")
    _btnInviteTempUser = (By.XPATH, "//button[@ng-click='addTemporaryAccessTime()' and @class='btn btn-emphasis btn-xs hidden-xs']")
    _btnMInviteTempUser = (By.XPATH, "//button[@ng-click='addTemporaryAccessTime()' and @class='btn btn-emphasis visible-xs']")
    _iconLoading = (By.XPATH, "//p[@ng-if='contentLoading']")
    _lblDefaultAccessTimes = (By.XPATH, "//div[@ng-repeat='defaultAccessTime in defaultAccessTimes']//a")
    _chkAccessTimeAllDay = (By.XPATH,"//div[@class='list-group-item ng-scope']//div[@class='calendar-square']")
    _chkShowDefaultAccesstimes = (By.XPATH, "//input[@ng-model='showDefaultAccessTimes']")
    _chkShowMemberAccesstimes = (By.XPATH, "//input[@ng-model='showMemberAccessTimes']")
    _chkShowTemporaryAccesstimes = (By.XPATH, "//input[@ng-model='showTemporaryAccessTimes']")
    
    @staticmethod
    def _divDefaultAccessTimesSelector(item_label):
        return (By.XPATH, u"//div[@ng-repeat='defaultAccessTime in defaultAccessTimes']//a[.=\"{}\"]/..//div[@class='calendar-square']".format(item_label)) 
    @staticmethod
    def _lnkDefaultAccessTimes(item_label):
        return (By.XPATH, u"//div[@ng-repeat='defaultAccessTime in defaultAccessTimes']//a[.=\"{}\"]".format(item_label))
    @staticmethod
    def _btnDefaultAccessTimesRemover(item_label):
        return (By.XPATH, u"//div[@ng-repeat='defaultAccessTime in defaultAccessTimes']//a[.=\"{}\"]/..//span[@ng-click='removeDefaultAccessTime($event, defaultAccessTime)']".format(item_label))
    @staticmethod
    def _lblTempUser(user_email):
        return (By.XPATH, u"//span[.=\"{}\"]//following::span[@class='ng-binding' and contains(.,\"{}\")]".format(ApplicationConst.LBL_BEAMS_ACCESS_TIMES_TEMPORARY_USERS, user_email))   
    @staticmethod
    def _lnkSidebarTempUser(user_email, access_time_label):
        return (By.XPATH, u"//translate[.=\"{}\"]//following::span[@class='ng-binding' and contains(.,\"{}\")]/../..//a[.=\"{}\"]".format(ApplicationConst.LBL_BEAMS_ACCESS_TIMES_TEMPORARY_USERS, user_email, access_time_label))
    @staticmethod
    def _lnkSidebarMember(user_displayed_name):
        return (By.XPATH, u"//span[@ng-show='member.user' and normalize-space(.)=\"{}\"]/../..//a[@ng-click='addMemberAccessTime($event, member)']".format(user_displayed_name))
    @staticmethod
    def _lnkSidebarMemberAccessTime(user_displayed_name, access_time_label):
        return (By.XPATH, u"//span[@ng-show='member.user'  or @ng-show='user.first_name || user.last_name' and contains(text(),\"{}\")]/../..//a[.=\"{}\"]".format(user_displayed_name, access_time_label))
    @staticmethod
    def _lstSidebarMemberAccessTimes(user_displayed_name):
        return (By.XPATH, u"//span[@ng-show='member.user' and normalize-space(.)=\"{}\"]/../..//a[@ng-click='editMemberAccessTime($event, member, accessTime)']".format(user_displayed_name))
    @staticmethod
    def _chkAccessTimeOfUser(user_name):
        return (By.XPATH, u"//span[.='{}']/../..//div[@class='calendar-square']".format(user_name))

    
class AccessTimesSidebar(ElementBase):
    
    def __init__(self, driver, by=By.XPATH, locator=None):
        """      
        @summary: Constructor method
        @param driver: Web driver
        @param by: xpath of element
        @param locator: locator 
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        ElementBase.__init__(self, driver, by, locator)
    
    """ Properties  """
    
    @property
    def _iconLoading(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._iconLoading)
    @property
    def _chkShowDefaultAccessTime(self):
        return Element(self._driver, By.XPATH, "{}//input[@type='checkbox' and @ng-model='showDefaultAccessTimes']".format(self._value))
    @property
    def _btnAddDefaultAccessTime(self):
        return Element(self._driver, By.XPATH, "{}//button[@class='btn btn-emphasis btn-xs hidden-xs' and @ng-click='addDefaultAccessTime()']".format(self._value))
    @property
    def _chkShowMemberAccessTime(self):
        return Element(self._driver, By.XPATH, "{}//input[@type='checkbox' and @ng-model='showMemberAccessTimes']".format(self._value))
    @property
    def _btnAddMemberAccessTime(self):
        return Element(self._driver, By.XPATH, "{}//button[@ng-click='addMemberAccessTime()']".format(self._value))
    @property
    def _btnInviteTempUser(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._btnInviteTempUser)
    @property
    def _btnMInviteTempUser(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._btnMInviteTempUser)    
    @property
    def _lblDefaultAccessTimes(self):
        return ElementList(self._driver, *_AdminBeamAccessTimesPageLocator._lblDefaultAccessTimes)
    
    def _lnkSidebarMember(self, user_displayed_name):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._lnkSidebarMember(user_displayed_name))
    def _lnkSidebarMemberAccessTime(self, user_displayed_name, access_time_label):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._lnkSidebarMemberAccessTime(user_displayed_name, access_time_label))
    def _lstSidebarMemberAccessTimes(self, user_displayed_name):
        return ElementList(self._driver, *_AdminBeamAccessTimesPageLocator._lstSidebarMemberAccessTimes(user_displayed_name))
    
    
    """MOBILE UI"""
    @property
    def _btnMAddDefaultAccessTime(self):
        return Element(self._driver, By.XPATH, "{}//button[@class='btn btn-emphasis visible-xs' and @ng-click='addDefaultAccessTime()']".format(self._value))
    
    """ Methods """
    
    def wait_for_loading(self, timeout=5):
        """      
        @summary:  Wait for loading icon displays then disappears 
        @param timeout: Time to wait for loading icon displays then disappears
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._iconLoading.wait_until_displayed(10)
        self._iconLoading.wait_until_disappeared(timeout)

    
    """
    FOR DEFAULT ACCESS TIME 
    """ 
     
    def add_default_allday_access_time(self, access_days):
        """      
        @summary: Add default access time for all members of device group   
        @param access_days: Which days set for accessing
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMAddDefaultAccessTime.wait_until_clickable()
            self._btnMAddDefaultAccessTime.click_element()
        else:
            self._btnAddDefaultAccessTime.wait_until_clickable()
            self._btnAddDefaultAccessTime.click_element()
        
        from pages.suitable_tech.admin.dialogs.device_group_access_time_dialog import CreateDefaultAccessTimeDialog
        dialog = CreateDefaultAccessTimeDialog(self._driver)
        
        dialog.select_weekdays(access_days)
        
        dialog.select_all_day_button()
        
        dialog.submit()
        
        return self
    
        
    def add_default_timerange_access_time(self, access_days, starting_datetime, ending_datetime):
        """      
        @summary: Add default time range access time for all members of a device group      
        @param access_days: Which days set for members access
        @param starting_datetime: specify starting time for access
        @param ending_datetime: specify ending time for access
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMAddDefaultAccessTime.wait_until_clickable()
            self._btnMAddDefaultAccessTime.click_element()
        else:
            self._btnAddDefaultAccessTime.wait_until_clickable()
            self._btnAddDefaultAccessTime.click_element()
        
        from pages.suitable_tech.admin.dialogs.device_group_access_time_dialog import CreateDefaultAccessTimeDialog
        dialog = CreateDefaultAccessTimeDialog(self._driver)
        
        dialog.select_weekdays(access_days)
        dialog.select_time_range(starting_datetime, ending_datetime)
        
        dialog.submit()
        return self
    
    
    def check_default_access_times_selected_by_label(self, access_time_label):
        """      
        @summary: Check the default access time is selected or not using label
        @param access_time_label: Label of the access time would like to check
        @return: background-color is rgb(153, 153,153): The access time is selected, "" : the access time is not selected.
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        access_time_selector = Element(self._driver, *_AdminBeamAccessTimesPageLocator._divDefaultAccessTimesSelector(access_time_label))
        style_value = access_time_selector.get_attribute("style")
        # if this item is selected, its style will turns to value 'background-color: rgb(153, 153, 153);';
        # otherwise, the style value is empty 
        return style_value != ""
    
    
    def is_default_access_times_selected(self, access_days):
        """      
        @summary: Check if the default access time is selected or not using access days   
        @param access_days: Which access days would like to check
        @return: True: access time is selected, False: access time is not selected
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        item_label = Utilities.generate_access_time_label(access_days) 
        return self.check_default_access_times_selected_by_label(item_label)


    def is_default_access_time_label_displayed(self, access_time_label):
        """      
        @summary: Check if the default access time is displayed or not by using access time label
        @param access_time_label: Label of access time would like to check 
        @return: True: The default access time is displayed, False: The default access time is not displayed
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        access_time_element = Element(self._driver, *_AdminBeamAccessTimesPageLocator._lnkDefaultAccessTimes(access_time_label))
        return access_time_element.is_displayed()
    
        
    def edit_default_access_time(self, access_time_label, new_access_days, new_starting_datetime=None, new_ending_datetime=None):
        """      
        @summary: Edit the default access time    
        @param access_time_label: new access time label would like to set
        @param new_starting_datetime: new stating date time would like to set
        @param new_ending_datetime: new ending date time would like to set
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        # open Edit Access Time dialog
        access_time_element = Element(self._driver, *_AdminBeamAccessTimesPageLocator._lnkDefaultAccessTimes(access_time_label))
        access_time_element.wait_until_displayed()
        access_time_element.click() 
        
        from pages.suitable_tech.admin.dialogs.device_group_access_time_dialog import EditDefaultAccessTimeDialog
        dialog = EditDefaultAccessTimeDialog(self._driver)
        
        dialog.select_weekdays(new_access_days)
        
        if new_starting_datetime and new_ending_datetime:            
            dialog.select_time_range(new_starting_datetime, new_ending_datetime)
        else:
            dialog.select_all_day_button() 
            
        dialog.submit()
        return self
    
    
    def unselect_default_access_time(self, access_days):
        """      
        @summary: Un-select a default access time by access days  
        @param access_days: days of the access time would like to be un-select
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        item_label = Utilities.generate_access_time_label(access_days) 
        return self.unselect_default_access_time_by_label(item_label)
    
    
    def unselect_default_access_time_by_label(self, access_time_label):
        """      
        @summary: Un-select a default access time by label 
        @param  access_time_label: label of access time would like to be un-select
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        access_time_selector = Element(self._driver, *_AdminBeamAccessTimesPageLocator._divDefaultAccessTimesSelector(access_time_label))
        style_value = access_time_selector.get_attribute("style")
        if style_value:
            access_time_selector.click()
        return self
    
    
    """
    FOR MEMBER ACCESS TIME 
    """ 
        
        
    def add_member_allday_access_time(self, user, access_days):
        """      
        @summary: Add access time for a member
        @param user: member who would like to be added access time for
        @param access_days: which days would like to be added
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        sidebar_member_lnk = self._lnkSidebarMember(UserAPI.get_displayed_name(user))
        sidebar_member_lnk.wait_until_clickable().click()
        
        from pages.suitable_tech.admin.dialogs.device_group_access_time_dialog import CreateMemberAccessTimeDialog
        dialog = CreateMemberAccessTimeDialog(self._driver)
        # handle cannot click member link to open edit dialog
        if not dialog.is_dialog_displayed(1):
            sidebar_member_lnk.jsclick()
            
        dialog.select_weekdays(access_days)
        dialog.select_all_day_button()
        dialog.submit()
        return self
    
    
    def add_member_timerange_access_time(self, user, access_days, starting_datetime, ending_datetime):
        """      
        @summary: Add time range for a member access time      
        @param user: member who would like to be added access time for
        @param access_days: which days would like to add for access time
        @param starting_datetime: starting time for access time
        @param ending_datetime: ending time for access time
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        sidebar_member_lnk = self._lnkSidebarMember(UserAPI.get_displayed_name(user))
        sidebar_member_lnk.wait_until_clickable().click()
        
        from pages.suitable_tech.admin.dialogs.device_group_access_time_dialog import CreateMemberAccessTimeDialog
        dialog = CreateMemberAccessTimeDialog(self._driver)

        # handle cannot click member link to open edit dialog
        if not dialog.is_dialog_displayed(1):
            sidebar_member_lnk.jsclick()

        dialog.select_weekdays(access_days)
        dialog.select_time_range(starting_datetime, ending_datetime)
        dialog.submit()
        return self
    
    
    def edit_member_access_time(self, user, user_access_time_label, new_access_days, new_starting_datetime=None, new_ending_datetime=None):
        """      
        @summary: Edit an existing member access time     
        @param user: member who would like to edit access time for
        @param user_access_time_label: label of user's access time would like to be edited
        @param new_access_days: new access days would like to set when editing
        @param starting_datetime: starting time to set when editing
        @param ending_datetime: ending time to set when editing
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        access_time_element = self._lnkSidebarMemberAccessTime(UserAPI.get_displayed_name(user), user_access_time_label)
        access_time_element.wait_until_displayed()
        access_time_element.click() 
        
        from pages.suitable_tech.admin.dialogs.device_group_access_time_dialog import EditDefaultAccessTimeDialog
        dialog = EditDefaultAccessTimeDialog(self._driver)
        
        dialog.select_weekdays(new_access_days)
        
        if new_starting_datetime and new_ending_datetime:            
            dialog.select_time_range(new_starting_datetime, new_ending_datetime)
        else:
            dialog.select_all_day_button() 
            
        dialog.submit()
        return self
    
    
    def get_all_member_access_time_labels(self, user):
        """      
        @summary: Get all access time labels of a member       
        @param user: The member who would like to get all access time labels of 
        @return: All access time labels of a member 
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        lst_user_access_times = self._lstSidebarMemberAccessTimes(user.get_displayed_name())
        
        access_time_labels = []
        access_time_items = lst_user_access_times.get_all_elements()
        for access_time in access_time_items:
            if(access_time and access_time.text):
                access_time_labels.append(access_time.text)
        
        return access_time_labels
    
    
    def is_member_access_time_label_displayed(self, user, user_access_time_label):
        """      
        @summary: Check if a member access time label is displayed or not  
        @param user: member who would like to check
        @param user_access_time_label: access time label to check
        @return: True: The member access time is displayed, False: The member access time is not displayed
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        access_time_element = self._lnkSidebarMemberAccessTime(UserAPI.get_displayed_name(user), user_access_time_label)
        return access_time_element.is_displayed()
    
    
    def is_member_allday_access_time_displayed(self, user, access_days):
        """      
        @summary: Check if the member all day access time is displayed or not
        @param user: member would like to check
        @param access_days: which days would like to check
        @return: True: The member all day access time is displayed, False: The member all day access time is not displayed
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if not access_days:
            return False
        access_time_label = Utilities.generate_access_time_label(access_days)
        
        return self.is_member_access_time_label_displayed(user, access_time_label)


class AccessTimesCalendar(ElementBase):
    
    """ Methods """
    def __init__(self, driver, by=By.XPATH, locator=None):
        """      
        @summary: Constructor method    
        @param driver: Web driver
        @param by: xpath of element
        @param locator: locator 
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        ElementBase.__init__(self, driver, by, locator)
    
    
    @property
    def _ddlCreate(self):
        return DropdownList(self._driver, By.XPATH, "{}//div[@class='btn-group dropdown']".format(self._value))  
    @property
    def _btnMonthView(self):
        return Element(self._driver, By.XPATH, "{}//div[@class='pull-right']//button[@ng-click=\"changeCalendarView('month')\"]".format(self._value))  
    @property
    def _btnWeekView(self):
        return Element(self._driver, By.XPATH, "{}//div[@class='pull-right']//button[@ng-click=\"changeCalendarView('agendaWeek')\"]".format(self._value))  
    @property
    def _btnDayView(self):
        return Element(self._driver, By.XPATH, "{}//div[@class='pull-right']//button[@ng-click=\"changeCalendarView('agendaDay')\"]".format(self._value))
    @property
    def _btnCalendarPrev(self):
        return Element(self._driver, By.XPATH, "{}//div[@class='pull-right']//button[@ng-click='calendarPrev()']".format(self._value))
    @property
    def _btnCalendarNext(self):
        return Element(self._driver, By.XPATH, "{}//div[@class='pull-right']//button[@ng-click='calendarNext()']".format(self._value))
    @property
    def _lstWeekViewEventHeader(self):
        return WeekviewEventHeader(self._driver, By.XPATH, "{}//table[@class='fc-agenda-days fc-border-separate']/thead//th".format(self._value))
    @property
    def _lstWeekViewEventList(self):
        return WeekviewAllEvents(self._driver, By.XPATH, "{}//div[@class='fc-event-inner']/..".format(self._value))
    
    def is_day_view(self):
        class_attr = self._btnDayView.get_attribute("class");
        return Utilities.does_contain_whole_word("active")(class_attr)
    def is_month_view(self):
        class_attr = self._btnMonthView.get_attribute("class");
        return Utilities.does_contain_whole_word("active")(class_attr)
    def is_week_view(self):
        class_attr = self._btnWeekView.get_attribute("class");
        return Utilities.does_contain_whole_word("active")(class_attr)
    def get_all_weekly_access_times_events(self, event_title=None):
        if event_title == None:
            event_title = ApplicationConst.LBL_ALL_MEMBERS
            
        if not self.is_week_view():
            return None
        
        calendar_header = self._lstWeekViewEventHeader
        calendar_header.parse_header_info()
        header_info = calendar_header.get_header_column_info()
        
        events = self._lstWeekViewEventList.parse_events(header_info, event_title)
           
        return events

    
class AdminBeamAccessTimesPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam Access Times page.
        This page will be opened after clicking Access Times tab on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/beams/787/access/ for more details.
    @page: Beam Access Times page
    @author: Quang Tran
    """

    """    Properties    """
    def _lblTempUser(self, value):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._lblTempUser(value))
    
    
    @property
    def _pnlAccessTimesSideBar(self):
        return AccessTimesSidebar(self._driver, *_AdminBeamAccessTimesPageLocator._pnlAccessTimesSideBar)
    @property
    def _pnlAccessTimesCalendar(self):
        return AccessTimesCalendar(self._driver, *_AdminBeamAccessTimesPageLocator._pnlAccessTimesCalendar)    
    @property
    def _btnInviteTempUser(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._btnInviteTempUser)
    @property
    def _btnMInviteTempUser(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._btnMInviteTempUser)
    @property
    def _chkAccessTimeAllDay(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._chkAccessTimeAllDay)
    def _lnkSidebarTempUser(self, user_email, access_time_label):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._lnkSidebarTempUser(user_email, access_time_label))
    def _chkAccessTimeOfUser(self, user_displayed_name):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._chkAccessTimeOfUser(user_displayed_name))
    @property
    def _chkShowDefaultAccesstimes(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._chkShowDefaultAccesstimes)
    @property
    def _chkShowMemberAccesstimes(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._chkShowMemberAccesstimes)
    @property
    def _chkShowTemporaryAccesstimes(self):
        return Element(self._driver, *_AdminBeamAccessTimesPageLocator._chkShowTemporaryAccesstimes)

    """    Methods    """
    
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: Web driver
        @author: Quang Tran
        @created_date: August 08, 2016
        """     
        AdminBeamsCommonPage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        
    
    def _wait_for_loading(self, timeout=None):
        """      
        @summary: Wait for access time bar completed loading
        @param timeout: time would like to wait
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        self._pnlAccessTimesSideBar.wait_for_loading(timeout)


    """
    FOR DEFAULT ACCESS TIME 
    """ 
        
        
    def add_default_allday_access_times(self, access_days=""):
        """      
        @summary: Add default all day access time
        @param access_days: which days would like to add for access time
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not access_days):
            access_days = []
            access_days.append(WeekDays.Mon)
        
        self._wait_for_loading(10)
        self._pnlAccessTimesSideBar.add_default_allday_access_time(access_days)
        
        return self
    
    
    def add_default_timerange_access_times(self, access_days, starting_datetime, ending_datetime):
        """      
        @summary: Add default time range for access time
        @param access_days: which days would like to set for access time
        @param starting_datetime: starting time would like to set for access time
        @param ending_datetime:ending time would like to set for access time
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not access_days):
            access_days = []
            access_days.append(WeekDays.Mon)
        
        self._wait_for_loading()
        self._pnlAccessTimesSideBar.add_default_timerange_access_time(access_days, starting_datetime, ending_datetime)
        
        return self
    
    
    def edit_default_access_times(self, access_time_label, new_access_days="", new_starting_datetime=None, new_ending_datetime=None):
        """      
        @summary: Edit the default access time
        @param access_time_label: new label to set for editing access time
        @param new_access_days: new days set for editing access time
        @param new_starting_datetime: new starting and ending time set for editing access time
        @param new_ending_datetime: new ending time set for editing access time
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not new_access_days):
            new_access_days = []
            new_access_days.append(WeekDays.Mon)
        
        self._wait_for_loading()
        self._pnlAccessTimesSideBar.edit_default_access_time(access_time_label, new_access_days, new_starting_datetime, new_ending_datetime)
        
        return self
        
    
    def is_default_allday_access_times_selected(self, access_days):
        """      
        @summary: Check if a default all day access time selected or not      
        @param access_days: access days of the access time would like to check 
        @return: background-color: rgb(153, 153, 153): is the access time selected, "": the access time is not selected
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not access_days):
            return False
        self._wait_for_loading()
        
        item_label = Utilities.generate_access_time_label(access_days)
        
        access_time_selector = Element(self._driver, *_AdminBeamAccessTimesPageLocator._divDefaultAccessTimesSelector(item_label))
        style_value = access_time_selector.get_attribute("style")
        # if this item is selected, its style will turns to value 'background-color: rgb(153, 153, 153);';
        # otherwise, the style value is empty 
        return style_value != ""
    
    
    def is_default_access_time_label_displayed_on_sidebar(self, access_time_label):
        """      
        @summary: Check if the default access time label is displayed on side bar or not     
        @param access_time_label: label of access time would like to check
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        self._wait_for_loading()
        return self._pnlAccessTimesSideBar.is_default_access_time_label_displayed(access_time_label)
    
    
    def is_default_allday_access_time_displayed_on_calendar(self, access_days):
        """      
        @summary: Check if the default all day access time is displayed on calendar or not  
        @param access_days: access days of the access time would like to check
        @return: True: The default all day access time is displayed on calendar
                False: The default all day access time is not displayed on calendar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        # self._wait_for_loading()
        pnl_calendar = self._pnlAccessTimesCalendar
        
        if pnl_calendar.is_week_view():
            events = pnl_calendar.get_all_weekly_access_times_events(ApplicationConst.LBL_ALL_MEMBERS)
            for event in events:
                if not event.is_all_day():
                    continue
                event_access_days = event._access_days
                if Utilities.does_contain(access_days, event_access_days):
                    return True
        else:
            raise FunctionNotSupportedException("The access times checking function is not supported on Month view or Day view")
    
    
    def is_default_timerange_access_time_displayed_on_calendar(self, access_days, starting_datetime, ending_datetime):
        """      
        @summary: Check if the default time range access time is displayed on calendar or not   
        @param access_days: days of the access time would like to check
        @param starting_datetime: starting time of access time would like to check
        @param ending_datetime: ending date time of access time would like to check
        @return: True: The default time range access time is displayed on calendar
                False: The default time rang access time is not displayed on calendar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        self._wait_for_loading()
        pnl_calendar = self._pnlAccessTimesCalendar
        
        start_hr = str(int (starting_datetime.strftime("%I")))
        start_mn = starting_datetime.strftime("%M")
        start_mr = starting_datetime.strftime("%p")
        if start_mr == "AM":
            start_mr = 'a'
        else:
            start_mr = 'p'
        
        end_hr = str(int (ending_datetime.strftime("%I")))
        end_mn = ending_datetime.strftime("%M")
        end_mr = ending_datetime.strftime("%p")
        if end_mr == "AM":
            end_mr = 'a'
        else:
            end_mr = 'p'
            
        expected_label = "{}:{}{} - {}:{}{}".format(start_hr, start_mn, start_mr, end_hr, end_mn, end_mr)
        
        if pnl_calendar.is_week_view():
            events = pnl_calendar.get_all_weekly_access_times_events()
            for event in events:
                if event.is_all_day():
                    continue
                event_access_days = event._access_days
                event_time_range = event._time_range
                if Utilities.does_contain(access_days, event_access_days):
                    if event_time_range and expected_label == event_time_range:
                        return True
        
        return False
    
    
    """
    FOR MEMBER ACCESS TIME 
    """
    
    def add_member_allday_access_times(self, user, access_days):
        """      
        @summary: Add member all day access time     
        @param user: member who would like to add access time for
        @param access_days: which days would like to add for member access time
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not access_days):
            access_days = []
            access_days.append(WeekDays.Mon)
        
        self._wait_for_loading()
        self._pnlAccessTimesSideBar.add_member_allday_access_time(user, access_days)
        
        return self
        
    
    def add_member_timerange_access_times(self, user, access_days, starting_datetime, ending_datetime):
        """      
        @summary: Add time range access time for a member 
        @param user: member who would like to add access time for
        @param access_days: which days to add for member access time
        @param starting_datetime, ending_datetime: starting date time would like to add for member access time
        @param ending_datetime: ending date time would like to add for member access time
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not access_days):
            access_days = []
            access_days.append(WeekDays.Mon)
        
        self._wait_for_loading()
        self._pnlAccessTimesSideBar.add_member_timerange_access_time(user, access_days, starting_datetime, ending_datetime)
        
        return self
    
    
    def edit_member_access_times(self, user, access_time_label, new_access_days, new_starting_datetime=None, new_ending_datetime=None):
        """      
        @summary: Edit access time for a member        
        @param user: member would like to edit access time
        @param new_access_days: new access days would like to set for editing member access time
        @param new_starting_datetime: new ending date time would like to set for editing
        @param new_ending_datetime: new ending date time would like to set for editing
        @return: AccessTimesSidebar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        if(not new_access_days):
            access_days = []
            access_days.append(WeekDays.Mon)
        
        self._wait_for_loading()
        self._pnlAccessTimesSideBar.edit_member_access_time(user, access_time_label, new_access_days, new_starting_datetime, new_ending_datetime)
        
        return self
    
    
    def is_member_access_time_label_displayed_on_sidebar(self, user, access_time_label):
        """      
        @summary: Check if member access time label is displayed or not
        @param user: member who would like to check
        @param access_time_label: label of access time would like to check
        @return: True: The member access time label is displayed on side bar
                False: The member access time label is not displayed on side bar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        return self._pnlAccessTimesSideBar.is_member_access_time_label_displayed(user, access_time_label)
    
    
    def is_member_allday_access_time_displayed_on_calendar(self, user, access_days):
        """      
        @summary: Check if a member all day access time is displayed on calendar or not 
        @param user: member who would like to check
        @param access_days: access days of member access time would like to check
        @return: True: The member all day access time is displayed on calendar
                False: The member all day access time is not displayed on calendar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        pnl_calendar = self._pnlAccessTimesCalendar
        
        if pnl_calendar.is_week_view():
            events = pnl_calendar.get_all_weekly_access_times_events(event_title=UserAPI.get_displayed_name(user))
            for event in events:
                if not event.is_all_day():
                    continue
                event_access_days = event._access_days
                if Utilities.does_contain(access_days, event_access_days):
                    return True
        else:
            raise FunctionNotSupportedException("The access times checking function is not supported on Month view or Day view")

        return False

    
    def is_member_timerange_access_time_displayed_on_calendar(self, user, access_days, starting_datetime, ending_datetime):
        """      
        @summary: Check if a member time range access time is displayed on calendar or not
        @param user: member who would like to check
        @param access_days: which days of member access time would like to check
        @param starting_datetime: starting time of member access time would like to check
        @param ending_datetime: ending time of member access time would like to check
        @return: True: The member access time time range is displayed on calendar
                False: The member access time time range is not displayed on calendar
        @author: Quang Tran
        @created_date: August 08, 2016
        """
        pnl_calendar = self._pnlAccessTimesCalendar
        
        start_hr = str(int (starting_datetime.strftime("%I")))
        start_mn = starting_datetime.strftime("%M")
        start_mr = starting_datetime.strftime("%p")
        if start_mr == "AM":
            start_mr = 'a'
        else:
            start_mr = 'p'
        
        end_hr = str(int (ending_datetime.strftime("%I")))
        end_mn = ending_datetime.strftime("%M")
        end_mr = ending_datetime.strftime("%p")
        if end_mr == "AM":
            end_mr = 'a'
        else:
            end_mr = 'p'
            
        expected_label = "{}:{}{} - {}:{}{}".format(start_hr, start_mn, start_mr, end_hr, end_mn, end_mr)
        
        
        if pnl_calendar.is_week_view():
            events = pnl_calendar.get_all_weekly_access_times_events(event_title=UserAPI.get_displayed_name(user))
            for event in events:
                if event.is_all_day():
                    continue
                event_access_days = event._access_days
                event_time_range = event._time_range
                if Utilities.does_contain(access_days, event_access_days):
                    if event_time_range and expected_label == event_time_range:
                        return True
        else:
            raise FunctionNotSupportedException("The access times checking function is not supported on Month view or Day view")
        
        return False
    
        
    """
    FOR TEMPORARY ACCESS TIME 
    """    
    def invite_temporary_user(self, user, start_date=None, end_date=None, link_to_beam_sofware=None, default_invitation=None, require_session_answer=None):
        """
        @summary: Invite a temporaty user        
        @param user: The temporary user
        @param start_date: Staring date
        @param end_date: Ending date
        @param link_to_beam_sofware: Include a link to the Beam software checkbox [True/False]
        @param default_invitation: Include the default invitation message checkbox [True/False]
        @param require_session_answer: Require session answer checkbox [True/False]        
        @return: AdminBeamAccessTimesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._wait_for_loading(5)
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMInviteTempUser.wait_until_clickable().click_element()
        else:
            self._btnInviteTempUser.wait_until_clickable().click_element()
        sleep(2)
        from pages.suitable_tech.admin.dialogs.invite_a_temporary_user import InviteTempUserDialog
        InviteTempUserDialog(self._driver).submit_invite_information(user, start_date, end_date, link_to_beam_sofware, default_invitation, require_session_answer)
        return self
    
    
    def is_temporary_user_existed(self, user):
        """      
        @summary: Check if a temporary user is existed or not        
        @param user: user who would like to check
        @return: True: The temporary user is existed, False: The temporary user is not existed
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        return self._lblTempUser(user.email_address).is_displayed()
    
    
    def delete_temporary_user(self, user):
        return self


    def edit_temporary_access_times(self, user, access_time_label, start_date=None, end_date=None, link_to_beam_sofware=None, default_invitation=None, require_session_answer=None):
        """      
        @summary: Edit access time for a temporary user     
        @param user: user who would like to edit
        @param access_time_label: label of temporary user access time would like to edit
        @param start_date: starting date time would like to set for editing temporary access time
        @param end_date: ending date time would like to set for editing temporary access time
        @param link_to_beam_software: check or un-check the 'Include a link to the Beam software' checkbox
        @param default_invitation: check or un-check the 'Include the default invitation message' checkbox
        @param require_session_answer: check or un-check the 'Require session answer' checkbox
        @return: AdminBeamAccessTimesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._wait_for_loading(5)
        self._lnkSidebarTempUser(user.email_address, access_time_label).wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.invite_a_temporary_user import EditTemporaryAccessTime
        EditTemporaryAccessTime(self._driver).edit_temporary_access_time(start_date, end_date, link_to_beam_sofware, default_invitation, require_session_answer)
        return self
    
    
    def is_temporary_time_range_access_time_displayed_on_calendar(self, user, access_day, starting_datetime, ending_datetime):
        """      
        @summary: Check if a access time of a temporary user is displayed on calendar or not    
        @param user: user who would like to check
        @param access_day: days of temporary user access time would like to check
        @param starting_datetime: starting time of temporary user access time would like to check
        @param ending_datetime: ending time of temporary user access time would like to check
        @return: True: The temporary time range access time is displayed on calendar
                False: The temporary time range access time is not displayed on calendar
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        pnl_calendar = self._pnlAccessTimesCalendar
        
        start_hr = str(int (starting_datetime.strftime("%I")))
        start_mn = starting_datetime.strftime("%M")
        start_mr = starting_datetime.strftime("%p")
        if start_mr == "AM":
            start_mr = 'a'
        else:
            start_mr = 'p'
        
        end_hr = str(int (ending_datetime.strftime("%I")))
        end_mn = ending_datetime.strftime("%M")
        end_mr = ending_datetime.strftime("%p")
        if end_mr == "AM":
            end_mr = 'a'
        else:
            end_mr = 'p'
            
        expected_label = "{}:{}{} - {}:{}{}".format(start_hr, start_mn, start_mr, end_hr, end_mn, end_mr)
        
        
        if pnl_calendar.is_week_view():
            events = pnl_calendar.get_all_weekly_access_times_events(event_title=UserAPI.get_displayed_name(user))
            for event in events:
                if event.is_all_day():
                    continue
                event_access_days = event._access_days
                event_time_range = event._time_range
                if Utilities.does_contain(access_day, event_access_days):
                    if event_time_range and expected_label == event_time_range:
                        return True
        else:
            raise FunctionNotSupportedException("The access times checking function is not supported on Month view or Day view")
        
        return False
    

    def get_temporary_user_access_time_label(self, starting_datetime, ending_datetime):
        """      
        @summary: Get label of a temporary user access time 
        @param starting_datetime: starting time of temporary user access time would like to get label
        @param ending_datetime: ending time of temporary user access time would like to get label
        @return: label of temporary access time
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        from core.i18n.i18n_support import I18NSupport
        start_hr = str(int (starting_datetime.strftime("%I")))
        start_mn = starting_datetime.strftime("%M")
        start_mr = ApplicationConst.get_date_time_label(starting_datetime.strftime("%p")).lower()
                
        start_month = starting_datetime.strftime("%b")
        start_day = starting_datetime.strftime("%d").lstrip('0')
        start_year = starting_datetime.strftime("%Y")


        end_hr = str(int (ending_datetime.strftime("%I")))
        end_mn = ending_datetime.strftime("%M")
        end_mr = ApplicationConst.get_date_time_label(ending_datetime.strftime("%p")).lower()
            
        end_month = ending_datetime.strftime("%b")
        end_day = ending_datetime.strftime("%d").lstrip('0')
        end_year = ending_datetime.strftime("%Y")
        
        expected_label = "{} {}, {} {}:{} {} - {} {}, {} {}:{} {}".format(start_month, start_day, start_year, start_hr, start_mn, start_mr, end_month, end_day, end_year, end_hr, end_mn, end_mr)
        
        if (start_year == end_year and start_day == end_day and start_month == end_month):            
            expected_label = "{} {}, {} {}:{} {} - {}:{} {}".format(start_month, start_day, start_year, start_hr, start_mn, start_mr, end_hr, end_mn, end_mr)

        return I18NSupport.localize_date_time_string(expected_label)
    

    def toggle_accesstime_all_day(self, select=True):
        """      
        @summary: Check or uncheck All day every day
        @author: Quang Tran
        @created_date: July 25, 2018
        """
        if select:
            if not self._chkAccessTimeAllDay.get_attribute("style"):
                self._chkAccessTimeAllDay.click()
        else:
            if self._chkAccessTimeAllDay.get_attribute("style"):
                self._chkAccessTimeAllDay.click()
        return  self


    def toggle_accesstime_of_user(self, user_name, select=True):
        """      
        @summary: Check or uncheck event accesstime of user
        @author: Quang Tran
        @created_date: July 25, 2018
        """
        if select:
            if not self._chkAccessTimeOfUser(user_name).get_attribute("style"):
                self._chkAccessTimeOfUser(user_name).click()
        else:
            if self._chkAccessTimeOfUser(user_name).get_attribute("style"):
                self._chkAccessTimeOfUser(user_name).click()
        return  self


    def toggle_show_accesstime(self, default_accesstime=True, member_accesstime=True, temp_accesstime=True):
        """      
        @summary: Check or uncheck Show accesstime on sidebar
        @author: Quang Tran
        @created_date: July 25, 2018
        """
        if default_accesstime:
            self._chkShowDefaultAccesstimes.check()
        else:
            self._chkShowDefaultAccesstimes.uncheck()

        if member_accesstime:
            self._chkShowMemberAccesstimes.check()
        else:
            self._chkShowMemberAccesstimes.uncheck()

        if temp_accesstime:
            self._chkShowTemporaryAccesstimes.check()
        else:
            self._chkShowTemporaryAccesstimes.uncheck()
        return  self

