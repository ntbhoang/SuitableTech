from pages.suitable_tech.user.user_template_page import UserTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element

class _PasswordChangeCompletePageLocator(object):
    _lblHeader = (By.XPATH, "//section[@class='masthead registration']//h2")
    _btnContinue = (By.CSS_SELECTOR, "section[class='content'] a[href='/accounts/home/']")
    

class PasswordChangeCompletePage(UserTemplatePage):
    """
    @description: This is page object class for Password Change Complete page. 
        This page will be opened after changing password in Change Password page.
        Please visit https://staging.suitabletech.com/accounts/password_change/done/ for more details.
    @page: Password Change Complete page
    @author: Thanh Le
    """


    """    Properties    """   
    @property
    def _lblHeader(self):
        return Element(self._driver, *_PasswordChangeCompletePageLocator._lblHeader)
    @property
    def _btnContinue(self):
        return Element(self._driver, *_PasswordChangeCompletePageLocator._btnContinue)
    
    
    """    Methods    """
    def __init__(self, driver):    
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        UserTemplatePage.__init__(self, driver)   
        self._btnContinue.wait_until_displayed()


    def continue_login(self, temp_pass=True):
        """
        @summary: Click continue button
        @return: True if welcome user page is displayed, False for vice versa
        @author: Thanh Le
        """
        self._btnContinue.wait_until_clickable().click()
        self._btnContinue.wait_until_disappeared()
        if temp_pass:
            from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
            return SimplifiedDashboardPage(self._driver)
        from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
        return WelcomeToBeamPage(self._driver)


    def is_welcome_user_page_displayed(self):
        """
        @summary: Check if welcome user page display
        @author: Thanh Le
        """
        from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
        return WelcomeToBeamPage(self._driver).is_welcome_user_page_displayed()

