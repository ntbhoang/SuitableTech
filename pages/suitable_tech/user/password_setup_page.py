from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.user.user_template_page import UserTemplatePage
from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
from common.constant import Constant


class _PasswordSetupPageLocator(object):
    _txtNewPassword = (By.XPATH, "//input[@id='id_new_password1']")
    _txtConfirmPassword = (By.XPATH, "//input[@id='id_new_password2']")
    _btnSetPassword = (By.XPATH, "//input[@class='button primary' and @type='submit']")
    _lblErrorMessage = (By.XPATH, "//ul[@class='errorlist']")    
    _lblErrorNote = (By.XPATH, "//p[@class='errornote']")
    

class PasswordSetupPage(UserTemplatePage):
    """
    @description: This is page object class for Password Setup page. 
        This page will be opened after clicking on Activation link in Welcome email.
        Please visit PasswordSetupPage for more details.
    @page: Password Setup page
    @author: Thanh Le
    """

    """    Properties    """   
    @property
    def _txtNewPassword(self):
        return Element(self._driver, *_PasswordSetupPageLocator._txtNewPassword)
    @property
    def _txtConfirmPassword(self):
        return Element(self._driver, *_PasswordSetupPageLocator._txtConfirmPassword)
    @property
    def _btnSetPassword(self):
        return Element(self._driver, *_PasswordSetupPageLocator._btnSetPassword)
    @property
    def _lblErrorMessage(self):
        return Element(self._driver, *_PasswordSetupPageLocator._lblErrorMessage)    
    @property
    def _lblErrorNote(self):
        return Element(self._driver, *_PasswordSetupPageLocator._lblErrorNote)
    
    
    """    Methods    """
    def __init__(self, driver, activation_link=None): 
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        if(activation_link):
            driver.get(activation_link)
            
        UserTemplatePage.__init__(self, driver)   
        
    
    def set_password(self, password=Constant.DefaultPassword, wait_for_completed=True):
        """
        @summary: This action use to input password textbox   
        @author: Thanh Le
        @parameter: <password>: password string
                    <wait_for_completed>: boolean value to decide wait for complete or not
        @return welcome_to_beam_page page object
        """
        return self._submit_set_password_form(password, password)
    
    
    def set_password_expecting_error(self, new_password, confirm_password):
        """
        @summary: This action use to work with expected failure case when inputting invalid password   
        @author: Thanh Le
        @parameter: <new_password>: new password string
                    <confirm_password>: confirm password string
        @return PasswordSetupPage itself
        """
        self._submit_set_password_form(new_password, confirm_password)
        return self
    
    
    def _submit_set_password_form(self, new_password, confirm_password):
        """
        @summary: This action use to perform inputting password form   
        @author: Thanh Le
        @parameter: <new_password>: new password string
                    <confirm_password>: confirm password string
        """
        self._txtNewPassword.type(new_password)
        self._txtConfirmPassword.type(confirm_password)
        self._btnSetPassword.wait_until_clickable().click_element()
        self._btnSetPassword.wait_until_disappeared(10)
        
        current_url = self._driver.current_url
        
        if 'home' in current_url:
            return SimplifiedDashboardPage(self._driver)
        return WelcomeToBeamPage(self._driver)
    
    
    def get_set_password_error_message(self):
        """
        @summary: This action use to get set password error message 
        @author: Thanh Le
        @return: password error message
        """
        return "{} {}".format(self._lblErrorNote.text, self._lblErrorMessage.text)
    
    
    def is_page_dislayed(self):
        """
        @summary: Check if page is displayed 
        @author: Thanh Le
        @return True if page is displayed , False for vice versa
        """
        return self._txtNewPassword.is_displayed()

