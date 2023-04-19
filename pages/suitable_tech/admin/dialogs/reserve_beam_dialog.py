from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.editable_combobox import EditableCombobox
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from datetime import datetime
from core.webdriver.elements.datepicker import DatePicker
from common.helper import Helper
import locale
from common.constant import Language, Locale

class _ReserveABeamDialogLocator(object):
    _ecbxUser = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='reservation.user']")
    _txtStartingDate = (By.XPATH, "//div[@class='modal-content']//label[@for='start_date']/following-sibling::div//input")
    _txtStartingHour = (By.CSS_SELECTOR, "div[ng-model='reservation.start_time'] input[ng-model='hours']")
    _txtStartingMinute = (By.CSS_SELECTOR, "div[ng-model='reservation.start_time'] input[ng-model='minutes']")
    _btnStartingMeridian = (By.CSS_SELECTOR, "div[ng-model='reservation.start_time'] button[ng-click='toggleMeridian()']")
    _btnStartingDatePicker = (By.XPATH, "//div[@class='modal-content']//label[@for='start_date']/following-sibling::div/span[@class='input-group-btn']//button")
    _txtEndingDate = (By.XPATH, "//div[@class='modal-content']//label[@for='end_date']/following-sibling::div//input")
    _txtEndingHour = (By.CSS_SELECTOR, "div[ng-model='reservation.end_time'] input[ng-model='hours']")
    _txtEndingMinute = (By.CSS_SELECTOR, "div[ng-model='reservation.end_time'] input[ng-model='minutes']")
    _btnEndingMeridian = (By.CSS_SELECTOR, "div[ng-model='reservation.end_time'] button[ng-click='toggleMeridian()']")
    _btnEndingDatePicker = (By.XPATH, "//div[@class='modal-content']//label[@for='end_date']/following-sibling::div/span[@class='input-group-btn']//button")
    _btnDeleteReservation = (By.XPATH, "//div[@class='modal-content']//button[@class='btn btn-danger pull-left ng-scope']")
    _btnCustomTimeZone = (By.XPATH, "//div[@class='modal-content']//div[@class='btn-group']//label[contains(@uib-btn-radio,'custom')]")
    _ecbxCustomTimeZone = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='customTimeZone.name']")
    _lblAlertMessage = (By.XPATH, "//div[@class='alert alert-warning ng-scope']")
    
