from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.accountsettings.account_setting_common_page import AccountSettingsCommonPage
from common.application_constants import ApplicationConst
from core.webdriver.elements.element_list import ElementList


class _NotificationsPageLocator(object):
    _btnEnableAll = (By.CSS_SELECTOR, "button[ng-click='enableAll()']")
    _btnDisableAll = (By.CSS_SELECTOR, "button[ng-click='disableAll()']")
    _btnRestoreDefaults = (By.CSS_SELECTOR, "button[ng-click='restoreDefaults()']")
    _lblHeader = (By.CSS_SELECTOR, "h2[class='heading']")
    _chkNotifications = (By.CSS_SELECTOR,"input[type='checkbox']")
    
    @staticmethod
    def _chkHasLabel(check_box_label):
        return (By.XPATH, u"//td[.=\"{}\"]/following-sibling::td/input[@type='checkbox']".format(check_box_label))
        
    
class AccountNotificationsPage(AccountSettingsCommonPage):
    """
    @description: This is page object class for Notifications page.
        This page will be opened after clicking Notifications link in Your Account page.
        Please visit https://staging.suitabletech.com/manage/#/account/notifications/ for more details.
    @page: Notifications page
    @author: Thanh Le
    """

    """    Properties """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_NotificationsPageLocator._lblHeader)
    @property
    def _btnEnableAll(self):
        return Element(self._driver, *_NotificationsPageLocator._btnEnableAll)
    @property
    def _btnDisableAll(self):
        return Element(self._driver, *_NotificationsPageLocator._btnDisableAll)
    @property
    def _btnRestoreDefaults(self):
        return Element(self._driver, *_NotificationsPageLocator._btnRestoreDefaults)
    @property
    def _chkNotifications(self):
        return ElementList(self._driver, *_NotificationsPageLocator._chkNotifications)

    def _chkHasLabel(self, check_box_label):
        """
        We use this method to find and interact with all checkboxes in this page instead of capture all checkboxes Xpath
        """
        return Element(self._driver, *_NotificationsPageLocator._chkHasLabel(check_box_label))
    
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method        
        @param driver: Web Driver
        @author: Thanh Le
        @created_date: August 05, 2016
        """  
        AccountSettingsCommonPage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
    
    
    def _toogle_check_box(self, check_box_label, select=True, wait_for_completed=True):
        """      
        @summary: Toggle any checkbox using checkbox's label and select value        
        @param check_box_label: checkbox's label
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._driver.scroll_down_to_bottom()
        class_attribute = self._chkHasLabel(check_box_label).get_attribute("class")
        action = True
        if select:
            if class_attribute.find("ng-not-empty")>0:
                action = False
            else:
                self._chkHasLabel(check_box_label).wait_until_clickable().check()
        else:
            if class_attribute.find("ng-empty")>0:
                action = False
            else:
                self._chkHasLabel(check_box_label).wait_until_clickable().uncheck()
        
        if wait_for_completed and action:
            self.wait_untill_success_msg_disappeared()
    
    
    def toggle_become_admin_notification(self, select=True):
        """      
        @summary: Toggle checkbox "I become an administrator".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_BECOME_AN_ADMIN, select)
        return self
    
    
    def toggle_added_or_removed_from_device_group_notification(self, select=True):
        """      
        @summary: Toggle checkbox "I am added to or removed from a device group".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_ADDED_OR_REMOVED_FROM_DEVICE_GROUP, select)
        return self
    
    
    def toggle_device_group_members_are_added_or_removed(self, select=True):
        """      
        @summary: Toggle checkbox "Device group members are added or removed".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_DEVICE_MEMBERS_GROUP_ARE_ADDED_REMOVED, select)
        return self
    
    
    def toggle_device_groups_are_added_or_removed(self, select=True):
        """      
        @summary: Toggle checkbox "Device groups are added or removed".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_DEVICE_GROUPS_ARE_ADDED_REMOVED, select)
        return self
    
    
    def toggle_device_groups_settings_are_changed(self, select=True):
        """      
        @summary: Toggle checkbox "Device group settings are changed".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_DEVICE_GROUPS_SETTINGS_ARE_CHANGED, select)
        return self
    
    
    def toggle_i_can_change_device_settings_or_answer_calls(self, select=True):
        """      
        @summary: Toggle checkbox "Device group settings are changed".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_I_CAN_CHANGE_DEVICE_SETTINGS_OR_ANSWER_CALLS, select)
        return self
    
    
    def toggle_i_reserve_beams(self, select=True):
        """      
        @summary: Toggle checkbox "I reserve Beams".        
        @param select: Set select=True to check, select=False to uncheck. Default value is True
        @return: AccountNotificationsPage page object
        @author: Tan Le
        @created_date: September 21, 2017
        """
        self._toogle_check_box(ApplicationConst.CHK_NOTIFY_I_RESERVE_BEAMS, select)
        return self
    
    
    def enable_all_notifications(self):
        """      
        @summary: Select all checkboxes
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._btnEnableAll.wait_until_clickable().click()
        self.wait_for_loading()
        return self


    def are_all_notifications_enabled(self):
        """
        @summary: Check if all checkboxes are selected or not
        @return: AccountNotificationsPage page object
        @author: Khoi Ngo
        @created_date: September 29, 2017
        """
        all_chkboxes = self._chkNotifications.get_all_elements()
        for chkbox in all_chkboxes:
            if not chkbox.is_selected():
                return False
        return True


    def disable_all_notifications(self):
        """
        @summary: Deselect all checkboxes
        @return: AccountNotificationsPage page object
        @author: Khoi Ngo
        @created_date: September 29, 2017
        """
        self._btnDisableAll.wait_until_clickable().click()
        self.wait_for_loading()
        return self


    def are_all_notifications_disabled(self):
        """
        @summary: Check if all checkboxes are deselected or not
        @return: AccountNotificationsPage page object
        @author: Khoi Ngo
        @created_date: September 29, 2017
        """
        all_chkboxes = self._chkNotifications.get_all_elements()
        for chkbox in all_chkboxes:
            if chkbox.is_selected():
                return False
        return True


    def get_notifications_checkboxes_status(self):
        """
        @summary: Get default value of all checkboxes
        @return: AccountNotificationsPage page object
        @author: Khoi Ngo
        @created_date: September 29, 2017
        """
        all_chkboxes = self._chkNotifications.get_all_elements()
        chk_list = []
        for chkbox in all_chkboxes:
            chk_list.append(chkbox.is_selected())
        return chk_list


    def restore_to_default_notifications(self):
        """
        @summary: Restore all checkboxes to their default value
        @return: AccountNotificationsPage page object
        @author: Khoi Ngo
        @created_date: September 29, 2017
        """
        self._btnRestoreDefaults.wait_until_clickable().click()
        self.wait_for_loading()
        return self

