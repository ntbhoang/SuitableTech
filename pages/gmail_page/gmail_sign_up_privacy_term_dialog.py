from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.gmail_page.gmail_sign_up_successfully_page import GmailSignUpSuccessfullyPage
from pages.basepage import BasePage


class _GmailPrivacyAndTermDialogLocator(object):
    _btnDown = (By.XPATH, "//div[@id='tos-scroll-button']")
    _btnAgree = (By.XPATH, "//input[@id='iagreebutton']")
    _btnCancel = (By.XPATH, "//input[@id='cancelbutton']")


class GmailPrivacyAndTermDialog(BasePage):
    """
    @description: This page object is used for accept Gmail privacy And term when signing up 
    @page: Gmail Privacy And Term Dialog
    @author: Thanh Le
    @created_date: December 01, 2016  
    """
    
    
    """    Properties    """
    @property
    def _btnDown(self):
        return Element(self._driver, *_GmailPrivacyAndTermDialogLocator._btnDown)
    @property
    def _btnAgree(self):
        return Element(self._driver, *_GmailPrivacyAndTermDialogLocator._btnAgree)
    @property
    def _btnCancel(self):
        return Element(self._driver, *_GmailPrivacyAndTermDialogLocator._btnCancel)
    
    
    """    Methods    """
    def __init__(self, driver):      
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        @created_date: December 01, 2016  
        """   
        BasePage.__init__(self, driver)        
    
    
    def agree_gmail_privacy_term(self):
        """
        @summary: method to agree Gmail privacy and term
        @return: Gmail Sign Up Successfully Page
        @author: Thanh Le
        @created_date: December 01, 2016  
        """
        while (not self._btnAgree.is_displayed(3)):
            self._btnDown.click()
        self._btnAgree.click()
        return GmailSignUpSuccessfullyPage(self._driver)

