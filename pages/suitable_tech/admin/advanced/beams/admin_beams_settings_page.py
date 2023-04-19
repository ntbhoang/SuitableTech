from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from pages.suitable_tech.admin.dialogs.choose_users_dialog import ChooseUsersDialog
from pages.suitable_tech.admin.advanced.beams.admin_beams_all_devices_page import AdminBeamsAllDevicesPage
from common.application_constants import ApplicationConst
from core.utilities.utilities import Utilities
from common.helper import Helper

class _AdminBeamsSettingsLocator(object):
    _btnAddAdministrators = (By.XPATH, "//button[@ng-click='addAdminUser()']")
    _btnDeleteGroup = (By.XPATH, "//button[@ng-click='delete()']")
    _chkBattery = (By.ID, "notify_admins_battery")
    _chkLastPilot = (By.ID, "notify_last_pilot")
    _chkAccessRequest = (By.ID, "notify_access_requests")
    _txtAccessRequest = (By.XPATH, "//input[@ng-model='group.access_request_link']")
    _txtDeviceGroupName = (By.XPATH, "//input[@ng-model='inputValue']")
    _btnAddSessionAnswerUser = (By.XPATH, "//button[@ng-click='addAnswerUser()']")
    _chkAllAuthMethods = (By.XPATH, "//input[@ng-model='authMethods.a']")
    _chkSuitableTechnologies = (By.XPATH, "//input[@ng-model='authMethods.s']")
    _chkGoogle = (By.XPATH, "//input[@ng-model='authMethods.g']")    
    _btnCopyToClipboard = (By.XPATH, "//button[contains(@ng-click,'copyToClipboard')]")
    _btnEditGroupName = (By.XPATH, "//button[contains(@ng-click,'turnOnEditMode')]")   
    _btnSaveChangeGroupName =  (By.XPATH, "//button[contains(@ng-click,'save(inputValue)')]")
    _iconBeamContentImage = (By.CSS_SELECTOR, "beam-content-link img")
    _iconEditBeamContent = (By.CSS_SELECTOR, "div[ng-repeat='content in beamContent'] div[ng-click='edit()']")
    _btnRemoveBeamContent = (By.CSS_SELECTOR, "div[ng-repeat='content in beamContent'] div[ng-click='delete()']")
    _btnContinueRemoveBeamContent = (By.CSS_SELECTOR, "button[ng-click='confirmFn()']")
    _btnSaveBeamContent = (By.CSS_SELECTOR, "div[ng-repeat='content in beamContent'] div[ng-click='save()']")
    _btnCancelEditBeamContent = (By.CSS_SELECTOR, "div[ng-repeat='content in beamContent'] div[ng-click='cancel()']")
    _txtStartingHour = (By.CSS_SELECTOR, "div[ng-model='startTime'] input[ng-model='hours']")
    _txtStartingMinute = (By.CSS_SELECTOR, "div[ng-model='startTime'] input[ng-model='minutes']")
    _btnStartingMeridian = (By.CSS_SELECTOR, "div[ng-model='startTime'] button[ng-click='toggleMeridian()']")
    _txtEndingHour = (By.CSS_SELECTOR, "div[ng-model='endTime'] input[ng-model='hours']")
    _txtEndingMinute = (By.CSS_SELECTOR, "div[ng-model='endTime'] input[ng-model='minutes']")
    _btnEndingMeridian = (By.CSS_SELECTOR, "div[ng-model='endTime'] button[ng-click='toggleMeridian()']")

    @staticmethod
    def _itmAdminAvailable(value):
        return (By.XPATH, u"//div[@class=\"available-contacts contacts-list\"]//p[text()=\"{}\"]".format(value))
    @staticmethod
    def _lnkAdminName(value):
        return (By.XPATH, u"//span[@for='user']//a[.=\"{}\"]".format(value))
    @staticmethod
    def _lnkRemoveAdmin(displayed_name):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::div[@class='media-body']//span[contains(@class, 'icon-remove')]".format(displayed_name))
    @staticmethod
    def _chkHasLabel(check_box_label):
        return (By.XPATH, u"//translate[.=\"{}\"]/../input[@type='checkbox']".format(check_box_label))
    @staticmethod
    def _btnRemoveSessionAnswerUser(user_displayed_name):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::div[@class='media-body']//a[@ng-click='removeAnswerUser($event, user)']".format(user_displayed_name))
    @staticmethod
    def _chkBeamContentDay(day):
        return (By.XPATH, u".//div[@ng-click='!isEditing || toggleDay(\"{}\")']/checker/span/span".format(day))
    @staticmethod
    def _lnkAnswerRequestUser(value):
        return (By.XPATH, u"//section[@class='settings-section ng-scope']//span[@for='user']//a[.=\"{}\"]".format(value))


class AdminBeamsSettingsPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam Settings page.
        This page will be opened after clicking Settings tab on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/beams/787/settings/ for more details.
    @page: Beam Settings page
    @author: Thanh Le
    """


    """    Properties    """
    
    @property
    def _iconBeamContentImage(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._iconBeamContentImage)
    @property
    def _iconEditBeamContent(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._iconEditBeamContent)
    @property
    def _btnSaveChangeGroupName(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnSaveChangeGroupName)
    @property
    def _btnEditGroupName(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnEditGroupName)
    @property
    def _btnCopyToClipboard(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnCopyToClipboard)
    @property
    def _chkAllAuthMethods(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkAllAuthMethods)
    @property
    def _chkSuitableTechnologies(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkSuitableTechnologies)
    @property
    def _chkGoogle(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkGoogle)
    @property
    def _txtDeviceGroupName(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._txtDeviceGroupName)
    @property
    def _btnAddAdministrators(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnAddAdministrators)
    @property
    def _btnDeleteGroup(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnDeleteGroup)
    @property
    def _chkBattery(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkBattery)
    @property
    def _chkLastPilot(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkLastPilot)
    @property
    def _chkAccessRequest(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkAccessRequest)
    @property
    def _txtAccessRequest(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._txtAccessRequest)
    @property
    def _btnAddSessionAnswerUser(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnAddSessionAnswerUser)
    @property
    def _btnRemoveBeamContent(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnRemoveBeamContent)
    @property
    def _btnContinueRemoveBeamContent(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnContinueRemoveBeamContent)
    @property
    def _btnSaveBeamContent(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnSaveBeamContent)
    @property
    def _btnCancelEditBeamContent(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnCancelEditBeamContent)
    @property
    def _txtStartingHour(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._txtStartingHour)
    @property
    def _txtStartingMinute(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._txtStartingMinute)
    @property
    def _btnStartingMeridian(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnStartingMeridian)
    @property
    def _txtEndingHour(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._txtEndingHour)
    @property
    def _txtEndingMinute(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._txtEndingMinute)
    @property
    def _btnEndingMeridian(self):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnEndingMeridian)

    def _itmAdminAvailable(self, value):
        return Element(self._driver, *_AdminBeamsSettingsLocator._itmAdminAvailable(value))
    
    def _lnkAdminName(self, value):
        return Element(self._driver, *_AdminBeamsSettingsLocator._lnkAdminName(value))
    
    def _lnkRemoveAdmin(self, displayed_name):
        return Element(self._driver, *_AdminBeamsSettingsLocator._lnkRemoveAdmin(displayed_name))

    def _lnkAnswerRequestUser(self, value):
        return Element(self._driver, *_AdminBeamsSettingsLocator._lnkAnswerRequestUser(value))

    def _chkHasLabel(self, check_box_label):
        """
        we use this method to find and interact with all checkboxes in this page instead of capture all checkboxes Xpath
        """
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkHasLabel(check_box_label))
    def _btnRemoveSessionAnswerUser(self, user_displayed_name):
        return Element(self._driver, *_AdminBeamsSettingsLocator._btnRemoveSessionAnswerUser(user_displayed_name))
    def _chkBeamContentDay(self, day):
        return Element(self._driver, *_AdminBeamsSettingsLocator._chkBeamContentDay(day))

    
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
        self.wait_for_loading(2)
        
    
    def is_administrator_existed(self, admin_name):
        """      
        @summary: Check if an administrator is existed or not 
        @param admin_name: name of administrator would like to check
        @return: True: the admin is existed, False: the admin is not existed
        @author: Thanh Le   
        @created_date: September 30, 2016
        """
        return self._lnkAdminName(admin_name).is_displayed()
    
    
    def change_device_group_name(self, value, wait_for_completed=True):
        """      
        @summary: Change name of a device group     
        @param value: new name would like to change for device group
        @return: AdminBeamsSettingsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        self._btnEditGroupName.click()
        self._txtDeviceGroupName.type(value)
        self._btnSaveChangeGroupName.click()
        if (wait_for_completed):
            self.wait_untill_success_msg_disappeared()
        return self
    
    
    def add_administrator(self, user, wait_for_completed = True):
        """      
        @summary: Add an administrator for a device group      
        @param wait_untill_success_msg_disappeared: dismiss the successful message
        @return: AdminBeamsSettingsPage
        @author: Thanh Le  
        @created_date: September 30, 2016
        """
        self.click_add_administrators_button()
        self.select_administrator(user, wait_for_completed)
        #The Save button is removed from the page (0.43 release)
        #self.save_changes(wait_for_completed)
        return self
    
    
    def click_add_administrators_button(self):
        """      
        @summary: Clicking on "Add Administrators" button      
        @author: Thanh Le  
        @created_date: March 06, 2016
        """
        self.wait_for_loading()
        self._btnAddAdministrators.wait_until_clickable().click_element()
        return AdminBeamsSettingsPage(self._driver)
    
    
    def select_administrator(self, user, wait = True):
        """      
        @summary: select an administrator     
        @author: Thanh Le  
        @created_date: March 06, 2016
        """
        ChooseUsersDialog(self._driver).choose_user(user.email_address)
        if wait:
            #self.wait_for_loading()
            self.wait_untill_success_msg_disappeared()
        return self
    
    
    def is_administrator_exists_in_available(self, user):
        """      
        @summary: Check if an admin exist in available or not   
        @param user: account of admin would like to check 
        @return: True: The Remove button displayed, False: The Remove button is not displayed
        @author: Thanh Le   
        @created_date: March 06, 2017   
        """
        ChooseUsersDialog(self._driver).search_user(user.email_address)
        self.wait_for_loading()
        return self._itmAdminAvailable(user.email_address).is_displayed(2)
    
    
    def get_link_access_request(self):
        """      
        @summary: Get the access request link
        @return: AdminBeamsSettingsPage
        @author: Khoi Ngo    
        @created_date: September 30, 2016
        """
        return self._txtAccessRequest.get_attribute("value")
    
    
    def is_admin_removable(self, displayed_name):
        """      
        @summary: Check if an admin can be removed or not     
        @param displayed_name: name of admin would like to check 
        @return: True: The Remove button displayed, False: The Remove button is not displayed
        @author: Thanh Le   
        @created_date: September 30, 2016   
        """
        self.wait_for_loading(5)
        return self._lnkRemoveAdmin(displayed_name).is_displayed(5)
    
    
    def is_device_group_removable(self):
        """      
        @summary: Check if the Remove button in device group is enable or not   
        @return: True: the Remove button is enable, False: the Remove button is disable
        @author: Thanh Le   
        @created_date: September 30, 2016
        """
        return self._btnDeleteGroup.is_displayed(5)
    
    
    def delete_device_group(self, wait_for_completed=True):
        """      
        @summary: Delete a device group
        @param wait_for_completed: time wait for delete completely 
        @return: AdminBeamsSettingsPage
        @author: Thanh Le    
        @created_date: September 30, 2016
        """
        self._btnDeleteGroup.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
            
        return AdminBeamsAllDevicesPage(self._driver)
    
    
    def remove_admin_user(self, diplayed_name, wait_for_completed=True):
        """      
        @summary: Remove admin user by full name
        @param diplayed_name: full name of an admin would like to remove 
        @param wait_for_completed: time wait for remove completely 
        @return: AdminBeamsSettingsPage
        @author: Thanh Le    
        @created_date: September 30, 2016
        """
        self._lnkRemoveAdmin(diplayed_name).wait_until_clickable().click_element()
        return self
    
       
    def _toogle_check_box(self, check_box_label, select=True):
        """      
        @summary: Toggle a check box in Settings page by label
        @param check_box_label: label of which check box would like to toogle
        @param select: check or un-check the checkbox
        @return: AdminBeamsSettingsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        @note: Due to 'Save Change' button is only enabled when Device group setting page has a change so we need to uncheck
        then check again to make a change.
        """
        if(select):
            if not (self._chkHasLabel(check_box_label).is_selected()):
                self._chkHasLabel(check_box_label).scroll_to().check()
        else:
            if (self._chkHasLabel(check_box_label).is_selected()):
                self._chkHasLabel(check_box_label).scroll_to().uncheck()
            
    
    def toggle_request_access_notification(self, select=True):
        """      
        @summary: Toggle the 'Notify administrators when someone requests access to this group' checkbox
        @param select: check or uncheck
        @return: AdminBeamsSettingsPage
        @author: Thanh Le  
        @created_date: September 30, 2016 
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_REQUEST_ACCESS, select)
        return self       
    
    
    def toggle_left_off_charger_notification_for_admin(self, select=True):
        """      
        @summary: Toggle 'Notify administrators if a Beam is left off the charger' checkbox
        @param select: check or uncheck the checkbox
        @return: AdminBeamsSettingsPage
        @author: Thanh Le    
        @created_date: September 30, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_ADMIN_IF_BEAM_LEFT_OFF_CHARGER, select)
        return self
    
    
    def toggle_left_off_charger_notification_for_last_pilot(self, select=True):
        """      
        @summary: Toggle 'Notify the last pilot if a Beam is left off the charger' checkbox     
        @param select: check or uncheck the checkbox
        @return: AdminBeamsSettingsPage
        @author: Thanh Le 
        @created_date: September 30, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_PILOT_IF_BEAM_LEFT_OFF_CHARGER, select)
        return self  
    
    
    def toggle_left_off_all_authentication_methods(self, select=True):
        """      
        @summary: This action is used to toggle left off all authentication methods 
        @param select: boolean value to decide toogle or not
        @author: Thanh Le 
        @created_date: September 30, 2016   
        """
        self._toogle_check_box(ApplicationConst.LBL_BEAM_ALL_AUTHENTICATION_METHODS, select)
        return self
    
    
    def toggle_left_off_suitable_technologies_methods(self, select=True):
        """      
        @summary: This action is used to toggle left of suitable technology method
        @param select: boolean value to decide toggle or not
        @author: Thanh Le     
        @created_date: September 30, 2016
        """
        if(select):
            self._chkSuitableTechnologies.check()
        else:
            self._chkSuitableTechnologies.uncheck()
        return self
    
    
    def toggle_left_off_google_methods(self, select=True):
        """      
        @summary: This action is used to toggle left off google methods
        @param select: boolean value to decide toggle or not
        @author: Thanh Le   
        @created_date: September 30, 2016 
        """
        if(select):
            self._chkGoogle.check()
        else:
            self._chkGoogle.uncheck()            
        return self 
    

    def add_user_to_session_answer(self, user, wait_for_completed=True):
        """      
        @summary: Add a user to session answer
        @param user: user would like to add to session answer
        @param wait_for_completed: timeout to wait for complete adding
        @return: AdminBeamsSettingsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        self._btnAddSessionAnswerUser.click()
        choose_users_dialog = ChooseUsersDialog(self._driver)
        choose_users_dialog.choose_user(user.email_address)
        
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
            
        return self
        
    
    def remove_user_from_session_answer(self, user, wait_for_completed=True):
        """      
        @summary: Remove a user from session answer
        @param user: user would like to remove from session answer
        @param wait_for_completed: timeout to wait for complete adding
        @return: AdminBeamsSettingsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        self._driver.scroll_down_to_bottom()
        self._btnRemoveSessionAnswerUser(user.get_displayed_name()).click()
        #The Save button is removed from the page (0.43 release)
        #self.save_changes(wait_for_completed)
        return self


    def is_page_displayed(self, time_out=None):
        """      
        @summary: Check if a page is displayed or not
        @param time_out: time to wait for display
        @return: AdminBeamsSettingsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        return self._lblHeader.is_displayed(time_out)
        
    
    def click_copy_to_clipboard_button(self):
        """      
        @summary: Clicking on copy to clipboard button
        @return: AdminBeamsSettingsPage
        @author: Thanh Le
        @created_date: September 30, 2016
        """
        self._btnCopyToClipboard.wait_until_displayed()
        self._btnCopyToClipboard.click()
        return self
    
    
    def is_beam_content_image_display(self, time_out=None):        
        return self._iconBeamContentImage.is_displayed(time_out)
    
    def get_beam_content_icon_link(self):
        """      
        @summary: Get user icon link of a user
        @return: file_url: correct user icon link
        @author: Quang Tran
        """
        file_url = self._iconBeamContentImage.get_attribute("src")
        return Utilities.correct_link(file_url)
    
    
    def goto_setting_tab(self):
        """      
        @summary: Click Notifications link to go to Notifications tab        
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        
        self._lnkSetting.click_element()
        self.wait_for_loading()
        from pages.suitable_tech.accountsettings.account_settings_page import AccountSettingsPage
        return AccountSettingsPage(self._driver)        
    
    
    def select_Dispplay_url_connect_invitation(self, select = True):
        self._toogle_check_box(ApplicationConst.LBL_DISPLAY_URL_REQUEST, select)    
        self.wait_untill_success_msg_disappeared()
        return self


    def open_edit_beam_content(self):
        """
        @summary: Open edit beam content
        @author: Thanh Le
        @created_date: September 22, 2017
        """
        self._iconEditBeamContent.wait_until_clickable().scroll_to().click()
        return self


    def remove_beam_content_image(self):
        """
        @summary: Remove beam content image
        @author: Thanh Le
        @created_date: September 22, 2017
        """
        self.open_edit_beam_content()
        self._btnRemoveBeamContent.wait_until_clickable().click()
        #user jsclick to hanld on mobile
        self._btnContinueRemoveBeamContent.wait_until_clickable().jsclick()
        self._iconBeamContentImage.wait_until_disappeared(3)
        return self


    def is_beam_content_image_removed(self):
        """
        @summary: Check if beam content image is removed or not
        @author: Thanh Le
        @created_date: September 22, 2017
        """
        return self._iconBeamContentImage.is_disappeared()


    def select_time_range(self, starting_datetime, ending_datetime):
        """
        @summary: Select a time range of display time
        @param:
            - starting_datetime: select starting time to display
            - ending_datetime: select ending time to display
        @author: Thanh Le
        @created_date: September 25, 2017
        """
        start_hour = starting_datetime.strftime("%I")
        start_minute = starting_datetime.strftime("%M")
        start_meridian = ApplicationConst.get_date_time_label(starting_datetime.strftime("%p"))

        self._txtStartingHour.type( str(start_hour) )
        self._txtStartingMinute.type( str(start_minute) )
        if(self._btnStartingMeridian.text != start_meridian):
            self._btnStartingMeridian.click()

        end_hour = ending_datetime.strftime("%I")
        end_minute = ending_datetime.strftime("%M")
        end_meridian = ApplicationConst.get_date_time_label(ending_datetime.strftime("%p"))

        self._txtEndingHour.type( str(end_hour) )
        self._txtEndingMinute.type( str(end_minute) )
        if(self._btnEndingMeridian.text != end_meridian):
            self._btnEndingMeridian.click()
        return self


    def update_beam_content(self, display_days="", starting_datetime="", ending_datetime="", new_image_name="", cancel=False):
        """
        @summary: Update schedule for beam content
        @param display_days: Which days set for beam content displays
        @param starting_datetime: specify starting time for display
        @param ending_datetime: specify ending time for display
        @author: Thanh Le
        @created_date: September 25, 2017
        """
        if new_image_name:
            self.remove_beam_content_image()
            self.open_beam_content_dialog()
            from pages.suitable_tech.admin.dialogs.beam_content_dialog import BeamContentDialog
            BeamContentDialog(self._driver).choose_beam_content_image(new_image_name)

        self.open_edit_beam_content()
        if display_days:
            all_days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
            for acronym_day in all_days:
                if "glyphicon-check" in self._chkBeamContentDay(acronym_day).get_attribute("class"):
                    self._chkBeamContentDay(acronym_day).click()

            display_days = display_days.split(',')
            for day in display_days:
                self._chkBeamContentDay(day[:3]).click()

        if starting_datetime and ending_datetime:
            self.select_time_range(starting_datetime, ending_datetime)

        if cancel == False:
            self._btnSaveBeamContent.wait_until_clickable().scroll_to().click()
        else:
            self._btnCancelEditBeamContent.wait_until_clickable().scroll_to().click()
        return self


    def is_beam_content_days_updated(self, display_days):
        """
        @summary: Check if beam content days is updated or not
        @param display_days: Which days set for beam content displays
        @author: Thanh Le
        @created_date: September 25, 2017
        """
        display_days = display_days.split(',')
        for day in display_days:
            if "glyphicon-check" not in self._chkBeamContentDay(day[:3]).get_attribute("class"):
                return False
        return True


    def is_beam_content_days_default_value(self):
        """
        @summary: Check if beam content days is default value or not
        @author: Thanh Le
        @created_date: September 25, 2017
        """
        all_days = ["mon", "tue", "wed", "thu", "fri"]
        for day in all_days:
            if "glyphicon-check" not in self._chkBeamContentDay(day).get_attribute("class"):
                return False
        starting_datetime = Helper.generate_date_time(hour_delta=8)
        ending_datetime = Helper.generate_date_time(hour_delta=18)
        return self.is_beam_content_time_updated(starting_datetime, ending_datetime)


    def is_beam_content_time_updated(self, starting_datetime, ending_datetime):
        """
        @summary: Check if beam content time is updated or not
        @param starting_datetime: specify starting time for display
        @param ending_datetime: specify ending time for display
        @author: Thanh Le
        @created_date: September 25, 2017
        """
        if starting_datetime.strftime("%I") == self._txtStartingHour.get_attribute("value")\
            and starting_datetime.strftime("%M") == self._txtStartingMinute.get_attribute("value")\
            and ApplicationConst.get_date_time_label(starting_datetime.strftime("%p")) == self._btnStartingMeridian.text\
            and ending_datetime.strftime("%I") ==  self._txtEndingHour.get_attribute("value")\
            and ending_datetime.strftime("%M") == self._txtEndingMinute.get_attribute("value")\
            and ApplicationConst.get_date_time_label(ending_datetime.strftime("%p")) == self._btnEndingMeridian.text:
            return True
        return False


    def is_UI_auth_methods_disabled(self):
        """
        @summary: Check if UI auth methods is disabled or not
        @author: Khoi Ngo
        @created_date: October 9, 2017
        """
        if self._chkAllAuthMethods.get_attribute("disabled")\
            and self._chkSuitableTechnologies.get_attribute("disabled")\
            and self._chkGoogle.get_attribute("disabled"):
            return True
        return False


    def is_user_displayed_in_session_answer(self, user_name):
        """      
        @summary: Check if an user is existed or not in Session Answer
        @param user_name: name of user would like to check
        @return: True: the user is existed, False: the user is not existed
        @author: Thanh Le   
        @created_date: Oct 25, 2017
        """
        return self._lnkAnswerRequestUser(user_name).is_displayed()

