from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.user.user_template_page import UserTemplatePage
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime
from pages.suitable_tech.user.password_setup_page import PasswordSetupPage
from pages.suitable_tech.user.password_reset_message_sent_page import PasswordResetMessageSentPage
from common.email_detail_constants import EmailDetailConstants


class _PasswordResetPageLocator(object):
    _txtEmail = (By.XPATH, "//input[@id='id_email']")
    _btnResetPassword = (By.XPATH, "//div[@class='actions']/input[@type='submit']")
    
    
class PasswordResetPage(UserTemplatePage):
    """
    @description: This is page object class for Password Reset Page.
        This page appear after user click on link "activate" via email
    @page: Password Reset Page
    @author: Thanh Le
    """
    
    
    """ Property """
    @property
    def _txtEmail(self):
        return Element(self._driver, *_PasswordResetPageLocator._txtEmail)
    @property
    def _btnResetPassword(self):
        return Element(self._driver, *_PasswordResetPageLocator._btnResetPassword)
    
    
    """ Method """
    def __init__(self, driver):    
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        UserTemplatePage.__init__(self, driver)
        
           
    def submit_reset_password_form(self, email):
        """
        @summary: This action use to submit reset password textbox   
        @parameter: <email>: account email string
        @return PasswordResetMessageSentPage page object
        @author: Thanh Le
        """
        self._txtEmail.wait_until_displayed()
        self._txtEmail.type(email)
        self._btnResetPassword.click_element()
        return PasswordResetMessageSentPage(self._driver)
    
        
    def reset_user_password(self, email, new_password):
        """
        @summary: This action use to reset reset password   
        @parameter: <email>: account email string
                    <new_password>: new password string
        @Update: Duy nguyen 25 Aug 2016 - Update "delete email content" in order to delete old message, 
                then GG can wait for new coming message.
        @return: PasswordSetupPage
        @author: Thanh Le
        """
        GmailUtility.delete_all_emails(receiver=email)
        self.submit_reset_password_form(email)
        reset_password_link = GmailUtility.get_reset_password_link(
                                mail_subject=EmailDetailConstants.PasswordResetEmailTitle,
                                receiver=email, 
                                sent_day=datetime.now())
        
        return PasswordSetupPage(self._driver, reset_password_link).set_password(new_password)
    
    