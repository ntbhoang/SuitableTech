from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage
from common.constant import Constant
from pages.gmail_page.gmail_sign_up_privacy_term_dialog import GmailPrivacyAndTermDialog

class _GmailSignUpPageLocator(object):
    _txtFirstName = (By.XPATH, "//input[@id='FirstName']")
    _txtLastName = (By.XPATH, "//input[@id='LastName']")
    _txtGmailAddress = (By.XPATH, "//input[@id='GmailAddress']")
    _txtPassword = (By.XPATH, "//input[@id='Passwd']")
    _txtConfirmPassword = (By.XPATH, "//input[@id='PasswdAgain']")
    _ddlBirthMonth = (By.XPATH, "//span[@id='BirthMonth']")
    _txtBirthDay = (By.XPATH, "//input[@id='BirthDay']")
    _txtBirthYear = (By.XPATH, "//input[@id='BirthYear']")
    _ddlGender = (By.XPATH, "//div[@id='Gender']")
    _txtRecoveryPhoneNumber = (By.XPATH, "//input[@id='RecoveryPhoneNumber']")
    _txtRecoveryEmailAddress = (By.XPATH, "//input[@id='RecoveryEmailAddress']")
    _ddlLocation = (By.XPATH, "//div[@id='CountryCode']")
    _btnSubmit = (By.XPATH, "//input[@id='submitbutton']")
    
    @staticmethod
    def _ddlSelectedValue(value):
        return (By.XPATH, u"//div[@class='goog-menuitem-content' and contains(.,\"{}\")]".format(value))
    

class GmailSignUpPage(BasePage):
    """
    @description: This is page object class for Sign Up Google page.
    @page: Gmail Sign Up Page
    @author: Thanh Le
    @created_date: December 01, 2016
    """   
    
    """ Property """
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtFirstName)
    @property
    def _txtLastName(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtLastName)
    @property
    def _txtGmailAddress(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtGmailAddress)
    @property
    def _txtPassword(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtPassword)
    @property
    def _txtConfirmPassword(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtConfirmPassword)
    @property
    def _ddlBirthMonth(self):
        return Element(self._driver, *_GmailSignUpPageLocator._ddlBirthMonth)    
    @property
    def _txtBirthDay(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtBirthDay)    
    @property
    def _txtBirthYear(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtBirthYear)
    @property
    def _ddlGender(self):
        return Element(self._driver, *_GmailSignUpPageLocator._ddlGender)
    @property
    def _txtRecoveryPhoneNumber(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtRecoveryPhoneNumber)
    @property
    def _txtRecoveryEmailAddress(self):
        return Element(self._driver, *_GmailSignUpPageLocator._txtRecoveryEmailAddress) 
    @property
    def _ddlLocation(self):
        return Element(self._driver, *_GmailSignUpPageLocator._ddlLocation) 
    @property
    def _btnSubmit(self):
        return Element(self._driver, *_GmailSignUpPageLocator._btnSubmit)
       
    def _ddlSelectedValue(self, value):
        return Element(self._driver, *_GmailSignUpPageLocator._ddlSelectedValue(value))
    
    
    """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: WebDriver
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        BasePage.__init__(self, driver)
        self._txtFirstName.wait_until_displayed()
        
        
    def sign_up_gmail(self, google_account):
        """
        @summary: sign up gmail  
        @param gmail_address: gmail address to create
        @return: Gmail Privacy And Term Dialog
        @author: Thanh Le
        @created_date: December 01, 2016
        """ 
        self._txtFirstName.type(google_account.firstName)
        self._txtLastName.type(google_account.lastName) 
        self._txtGmailAddress.type(google_account.emailAddress)
        self._txtPassword.type(google_account.password)
        self._txtConfirmPassword.type(google_account.confirmPassword)
        self._selectBirthMonth(google_account.birthMonth)
        self._txtBirthDay.type(google_account.birthDay)
        self._txtBirthYear.type(google_account.birthYear)
        self._selectGender(google_account.gender)
        self._btnSubmit.scroll_to().click()
        return GmailPrivacyAndTermDialog(self._driver)
    
    
    def open(self):
        """
        @summary: navigate directly to Google SignUp Page
        @return: Gmail Sign UP Page 
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        self._driver.get(Constant.GoogleSignUpURL)
        return self
    
    
    def _selectBirthMonth(self, month):
        """
        @summary: select Birth Month 
        @param month: January, February,..., December
        @return: Gmail Sign UP Page 
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        self._ddlBirthMonth.click()
        self._ddlSelectedValue(month).click()
        return self
    
    
    def _selectGender(self, gender):
        """
        @summary: method to select Gender
        @param gender: Female/Male
        @return: Gmail Sign UP Page 
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        self._ddlGender.click()
        self._ddlSelectedValue(gender).click()
        return self

