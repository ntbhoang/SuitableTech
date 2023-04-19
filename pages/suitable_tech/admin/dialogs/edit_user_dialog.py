from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase



class _EditUserDlgLocator(object):
    _chkAllowUserAsAdminOrg = (By.XPATH,"//input[@type='checkbox' and @ng-model='user.is_admin']")
    _iconLoading = (By.CSS_SELECTOR, '.fa.fa-lg.fa-spin.fa-circle-o-notch.loader.ng-scope')
    _txtUserGroups = (By.CSS_SELECTOR,"tags-input[ng-model='userGroups'] input")
    _txtDeviceGroups = (By.CSS_SELECTOR,"tags-input[ng-model='deviceGroups'] input")
    _itmSuggestion = (By.CSS_SELECTOR, "li[ng-click='addSuggestionByIndex($index)']")
    _txtFirstName = (By.CSS_SELECTOR, "input[ng-model='user.first_name']")
    _txtLastName = (By.CSS_SELECTOR, "input[ng-model='user.last_name']")

    @staticmethod
    def _icnRemoveGroup(group_name):
        return (By.XPATH, u"//span[text()=\"{}\"]/../a[@ng-click='$removeTag()']".format(group_name))

class EditUserDialog(DialogBase):
    """
    @description: This page object is used for Edit User Dialog.
    This dialog appear when user want to edit user
    @page: Edit User Dialog.
    
    """
    
    """    Properties    """
    @property
    def _iconLoading(self):
        return Element(self._driver, *_EditUserDlgLocator._iconLoading)
    @property
    def _chkAllowUserAsAdminOrg(self):
        return Element(self._driver, *_EditUserDlgLocator._chkAllowUserAsAdminOrg)
    @property
    def _txtUserGroups(self):
        return Element(self._driver, *_EditUserDlgLocator._txtUserGroups)
    @property
    def _txtDeviceGroups(self):
        return Element(self._driver, *_EditUserDlgLocator._txtDeviceGroups)
    @property
    def _itmSuggestion(self):
        return Element(self._driver, *_EditUserDlgLocator._itmSuggestion)
    @property
    def _txtLastName(self):
        return Element(self._driver, *_EditUserDlgLocator._txtLastName)
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_EditUserDlgLocator._txtFirstName)
    
    def _icnRemoveGroup(self, group_name):
        return Element(self._driver, *_EditUserDlgLocator._icnRemoveGroup(group_name))

    """    Methods    """
    def __init__(self, driver):      
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """   
        DialogBase.__init__(self, driver)


    def is_allow_user_to_administrater_org_enabled(self):
        """
        @summary: Check if allow user administer checkbox is enabled
        @return: True: the Allow user as Administrator of org is enabled
                False: the Allow user as  Administrator of org is disabled
        @author: Thanh Le
        """
        return self._chkAllowUserAsAdminOrg.is_enabled()


    def edit_user(self, verified_domain_user = False, first_name = None, last_name = None, add_user_groups=[], add_device_groups=[], remove_user_groups=[], remove_device_groups=[], allow_administer=False, cancel=False):
        """
        @summary: Edit user on edit user dialog
        @param: user_groups: add user to these user groups
        @param device_groups: add user to these device groups
        @param allow_administer: allow user to administer or not
        @param cancel: cancel changes or not
        @author: Khoi Ngo
        @created_date: October 10, 2017
        """
        self._iconLoading.wait_until_disappeared(10)
        if verified_domain_user:
            self._txtFirstName.clear()
            self._txtFirstName.send_keys(first_name)
            self._txtLastName.clear()
            self._txtLastName.send_keys(last_name)

        for add_user_group in add_user_groups:
            self._txtUserGroups.send_keys(add_user_group)
            self._itmSuggestion.click()

        for add_device_group in add_device_groups:
            self._txtDeviceGroups.send_keys(add_device_group)
            self._itmSuggestion.click()

        for remove_user_group in remove_user_groups:
            self._icnRemoveGroup(remove_user_group).click()

        for remove_device_group in remove_device_groups:
            self._icnRemoveGroup(remove_device_group).click()

        if allow_administer:
            self._chkAllowUserAsAdminOrg.check()
        else:
            self._chkAllowUserAsAdminOrg.uncheck()

        if cancel:
            self._btnCancel.click()
        else:
            self.submit()
        return self


    def is_firstname_lastname_field_display(self):
        """
        @summary: Check if last name and first name field display or not
        @author: Khoi Ngo
        @created_date: Nov 16, 2017
        """
        return (self._txtFirstName.is_displayed(2) and self._txtLastName.is_displayed(2))

