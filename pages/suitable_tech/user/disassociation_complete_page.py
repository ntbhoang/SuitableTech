from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.user.password_reset_page import PasswordResetPage
from pages.basepage import BasePage
from pages.suitable_tech.user.user_template_page import UserTemplatePage


class _DisassociationCompletedPageLocator(object):
    _lnkResetPassword = (By.XPATH, "//a[@href='/accounts/password_reset/']")
    _lnkLogin = (By.XPATH, "//a[@href='/accounts/login/']")
    _lblHeader = (By.XPATH, "//section[@class='masthead registration']//h2")

        
class DisassociationCompletedPage(UserTemplatePage):
    """
    @description: This is page object class for Disassociate Complete page.
    This page appear after user get out of GSSO Authentication
    @page: Confirm Association Page 
    @author: Thanh Le
    """
    
    
    """    Properties    """      
    @property
    def _lblSusscessfulLogout(self):
        return Element(self._driver, *_DisassociationCompletedPageLocator._lblSusscessfulLogout)
    @property
    def _lnkResetPassword(self):
        return Element(self._driver, *_DisassociationCompletedPageLocator._lnkResetPassword)
    @property
    def _lnkLogin(self):
        return Element(self._driver, *_DisassociationCompletedPageLocator._lnkLogin)
    @property
    def _lblHeader(self):
        return Element(self._driver, *_DisassociationCompletedPageLocator._lblHeader)
    
    
        """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """   
        BasePage.__init__(self, driver)
    
    
    def is_page_displayed(self):
        """
        @summary: Check if page is displayed
        @return: True if page is displayed. False for page is not displayed
        @author: Duy Nguyen
        """
        return (self._lblHeader.is_displayed() and self._lnkResetPassword.is_displayed() and self._lnkLogin.is_displayed())
        
        
    def reset_password(self, user):
        """
        @summary: This action is used to reset password for a user
        @parameter: <user>: user would like to reset password
        @return: PasswordResetPage
        @author: Duy Nguyen
        """
        self._lnkResetPassword.click_element()
        return PasswordResetPage(self._driver).reset_user_password(user.email_address, user.password)

