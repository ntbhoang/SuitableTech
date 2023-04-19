from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.organization.admin_organization_common_page import OrganizationCommonPage

class _OrganizationDeviceSupportPageLocator(object):
    _txtSearch = (By.CSS_SELECTOR, "input[type='search']")
    _tblDevices = (By.XPATH, "//table")

class OrganizationDeviceSupportPage(OrganizationCommonPage):
    """
    @description: This is page object class for Admin Organization Authentication page.
        This page will be opened after clicking Device Support tab on Organization page.
        Please visit https://stg1.suitabletech.com/manage/129/#/organization/devicesupport/ for more details.
    @page: Admin Organization Device Support page
    @author: thanh.viet.le
    """

    """    Properties    """
    @property
    def _txtSearch(self):
        return Element(self._driver, *_OrganizationDeviceSupportPageLocator._txtSearch)
    @property
    def _tblDevices(self):
        return Element(self._driver, *_OrganizationDeviceSupportPageLocator._tblDevices)
    
    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web driver 
        @author: Khoi Ngo       
        """      
        OrganizationCommonPage.__init__(self, driver)


    def check_table_devices_can_sort(self):
        """
        @summary: Check table can sort with each label header
        @return: True if table can sort with all label when click for each, Fail if table can not sort
        @author: Khoi Ngo
        @created_date: Oct 30, 2017
        """
        xpath_table = self._tblDevices._value
        return self.check_sort_table_work(xpath_table)


