from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
import urllib

class _BeamSoftwareInstallersLocator(object):
    _btnDownload = (By.XPATH, "//a[@id='download-btn']")
    _lblHeader = (By.XPATH, "//section[@class='masthead info']//h2")
    
    
class BeamSoftwareInstallersPage(AdminTemplatePage):
    """
    @description: This is page object class for Beam Software Installer Page.
    @page:  Beam Software Installer Page
    @author: Thanh Le
    """
    
    
    """    Properties    """
    @property
    def _btnDownload(self):
        return Element(self._driver, *_BeamSoftwareInstallersLocator._btnDownload)
    @property
    def _lblHeader(self):
        return Element(self._driver, *_BeamSoftwareInstallersLocator._lblHeader)
    
    """    Methods    """
    def __init__(self, driver): 
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """          
        AdminTemplatePage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
    
    
    def get_download_link_status(self):
        """
        @summary: get status code after run download Beam installer
        @return: return download status code, example 200 for successful
        @author: Thanh Le
        """
        try:
            self._btnDownload.wait_until_displayed()
            download_link = self._btnDownload.get_attribute("href")
            return urllib.request.urlopen(download_link).code
        except Exception as ex:
            return (str(ex))
        