class ReserveABeamDialog(DialogBase):
    """
    @description: This is page object class for Reserve A Beam Dialog. You need to init it before using in page class.
    @page: Reserve A Beam Dialog
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _ecbxUser(self):
        return EditableCombobox(self._driver, *_ReserveABeamDialogLocator._ecbxUser)
    @property
    def _txtStartingDate(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._txtStartingDate)    
    @property
    def _txtStartingHour(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._txtStartingHour)        
    @property
    def _txtStartingMinute(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._txtStartingMinute)        
    @property
    def _btnStartingMeridian(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._btnStartingMeridian)
    @property
    def _btnStartingDatePicker(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._btnStartingDatePicker)
    @property
    def _txtEndingDate(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._txtEndingDate)
    @property
    def _txtEndingHour(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._txtEndingHour)        
    @property
    def _txtEndingMinute(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._txtEndingMinute)        
    @property
    def _btnEndingMeridian(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._btnEndingMeridian)
    @property
    def _btnEndingDatePicker(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._btnEndingDatePicker)    
    @property
    def _btnDeleteReservation(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._btnDeleteReservation)
    @property
    def _lblSuccessMessage(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._lblSuccessMessage)
    @property
    def _btnCustomTimeZone(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._btnCustomTimeZone)   
    @property
    def _ecbxCustomTimeZone(self):
        return EditableCombobox(self._driver, *_ReserveABeamDialogLocator._ecbxCustomTimeZone)
    @property
    def _lblAlertMessage(self):
        return Element(self._driver, *_ReserveABeamDialogLocator._lblAlertMessage)
    
    
    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """          
        DialogBase.__init__(self, driver)
    
        
    def reserve_a_beam(self, start_time, end_time, user=None, correct_time=True):
        """
        @summary: This action use to reserve a beam
        @author: Thanh Le
        @parameter: device_name: beam device
        @parameter: user_name: user name string
        @parameter: start_date: starting date
        @parameter: end_date: ending date
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: March 15, 2017
        """
        from core.i18n.i18n_support import I18NSupport
        if(user != None):
            self._ecbxUser.select_value_that_search_value_is_different_displayed_value(user.email_address, user.first_name + " " + user.last_name, "//div[@class='modal-content']//div[@ng-model='reservation.user']")

        if(start_time):
            self.select_starting_date(start_time)
            self._txtStartingHour.type(datetime.strftime(start_time, "%I"))
            self._txtStartingMinute.type(datetime.strftime(start_time, "%M"))
            meridian = I18NSupport.localize_date_time_string(datetime.strftime(start_time, "%p"))
            
            if(self._btnStartingMeridian.text != meridian):
                self._btnStartingMeridian.click()
                
        if(end_time):
            self.select_ending_date(end_time)
            self._txtEndingHour.type(datetime.strftime(end_time, "%I"))
            self._txtEndingMinute.type(datetime.strftime(end_time, "%M"))
            meridian = I18NSupport.localize_date_time_string(datetime.strftime(end_time, "%p"))
            
            if(self._btnEndingMeridian.text != meridian):
                self._btnEndingMeridian.click()
                
        self.submit(correct_time)
        if correct_time:
            self._wait_for_dialog_disappeared()
            from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage 
            return AdminBeamDetailPage(self._driver)
        else:
            return self
    
        
    def select_starting_date(self, start_date):
        """
        @summary: This action is used to select starting date
        @author: Thanh Le
        @parameter: start_date:: starting date
        """
        self._btnStartingDatePicker.wait_until_clickable().click()
        date_picker = DatePicker(self._driver, By.XPATH, "//label[@for='start_date']/following-sibling::div//ul")
        if not date_picker.is_displayed(1):
            self._btnStartingDatePicker.jsclick()
        date_picker.select_day(int(datetime.strftime(start_date, "%d")), int(datetime.strftime(start_date, "%m")), int(datetime.strftime(start_date, "%Y")))
    
    
    def select_ending_date(self, end_date):
        """
        @summary: This action is used to select ending date
        @author: Thanh Le
        @parameter: end_date: ending date
        """
        self._btnEndingDatePicker.scroll_to().click()
        date_picker = DatePicker(self._driver, By.XPATH, "//label[@for='end_date']/following-sibling::div//ul")
        if not date_picker.is_displayed(1):
            self._btnStartingDatePicker.jsclick()
        date_picker.select_day(int(datetime.strftime(end_date, "%d")), int(datetime.strftime(end_date, "%m")), int(datetime.strftime(end_date, "%Y")))
        
    
    def delete_the_reservation(self):
        """
        @summary: This action is used to delete the reservation
        @return: AdminReservationsPage / AdminBeamDetailPage
        @author: Thanh Le
        @created_date: March 20, 2017
        """
        self._btnDeleteReservation.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        confirm_dialog = ConfirmActionDialog(self._driver)
        if not confirm_dialog._btnContinue.is_displayed(2): 
            self._btnDeleteReservation.jsclick()
        confirm_dialog.continue_dialog()
        
        from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage
        return AdminBeamDetailPage(self._driver)
    
    
    def custom_timezone(self, time_zone):
        """
        @summary: This action is used to click Custom Time Zone button
        @return: AdminReservationsPage / AdminBeamDetailPage
        @author: Tan Le
        @created_date: October 10, 2017
        """
        self._btnCustomTimeZone.wait_until_clickable().click()
        self._ecbxCustomTimeZone.wait_until_clickable()
        self._ecbxCustomTimeZone.select(time_zone, self._ecbxCustomTimeZone._value)
        return self
    
    def save_changes(self):
        self.submit()
        self._wait_for_dialog_disappeared()
        from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage 
        return AdminBeamDetailPage(self._driver)
                
        
    def does_start_time_display_correctly(self, start_time, time_zone):
        new_time = Helper.convert_time_base_on_timezone(start_time, time_zone)
        displayed_day = self._driver.execute_script("return $(\"input[ng-model='reservation.start_date']\").val()")
        expected_day = self.format_day_on_edit_reservation_dialog(new_time)
        locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
        """Start day"""
        if(displayed_day != expected_day):
            print("Start day does not update as time zone")
            return False
        
        """timezone"""
        xpath = "//input[@ng-model='reservation.start_date']/ancestor::div[@class='well']/span[@class='small ng-binding']"
        displayed_timezone = self._driver.find_element(by=By.XPATH, value = xpath).text
        if displayed_timezone != "(" + time_zone + ")":
            print("At time in start time display incorrectly")
            return False
        
        """time"""
        displayed_time = u"{}:{} {} {}"
        displayed_hour = self._driver.execute_script("return $(\"div[ng-model='reservation.start_time'] input[placeholder='HH']\").val()")
        displayed_minute = self._driver.execute_script("return $(\"div[ng-model='reservation.start_time'] input[placeholder='MM']\").val()")
        displayed_meridian = self._driver.execute_script("return $(\"div[ng-model='reservation.start_time'] button[ng-click='toggleMeridian()']\").text()")
        xpath = "//div[@ng-model='reservation.start_time']/following-sibling::span"
        displayed_tz = self._driver.find_element(by=By.XPATH, value=xpath ).text
        displayed_time = displayed_time.format(displayed_hour, displayed_minute, displayed_meridian, displayed_tz)
        expected_time = self.format_time_on_edit_reservation_dialog(new_time)

        if(displayed_time != expected_time):
            print("Start time display incorrectly. Expect '{}' but found '{}'".format(expected_time, displayed_time))
            return False
        
        return True
            
            
    def does_end_time_display_correctly(self, start_time, time_zone):
        new_time = Helper.convert_time_base_on_timezone(start_time, time_zone)
        displayed_day = self._driver.execute_script("return $(\"input[ng-model='reservation.end_date']\").val()")
        expected_day = self.format_day_on_edit_reservation_dialog(new_time)
        locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
        """Start day"""
        if(displayed_day != expected_day):
            print("End day does not update as time zone")
            return False
        
        """timezone"""
        xpath = "//input[@ng-model='reservation.end_date']/ancestor::div[@class='well']/span[@class='small ng-binding']"
        displayed_timezone = self._driver.find_element(by=By.XPATH, value = xpath).text
        if displayed_timezone != "(" + time_zone + ")":
            print("At time in end time display incorrectly")
            return False
        
        """time"""
        displayed_time = u"{}:{} {} {}"
        displayed_hour = self._driver.execute_script("return $(\"div[ng-model='reservation.end_time'] input[placeholder='HH']\").val()")
        displayed_minute = self._driver.execute_script("return $(\"div[ng-model='reservation.end_time'] input[placeholder='MM']\").val()")
        displayed_meridian = self._driver.execute_script("return $(\"div[ng-model='reservation.end_time'] button[ng-click='toggleMeridian()']\").text()")
        xpath = "//div[@ng-model='reservation.end_time']/following-sibling::span"
        displayed_tz = self._driver.find_element(by=By.XPATH, value=xpath ).text
        displayed_time = displayed_time.format(displayed_hour, displayed_minute, displayed_meridian, displayed_tz)
        expected_time = self.format_time_on_edit_reservation_dialog(new_time)
        if(displayed_time != expected_time):
            print("End time display incorrectly. Expect '{}' but found '{}'".format(expected_time, displayed_time))
            return False

        return True
    
    
    def format_day_on_edit_reservation_dialog(self, time):
        language = self._driver._driverSetting.language
        if language == Language.ENGLISH:
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
        elif language == Language.FRENCH:
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.FR))
        else:
            result = u"{}月 {}"
            return result.format(str(int(time.strftime("%m"))), time.strftime("%d, %Y"))
        
        result = time.strftime("%B %d, %Y")
        locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
        return result
    
    
    def format_time_on_edit_reservation_dialog(self, time):
        result = time.strftime("%I:%M %p %Z")
        if self._driver._driverSetting.language == Language.JAPANESE:
            if time.strftime("%p")=="AM":
                return result.replace("AM", "午前")
            else:
                return result.replace("PM", "午後")
        return result
            

    def is_alert_dialog_msg_display(self, wait_time = None):
        return self._lblAlertMessage.is_displayed(wait_time)


    def get_alert_dialog_msg (self):
        self._lblAlertMessage.wait_until_displayed()
        return self._lblAlertMessage.text
    