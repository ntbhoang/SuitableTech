from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase


class _EditUserGroupDlgLocator(object):
    _txtUserGroupName = (By.XPATH,"//div[@class='modal-content']//input[@ng-model='group.name']")


class EditUserGroupDialog(DialogBase):
    """
    @description: This Page Object is used for Edit User Group Dialog.
    This dialog appear when user want to edit user group
    @page: Edit User Group Dialog
    
    """
    
    
    """    Properties    """
    @property
    def _txtUserGroupName(self):
        return Element(self._driver, *_EditUserGroupDlgLocator._txtUserGroupName)
    @property
    def _btnSave(self):
        return Element(self._driver, *_EditUserGroupDlgLocator._btnSave)
    @property
    def _btnCancel(self):
        return Element(self._driver, *_EditUserGroupDlgLocator._btnCancel)
    
    
    """    Methods    """
    def __init__(self, driver):    
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """       
        DialogBase.__init__(self, driver)
    
                        
    def change_user_group_name(self, value):
        """
        @summary: This action is used to change user group name
        @param: value: new name would like to set for user group
        @return: EditUserGroupDialog
        @author: Thanh Le
        
        """
        self._txtUserGroupName.type(value)
        self.submit()
        return self
