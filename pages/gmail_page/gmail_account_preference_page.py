from pages.basepage import BasePage
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By


class _GmailAccPreferencePageLocator(object):
    _btnRegisterToDelete = (By.XPATH,"//a[contains(@href,'preferences%23deleteservices')]")
    
    @staticmethod
    def _lnkRemoveGoogleAccount():
        return (By.XPATH, "//a[@href='/deleteaccount']")    

    
class GmailAccPreferencePage(BasePage):
    """
    @description: This is page object class for Account Preference Google page.
    @page: Account Preference Page
    @author: Duy Nguyen
    """
    
    
    """    Properties    """  
    @property
    def _lnkRemoveGoogleAccount(self):
        return Element(self._driver, *_GmailAccPreferencePageLocator._lnkRemoveGoogleAccount())
    @property
    def _btnRegisterToDelete(self):
        return Element(self._driver, *_GmailAccPreferencePageLocator._btnRegisterToDelete)
    
    
    """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: web driver
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        BasePage.__init__(self, driver)


    def go_to_delete_account_page(self):
        """
        @summary: This action use to go to delete account page by clicking "Delete" button and "Remove Google Account" link
        @return: GmailDeleteAccountPage
        @author: Duy Nguyen       
        @created_date: October 03, 2016
        """
        self._lnkRemoveGoogleAccount.click()
        from pages.gmail_page.gmail_delete_account_page import GmailDeleteAccountPage
        return GmailDeleteAccountPage(self._driver)