from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage


class _BeamHelpCenterPageLocator(object):
    _lblHeader = (By.XPATH, "//div[@class='uk-panel']/h1")
    

class BeamHelpCenterPage(BasePage):
    """
    @description: This is page object class for Beam Help Center Page.
        Please visit http://support.suitabletech.com/ for more details
    @page: Beam Help Center Page
    @author: Thanh Le
    """
    
    
    """    Properties    """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_BeamHelpCenterPageLocator._lblHeader)    
    
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        BasePage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        
    
    def is_page_displayed(self):      
        """      
        @summary: Check if page is displayed
        @return: True: the page is displayed
                False: the page is not displayed
        @author: Thanh Le
        """  
        return self._lblHeader.is_displayed()

