from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from core.webdriver.elements.element_list import ElementList
from datetime import datetime


class _AdminReservationsPageLocator(object):
    _btnReserveABeam = (By.XPATH, "//button[@type='button' and @ng-click='addReservation()']")
    _txtSearchReservation = (By.XPATH, "//input[@type='search']")
    _btnClearSearchReservation = (By.XPATH, "//span[contains(@class, 'clear-input')]")
    _lblNoReservations = (By.XPATH, "//h5//span")
    _iconLoading = (By.XPATH, "//div[@class='loading-indicator']")
    _btnShow = (By.XPATH, "//button[@class='btn btn-default dropdown-toggle']")
    _ddlConfirmedReservations = (By.XPATH, "//li[@ng-class=\"{'selected': resFilter.includeConfirmed}\"]")
    _ddlReservationRequests = (By.XPATH, "//li[@ng-class=\"{'selected': resFilter.includeRequests}\"]")
    _ddlRejectedRequests = (By.XPATH, "//li[@ng-class=\"{'selected': resFilter.includeRejected}\"]")
    
    @staticmethod
    def _lnkReservationRecord(value):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::tr[contains(@class, 'reservation')]".format(value))
    

class AdminReservationsPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam Reservations page.
        This page will be opened after clicking Reservations tab on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/beams/787/reservations/ for more details.
    @page: Beam Reservations page
    @author: thanh.viet.le
    """

    """    Properties    """    
    @property
    def _btnReserveABeam(self):
        return Element(self._driver, *_AdminReservationsPageLocator._btnReserveABeam)
    @property
    def _lblErrorMessage(self):
        return Element(self._driver, *_AdminReservationsPageLocator._lblErrorMessage)
    @property
    def _txtSearchReservation(self):
        return Element(self._driver, *_AdminReservationsPageLocator._txtSearchReservation)
    @property
    def _btnClearSearchReservation(self):
        return Element(self._driver, *_AdminReservationsPageLocator._btnClearSearchReservation)
    @property
    def _lblNoReservations(self):
        return Element(self._driver, *_AdminReservationsPageLocator._lblNoReservations)
    @property
    def _iconLoading(self):
        return Element(self._driver, *_AdminReservationsPageLocator._iconLoading)
    @property
    def _btnShow(self):
        return Element(self._driver, *_AdminReservationsPageLocator._btnShow)
    @property
    def _ddlConfirmedReservations(self):
        return Element(self._driver, *_AdminReservationsPageLocator._ddlConfirmedReservations)
    @property
    def _ddlReservationRequests(self):
        return Element(self._driver, *_AdminReservationsPageLocator._ddlReservationRequests)
    @property
    def _ddlRejectedRequests(self):
        return Element(self._driver, *_AdminReservationsPageLocator._ddlRejectedRequests)
    
    def _lnkReservationRecord(self, value):
        return Element(self._driver, *_AdminReservationsPageLocator._lnkReservationRecord(value))
    
    
    """    Methods    """
    def __init__(self, driver):     
        """      
        @summary: Constructor method        
        @param driver: Web driver
        @author: Thanh Le  
        @created_date: September 30, 2016
        """
        AdminBeamsCommonPage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        
    
    def create_reservation(self, device_name=None, user=None, start_time=None, end_time=None):
        """      
        @summary: Create a reservation 
        @param device_name: device name
        @param user: user name
        @param start_time: starting time
        @param end_time: ending time
        @author: Thanh le     
        @created_date: September 30, 2016
        """
        record_starting_date = start_time
        record_period_in_minutes = 10 # default value is 10 minutes
        if(start_time != None and end_time != None):
            record_period_in_minutes = (end_time - start_time).minutes
            
        if(start_time==None and end_time==None):
            available_record = self.find_available_device(device_name, record_starting_date, record_period_in_minutes)
            if(available_record):
                start_time = available_record.get_starting_date_time()
                end_time = available_record.get_ending_date_time()
        
        self._btnReserveABeam.click()
        from pages.suitable_tech.admin.dialogs.reserve_beam_dialog import ReserveABeamDialog        
        reserveBeam = ReserveABeamDialog(self._driver)
        reserveBeam.reserve_a_beam(device_name, user, start_time, end_time)
            
        return self
    
    
    def get_reserve_success_message(self):
        """      
        @summary: This action is used to get reserve success message
        @return: text of message
        @author: Thanh le
        @created_date: September 30, 2016
        """
        return self._lblSuccessMessage.text
    
    
    def is_reservation_displayed(self, value):
        """      
        @summary: Check if reservation is displayed
        @param True: the reservation is displayed
                False: the reservation is not displayed
        @author: Thanh le     
        @created_date: September 30, 2016
        """
        return self._lnkReservationRecord(value).is_displayed()
    
    
    def get_no_reservations_message(self):
        """      
        @summary: This action is used to get no reservation detail text
        @return: the message says no reservation text content
        @author:  Thanh Le       
        @created_date: September 30, 2016
        """
        return self._lblNoReservations.text
    
    
    def delete_reservation(self, value):
        """      
        @summary: This action is used to delete reservation value 
        @param value: reservation value
        @return: AdminReservationsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        self.search_for_reservation(value)
        self._lnkReservationRecord(value).click()
        self._btnDeleteReservation.click()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        self._btnDeleteReservation.wait_until_disappeared()
        self._btnClearSearchReservation.click()
        self._lnkReservationRecord(value).wait_until_disappeared()
        return self
    
    
    def get_reserve_error_message(self):
        """      
        @summary: This action is used to get reserve error message  
        @return: the reserve error message text content
        @author: Thanh le   
        @created_date: September 30, 2016
        """
        return self._lblErrorMessage.text
    
    
    def click_reservation_device_link(self, device_name):
        """      
        @summary: This action is used to click reservation device link  
        @param device name: device name 
        @return: AdminBeamDetailPage
        @author: Thanh le
        @created_date: September 30, 2016
        """
        self._get_reservation_record(device_name).click()
        from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage
        return AdminBeamDetailPage(self._driver, device_name)
    
        
    def click_reservation_user_link(self, user):
        """      
        @summary: this action is used to click reservation user link
        @param user: user name 
        @author: Thanh le   
        @created_date: September 30, 2016
        """
        self._get_reservation_record(user).click()
        from pages.suitable_tech.admin.advanced.users.admin_user_detail_page import AdminUserDetailPage
        return AdminUserDetailPage(self._driver)
    
        
    def search_for_reservation(self, value):      
        """      
        @summary: This action is used for search reservation
        @param value: reservation value 
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        self._txtSearchReservation.type(value)
        return self


    def _get_all_reservation_records(self, device_name=None, reserved_day = None):
        """      
        @summary: This action is used to get all reservation record    
        @param device_name: device name
        @param reserved_day: reservation date
        @author: Thanh le
        @created_date: September 30, 2016
        """
        reservations = []
        
        if(device_name):
            self._txtSearchReservation.type(device_name)
            self._iconLoading.wait_until_disappeared()
            
        day_locator = "//div[@ng-repeat='dateGroup in dateGroups']//h4"
        if(reserved_day):
            day_label = reserved_day.strftime("%A %b %dth")
            day_locator = u"//div[@ng-repeat='dateGroup in dateGroups']//h4[.=\"{}\"]".format(day_label)
            
        day_list = ElementList(self._driver, By.XPATH, day_locator)
        day_count = day_list.count(15)
        
        day_format = "%A %b %dth %Y" # Friday Jul 15th 2016
        current_year = datetime.now().year
        if(day_count > 0):
            all_day_label = day_list.get_all_elements()
            for day_label in all_day_label:
                try:
                    day = datetime.strptime(\
                            ("{} {}".format(day_label.text, current_year)),\
                            day_format)
                    records = self._get_all_reservation_records_on_day(day)
                    if(records):
                        reservations.extend(records)
                except ValueError:
                    pass # ignore
                
        return reservations
    
    
    def _get_all_reservation_records_on_day(self, day):
        """      
        @summary: This action is used to get all reservation record on day 
        @param day: The specific date
        @author: Thanh le
        @created_date: September 30, 2016
        """
        reservations = []
        day_label = day.strftime("%A %b %d") + "th"
        time_locator = u"//h4[.=\"{}\"]/following-sibling::table[1]//td[@class='reservation-time ng-binding']".format(day_label)
        time_list = ElementList(self._driver, By.XPATH, time_locator)
        time_count = time_list.count()
        all_time_items = time_list.get_all_elements()
        
        device_locator = u"//h4[.=\"{}\"]/following-sibling::table[1]//td[@class='reservation-details']/div[1]/div[@class='media-body media-middle']//a".format(day_label)
        device_list = ElementList(self._driver, By.XPATH, device_locator)
        device_count = device_list.count()
        all_device_items = device_list.get_all_elements()
        
        if(time_count == device_count):
            for i in range(0, time_count):
                device_name = all_device_items[i].text
                r_time = all_time_items[i].text.replace("WIB","").strip()
                starting_time = r_time.split("\n")[0] # 11:00 AM
                ending_time = r_time.split("\n")[1]
                
                starting_date_time = self._convert_reserved_time_value_to_date_time(day, starting_time)
                ending_date_time = self._convert_reserved_time_value_to_date_time(day, ending_time)
                if(starting_date_time and ending_date_time):
                    reservations.append(_Reservation(device_name, starting_date_time, ending_date_time))
                    
        return reservations
    
    
    def _convert_reserved_time_value_to_date_time(self, current_day, time_value_to_be_converted):
        """      
        @summary: This action is used to convert reserved time value to date time 
        @param current_day: current date
        @param time_value_to_be_converted: time to convert
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        result_day = None    
        full_day_format = "%b %d %I:%M %p" # Jul 18th 11:00 AM
        time_value_to_be_converted = time_value_to_be_converted.replace("th","").strip()
        try:
            result_day = datetime.strptime(time_value_to_be_converted.replace("th",""), full_day_format)
        except ValueError:
            # time_value_to_be_converted is in format '%I:%M %p'  (11:00 AM)
            day_label = datetime.strftime(current_day, "%b %d ") + time_value_to_be_converted
            try:
                result_day = datetime.strptime(day_label,full_day_format)
            except ValueError:
                pass #ignore
        
        if(result_day):
            result_day = result_day.replace(year = datetime.now().year)
        return result_day
    
    
    def filter_reservation(self, confirmed_reservation, requested_reservation, rejected_reservation):
        """      
        @summary: This action is to filter reservations
        @param confirmed_reservation: True if checking Confirmed Reservation
        @param requested_reservation: True if checking Requested Reservation
        @param rejected_reservation: True if checking Rejected Reservation
        @return: AdminReservationsPage
        @author: Thanh Le  
        @created_date: April 25, 2017
        """      
        does_confirmed_checked = self._driver.find_hidden_element(*_AdminReservationsPageLocator._ddlConfirmedReservations).get_attribute('class') == 'select-item selected'
        does_requested_checked = self._driver.find_hidden_element(*_AdminReservationsPageLocator._ddlReservationRequests).get_attribute('class') == 'select-item selected'
        does_rejected_checked = self._driver.find_hidden_element(*_AdminReservationsPageLocator._ddlRejectedRequests).get_attribute('class') == 'select-item selected'
        
        if(confirmed_reservation and does_confirmed_checked == False) or (does_confirmed_checked and confirmed_reservation == False):
            self._btnShow.click()
            self._ddlConfirmedReservations.wait_until_clickable().click()
        if(requested_reservation and does_requested_checked == False) or (does_requested_checked and requested_reservation == False):
            self._btnShow.click()
            self._ddlReservationRequests.wait_until_clickable().click()
        if(rejected_reservation and does_rejected_checked == False) or (does_rejected_checked and rejected_reservation == False):
            self._btnShow.click()
            self._ddlRejectedRequests.wait_until_clickable().click()
        
        if self._iconLoading.is_displayed(2):
            self._iconLoading.wait_until_disappeared(5)
        return self
        
        
    def are_reservations_filtered_correctly(self, confirmed_reservation, requested_reservation, rejected_reservation):
        """
        @summary: This action is to check that the reservations are filtered correctly or not 
        @param confirmed_reservation: True if Confirmed Reservations display
        @param requested_reservation: True if Requested Reservations display
        @param rejected_reservation: True if Rejected Reservations display
        @return: True if reservations are shown correctly
                 False if reservations are shown incorrectly
        @author: Thanh Le  
        @created_date: April 25, 2017
        """        
        expected_result = [confirmed_reservation, requested_reservation, rejected_reservation]
        actual_result = [True, True, True]
        
        actual_result[0] = not (ElementList(self._driver, By.XPATH, u"//reservations-list//tr[@class='reservation ng-scope confirmed']").count() == 0)
        actual_result[1] = not (ElementList(self._driver, By.XPATH, u"//reservations-list//tr[@class='reservation ng-scope requested']").count() == 0)
        actual_result[2] = not (ElementList(self._driver, By.XPATH, u"//reservations-list//tr[@class='reservation ng-scope rejected']").count() == 0)
        
        return expected_result == actual_result

            
class _Reservation(object):
    def __init__(self, device_name, starting_date_time, ending_date_time):
        """      
        @summary: Constructor method        
        @param device_name: device name
        @param starting_date_time: starting date
        @param ending_date_time: ending date
        @author: Thanh Le  
        @created_date: September 30, 2016
        """
        self._device_name = device_name
        self._starting_date_time = starting_date_time
        self._ending_date_time = ending_date_time
    
        
    def get_device_name(self): 
        """      
        @summary: This action is used to get device name     
        @return: string of device name 
        @author: Thanh Le  
        @created_date: September 30, 2016
        """
        return self._device_name
    
    
    def get_starting_date_time(self):
        """      
        @summary: This action is used to get starting date time  
        @return: date time   
        @author: Thanh Le  
        @created_date: September 30, 2016
        """
        return self._starting_date_time
    
    
    def get_ending_date_time(self):   
        """      
        @summary: This action is used to get ending date time
        @return: date time        
        @author: Thanh Le  
        @created_date: September 30, 2016
        """
        return self._ending_date_time