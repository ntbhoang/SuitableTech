from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage
from pages.suitable_tech.user.user_template_page import UserTemplatePage


class _ConfirmAssociationPageLocator(object):
    _txtfFormContent = (By.XPATH, "//section[@class='content']//form[@method='post']") 
    _btnYes = (By.XPATH, "//button[@class='radius button']")
    _btnNo = (By.XPATH, "//a[@href='/accounts/login/']")

    
class ConfirmAssociationPage(UserTemplatePage):
    """
    @description: This is page object class for Confirm Associate page.
    @page: Confirm Association Page 
    @author: Thanh Le
    """
    
    
    """    Properties    """  
    @property
    def _btnYes(self):
        return Element(self._driver, *_ConfirmAssociationPageLocator._btnYes)
    @property
    def _btnNo(self):
        return Element(self._driver, *_ConfirmAssociationPageLocator._btnNo)
    @property
    def _txtfFormContent(self):
        return Element(self._driver, *_ConfirmAssociationPageLocator._txtfFormContent)
    
    
        """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Duy Nguyen
        """     
        BasePage.__init__(self, driver)
        
        
    def change_auth(self, value=True):
        """      
        @summary: This action is used to set an account become GSSO authentication
        @param value: boolean value to decide change GSSO authentication or not
        @return WelcomeToBeamPage if True, LoginPage if False
        @author: Duy Nguyen
        """ 
        if value:
            return self.accept_change_authentication()
        else:
            return self.decline_change_authentication()
            
    
    def accept_change_authentication(self):
        """
        @summary: click on 'Yes' button on "Confirm New Authentication Method" page at the first time you sign in
         with gmail authorize  
        @return:  WelcomeToBeamPage
        @author: Thanh Le
        """
        self._btnYes.click()
        from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
        return SimplifiedDashboardPage(self._driver)
    
    
    def decline_change_authentication(self):
        """
        @summary: click on 'No' button on "Confirm New Authentication Method" page at the first time you sign in
         with gmail authorize  
        @return:  LoginPage
        @author: Thanh Le
        """
        self._btnNo.click()
        from pages.suitable_tech.user.login_page import LoginPage
        return LoginPage(self._driver)
        
    
    def get_warning_message(self):
        """      
        @summary: This action is used to get warning message text
        @return: warning message text
        @author: Duy Nguyen
        """
        return self._txtfFormContent.text
        

    def is_page_displayed(self, timeout=10):
        """
        @summary: check "Confirm New Authentication Method" display or not
        @return: True if displays otherwise False
        @author: Thanh Le
        """
        return self._btnYes.is_displayed(timeout)

