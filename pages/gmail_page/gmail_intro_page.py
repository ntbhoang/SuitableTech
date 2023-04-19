from pages.basepage import BasePage
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By


class _GmailIntroPageLocator(object):
    _lnkRemoveAccount = (By.XPATH, "//a[@href='preferences?pli=1#deleteservices']")
    _lnkAccountPreference = (By.XPATH, "//a[@href='preferences']")
    _lnkUserOptions = (By.XPATH, "//a[@role='button' and contains(@href, 'accounts.google.com')]")
    
    
class GmailIntroPage(BasePage):
    """
    @description: This is page object class for Introduce Google page.
    @page: GmailIntroPage
    @author: Duy Nguyen
    """
    
    
    """    Properties    """  
    @property
    def _lnkRemoveAccount(self):
        return Element(self._driver, *_GmailIntroPageLocator._lnkRemoveAccount)
    @property
    def _lnkAccountPreference(self):
        return Element(self._driver, *_GmailIntroPageLocator._lnkAccountPreference)
    @property
    def _lnkUserOptions(self):
        return Element(self._driver, *_GmailIntroPageLocator._lnkUserOptions)


    """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: web driver
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        BasePage.__init__(self, driver)
        self._lnkUserOptions.wait_until_displayed()
        
    
    def remove_google_account(self):
        """
        @summary: This action use to initialize delete google account function.  
        @return: GmailAccPreferencePage
        @author: Duy Nguyen  
        @created_date: October 03, 2016
        """
        self._lnkAccountPreference.click()
        from pages.gmail_page.gmail_account_preference_page import GmailAccPreferencePage
        return GmailAccPreferencePage(self._driver).go_to_delete_account_page().complete_delete_account()
    