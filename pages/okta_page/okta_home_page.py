from pages.basepage import BasePage
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By
from core.webdriver.elements.dropdownlist import DropdownList

class _OktaHomePageLocator(BasePage):
    _ddlUserDropDownMenu = (By.XPATH, "//div[@data-se='user-menu']")
    _imgLogo = (By.XPATH, "//a[@class='logo-wrapper']//img")
    
class OktaHomePage(BasePage):
    """
    @description: This is page object class for OneLogin Page
    @page: One Login Page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _ddlUserDropDownMenu(self):
        return DropdownList(self._driver, *_OktaHomePageLocator._ddlUserDropDownMenu)
    @property
    def _imgLogo(self):
        return Element(self._driver, *_OktaHomePageLocator._imgLogo)
    

    """    Methods    """
    def __init__(self, driver, wait_for_loading=True):
        """
        @summary: Constructor method
        @parameter: driver: Web Driver
                    wait_for_loading: boolean value to decide wait for loading or not
        @author: Thanh Le
        """
        BasePage.__init__(self, driver)
        if(wait_for_loading):
            self._imgLogo.wait_until_displayed()   
        
        
    def goto_setting_page(self):
        """
        @summary: goto setting page
        @return: Okta setting page
        @author: Thanh Le
        """
        self._ddlUserDropDownMenu.wait_until_displayed()
        self._ddlUserDropDownMenu.select_by_partial_text("Settings")
        from pages.okta_page.okta_setting_page import OktaSettingPage
        return OktaSettingPage(self._driver)
        
        