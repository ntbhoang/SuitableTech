from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from common.constant import Constant, Platform
from core.utilities.gmail_utility import GmailUtility
from core.webdriver.elements.dropdownlist import DropdownList
from pages.basepage import BasePage


class _UserTemplatePageLocator(object):
    _lnkHome = (By.XPATH, "//a[@href='/']")
    _lnkBeamPro = (By.XPATH, "//section[@class='top-bar-section']//a[@href='//staging.suitabletech.com/beampro/']")
    _lnkBeamPlus = (By.XPATH, "//section[@class='top-bar-section']//a[@href='//staging.suitabletech.com/beam-plus/']")
    _lnkBlog = (By.XPATH, "//section[@class='top-bar-section']//a[@href='http://blog.suitabletech.com/']")
    _lnkTestDrive = (By.XPATH, "//section[@class='top-bar-section']//a[@href='//staging.suitabletech.com/testdrive/']")
    _lnkGetBeam = (By.XPATH, "//section[@class='top-bar-section']//a[@href='//staging.suitabletech.com/getbeam/']")
    _lnkLogin = (By.XPATH, "//a[@href='//stg1.suitabletech.com/accounts/home/']")
    _ddlUserMenu = (By.XPATH, "//section//ul[@class='right']/li")
    _lnkLogout = (By.XPATH, "//a[@href='/accounts/logout/']")
    _lblNotificationMessage = (By.XPATH, "//div[@class='large-12 columns text-center']")     
    
    """popup Primary Org Contact"""
    _popupPrimaryOrgContact = (By.XPATH, "//div[@class='organization ng-scope']")
    _btnDismissOrgContact = (By.XPATH, "//div[@class='organization ng-scope']//button[contains(@ng-click,'dismiss')]")
    _btnSaveOrgContact = (By.XPATH, "//div[@class='organization ng-scope']//button[contains(@ng-click,'save')]")
    
    """Button Top Bar at Sign out page on Mobile"""
    _btnMTopBar = (By.XPATH, "//li[@class='toggle-topbar menu-icon']/a")
    
    
