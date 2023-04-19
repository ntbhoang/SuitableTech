from pages.basepage import BasePage
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By


class _GmailDeleteAccountPageLocator(object):
    _lblFirstAgreement = (By.XPATH, "//label[@for='i1']")
    _lblSecondAgreement = (By.XPATH,"//label[@for='i2']")
        
    @staticmethod
    def _btnDeleteAccount():
        return (By.XPATH,"//div[@class='O Ya rb pa']")
    
    
class GmailDeleteAccountPage(BasePage):
    """
    @description: This is page object class for Delete Account Google page.
    @page: Account Preference Page
    @author: Duy Nguyen
    """
    
    """    Properties    """  
    @property
    def _lblFirstAgreement(self):
        return Element(self._driver, *_GmailDeleteAccountPageLocator._lblFirstAgreement)
    @property
    def _lblSecondAgreement(self):
        return Element(self._driver, *_GmailDeleteAccountPageLocator._lblSecondAgreement)
    @property
    def _btnDeleteAccount(self):
        return Element(self._driver, *_GmailDeleteAccountPageLocator._btnDeleteAccount())
    
    
    """    Methods    """
    
    
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: web driver
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        BasePage.__init__(self, driver)


    def complete_delete_account(self):
        """
        @summary: Click on 2 confirm checkbox in order to complete deleting google account.
        @author: Duy Nguyen      
        @created_date: October 03, 2016
        """
        self._lblFirstAgreement.click()
        self._lblSecondAgreement.click()
        self._btnDeleteAccount.click()