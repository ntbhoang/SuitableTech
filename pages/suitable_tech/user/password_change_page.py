from pages.suitable_tech.user.user_template_page import UserTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.user.password_change_complete_page import PasswordChangeCompletePage


class _PasswordChangePageLocator(object):
    _txtNewPassword =  (By.XPATH, "//input[@id='id_new_password1']")
    _txtConfirmPassword = (By.XPATH, "//input[@id='id_new_password2']")
    _txtOldPassword = (By.XPATH, "//input[@id='id_old_password']")
    _lblHeader = (By.XPATH, "//section[@class='masthead registration']//h2")
    _btnChangePassword = (By.XPATH, "//input[@name='submit']")
    
    
class PasswordChangePage(UserTemplatePage):
    """
    @description: This is page object class for Password Change page. 
        This page will be opened after clicking on Change Your Password link in Account Settings page.
        Please visit https://staging.suitabletech.com/accounts/password_change/ for more details.
    @page: Password Change page
    @author: Thanh Le
    """


    """    Properties    """   
    @property
    def _lblHeader(self):
        return Element(self._driver, *_PasswordChangePageLocator._lblHeader) 
    @property
    def _txtNewPassword(self):
        return Element(self._driver, *_PasswordChangePageLocator._txtNewPassword)
    @property
    def _txtConfirmPassword(self):
        return Element(self._driver, *_PasswordChangePageLocator._txtConfirmPassword)
    @property
    def _txtOldPassword(self):
        return Element(self._driver, *_PasswordChangePageLocator._txtOldPassword)
    @property
    def _btnChangePassword(self):
        return Element(self._driver, *_PasswordChangePageLocator._btnChangePassword)
    
    
    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """     
        UserTemplatePage.__init__(self, driver)   
        self._lblHeader.wait_until_displayed(5)
        
    
    def change_password(self, new_password, old_password):
        """
        @summary: This action use to change password  
        @parameter: <new_password>: new password string
                    <old_password>: old password string
        @return PasswordChangeCompletePage page object
        @author: Thanh Le
        """
        self._txtNewPassword.type(new_password)
        self._txtConfirmPassword.type(new_password)
        self._txtOldPassword.type(old_password)
        self._btnChangePassword.click_element()
        return PasswordChangeCompletePage(self._driver)

