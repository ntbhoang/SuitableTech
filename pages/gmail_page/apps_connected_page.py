from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage
from common.constant import Constant


class _AppsConnectedPageLocator(object):
    _lnkBeamApp = (By.XPATH, "//div[@role='listitem']//div[starts-with(@aria-label, 'Beam')]")
    _btnRemoveBeamApp = (By.XPATH, "//div[@role='listitem']//div[starts-with(@aria-label, 'Beam')]/..//span[.='Remove']")
    _btnOK = (By.XPATH, "(//div[@role='button']//span[.='OK'])[2]/../..")
    _lblRemoveSuccess = (By.XPATH, "//div[@aria-live='assertive' and contains(., 'Beam')]")
    

class AppsConnectedPage(BasePage):
    """
    @description: This is page object class for Sign In Google page.
    @page: GmailSignInPage
    @author: Duy Nguyen
    """   
    
    
    """ Property """
    @property
    def _lnkBeamApp(self):
        return Element(self._driver, *_AppsConnectedPageLocator._lnkBeamApp)
    @property
    def _btnRemoveBeamApp(self):
        return Element(self._driver, *_AppsConnectedPageLocator._btnRemoveBeamApp)
    @property
    def _btnOK(self):
        return Element(self._driver, *_AppsConnectedPageLocator._btnOK)
    @property
    def _lblRemoveSuccess(self):
        return Element(self._driver, *_AppsConnectedPageLocator._lblRemoveSuccess)
    
    
    
        """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method  
        @param driver: web driver
        @author: Duy Nguyen
        @created_date: October 03, 2016
        """
        BasePage.__init__(self, driver)
    
    
    def open(self):
        """
        @summary: use to navigate to Apps connected page of google account
        @return: Apps connected page
        @author: Thanh Le
        @created_date: October 03, 2016
        """
        self._driver.get(Constant.AppsConnectedURL)
        return self
        
        
    def remove_beam_from_connected_apps(self):
        """
        @summary: remove beam from google account
        @return: Apps connected page
        @author: Thanh Le
        @created_date: October 03, 2016
        """
        self._lnkBeamApp.wait_until_clickable().click()
        self._btnRemoveBeamApp.wait_until_clickable().click()
        self._btnOK.wait_until_clickable().click()
        self._lblRemoveSuccess.wait_until_displayed()
        return self
        
        
    def is_beam_connected(self):
        """
        @summary: Check beam connected
        @return: Apps connected page
        @author: Thanh Le
        @created_date: October 03, 2016
        """
        return self._lnkBeamApp.is_displayed(2)
        
        