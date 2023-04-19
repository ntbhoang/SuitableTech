from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By
from pages.basepage import BasePage


class _OneLoginPageLocator(object):
    _txtEmail = (By.ID, "user_email")
    _txtPassword = (By.ID, "user_password")
    _btnSignIn = (By.ID, "user_submit")


class OneLoginPage(BasePage):
    """
    @description: This is page object class for OneLogin Page
    @page: One Login Page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _txtEmail(self):
        return Element(self._driver, *_OneLoginPageLocator._txtEmail)
    @property
    def _txtPassword(self):
        return Element(self._driver, *_OneLoginPageLocator._txtPassword)
    @property
    def _btnSignIn(self):
        return Element(self._driver, *_OneLoginPageLocator._btnSignIn)


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


    def login(self,email, password):
        """
        @summary: This action use to login ST page
        @parameter: <email>: email string
                    <password>: password string
        @return: OneLogin_Page
        @author: Thanh Le
        """
        return self._submit_login_form(email, password)


    def _submit_login_form(self, email, password):
        """
        @summary: This action use to perform submit login SSO form
        @parameter: <email_address>: email string
                    <password>: password string
        @author: Thanh Le
        """
        self._btnSignIn.wait_until_displayed()
        self._txtEmail.type(email)
        self._txtPassword.type(password)
        self._btnSignIn.click_element()
        self._btnSignIn.wait_until_disappeared()
        return self

