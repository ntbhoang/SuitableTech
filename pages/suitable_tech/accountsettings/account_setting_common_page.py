from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element


class _AccountSettingsCommonLocator(object):
    _lnkHome = (By.XPATH, "//ul[@class='nav nav-pills account-nav nav-stacked']/li[@class='ng-scope']/a")
    _lnkSetting = (By.XPATH, "//li[@class='active']/a/span[@class='ng-scope']")
    _lnkNotification = (By.XPATH, "//a[@href='#/account/notifications/']")


class AccountSettingsCommonPage(AdminTemplatePage):
    """
    @description: This is page object class that contains all controls and methods shared across all Account Settings pages.
        This class is ONLY for inheriting.
    @page: Admin Template Page
    @author: Thanh Le
    """
    
    """    Properties    """
    @property
    def _lnkHome(self):
        return Element(self._driver, *_AccountSettingsCommonLocator._lnkHome)    
    @property
    def _lnkSetting(self):
        return Element(self._driver, *_AccountSettingsCommonLocator._lnkSetting)
    @property
    def _lnkNotification(self):
        return Element(self._driver, *_AccountSettingsCommonLocator._lnkNotification)
    
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method          
        @param driver: Web Driver 
        @author: Thanh Le
        """
        AdminTemplatePage.__init__(self, driver)
        self.wait_for_loading()
    
    
    def goto_home(self):
        """      
        @summary: Go to Admin Dashboard page by clicking Home link on Account Settings page of an advance admin      
        @return: AdminDashboardPage
        @author: Thanh le
        """
        self._lnkHome.click()
        from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
        return AdminDashboardPage(self._driver)
    
    
    def goto_simplify_normal_user_home(self):
        """      
        @summary: Go to Simplified normal user Home page by clicking Home link on Account Settings page of a simplified normal user       
        @return: SimplifiedDashboardPage
        @author: tham.nguyen
        @created_date: Aug 16 2016
        """
        self._lnkHome.click()
        from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
        return SimplifiedDashboardPage(self._driver)
    
    
    def goto_simplified_admin_home(self):
        """      
        @summary: Go to Simplified Admin Home page by clicking Home link on Account Setting of a simplified admin        
        @return: SimplifiedDashboardPage
        @author: Thanh Le
        """
        #wait msg disappeared to handle on mobile
        self.wait_untill_success_msg_disappeared()
        self._lnkHome.scroll_to().click()
        from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
        return SimplifiedDashboardPage(self._driver)
        

    def goto_notifications_tab(self):
        """      
        @summary: Click Notifications link to go to Notifications tab        
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        self._lnkNotification.click_element()
        self.wait_for_loading()
        from pages.suitable_tech.accountsettings.account_notifications_page import AccountNotificationsPage 
        return AccountNotificationsPage(self._driver)