from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage

class _GmailSignUpSuccessfullyPageLocator(object):
    _lblSuccessfulMessage = (By.XPATH, "//div[@class= 'welcome' and contains(.,'Your new email address is')]")
    

class GmailSignUpSuccessfullyPage(BasePage):
    """
    @description: This page object displays after a gmail account is created successfully
    @page: Gmail Sign Up Successfully Page
    @author: Thanh Le
    @created_date: December 01, 2016
    """
    
    """    Properties    """
    @property
    def _lblSuccessfulMessage(self):
        return Element(self._driver, *_GmailSignUpSuccessfullyPageLocator._lblSuccessfulMessage)
    
    
    """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: WebDriver
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        BasePage.__init__(self, driver)
        self._lblSuccessfulMessage.wait_until_displayed()
    
    
    def is_successful_message_displayed(self):
        """
        @summary: Check successful message displays or not
        @return: True if gmail is created successfully 
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        return self._lblSuccessfulMessage.is_displayed()

