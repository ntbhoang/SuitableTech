from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage


class _OthersPageLocator(object):
    _lblHeader = (By.XPATH, "//h2")
    _txtContent = (By.XPATH, "//div[@class='row']//div[@class='large-12 columns text-center']")


class OthersPage(AdminTemplatePage):
    """
    @description: This is page object class for Others page.
    @page: Others page(includes: approve request, error page, reject page and some pages like that).
    @author: Khoi Ngo
    """


    """    Properties    """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_OthersPageLocator._lblHeader)
    @property
    def _txtContent(self):
        return Element(self._driver, *_OthersPageLocator._txtContent)
   
    
    """    Methods    """
    def __init__(self, driver, wait_for_page_load=False):
        """      
        @summary: Constructor method    
        @param 
            driver: Web Driver 
        @author: Khoi Ngo
        """
        self._driver = driver
        if wait_for_page_load:
            AdminTemplatePage.__init__(self, driver)
            
    
    def open(self, url):
        """
        @summary: open page
        @param url: AUT's url needs to open
        @return: return OthersPage
        @author: Thanh Le
        """
        self._driver.get(url)
        return OthersPage(self._driver, True)
    

    def get_header(self):
        """
        @summary: This action use to get header value  
        @author: Khoi Ngo
        @return: header text
        """
        return self._lblHeader.text
    
    
    def get_msg_content(self): 
        """
        @summary: This action use to get message value  
        @author: Khoi Ngo
        @return: message text
        """        
        return self._txtContent.text
