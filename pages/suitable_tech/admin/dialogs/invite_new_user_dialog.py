from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from core.webdriver.elements.editable_combobox import EditableCombobox


class _InviteNewUserLocator():
    _txtInviteUserEmail = (By.XPATH, "//div[@class='modal-content']//input[@name='email']")
    _txtInviteUserFirstName = (By.XPATH, "//div[@class='modal-content']//input[@name='first_name']")
    _txtInviteUserLastName = (By.XPATH, "//div[@class='modal-content']//input[@name='last_name']")
    _lblInviteSuccessMessage = (By.XPATH, "//div[@class='alert alert-success']//span[@ng-bind-html='message.content']")
    _dlgInviteUser = (By.XPATH, "//div[@class='modal-content']")
    _chkIncludeALinkToBeamSoftware = (By.XPATH, "//div[@class='modal-content']//input[@ng-model='invitation.show_installer_link' and @type='checkbox']")
    _chkEmailACopyToMyseft = (By.XPATH, "//div[@class='modal-content']//input[@ng-model='invitation.ccme' and @type='checkbox']")
    _chkIncludeTheDefaultInvitationMessage = (By.XPATH, "//div[@class='modal-content']//input[@ng-model='invitation.use_default_invite_message' and @type='checkbox']")
    _ecbxDeviceGroups = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='invitation.device_groups']")
    _ecbxUserGroups = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='invitation.user_groups']")
    

class InviteNewUserDialog(DialogBase):
    """
    @description: This is page object class for Invite New User Dialog. You need to init it before using in page class.
    @page: Invite New User Dialog
    @author: Thanh Le
    """


    """    Properties    """    
    @property
    def _txtInviteUserEmail(self):
        return Element(self._driver, *_InviteNewUserLocator._txtInviteUserEmail)
    @property
    def _txtInviteUserFirstName(self):
        return Element(self._driver, *_InviteNewUserLocator._txtInviteUserFirstName)
    @property
    def _txtInviteUserLastName(self):
        return Element(self._driver, *_InviteNewUserLocator._txtInviteUserLastName)
    @property
    def _lblInviteSuccessMessage(self):
        return Element(self._driver, *_InviteNewUserLocator._lblInviteSuccessMessage)
    @property
    def _dlgInviteUser(self):
        return Element(self._driver, *_InviteNewUserLocator._dlgInviteUser)
    @property
    def _chkIncludeALinkToBeamSoftware(self):
        return Element(self._driver, *_InviteNewUserLocator._chkIncludeALinkToBeamSoftware)
    @property
    def _chkEmailACopyToMyseft(self):
        return Element(self._driver, *_InviteNewUserLocator._chkEmailACopyToMyseft)
    @property
    def _chkIncludeTheDefaultInvitationMessage(self):
        return Element(self._driver, *_InviteNewUserLocator._chkIncludeTheDefaultInvitationMessage)
    @property
    def _ecbxDeviceGroups(self):
        return EditableCombobox(self._driver, *_InviteNewUserLocator._ecbxDeviceGroups)
    @property
    def _ecbxUserGroups(self):
        return EditableCombobox(self._driver, *_InviteNewUserLocator._ecbxUserGroups)
    
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """   
        DialogBase.__init__(self, driver)
        
    
    def submit_invite_information(self, user, wait_for_completed=True):  
        """
        @summary: This action is used to submit invite user information
        @author: Thanh Le
        @parameter: user: user object
                    wait_for_completed: boolean value to decide waiting or not
        """      
        self.enter_invite_information(user)
        self.submit(wait_for_completed)  
    
    
    def submit_invite_information_for_simple_form(self, user):   
        """
        @summary: This action is used to submit invite user simple information
        @author: Thanh Le
        @parameter: user: user object
        """    
        self.enter_invite_information_for_simple_form(user);
        self.submit() 
    
        
    def enter_invite_information(self, user):
        """
        @summary: This action is used to enter invite user information
        @author: Thanh Le
        @parameter: user: user object
        @return: InviteNewUserDialog
        """    
        self.enter_invite_information_for_simple_form(user)
        if(user.device_group != None):
            self._ecbxDeviceGroups.select(user.device_group, self._ecbxDeviceGroups._value)
        if(user.user_group != None):
            self._ecbxUserGroups.select(user.user_group, self._ecbxUserGroups._value)
        
        # handle test run more stable on IE browser
        from time import sleep
        sleep(1)
        return self
     
    
    def enter_invite_information_for_simple_form(self, user):
        """
        @summary: This action is used to enter invite user simple information
        @author: Thanh Le
        @parameter: user: user object
        @return: InviteNewUserDialog
        """    
        if(user.email_address != None):
            self._txtInviteUserEmail.type(user.email_address)        
        """checkbox include a link to beam software"""
        if user.invitation_settings.include_a_link_to_the_beam_software:
            self._chkIncludeALinkToBeamSoftware.check()
        else:
            self._chkIncludeALinkToBeamSoftware.uncheck()
        """checkbox include the default invitation message"""
        if user.invitation_settings.include_the_default_invitation_message is not None:
            if user.invitation_settings.include_the_default_invitation_message:
                self._chkIncludeTheDefaultInvitationMessage.check()
            else:
                self._chkIncludeTheDefaultInvitationMessage.uncheck()
        """checkbox email a copy to myself"""
        if user.invitation_settings.email_a_copy_to_myself:
            self._chkEmailACopyToMyseft.check()
        else:
            self._chkEmailACopyToMyseft.uncheck()
        return self    
    
    
    def is_invite_user_button_disabled(self):
        """
        @summary: Check if invite user button disabled
        @author: Thanh Le
        @return: True if invite user button disabled, False for vice versa
        """    
        return (self._btnSubmitChanges.get_attribute("disabled") == "disabled")
    
    
    def get_invite_user_success_message(self):
        """
        @summary: This action is used to get invite user success message
        @author: Thanh Le
        @return: success message text
        """    
        return self._lblInviteSuccessMessage.text
    
        
    def is_invite_user_dialog_displayed(self):
        """
        @summary: Check if invite user dialog display
        @author: Thanh Le
        @return: True if invite user dialog display, False for vice versa
        """    
        if(self._dlgInviteUser.is_disappeared()):
            return False
        else:
            return True