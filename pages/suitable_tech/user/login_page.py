from pages.suitable_tech.user.user_template_page import UserTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
from pages.gmail_page.gmail_sign_in_page import GmailSignInPage
from pages.suitable_tech.user.password_reset_page import PasswordResetPage
from common.constant import Constant


class _LoginPageLocator(object):
    _txtUsername = (By.ID, "id_username")
    _txtPassword = (By.ID, "id_password")
    _txtEmail = (By.ID, "id_email")
    _btnSignIn = (By.ID, "id_submit")
    _lblLoginError = (By.XPATH, "//p[@class='errornote']")
    _btnLoginGoogle = (By.XPATH, "//div[@id='googleBtn']")
    _btnLoginSSO = (By.XPATH, "//div[@id='ssoBtn']")
    _lnkForgotPassword = (By.XPATH, "//a[@id='id_forgot']")
    

class LoginPage(UserTemplatePage):
    """
    @description: This is page object class for Login page.
        Please visit https://staging.suitabletech.com/accounts/login/ for more details
    @page: Login page
    @author: Thanh Le
    """
    
    
    """    Properties    """      
    @property
    def _txtUsername(self):
        return Element(self._driver, *_LoginPageLocator._txtUsername)
    @property
    def _txtPassword(self):
        return Element(self._driver, *_LoginPageLocator._txtPassword)
    @property
    def _btnSignIn(self):
        return Element(self._driver, *_LoginPageLocator._btnSignIn)
    @property
    def _lblLoginError(self):
        return Element(self._driver, *_LoginPageLocator._lblLoginError)
    @property
    def _btnLoginGoogle(self):
        return Element(self._driver, *_LoginPageLocator._btnLoginGoogle)
    @property
    def _lnkForgotPassword(self):
        return Element(self._driver, *_LoginPageLocator._lnkForgotPassword)
    @property
    def _btnLoginSSO(self):
        return Element(self._driver, *_LoginPageLocator._btnLoginSSO)
    @property
    def _txtEmail(self):
        return Element(self._driver, *_LoginPageLocator._txtEmail)
    
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """    
        UserTemplatePage.__init__(self, driver, False)
    
        
    def open(self):
        """
        @summary: This action use to navigate ST page
        @return Login page object
        @author: Thanh Le
        """
        self._driver.get(Constant.SuitableTechLoginURL)
        self._btnSignIn.wait_until_displayed()
        return self
    
    
    def is_page_displayed(self):
        """
        @summary: Check if login page is displayed or not
        @return: True if login page is displayed , False if the login page is not displayed
        @author: Thanh Le
        """
        return self._btnSignIn.is_displayed(3)
    

    def wait_until_username_display(self):
        """
        @summary: wait until username display
        @author: Tan Le
        """       
        from time import sleep
        sleep(3)
        try:
            timeout = 1
            while(timeout <= 60):
                try:
                    username = self._driver.execute_script("return $('.dropdown-header.ng-binding').text()")
                    if username:
                        break
                    else:
                        timeout += 1
                        sleep(1)
                except:
                    pass
        except Exception as ex:
            raise ex
        
             
    def login(self, email, password, simplifiedUser=False):
        """
        @summary: This action use to login ST page
        @parameter: <email>: email string
                    <password>: password string
        @return: AdminDashboardPage if user is admin, SimplifiedDashboardPage if user isn't admin
        @author: Thanh Le
        """
        self._submit_login_form(email, password)
        self.wait_until_username_display()
        if simplifiedUser:
            return SimplifiedDashboardPage(self._driver)
        return AdminDashboardPage(self._driver)
    
    
    def login_as_sso_onelogin(self, email, password, simplifiedUser=True):
        """
        @summary: This action use to login with OneLogin account
        @parameter: <email>: email string
                    <password>: password string
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        self.login_sso(email)
        from pages.suitable_tech.user.onelogin_page import OneLoginPage
        OneLoginPage(self._driver).login(email, password)
        self.wait_until_username_display()
        if simplifiedUser:
            return SimplifiedDashboardPage(self._driver)
        return AdminDashboardPage(self._driver)

    
    def login_as_sso_okta(self, email, password):
        """
        @summary: This action use to login with Okta account
        @parameter: <email>: email string
                    <password>: password string
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        self.login_sso(email)
        from pages.okta_page.okta_sign_in_page import OktaSignInPage
        OktaSignInPage(self._driver).login(email, password)
        return AdminDashboardPage(self._driver)
    
    
    def login_sso(self, email):
        """
        @summary: This action use to perform submit login SSO form
        @parameter: <email_address>: email string
        @author: Thanh Le
        """
        self._btnLoginSSO.click()
        self._txtEmail.wait_until_displayed()
        self._txtEmail.type(email) 
        self._btnSignIn.click_element()
        return self
    
    
    def login_as_unwatched_video_user(self, email_address, password=None):
        """
        @summary: This action use to login ST page with account which have never watch video
        @parameter: <email_address>: email string
                    <password>: password string
        @return: WelcomeToBeamPage
        @author: Thanh Le
        """
        if password is None:
            password = Constant.DefaultPassword
        self._submit_login_form(email_address, password)
        from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
        return WelcomeToBeamPage(self._driver)
    
    
    def login_as_unactivated_user(self, email_address, password=None):
        """
        @summary: This action use to login ST page with account which have never activities
        @param email_address: email string
        @param password: password string
        @return: PasswordChangePage
        @author: Thanh Le
        @created: January 09, 2017
        """
        if password is None:
            password = Constant.DefaultPassword
        self._submit_login_form(email_address, password)
        from pages.suitable_tech.user.password_change_page import PasswordChangePage
        return PasswordChangePage(self._driver)
    
    
    def login_as_advanced_admin_and_invite_new_user(self, user, email_address, password, is_admin_watched_video=True):
        """      
        @summary: Log into Suitabletech and invite a new normal user (Not including activation step)        
        @parameter: user: User object that contains user information
                    email_address: Email address of admin user that used to login
                    password: Password of admin user that used to login
        @return: AdminDashboardPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        dashboard_page = None
        if is_admin_watched_video:
            dashboard_page = self.login(email_address, password, )\
                .goto_admin_dashboard_page()
        else:
            dashboard_page = self.login_as_unwatched_video_user(email_address, password)\
                .goto_admin_dashboard_page_by_menu_item()
                
        return dashboard_page.invite_new_user(user)


    def login_expecting_error(self, email, password):
        """
        @summary: This action use to work with expected failure login case
        @parameter: <email_address>: email string
                    <password>: password string
        @return: Login page itself
        @author: Thanh Le
        """
        self._submit_login_form(email, password)
        return self
    
        
    def _submit_login_form(self, email, password):
        """
        @summary: This action use to perform submit login form
        @parameter: <email_address>: email string
                    <password>: password string
        @author: Thanh Le
        """
        self._btnSignIn.wait_until_displayed(10)
        self._txtUsername.type(email)
        self._txtPassword.type(password)     
        self._btnSignIn.jsclick()
        self._btnSignIn.wait_until_disappeared()

        
    def get_login_error_message(self): 
        """
        @summary: This action use to get login error message
        @return: login error message
        @author: Thanh Le
        """
        return self._lblLoginError.text
    
    
    def log_in_with_exist_google_account(self, email):
        """
        @summary: This action use to login ST page by GSSO authentication with remember google account
        @parameter: <email>: google email string
        @return: WelcomeToBeamPage page object
        @author: Thanh Le
        """
        self._btnLoginGoogle.click()
        gmail = GmailSignInPage(self._driver)
        gmail.sign_in_exist_account(email)
        from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
        return WelcomeToBeamPage(self._driver)
    
    
    def goto_google_signin_page(self):
        """
        @summary: This action use to click on "sign in with google button"
        @return: GmailSignInPage
        @author: Thanh Le
        """
        self._btnLoginGoogle.wait_until_displayed(10)
        if self._btnLoginGoogle.is_displayed():
            self._btnLoginGoogle.wait_until_clickable().click_element()
            self._btnLoginGoogle.wait_until_disappeared(5)
        return GmailSignInPage(self._driver)
    

    def login_with_google(self, email, password=Constant.DefaultPassword):
        """
        @summary: This action use to login ST page by GSSO authentication with account have already watch video
        @parameter: <email>: google email string
                    <password>: password string
        @return: SimplifiedDashboardPage page object
        @author: Thanh Le
        """
        self._btnLoginGoogle.click()
        gmail = GmailSignInPage(self._driver)
        gmail.sign_in_exist_account(email, password)
        return SimplifiedDashboardPage(self._driver)
    
    
    def login_as_unwatched_google_user(self, email=None, password=Constant.DefaultPassword):
        """
        @summary: This action use to login ST page by GSSO authentication with account has't watched video
        @parameter: <email>: google email string
                    <password>: password string
        @return: WelcomeToBeamPage page object
        @author: Thanh Le
        """
        self._btnLoginGoogle.wait_until_clickable().click()
        gmail = GmailSignInPage(self._driver)
        gmail.sign_in_exist_account(email, password)
        from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
        return WelcomeToBeamPage(self._driver)
        
        
    def goto_forgot_password_page(self):
        """
        @summary: This action use to go to forgot password page
        @return: PasswordResetPage page object
        @author: Thanh Le
        """
        self._lnkForgotPassword.click_element()
        self._lnkForgotPassword.wait_until_disappeared()
        return PasswordResetPage(self._driver)
    
    
    def login_with_google_as_new_auth(self, email, password=None, logged_in_before=False):
        """
        @summary: This action use to work with google account which haven't got GSSO authentication
        @parameter: <email>: google email string
                    <password>: password string
                    <logged_in_before>: boolean value to know if this account used to have GSSO authentication
        @return: ConfirmAssociationPage page object
        @author: Thanh Le
        """
        if password is None:
            password = Constant.DefaultPassword
        self._btnLoginGoogle.wait_until_clickable().click_element()
        self._btnLoginGoogle.wait_until_disappeared()
        if(self._btnLoginGoogle.is_displayed(1)):
            self._btnLoginGoogle.wait_until_clickable().click_element()
            self._btnLoginGoogle.wait_until_disappeared()
        gmail = GmailSignInPage(self._driver)
        if logged_in_before:
            gmail.sign_in_exist_account(email, password)
        else:
            gmail.submit_sign_in_credential(email, password)
        from pages.suitable_tech.user.confirm_association_page import ConfirmAssociationPage
        return ConfirmAssociationPage(self._driver)
    
    
    def login_with_google_account_expecting_error(self, email):
        """
        @summary: This action use to work with expected failure google login
        @return: GmailSignInPage
        @author: Duy Nguyen
        """
        self._btnLoginGoogle.click()
        gmail = GmailSignInPage(self._driver)
        return gmail.sign_in_with_expecting_error_google_account(email)
    
    
    def goto_confirm_association_page(self, email, password=None):
        """
        @summary: This action use to go to allow access page of Google when a brand new google account login with GSSO authentication
        @parameter: <email>: google email string
                    <password>: password string
        @return: AllowAssociationPage
        @author: Duy Nguyen
        """
        if password is None:
            password = Constant.DefaultPassword        
        self._btnLoginGoogle.click_element()
        gmail = GmailSignInPage(self._driver)
        gmail.submit_sign_in_credential(email, password)
        from pages.suitable_tech.user.confirm_association_page import ConfirmAssociationPage
        return ConfirmAssociationPage(self._driver)
    
    
    def login_to_force_restore_gsso_authentication_account(self, email, password=None):
        """
        @summary: This action use to login by GSSO authentication to restore gsso authentication
        @parameter: <email>: google email string
                    <password>: password string
        @return: Welcome Page
        @author: Duy Nguyen
        """
        if password is None:
            password = Constant.DefaultPassword        
        self._btnLoginGoogle.click()
        gmail = GmailSignInPage(self._driver)
        gmail.sign_in_exist_account(email, password)
        try:
            from pages.suitable_tech.user.confirm_association_page import ConfirmAssociationPage
            ConfirmAssociationPage(self._driver).is_page_displayed()
        finally:
            from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
            return WelcomeToBeamPage(self._driver)
        
    