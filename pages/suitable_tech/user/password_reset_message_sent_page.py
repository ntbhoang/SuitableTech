from core.webdriver.elements.element import Element
from pages.suitable_tech.user.user_template_page import UserTemplatePage
from selenium.webdriver.common.by import By


class _PasswordResetMessageSentPageLocator(object):
    _lblHeader = (By.XPATH, "//section[@class='masthead registration']//h2")
    
    
class PasswordResetMessageSentPage(UserTemplatePage):
    """
    @description: This is page object class for Password Reset Message Sent page. 
        This page will be opened after inputting email account and clicking submit button to reset password.
    @page: Password Reset Message Sent page
    @author: Thanh Le
    """
    
    
    """ Property """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_PasswordResetMessageSentPageLocator._lblHeader)
    
    
    """ Method """
    def __init__(self, driver): 
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        UserTemplatePage.__init__(self, driver)
        self._lblHeader.wait_until_displayed(5)
        
    
    def is_page_displayed(self):
        """
        @summary: Check if page is displayed 
        @return: True if page is displayed , False if the page is not displayed
        @author: Thanh Le
        """
        return self._lblHeader.is_displayed()
    
    