class UserTemplatePage(BasePage):
    """
    @description: This is page object class that contains all controls and methods shared across all User pages. 
        This class is ONLY for inheriting.
    @page: User Template Page
    @author: Thanh Le
    """
    
    """    Properties    """    
    @property
    def _popupPrimaryOrgContact(self):
        return Element(self._driver, *_UserTemplatePageLocator._popupPrimaryOrgContact)
    @property
    def _btnDismissOrgContact(self):
        return Element(self._driver, *_UserTemplatePageLocator._btnDismissOrgContact)
    @property
    def _btnSaveOrgContact(self):
        return Element(self._driver, *_UserTemplatePageLocator._btnSaveOrgContact)
    @property
    def _lnkHome(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkHome)
    @property
    def _lblNotificationMessage(self):
        return Element(self._driver, *_UserTemplatePageLocator._lblNotificationMessage)
    @property
    def _lnkBeamPro(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkBeamPro)
    @property
    def _lnkBeamPlus(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkBeamPlus)
    @property
    def _lnkBlog(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkBlog)
    @property
    def _lnkTestDrive(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkTestDrive)
    @property
    def _lnkGetBeam(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkGetBeam)
    @property
    def _lnkLogin(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkLogin)
    @property
    def _ddlUserMenu(self):
        return DropdownList(self._driver, *_UserTemplatePageLocator._ddlUserMenu)
    @property
    def _lnkLogout(self):
        return Element(self._driver, *_UserTemplatePageLocator._lnkLogout)
    @property
    def _hrefLogOut(self):
        return "/accounts/logout"
    @property
    def _hrefManageYourBeams(self):
        return "/manage/"
    @property
    def _hrefAccountSettings(self):
        return "/accounts/settings/"
    @property
    def _hrefDownloadInstaller(self):
        return "/installers"
    @property
    def _hrefDocumentation(self):
        return "/documentation/"
    @property
    def _hrefBeamHelp(self):
        return "/support/"

    """Button Top Bar at Sign out page on Mobile"""
    @property
    def _btnMTopBar(self):
        return DropdownList(self._driver, *_UserTemplatePageLocator._btnMTopBar)
    
    
    """    Methods      """
    def __init__(self, driver, wait_for_loading=True):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
                wait_for_loading: Boolean value to decide wait for loading or not
        @author: Thanh Le
        """ 
        BasePage.__init__(self, driver)
#         if(wait_for_loading):
#             self._lblChatboxHeader.wait_until_displayed()      
    
    
    def is_logged_in(self, time_out=5): 
        """
        @summary: Check if page is in login state
        @author: Thanh Le
        @parameter:<time_out>: waiting time
        @return: True if page is in login state, False for vice versa
        """
        if(self.is_login_button_displayed(time_out) and (Constant.SuitableTechURL in self._driver.current_url)):
            return False
        return True
    
    
    def get_current_user_displayed_name(self):
        """
        @summary: get current name at top right corner   
        @return: First and Lastname of logged user 
        @author: Thanh Le
        """
        if self._ddlUserMenu.is_displayed():
            return self._ddlUserMenu.get_selected_item()
        return None    
        
        
    def goto_login_page(self):
        """
        @summary: This action use to go to login page   
        @author: Thanh Le
        @return LoginPage page object
        """ 
        
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMTopBar.click()

        self._lnkLogin.wait_until_displayed(10)
        if self._lnkLogin.is_displayed():
            self._lnkLogin.click_element()
        from pages.suitable_tech.user.login_page import LoginPage
        return LoginPage(self._driver)
    
        
    def is_login_button_displayed(self, timeout=None):
        """
        @summary: Check if login button is displayed
        @author: Thanh Le
        @return True if login button is displayed. False for vice versa
        """
        return self._lnkLogin.is_displayed(timeout)
     
         
    def logout(self):
        """
        @summary: This action use to logout Suitable Tech page   
        @author: Thanh Le
        @return: SignoutCompletePage
        """
        if(self._driver._driverSetting.run_locally == False):
            self._driver.get(Constant.SuitableTechURL+self._hrefLogOut)
        else:
            # TODO: work around due bug INFR-2446
            try:
                self._driver.execute_script('$("dismissible[key=\'dashboard-advanced\'] .glyphicon.glyphicon-remove.dismiss").click();')
            except:
                pass
            self._driver.scroll_up_to_top()
            self._ddlUserMenu.select_by_href(self._hrefLogOut)
        from pages.suitable_tech.user.signout_complete_page import SignoutCompletePage
        return SignoutCompletePage(self._driver, True)
    
    
    def logout_and_login_again(self, email, password):
        """
        @summary: This action use to logout Suitable Tech page then login again with default admin user   
        @author: Thanh Le
        @parameter: email: email address
                    password: password
        @return: AdminDashboardPage if user is admin, SimplifiedDashboardPage if user isn't admin
        """ 
        return self.logout().goto_login_page().login(email, password)

    
    def logout_and_login_again_as_unwatched_video_user(self, email, password):
        """
        @summary: This action use to logout and login again with default admin user which has never watch fully introduction video  
        @author: Thanh Le
        @parameter: email: email address
                    password: password
        @return: WelcomeToBeamPage
        """ 
        return self.logout().goto_login_page().login_as_unwatched_video_user(email, password)
    
    
    def logout_and_login_again_as_new_user(self, email, password):
        """
        @summary: This action use to logout and login again with default user which has never watch fully introduction video  
        @author: Thanh Le
        @parameter: email: email address
                    password: password
        @return: WelcomeToBeamPage
        """ 
        return self.logout().goto_login_page().login_as_unwatched_video_user(email, password)
    
    
    def is_dropdownlist_item_existed(self, text):
        """
        @summary: Check if dropdownlist item is existed
        @author: Thanh Le
        @parameter: text: item string
        @return: True if dropdownlist item is existed. False for vice versa
        """
        return self._ddlUserMenu.is_item_existed(text)
    
    
    def is_dropdownlist_item_unexisted(self, text):
        """
        @summary: Check if dropdownlist item is not existed
        @author: Thanh Le
        @parameter: text: item string
        @return: True if dropdownlist item is unexisted. False for vice versa
        """
        return self._ddlUserMenu.is_item_not_existed(text)
    
    
    def goto_admin_dashboard_page_by_menu_item(self, dismiss = True):
        """
        @summary: This action use to go to admin dashboard page by menu item
        @author: Thanh Le
        @return: AdminDashboardPage page object
        """
#         Workaround for BUG_55 Account dropdown menu does not work
        self.wait_page_ready()
        if(self._driver._driverSetting.run_locally == False):
            self._driver.get(Constant.SuitableTechURL+self._hrefManageYourBeams)
        else:
            self._ddlUserMenu.wait_until_displayed()
            self._ddlUserMenu.select_by_href(self._hrefManageYourBeams)
            self._ddlUserMenu.wait_until_disappeared(5)
            if(self._ddlUserMenu.is_displayed(2)):
                self._ddlUserMenu.select_by_href(self._hrefManageYourBeams)
                self._ddlUserMenu.wait_until_disappeared(5)
            
        if dismiss:
            if self.is_primary_organization_contact_displayed(4):
                self._btnDismissOrgContact.click()
                self._popupPrimaryOrgContact.wait_until_disappeared(5)
           
        from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
        return AdminDashboardPage(self._driver)
    
    
    def dismiss_primary_organization_contact(self):
        """
        @summary: dismiss primary organization contact
        @author: Thanh Le
        @return: AdminDashboardPage page object
        """
        if self._btnDismissPrimaryOrgContact.is_displayed(3):
            self._btnDismissPrimaryOrgContact.click()
            self._btnDismissPrimaryOrgContact.wait_until_disappeared(10)
        
        
    def goto_simplified_dashboard_page_by_menu_item(self):        
        """
        @summary: This action use to go to simplified dashboard page by menu item
        @author: Thanh Le
        @return: SimplifiedDashboardPage page object
        """
        if(self._driver._driverSetting.run_locally == False):
            self._driver.get(Constant.SuitableTechURL+self._hrefManageYourBeams)
        else:
            self._ddlUserMenu.select_by_href(self._hrefManageYourBeams)
        
        from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage 
        return SimplifiedDashboardPage(self._driver)
    
    
    def goto_account_settings_page_by_menu_item(self):
        """
        @summary: This action use to go to personal account setting page by menu item
        @author: Thanh Le
        @return: SimplifiedDashboardPage page object
        """
        if(self._driver._driverSetting.run_locally == False):
            self._driver.get(Constant.SuitableTechURL+self._hrefAccountSettings)
        else:
            if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
                self._btnMTopBar.click()
                self._ddlUserMenu.select_by_href(self._hrefAccountSettings)
            else: 
                self._ddlUserMenu.select_by_href(self._hrefAccountSettings)
        from pages.suitable_tech.accountsettings.account_settings_page import AccountSettingsPage
        return AccountSettingsPage(self._driver)
    
    
    def approve_request_beam_access(self, user_email_address, admin_email_address):
        """      
        @summary: This action use to go to approve request beam access        
        @param: <user_email_address>: email address of user
                <admin_email_address>: ermail address of admin
        @return: User Template page
        @author: Thanh Le
        """
        approve_request_link = GmailUtility.get_approve_request_link(reply_to=user_email_address, receiver=admin_email_address)
        self._driver.get(approve_request_link)  
        return self
    
    
    def reject_request_beam_access(self, user_email_address, admin_email_address):
        """      
        @summary: This action use to go to reject request beam access  
        @param: <user_email_address>: email address of user
                <admin_email_address>: ermail address of admin
        @return: User Template page
        @author: Thanh Le
        """
        reject_request_link = GmailUtility.get_reject_request_link(reply_to=user_email_address, receiver=admin_email_address)
        self._driver.get(reject_request_link)
        return self
    
    
    def get_notification_message(self):
        """      
        @summary: This action use to get notification message    
        @author: Thanh Le
        @return: notification message
        """
        self._lblNotificationMessage.wait_until_displayed(5)
        notification = self._lblNotificationMessage.text
        if(notification != None):
            return notification.strip()
        else:
            return notification
        
    def is_primary_organization_contact_displayed (self, timeout=None):
        """      
        @summary: Check if the primary org contact is displayed in setting or not      
        @return: True: the primary org is displayed
                False: the primary org is not displayed
        @author: Thanh le
        """
        return  self._popupPrimaryOrgContact.is_displayed(timeout)

