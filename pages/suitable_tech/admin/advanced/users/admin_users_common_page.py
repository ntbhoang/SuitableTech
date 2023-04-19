from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from common.application_constants import ApplicationConst
from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
from common.constant import Language


class _AdminUsersCommonPageLocator(object):
    _btnInviteUser = (By.XPATH, "//button[@ng-click='inviteUser()']") 
    _btnCreateUserGroup = (By.XPATH, "//button[@ng-click='createUserGroup()']")
    _iconLoading = (By.XPATH, "//div[@on='usersContentLoading'][not (contains(@class,'ng-hide'))]//div[@class='loading-indicator']//span")
    _btnTools = (By.XPATH, "//button[@class='dropdown-toggle btn btn-link']")
    _lnkExportUser = (By.XPATH, "//a[@ng-click='exportUsers()']")
    _lnkImport = (By.XPATH, "//a[@ng-click='importContacts()']")
    _lblHeader = (By.XPATH, "//div[@class='row secondary-nav']//h3")

    
    @staticmethod
    def _lblUserProfileCard(value):
        return (By.XPATH, u"//h4[.=\"{}\"]/following::div[@ng-repeat='user in users']//div[@class='profile-title ng-binding' and normalize-space(.)=\"{}\"]".format(ApplicationConst.LBL_ADMIN_USERS_SECTION_USERS, value))
  
  
class AdminUsersCommonPage(AdminTemplatePage):
    """
    @description: This is page object class that contains all controls and methods shared across all Admin Users pages.
        This class is ONLY for inheriting.
    @page: Admin Users Common page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._lblHeader)
    @property
    def _btnInviteUser(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._btnInviteUser)
    @property
    def _btnCreateUserGroup(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._btnCreateUserGroup)
    @property
    def _iconLoading(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._iconLoading)
    @property
    def _btnTools(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._btnTools)
    @property
    def _lnkExportUser(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._lnkExportUser)
    @property
    def _lnkImport(self):
        return Element(self._driver, *_AdminUsersCommonPageLocator._lnkImport)
    
    def _lblUserProfileCard(self, value):
        return Element(self._driver, *_AdminUsersCommonPageLocator._lblUserProfileCard(value))
    
    
    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method
        @param driver: Web driver
        @author: Thanh Le     
        @created_date: October 03, 2016     
        """     
        AdminTemplatePage.__init__(self, driver)
#         self._lblHeader.wait_until_displayed()
        
        
    def _wait_for_loading(self, timeout=4):
        """      
        @summary: Wait for loading
        @param timeout: time to wait for loading
        @author: Thanh Le 
        @created_date: October 03, 2016          
        """
        self._iconLoading.wait_until_displayed(timeout)
        self._iconLoading.wait_until_disappeared(timeout)
        
    
    def create_new_user_group(self, user_group_name):
        """      
        @summary: Create a new user group         
        @param user_group_name: name of user group
        @return: Admin Users Common Page
        @author: Thanh Le  
        @created_date: October 03, 2016  
        """
        self._driver.scroll_up_to_top()
        self._btnCreateUserGroup.click()
        from pages.suitable_tech.admin.dialogs.create_user_group_dialog import CreateUserGroupDialog     
        return CreateUserGroupDialog(self._driver).submit_user_group_info(user_group_name)
    
    
    def invite_new_user(self, user, wait_for_completed=True):
        """      
        @summary: Invite a new user 
        @param user: user would like to invite
        @param wait_for_completed: time to wait for inviting completedly
        @return: Admin Users Common Page
        @author: Thanh Le   
        @created_date: October 03, 2016  
        """
        self._wait_for_loading()
        self._btnInviteUser.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        InviteNewUserDialog(self._driver).submit_invite_information(user, wait_for_completed)
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
        return self
    

    def import_users(self, data_file_path, new_device_group, new_user_group):
        """      
        @summary: Import users     
        @param data_file_path: path to import file
        @param new_device_group: device group would like to add users to
        @param new_user_group: user group would like to add users to
        @return: Admin Users Common Page 
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self._driver.scroll_up_to_top()
        self._btnTools.click_element()
        self._lnkImport.click_element()
        from pages.suitable_tech.admin.dialogs.import_users_dialog import ImportUsersDialog
        ImportUsersDialog(self._driver).submit_users_from_file(data_file_path, new_device_group, new_user_group)
        return self
        
        
    def import_users_expecting_error(self, data_file_path):
        """      
        @summary: Import an invalid user file   
        @param data_file_path: path to imported file
        @return: Admin Users Common Page 
        """
        self._btnTools.click_element()
        self._lnkImport.click_element()
        from pages.suitable_tech.admin.dialogs.import_users_dialog import ImportUsersDialog
        ImportUsersDialog(self._driver).submit_users_from_invalid_file(data_file_path)
        return self
    
        
    def _set_user_language(self):
        """
        @summary: Set language for new User. This is a work around for defect BUG_35
        @return: Welcome To Beam Page    
        @author: Thanh Le
        @created_date: Sep 21, 2016
        """
        if(self._driver._driverSetting.language==Language.ENGLISH):
            return WelcomeToBeamPage(self._driver)
        else:
            welcome_to_beam_url = self._driver.current_url
            WelcomeToBeamPage(self._driver).goto_account_settings_page_by_menu_item()\
                .set_language(self._driver._driverSetting.language)\
                .save_change()
                
            self._driver.get(welcome_to_beam_url)
            return WelcomeToBeamPage(self._driver)