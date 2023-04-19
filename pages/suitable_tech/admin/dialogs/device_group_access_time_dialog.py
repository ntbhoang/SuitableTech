from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from core.webdriver.elements.dropdownlist import DropdownList
from data_test.dataobjects.enum import WeekDays
from common.application_constants import ApplicationConst
from time import sleep


class AccessTimesDialogLocator(object):
    _ddlMemberChooser = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='accesstime.device_group_membership']")
    _txtFixedMemberDisplayedName = (By.XPATH, "//div[@class='modal-content']//span[@ng-show='fixedMember']")
    _btnAllDay = (By.XPATH, "//div[@class='modal-content']//div[@class='btn-group']/button[1]")
    _btnTimeRange = (By.XPATH, "//div[@class='modal-content']//div[@class='btn-group']/button[2]")
    _txtStartingHour = (By.CSS_SELECTOR, "form div[ng-model='accesstime.start_time'] input[ng-model='hours']")
    _txtStartingMinute = (By.CSS_SELECTOR, "form div[ng-model='accesstime.start_time'] input[ng-model='minutes']")
    _btnStartingMeridian = (By.CSS_SELECTOR, "form div[ng-model='accesstime.start_time'] button[ng-click='toggleMeridian()']")
    _txtEndingHour = (By.CSS_SELECTOR, "form div[ng-model='accesstime.end_time'] input[ng-model='hours']")
    _txtEndingMinute = (By.CSS_SELECTOR, "form div[ng-model='accesstime.end_time'] input[ng-model='minutes']")
    _btnEndingMeridian = (By.CSS_SELECTOR, "form div[ng-model='accesstime.end_time'] button[ng-click='toggleMeridian()']")
    _chkRequiredSessionAnswer = (By.CSS_SELECTOR, "input[ng-model='accesstime.answer_required']")
    
    @staticmethod
    def _chkWeekday(day_label):
        return (By.XPATH, u"//div[@class='modal-content']//label//translate[.=\"{}\"]/../input".format(day_label))
    
    
