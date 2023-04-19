from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.organization.admin_organization_common_page import OrganizationCommonPage
from common.application_constants import ApplicationConst


class _OrganizationAuthenticationPageLocator(object):
    _txtAPIKeyName = (By.XPATH, "//input[@ng-model='newApiKey.name']")
    _btnCreateAPIKey = (By.XPATH, "//form[@name='addApiKeyForm']//button[@type='submit']")
    _lnkAPIDocumentation = (By.XPATH, "//a[@href='/documentation/site-admin/web-api/']")
    _msgAlert = (By.XPATH, "//div[@class='alert alert-success ng-isolate-scope alert-dismissible']//div")

    """Mobile UI"""
    _msgMApiAlert = (By.XPATH, "//div[@class='alert alert-warning visible-xs ng-isolate-scope']")

    @staticmethod
    def _lnkAPIKeyName(value):
        return (By.XPATH, u"//tr[@ng-repeat='apiKey in apiKeys']//td[.=\"{}\"]".format(value))
    @staticmethod
    def _lnkDelteAPIKey(value):
        return (By.XPATH, u"//tr[@ng-repeat='apiKey in apiKeys']//td[.=\"{}\"]//following-sibling::td//a[.=\"{}\"]".format(value, ApplicationConst.LBL_DELETE))    
    
    
class OrganizationAuthenticationPage(OrganizationCommonPage):
    """
    @description: This is page object class for Admin Organization Authentication page.
        This page will be opened after clicking Authenticaton tab on Organization page.
        Please visit https://stg1.suitabletech.com/manage/129/#/organization/authentication/ for more details.
    @page: Admin Organization Authentication page
    @author: thanh.viet.le
    """

    """    Properties    """
    @property
    def _txtAPIKeyName(self):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._txtAPIKeyName)
    @property
    def _lnkAPIDocumentation(self):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._lnkAPIDocumentation)
    @property
    def _btnCreateAPIKey(self):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._btnCreateAPIKey)
    @property
    def _msgAlert(self):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._msgAlert)
    
    def _lnkDelteAPIKey(self, value):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._lnkDelteAPIKey(value))
    def _lnkAPIKeyName(self, value):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._lnkAPIKeyName(value))
    
    """Mobile UI"""
    @property
    def _msgMApiAlert(self):
        return Element(self._driver, *_OrganizationAuthenticationPageLocator._msgMApiAlert)


    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web driver 
        @author: Khoi Ngo       
        """      
        OrganizationCommonPage.__init__(self, driver)


    def create_api_key(self, key_name):
        """      
        @summary:  Create an APT key       
        @param key_name: name of API key would like to create
        @return: OrganizationSettingsPage
        @author: Khoi Ngo
        """
        self._txtAPIKeyName.type(key_name)
        self._btnCreateAPIKey.wait_until_clickable()
        self._btnCreateAPIKey.click_element()
        if not self._msgAlert.is_displayed(1):
            self._btnCreateAPIKey.jsclick()
        return self
    
    
    def is_api_key_existed(self, key_name, wait_time_out=None):
        """      
        @summary: Check if an API key is existed or not        
        @param
            - key_name: name of API key would like to check
            - wait_time_out: time to wait for API key displays
        @return: True: the API key is existed, False: the API key is not existed
        @author: Khoi Ngo
        """
        return self._lnkAPIKeyName(key_name).is_displayed(wait_time_out)
    
    
    def is_api_key_not_existed(self, key_name, wait_time_out=None):
        """      
        @summary: Check if an API key is not existed     
        @param 
            - key_name: name of API key would like to check
            - wait_time_out: time to wait for API key display
        @return: True: the API key is not existed, False: the API key is existed
        @author: Khoi Ngo
        """
        return self._lnkAPIKeyName(key_name).is_disappeared(wait_time_out)
    
    
    def delete_api_key(self, key_name):
        """      
        @summary: Delete an API key
        @param key_name: the API key name would like to delete 
        @return: OrganizationSettingsPage
        @author: Khoi Ngo   
        """
        #use jsclick() to handle bug on mobile
        self._lnkDelteAPIKey(key_name).jsclick()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        return self


    def get_text_msg(self):
        """      
        @summary: Get alert message    
        @return: Message of alert
        @author: Khoi Ngo
        """
        return self._msgAlert.text


    def is_create_new_api_key_btn_displayed(self):
        """
        @summary: Check if Create New API Key button is displayed
        @return: True/False
        @author: Khoi Ngo
        """
        self._lnkAPIDocumentation.scroll_to()
        return self._btnCreateAPIKey.is_displayed()


    def get_api_alert_msg(self):
        """
        @summary: Get alert API key generation not available on MOBILE site.    
        @return: message of alert
        @author: Khoi Ngo
        """
        return self._msgMApiAlert.scroll_to().text
