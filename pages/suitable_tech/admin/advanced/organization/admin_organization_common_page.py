from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from common.constant import Platform
from core.webdriver.elements.dropdownlist import DropdownList


class _OrganizatioCommonPageLocator(object):
    _lnkSettings = (By.CSS_SELECTOR, ".nav.nav-tabs a[href='#/organization/']")
    _lnkAuthentication = (By.CSS_SELECTOR, ".nav.nav-tabs a[href='#/organization/authentication/']")
    _lnkDeviceSupport = (By.CSS_SELECTOR, ".nav.nav-tabs a[href='#/organization/devicesupport/']")
    _lnkBilling = (By.CSS_SELECTOR, ".nav.nav-tabs a[href='#/organization/billing/']")

    """Mobile UI"""
    _ddl_MSettings = (By.XPATH, "//button[@class='btn btn-default dropdown-toggle ng-binding']/..")


class OrganizationCommonPage(AdminTemplatePage):
    """
    @description: This is page object class that contains all common controls/methods used across all Organization pages.
        This class is ONLY for inheriting.
    @page: Organization page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _lnkSettings(self):
        return Element(self._driver, *_OrganizatioCommonPageLocator._lnkSettings)
    @property
    def _lnkAuthentication(self):
        return Element(self._driver, *_OrganizatioCommonPageLocator._lnkAuthentication)
    @property
    def _lnkDeviceSupport(self):
        return Element(self._driver, *_OrganizatioCommonPageLocator._lnkDeviceSupport)
    @property
    def _lnkBilling(self):
        return Element(self._driver, *_OrganizatioCommonPageLocator._lnkBilling)

    """Mobile UI"""
    @property
    def _ddl_MSettings(self):
        return DropdownList(self._driver, *_OrganizatioCommonPageLocator._ddl_MSettings)
    @property
    def _hrefSettings(self):
        return "#/organization/"
    @property
    def _hrefAuthen(self):
        return "#/organization/authentication/"
    @property
    def _hrefDeviceSupport(self):
        return "#/organization/devicesupport/"

   
    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web driver 
        @author: Khoi Ngo       
        """      
        AdminTemplatePage.__init__(self, driver)


    def open_settings_tab(self):
        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            self._ddl_MSettings.select_by_href(self._hrefSettings)
        else:
            self._lnkSettings.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.organization.admin_organization_setting_page import OrganizationSettingsPage
        return OrganizationSettingsPage(self._driver)
    

    def open_billing_tab(self):
        self._lnkBilling.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.organization.admin_organization_billing_page import OrganizationBillingPage
        return OrganizationBillingPage(self._driver)
    
    
    def open_authentication_tab(self):
        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            self._ddl_MSettings.select_by_href(self._hrefAuthen)
        else:
            self._lnkAuthentication.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.organization.admin_organization_authentication_page import OrganizationAuthenticationPage
        return OrganizationAuthenticationPage(self._driver)


    def open_device_support_tab(self):
        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            self._ddl_MSettings.select_by_href(self._hrefDeviceSupport)
        else:
            self._lnkDeviceSupport.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.organization.admin_organization_device_support_page import OrganizationDeviceSupportPage
        return OrganizationDeviceSupportPage(self._driver)

