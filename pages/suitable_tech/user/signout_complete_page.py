from pages.suitable_tech.user.user_template_page import UserTemplatePage
from common.constant import Constant
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By

class _SignoutCompletePageLocator(object):
    _lblSignoutComplete = (By.XPATH, "//section[@class='masthead registration']")


class SignoutCompletePage(UserTemplatePage):
    """
    @description: This is page object class for Sign-out complete page.
        Please visit https://stg1.suitabletech.com/accounts/logout/ for more details
    @page: Home page
    @author: Thanh Le
    """

   
    """    Properties    """      
    @property
    def _lblSignoutComplete(self):
        return Element(self._driver, *_SignoutCompletePageLocator._lblSignoutComplete)
    
    
    """    Methods    """
    def __init__(self, driver, wait_for_loading=False):
        """      
        @summary: Constructor method    
        @parameter: driver: Web Driver
        @parameter: wait_for_loading: boolean value to decide wait for loading or not
        @author: Thanh Le
        @created: Jan-06-2017
        """  
        UserTemplatePage.__init__(self, driver, wait_for_loading)
        if(wait_for_loading):
            self._lblSignoutComplete.wait_until_displayed()
        
        
    def is_page_displayed(self):
        """
        @summary: Check if sign-out complete page is displayed or not
        @return: True if logout page is displayed , False if the logout page is not displayed
        @author: Thanh Le
        @created: Jan-06-2017
        """
        current_url = self._driver.current_url      
        return (current_url == Constant.SuitableTechLogoutURL or current_url == "{}#".format(Constant.SuitableTechLogoutURL))
        
        
    def open(self):
        """
        @summary: This action use to navigate Sign-Out Complete page
        @return SignoutCompletePage page object
        @author: Thanh Le
        @created: Jan-06-2017
        """
        self._driver.get(Constant.SuitableTechURL + self._hrefLogOut)
        return SignoutCompletePage(self._driver, True)

