from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage
from common.constant import Browser


class _AllowAssociationPageLocator(object):
    _lblPolicyMessage = (By.XPATH,"//div[@id='policy_message']")
    _btnNo = (By.XPATH, "//button[@id='submit_deny_access']")
    _btnYes = (By.XPATH,"//button[@id='submit_approve_access']")
    
    
class AllowAssociationPage(BasePage):
    """
    @description: This is page object class for Allow Associate Page.
        This page appear after user sign-in to google at the first time
    @page: Allow Associate Page
    @author: Thanh Le
    """
    

    """    Properties    """ 
    @property
    def _lblPolicyMessage(self):
        return Element(self._driver, *_AllowAssociationPageLocator._lblPolicyMessage)
    @property
    def _btnYes(self):
        return Element(self._driver, *_AllowAssociationPageLocator._btnYes)
    @property
    def _btnNo(self):
        return Element(self._driver, *_AllowAssociationPageLocator._btnNo)
    
    
        """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        @created_date: October 03, 2016
        """   
        BasePage.__init__(self, driver)
        
        
    def is_policy_message_displayed(self, wait_time = 3):
        """
        @summary: Check if policy message displayed
        @param wait_time: time to wait 
        @return: True : the policy message is displayed, False: the policy message is not displayed
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        return self._lblPolicyMessage.is_displayed(wait_time)
    
    
    def approve_access_account_info(self):
        """
        @summary: This action use to approve google can access account information
        @return: ConfirmAssociationPage
        @Author: Duy Nguyen
        @created_date: October 03, 2016
        """
        
        if(self._driver._driverSetting.browser_name == Browser.Safari):
            if self._btnYes.is_displayed(2):
                self._btnYes.wait_until_clickable().click()
        else:
            self._btnYes.wait_until_clickable().click()
        from pages.suitable_tech.user.confirm_association_page import ConfirmAssociationPage
        return ConfirmAssociationPage(self._driver)
    
    
    def deny_access_account_info(self):
        """
        @summary: This action use to deny google can access account information
        @return: LoginPage 
        @Author: Duy Nguyen
        @created_date: October 03, 2016
        """
        self._btnNo.wait_until_clickable()
        self._btnNo.click()
        from pages.suitable_tech.user.login_page import LoginPage
        return LoginPage(self._driver)