class CreateDefaultAccessTimeDialog(DialogBase):
    """
    @description: This page object is used for Creating Default Access Time Dialog
    This dialog appear when user select a Device group and want to set access time for this
    @page: Default Access Time Dialog
    @author: Quang Trang
    """


    """    Properties    """    
    @property
    def _btnAllDay(self):
        return Element(self._driver, *AccessTimesDialogLocator._btnAllDay)
    @property
    def _btnTimeRange(self):
        return Element(self._driver, *AccessTimesDialogLocator._btnTimeRange)
    @property
    def _txtStartingHour(self):
        return Element(self._driver, *AccessTimesDialogLocator._txtStartingHour)        
    @property
    def _txtStartingMinute(self):
        return Element(self._driver, *AccessTimesDialogLocator._txtStartingMinute)        
    @property
    def _btnStartingMeridian(self):
        return Element(self._driver, *AccessTimesDialogLocator._btnStartingMeridian)
    @property
    def _txtEndingHour(self):
        return Element(self._driver, *AccessTimesDialogLocator._txtEndingHour)        
    @property
    def _txtEndingMinute(self):
        return Element(self._driver, *AccessTimesDialogLocator._txtEndingMinute)        
    @property
    def _btnEndingMeridian(self):
        return Element(self._driver, *AccessTimesDialogLocator._btnEndingMeridian)
    @property
    def _chkRequiredSessionAnswer(self):
        return Element(self._driver, *AccessTimesDialogLocator._chkRequiredSessionAnswer)
    
    def _chkWeekday(self, day_label):
        return Element(self._driver, *AccessTimesDialogLocator._chkWeekday(day_label))
        
        
    """    Methods    """
    def __init__(self, driver):     
        """      
        @summary: Constructor method   
        @param driver: web driver
        @author: Quang Tran
        """   
        DialogBase.__init__(self, driver)
    
    
    def check_all_week_days(self):
        """      
        @summary: Select all week days of Access time dialog
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """  
        self._wait_for_loading_completed()
        sleep(1)
        for day in WeekDays:
            self._chkWeekday(ApplicationConst.get_date_time_label(day.name)).check()
        return self
        
        
    def uncheck_all_week_days(self):  
        """      
        @summary: De-select all week days of Access time dialog
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """    
        self._wait_for_loading_completed()
        sleep(1)
        for day in WeekDays:
            tmpday = ApplicationConst.get_date_time_label(day.name)
            self._chkWeekday(tmpday).wait_until_displayed(2)
            self._chkWeekday(tmpday).uncheck()
        return self
    
    
    def select_a_weekday(self, weekday = WeekDays.Mon):
        """      
        @summary: Select a specific day in week days
        @param:  weekday: the day would like to select
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """    
        self._wait_for_loading_completed()
        sleep(1)
        self._chkWeekday(ApplicationConst.get_date_time_label(weekday.name)).check()
        return self
    
    
    def select_weekdays(self, days):
        """      
        @summary: Select a specific days in week days
        @param:  days: the day would like to select
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """    
        
        self.uncheck_all_week_days()
        for day in days:
            self._chkWeekday(ApplicationConst.get_date_time_label(day.name)).check()
        return self
        
        
    def select_user(self, user):
        """      
        @summary: Select a user when creating a access time
        @param:  user: the day would like to select
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """    
        
        self._ddlMemberChooser.select_by_text(user)
        return self
    
    
    def select_all_day_button(self):
        """      
        @summary: Click all day button
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """    
        self._btnAllDay.click()
        return self
    
    
    def select_time_range(self, starting_datetime, ending_datetime ):
        """      
        @summary: Select a time range of access time
        @param:  
            - starting_datetime: select starting time to create access time
            - ending_datetime: select ending time to create access time
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """  
        start_hour = starting_datetime.strftime("%I")
        start_minute = starting_datetime.strftime("%M")
        start_meridian = ApplicationConst.get_date_time_label(starting_datetime.strftime("%p"))
        end_hour = ending_datetime.strftime("%I")
        end_minute = ending_datetime.strftime("%M")
        end_meridian = ApplicationConst.get_date_time_label(ending_datetime.strftime("%p"))
        
        self._btnTimeRange.click()
        
        self._txtStartingHour.type( str(start_hour) )
        self._txtStartingMinute.type( str(start_minute) )
        if(self._btnStartingMeridian.text != start_meridian):
                self._btnStartingMeridian.click()
        
        self._txtEndingHour.type( str(end_hour) )
        self._txtEndingMinute.type( str(end_minute) )
        if(self._btnEndingMeridian.text != end_meridian):
                self._btnEndingMeridian.click()
    
    
    def set_required_session_answer(self, checked = True):
        """      
        @summary: Check required session answer checkbox
        @param:  check: set or not set
        @return: CreateDefaultAccessTimeDialog
        @author: Quang Tran
        """ 
    
        if(checked):
            self._chkRequiredSessionAnswer.check()
        else:
            self._chkRequiredSessionAnswer.uncheck()

    
class EditDefaultAccessTimeDialog(CreateDefaultAccessTimeDialog):
    """
    @description: This page object is used for Edit Default Access Time Dialog
    This dialog appear when user select a Device group and want to edit access time
    @page: Edit Default Access Time Dialog
    @author: Quang Tran
    """
    
    
    """    Properties    """    
    @property
    def _btnDelete(self):
        return Element(self._driver, By.XPATH, "//div[@class='modal-content']//button[@ng-click='delete()']")
    
    
    """    Methods    """ 
    def __init__(self, driver):
        CreateDefaultAccessTimeDialog.__init__(self, driver)
        

class CreateMemberAccessTimeDialog(CreateDefaultAccessTimeDialog): 
    """
    @description: This page object is used for Creating Member Access Time Dialog
    This dialog appear when user select a Device group and want to create member access time
    @page: Create Member Access Time Dialog
    @author: Quang Tran
    """


    """    Properties    """
    @property
    def _ddlMemberChooser(self):
        return DropdownList(self._driver, *AccessTimesDialogLocator._ddlMemberChooser)
    @property
    def _txtFixedMemberDisplayedName(self):
        return Element(self._driver, *AccessTimesDialogLocator._txtFixedMemberDisplayedName)
     
     
    """    Methods    """      
    def __init__(self, driver):
        """      
        @summary: Constructor method   
        @param driver: web driver
        @author: Quang Tran
        """   
        CreateDefaultAccessTimeDialog.__init__(self, driver)
    

    def select_user(self, user):
        """      
        @summary: Select user to add access time   
        @param user: user would like to add to access time
        @return: CreateMemberAccessTimeDialog
        @author: Quang Tran
        """   
        if( self._txtFixedMemberDisplayedName.is_displayed(5)):
            return self
        
        self._ddlMemberChooser.select_by_text(user.get_displayed_name())
        return self

