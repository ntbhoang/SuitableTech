from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage
from common.constant import Constant
from pages.suitable_tech.user.confirm_association_page import ConfirmAssociationPage


class _GmailSignInPageLocator(object):
    _txtUserName = (By.XPATH, "//input[@name='Email' or @id='identifierId']")
    _btnNext= (By.XPATH, "//div[@id='identifierNext']")
    _txtPassword = (By.XPATH, "//div[@id='password']//input")
    _btnSignin = (By.XPATH, "//div[@id='passwordNext']")
    _chkKeepLogin = (By.XPATH, "//label[@class='remember']/descendant::input[@id='PersistentCookie']")
    _lblErrorMessage = (By.XPATH, ".//*[@id='errormsg_0_Email' and contains(.,\"Sorry, Google doesn't recognize that email.\")]")
 
    
    @staticmethod
    def _lnkAccount(value):
        return (By.XPATH, u"//p[.='{}']".format(value))

class GmailSignInPage(BasePage):
    """
    @description: This is page object class for Sign In Google page.
    @page: GmailSignInPage
    @author: Duy Nguyen
    """   
    
    
    """ Property """
    @property
    def _txtUserName(self):
        return Element(self._driver, *_GmailSignInPageLocator._txtUserName)
    @property
    def _btnNext(self):
        return Element(self._driver, *_GmailSignInPageLocator._btnNext)
    @property
    def _txtPassword(self):
        return Element(self._driver, *_GmailSignInPageLocator._txtPassword)
    @property
    def _btnSignin(self):
        return Element(self._driver, *_GmailSignInPageLocator._btnSignin)
    @property
    def _chkKeepLogin(self):
        return Element(self._driver, *_GmailSignInPageLocator._chkKeepLogin)
    @property
    def _lblErrorMessage(self):
        return Element(self._driver, *_GmailSignInPageLocator._lblErrorMessage())    
    
    
    def _lnkAccount(self, value):
        return Element(self._driver, *_GmailSignInPageLocator._lnkAccount(value))
    
    
        """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: web driver
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        BasePage.__init__(self, driver)
    
    
    def sign_in_exist_account(self, email, password=None):
        """
        @summary: This action use to submit username, password or click on existing google account.
        @param email: google account
        @param password: password
        @note: This action is used when tester want to handle authenticate both existing account and newly account
        @author: Duy Nguyen    
        @created_date: October 03, 2016
        """
        if (self._lnkAccount(email).is_displayed(5)):
            self._lnkAccount(email).wait_until_clickable().jsclick()
            self._lnkAccount(email).wait_until_disappeared()
        else:
            self.submit_sign_in_credential(email, password)
       
    
    def is_reenter_password(self, email):
        """
        @summary: This action is used as a checkpoint for specific testcase's verify point
        @param email: google account
        @return: Boolean value
        @author: Khoi Nguyen
        @created_date: October 03, 2016
        """
        self._txtUserName.type(email)
        self._btnNext.click_element()
        self._txtPassword.wait_until_displayed(5)
        return self._txtPassword.is_displayed()        
        
        
    def open(self):
        """
        @summary: use to navigate directly to Google SignIn Page
        @return: GmailSignInPage page 
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        self._driver.get(Constant.GoogleSignInURL)
        return self
    
    
    def log_in_gmail(self, email, password):
        """
        @summary: Action to work only when navigate directly to Google Sign in Page. It return object as Google Introduction Page"
        @param email: google account
        @param password: password
        @return: GmailIntroPage page object
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        self.submit_sign_in_credential(email, password)
            
        from pages.gmail_page.gmail_intro_page import GmailIntroPage
        return GmailIntroPage(self._driver)
    
    
    def sign_in_with_expecting_error_google_account(self, email):
        """
        @summary: This action is used to work when we sign-in with expected error of google account.
        @param email: google account
        @return: GmailIntroPage page object
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        self._txtUserName.type(email)
        self._btnNext.click()
        return self
    
    
    def is_google_error_message_displayed(self):
        """
        @summary: This action is used as a checkpoint for specific testcase's verify point.
        @return: True: the google error message is displayed/False: the google error message is not displayed
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        return self._lblErrorMessage.is_displayed()

    
    def sign_in_with_non_gsso_account(self, email, password):
        """
        @summary: This action is used to sign in with non gsso account
        @param email: google account
        @param password: password
        @return: Confirm Association Page
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        self.submit_sign_in_credential(email, password)
        return ConfirmAssociationPage(self._driver)
    
    
    def submit_sign_in_credential(self, email, password):
        """
        @summary: This action is used to submit sign in credential
        @param email: google account
        @param password: password
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        self.wait_page_ready(120)
        if 'oauthchooseaccount' in self._driver.current_url:
            self._driver.find_element(By.XPATH, ".//*[@id='view_container']/form//p[@data-email=\"{}\"]".format(email)).click()
        else:
            self._txtUserName.type(email)
            self._btnNext.wait_until_clickable().jsclick()
            self._txtPassword.wait_until_displayed()
            self.wait_page_ready(120)
            self._txtPassword.type(password)
            self._btnSignin.wait_until_clickable().jsclick()
            self._btnSignin.wait_until_disappeared()
            self.wait_page_ready(120)
            #Hanle for Login google issue
            if self._txtUserName.is_displayed(10):
                self._driver.back()
                self._driver.find_element(By.XPATH, ".//*[@id='view_container']/form//p[@data-email=\"{}\"]".format(email)).click()


