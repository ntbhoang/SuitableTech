from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.edit_device_dialog import EditDeviceDialog
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from time import sleep
from common.application_constants import ApplicationConst
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime
from common.constant import Browser, Platform
from core.webdriver.elements.element_list import ElementList


class _SimplifiedBeamDetailPageLocator(object):
    _btnEdit = (By.XPATH, "//button[@type='button' and @ng-click='edit()']")
    _btnBeamAdvanced = (By.XPATH, "//button[@class='btn btn-default' and @ng-click='showAdvanced()']")
    _lblBeamLocation = (By.XPATH, "//input[@ng-model='device.location']")
    _txtInvitedEmail = (By.XPATH, "//input[@ng-model='userToAdd']")
    _btnAddUser = (By.XPATH, "//button[@ng-click='addSelectedUser()']")
    _lblAlertMessage = (By.XPATH, "//div[@class='alert alert-success']//span[@ng-bind-html='message.content']")
    _iconLoading = (By.XPATH, "//div[@class='loading-indicator']/span")
    _lblBeamStatus = (By.XPATH, "//div[@class='text-muted' or @class='text-success']")
    _lblBeamProperties = (By.XPATH, "//dl[@class='dl-horizontal item-details']//dt")
    _lblBeamPropertiesValue = (By.XPATH, "//dl[@class='dl-horizontal item-details']//dd")
    
    
    @staticmethod
    def _btnRemoveUser(value):
        return (By.XPATH, u"//a[.=\"{}\"]/../following-sibling::td//div".format(value))
    @staticmethod
    def _chkCanManage(value):
        return (By.XPATH, u"//a[contains(.,\"{}\")]//parent::td//following-sibling::td//input[@ng-model='user._canManageGroup']".format(value))
    @staticmethod
    def _btnRemovePerson(value):
        return (By.XPATH, u"//a[contains(.,\"{}\")]//parent::td//following-sibling::td//button[@class='btn btn-danger btn-sm']".format(value))
    @staticmethod
    def _btnMRemovePerson(value):
        return (By.XPATH, u"//a[contains(.,'{}')]/..//parent::div[@class='col-xs-12']/../..//*[3]//button[@class='btn btn-danger btn-sm pull-right']".format(value))
    @staticmethod
    def _lnkAddedUser(value):
        return (By.XPATH, u"//table[@class='table table-hover']//a[contains(.,\"{}\")]".format(value))
    @staticmethod
    def _lnkMAddedUser(value):
        return (By.XPATH, u"//div[@class='panel panel-default visible-xs']//a[contains(.,\"{}\")]".format(value))

    '''Mobile UI'''
    @staticmethod
    def _chkMCanManage(value):
        return (By.XPATH, u"//a[contains(.,\"{}\")]/..//parent::div[@class='col-xs-12']/..//following-sibling::div[@class='row']//input[@ng-model='user._canManageGroup']".format(value))

class SimplifiedBeamDetailPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Simplified Beam Detail Page.
    This page appear when logging with Simplified user and select to manage a device
    @page:  Simplified Beam Detail Page
    @author: Thanh Le
    """
    
    
    """    Properties    """
    @property
    def _lblAlertMessage(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._lblAlertMessage)
    @property
    def _btnAddUser(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._btnAddUser)
    @property
    def _txtInvitedEmail(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._txtInvitedEmail)    
    @property
    def _btnEdit(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._btnEdit)
    @property
    def _btnBeamAdvanced(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._btnBeamAdvanced)
    @property
    def _lblBeamLocation(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._lblBeamLocation)
    @property
    def _iconLoading(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._iconLoading)
    @property
    def _lblBeamStatus(self):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._lblBeamStatus) 
    @property
    def _lblBeamProperties(self):
        return ElementList(self._driver, *_SimplifiedBeamDetailPageLocator._lblBeamProperties) 
    @property
    def _lblBeamPropertiesValue(self):
        return ElementList(self._driver, *_SimplifiedBeamDetailPageLocator._lblBeamPropertiesValue) 
    
    def _chkCanManage(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._chkCanManage(value))
    def _lnkAddedUser(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._lnkAddedUser(value))
    def _lnkMAddedUser(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._lnkMAddedUser(value))
    def _btnRemoveUser(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._btnRemoveUser(value))
    def _btnRemovePerson(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._btnRemovePerson(value))
    def _btnMRemovePerson(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._btnMRemovePerson(value))
    
    '''Mobile UI'''
    def _chkMCanManage(self, value):
        return Element(self._driver, *_SimplifiedBeamDetailPageLocator._chkMCanManage(value))
    
    """    Methods    """
    def __init__(self, driver):       
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """   
        AdminBeamsCommonPage.__init__(self, driver)
        #This is to make sure page is loaded completely
        self.wait_for_loading()
    
    
    def open_edit_device_dialog(self):
        """      
        @summary: This action is used to open edit device dialog
        @return: EditDeviceDialog
        @author: Thanh Le
        @created_date: 8/17/2016
        """
        self._btnEdit.wait_until_clickable()
        self._btnEdit.click_element()
        if not EditDeviceDialog(self._driver)._txtDeviceName.is_displayed(1):
            self._btnEdit.jsclick()
        return EditDeviceDialog(self._driver)
    
    
    def set_beam_name(self, new_beam_name):
        """      
        @summary: Used to set beam name         
        @param new_beam_name: The new name of Beam
        @return: SimplifiedBeamDetailPage
        @author: Thanh Le
        @created_date: 8/17/2016
        """
        dlg = self.open_edit_device_dialog()
        dlg.set_beam_name(new_beam_name)
        dlg.submit()
        self.wait_untill_success_msg_disappeared()
        
        return self    
    
    
    def set_beam_location(self, beam_location):
        """
        @summary: This action is used to set beam location   
        @author: Thanh Le
        @parameter: <beam_location>: Beam location string
        @return: SimplifiedBeamDetailPage
        """
        dlg = self.open_edit_device_dialog()
        dlg.set_beam_location(beam_location)
        dlg.submit()
        self.wait_untill_success_msg_disappeared()
        return self
    
    
    def set_beam_label(self, beam_label):
        """
        @summary: This action is used to set beam label   
        @author: Thanh Le
        @parameter: <beam_label>: Beam label string
        @return: SimplifiedBeamDetailPage
        """ 
        dlg = self.open_edit_device_dialog()
        dlg.set_beam_label(beam_label)
        dlg.submit()
        self.wait_untill_success_msg_disappeared()
        self.wait_page_ready()
        return self
    
    
    def get_beam_property(self, beam_property):
        beam_properties = self._lblBeamProperties.get_all_elements()
        for index, value in enumerate(beam_properties):
            if value.text == beam_property:
                return self._lblBeamPropertiesValue.get_element_at(index).text
    
    
    def is_beam_label_displayed(self, label):
        """
        @summary: Check if a Beam's label is displayed or not
        @return: True: the Beam's label is displayed
                False: the Beam's label is not displayed
        @author: Thanh Le
        """
        beam_labels = self.get_beam_property(ApplicationConst.LBL_LABEL_PROPERTY).split(",")
        
        for lbl in beam_labels:
            lbl = lbl.replace("\ue003","").replace("\ue007","")
            if( lbl.strip() == label):
                return True
        return False
        

    def set_user_can_manage(self, user, canmanage = True):
        """
        @summary: This action is used to set user can manage Beam device   
        @author: Thanh Le
        @parameter: <user>: user object
                    <canmanage>: boolean value to decide user can manage or not
        @return: SimplifiedBeamDetailPage
        """
        self._driver.scroll_down_to_bottom()
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            if(canmanage):
                self._chkMCanManage(user.email_address).check()
            else:
                self._chkMCanManage(user.email_address).uncheck()
        else:
            if(canmanage):
                self._chkCanManage(user.email_address).check()
            else:
                self._chkCanManage(user.email_address).uncheck()
            self.wait_for_loading()

        self.wait_page_ready()
        return self
    

    def add_user(self, user, wait_for_completed=True):
        """
        @summary: This action is used to add user   
        @parameter: <user>: user object
                    <dismiss_alert>: boolean value to decide dismiss alert or not
        @return: SimplifiedBeamDetailPage
        @author: Thanh Le
        """
        if(self._driver._driverSetting.browser_name == Browser.Safari):
            self._txtInvitedEmail.type(user.email_address)
        else:
            self._txtInvitedEmail.slow_type(user.email_address)
        
        self._btnAddUser.click()
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared(60)   
            
        return self
                
    
    def create_completed_simplified_normal_user(self, user):
        """      
        @summary: Create and active a new normal user
        @param user: user would like to create and activate
        @return: Home page
        @author: Thanh Le
        """
        self.add_user(user).logout()
        return self.get_temporary_password_and_complete_create_user(user)
                
                
    def create_completed_simplified_admin_user(self, user):
        """      
        @summary: Create and active a new admin user
        @param user: user would like to create and activate
        @return: Home page
        @author: Thanh Le
        """
        self.add_user(user).set_user_can_manage(user).logout()
        return self.get_temporary_password_and_complete_create_user(user)
    
    
    def get_temporary_password_and_complete_create_user(self, user):
        """      
        @summary: Get temporary password then logging on the website and changing password
        @param user: user would like to create and activate
        @return: Home page
        @author: Thanh Le
        """       
        tmp_password = GmailUtility.get_temporary_password_for_normal_user(receiver = user.email_address, sent_day=datetime.now(), localize = True)
        from pages.suitable_tech.user.login_page import LoginPage
        return LoginPage(self._driver).open()\
                .login_as_unactivated_user(user.email_address,tmp_password)\
                .change_password(user.password, tmp_password)\
                .goto_account_settings_page_by_menu_item()\
                .set_user_language(user)\
                .logout()
        
        
    def remove_user(self, user, wait_for_completed=True):
        """
        @summary: This action is used to remove user from manage Beam device   
        @parameter: <user>: user object
                    <wait_for_completed>: boolean value to decide wait for complete or not
        @return: SimplifiedBeamDetailPage
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMRemovePerson(user.email_address).scroll_to()
            self._btnMRemovePerson(user.email_address).click_element()
        else:    
            self._btnRemovePerson(user.email_address).scroll_to()
            self._btnRemovePerson(user.email_address).click_element()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        confirm_dialog = ConfirmActionDialog(self._driver)
        if not confirm_dialog.is_dialog_displayed():
            if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
                self._btnMRemovePerson(user.email_address).jsclick()
            else:
                self._btnRemovePerson(user.email_address).jsclick()
        confirm_dialog.continue_dialog()
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared(10)
            
        return self
     
     
    def is_user_added(self, user):     
        """
        @summary: Check if a user is added or not 
        @return: True: user is added
                False: user is not added
        @author: Thanh Le
        """
        self.wait_for_loading()
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            return self._lnkMAddedUser(user.email_address).is_displayed()
        else:
            return self._lnkAddedUser(user.email_address).is_displayed()
    
    
    def is_user_not_existed(self, user):
        """
        @summary: Check if a user is not existed
        @return: True: the user is not existed
                False: the user is existed
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            return self._lnkMAddedUser(user.email_address).is_disappeared()
        else:
            return self._lnkAddedUser(user.email_address).is_disappeared()
    
    
    def is_user_can_manage_checkbox_disabled(self, user):
        """
        @summary: Check if the user can manage checkbox is disabled
        @return: True: the user can manage check-box is enabled
                False: the user can manage check-box is disabled
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            can_manage_disabled = self._chkMCanManage(user.email_address).get_attribute("disabled")
        else:
            can_manage_disabled = self._chkCanManage(user.email_address).get_attribute("disabled")

        if can_manage_disabled == "true":
            return True
        else:
            return False


    def is_user_can_manage_checkbox_selected(self, user):
        """
        @summary: Check if the user can manage checkbox is disabled
        @return: True: the user can manage check-box is enabled
                False: the user can manage check-box is disabled
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            return self._chkMCanManage(user.email_address).is_selected()
        else:
            return self._chkCanManage(user.email_address).is_selected()
        

    def is_unlink_device_button_displayed(self):
        """
        @summary: Check if the Unlink a Beam device button is displayed
        @param: True: the Unlink a Beam device is displayed
                False: the Unlink a Beam device is not displayed
        @author: Thanh Le
        @return: True if the Unlink a Beam device button is displayed. False for vice versa
        """
        dlg = self.open_edit_device_dialog()
        
        if dlg.is_dialog_displayed():
            return dlg.is_button_unlink_displayed()
        else:
            return 'There is no modal popup.'
        
        
    def goto_beam_advance_setting(self):
        """
        @summary: This action is used to go to beam advance setting page
        @return: DeviceAdvanceSettingsDialog
        @author: Thanh Le
        """
        self._btnBeamAdvance.click()
        from pages.suitable_tech.admin.dialogs.device_advance_settings_dialog import DeviceAdvanceSettingsDialog
        return DeviceAdvanceSettingsDialog(self._driver)
    
        
    def goto_simplified_user_detail_page(self, user):
        """
        @summary: This action is used to go to simplified user detail page
        @return: SimplifiedUserDetailPage
        @author: Thanh Le
        """
        self._driver.scroll_down_to_bottom()
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._lnkMAddedUser(user.email_address).wait_until_clickable().click()
        else:
            self._lnkAddedUser(user.email_address).wait_until_clickable().click()
        sleep(5)
        from pages.suitable_tech.admin.simplified.user.simplified_user_detail_page import SimplifiedUserDetailPage
        return SimplifiedUserDetailPage(self._driver)
    
    
    def get_beam_label_tag_list(self):
        """
        @summary: This action is used to get beam label tag list in Edit Device dialog
        @return: the list of Beam label
        @author: Thanh Le
        """     
        dialog = self.open_edit_device_dialog()
        label_tag_list = dialog.get_all_beam_labels()
        dialog.cancel()
        return label_tag_list
    
    
    def get_beam_location(self):
        """
        @summary: Get location of Beam device
        @return: String of Beam location
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dialog = self.open_edit_device_dialog()
        location = self._lblBeamLocation.get_attribute("value")
        dialog.cancel()
        return location


    def set_beam_label_tag_list(self, beam_label_tag_list):
        """
        @summary: This action is used to set beam label tag list in Edit Device dialog
        @parameter: beam_label_tag_list: list of labels
        @return: SimplifiedBeamDetailPage
        @author: Thanh Le
        """
        dlg = self.open_edit_device_dialog()
        dlg._wait_for_dialog_appeared()
        dlg.remove_all_beam_labels()
        for label in beam_label_tag_list:
            dlg.add_beam_label(label)
        
        dlg.submit()
        self.wait_untill_success_msg_disappeared()
        self.wait_page_ready()
        self._lblBeamStatus.wait_until_displayed()
        if not self._lblBeamStatus.is_displayed(3):
            self._driver.refresh()
            self.wait_page_ready()
        return self
    
    
    def clear_beam_location(self):
        """
        @summary: This action is used to clear beam location
        @return: SimplifiedBeamDetailPage
        @author: Thanh Le
        """
        dlg = self.open_edit_device_dialog()
        dlg.clear_beam_location()
        dlg.submit()
        dlg._wait_for_dialog_disappeared()
        return self
    
    
    def clear_all_beam_label(self):
        """
        @summary: This action is used to clear all beam label
        @return: SimplifiedBeamDetailPage
        @author: Thanh Le
        """
        self.open_edit_device_dialog().remove_all_beam_labels().submit()
        return self

