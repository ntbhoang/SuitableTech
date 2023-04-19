from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.constant import Constant

class _OktaSignInPageLocator(object):
    _txtUsername = (By.ID, "okta-signin-username")
    _txtPassword = (By.ID, "okta-signin-password")
    _btnSignIn = (By.ID, "okta-signin-submit")

class OktaSignInPage(BasePage):
    """
    @description: This is page object class for OneLogin Page
    @page: One Login Page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _txtUsername(self):
        return Element(self._driver, *_OktaSignInPageLocator._txtUsername)
    @property
    def _txtPassword(self):
        return Element(self._driver, *_OktaSignInPageLocator._txtPassword)
    @property
    def _btnSignIn(self):
        return Element(self._driver, *_OktaSignInPageLocator._btnSignIn)


    """    Methods    """
    def __init__(self, driver, wait_for_loading=False):
        """
        @summary: Constructor method
        @parameter: driver: Web Driver
                    wait_for_loading: boolean value to decide wait for loading or not
        @author: Thanh Le
        """
        BasePage.__init__(self, driver)
        if(wait_for_loading):
            self._btnSignIn.wait_until_displayed()

    def open(self):
        """
        @summary: navigate directly to Okta Account URL
        @return: Okta page
        @author: Thanh Le
        @created_date: June 07, 2017
        """
        self._driver.get(Constant.OktaAccountURL)
        return self
    

    def login(self,email, password):
        """
        @summary: This action use to login ST page
        @parameter: <email>: email string
                    <password>: password string
        @return: OneLogin_Page
        @author: Thanh Le
        """
        return self._submit_login_form(email, password)
    
    
    def signin_to_homepage(self,email, password):
        """
        @summary: This action use to login ST page
        @parameter: <email>: email string
                    <password>: password string
        @return: Okta homepage
        @author: Thanh Le
        """
        self._submit_login_form(email, password)
        from pages.okta_page.okta_home_page import OktaHomePage
        return OktaHomePage(self._driver)


    def _submit_login_form(self, email, password):
        """
        @summary: This action use to perform submit login SSO form
        @parameter: <email_address>: email string
                    <password>: password string
        @author: Thanh Le
        """
        self._btnSignIn.wait_until_displayed()
        self._txtUsername.type(email)
        self._txtPassword.type(password)
        self._btnSignIn.click_element()
        self._btnSignIn.wait_until_disappeared()
        return self
