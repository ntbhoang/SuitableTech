from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase


class _CreateUserGroupDlgLocator(object):
    _txtUserGroupName = (By.XPATH, "//div[@class='modal-content']//input[@name='name']")
    
    
class CreateUserGroupDialog(DialogBase):
    """
    @description: This is page object class for Create User Group Dialog. You need to init it before using in page class.
    @page: Create User Group Dialog
    @author: Thanh Le
    """    
    
    
    """    Properties    """
    @property
    def _txtUserGroupName(self):
        return Element(self._driver, *_CreateUserGroupDlgLocator._txtUserGroupName)


    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method 
        @param driver: web driver
        @author: Thanh Le         
        """
        DialogBase.__init__(self, driver)
    
       
    def submit_user_group_info(self, user_group_name):
        """      
        @summary: Submit information on Create User Group form         
        @param user_group_name: name of user group would like to create
        @return: AdminUserGroupDetailPage
        @author: Thanh Le
        """
        self._txtUserGroupName.type(user_group_name)
        self.submit()
        from pages.suitable_tech.admin.advanced.users.admin_user_group_detail_page import AdminUserGroupDetailPage
        return AdminUserGroupDetailPage(self._driver)