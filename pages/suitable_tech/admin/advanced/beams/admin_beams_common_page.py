from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from common.constant import Platform

class _AdminBeamsPageLocator(object):
    _lnkDevices = (By.XPATH, "//li[contains(@ng-class, 'beams.group.devices')]//a[@ui-sref='beams.group.devices({groupid: activeGroupId()})']")
    _lnkMembers = (By.XPATH, "//li[@ui-sref-active='active']//a[contains(@href, '/members/')]")
    _lnkAccessTimes = (By.XPATH, "//li[@ui-sref-active='active']//a[contains(@href, '/access/')]")
    _lnkReservations = (By.XPATH, "//li[@ui-sref-active='active']//a[contains(@href, '/reservations/')]")
    _lnkSettings = (By.XPATH, "//li[@ui-sref-active='active']//a[contains(@href, '/settings/')]")
    _btnAllBeams = (By.XPATH,"//div[contains(@class, 'device-group-dropdown')]")
    _lnkCreateDeviceGroup = (By.XPATH, "//div[@class='dropdown header-buttons device-group-dropdown open']/descendant::button[@ng-click='createDeviceGroup()']")
    _lblHeader = (By.XPATH, "//div[@class='row device-group-header ng-scope']//h3[@class='detail-heading']")
    _btnBeamContent = (By.XPATH, "//button[@ng-click='addBeamContent()']")
    _lnkHelp = (By.XPATH,"//h3/small/a/span[@class='glyphicon glyphicon-question-sign']/..")

    """MOBILE UI"""
    _btnMNarvigation = (By.XPATH, "//div[@class='col-xs-12 visible-xs']//div[@class='btn-group dropdown header-buttons ng-scope']//button")
    _lstMNarvigation = (By.XPATH, "//div[@class='btn-group dropdown header-buttons ng-scope open']/ul")
    _lnkMDevices = (By.XPATH, "//div[@class='btn-group dropdown header-buttons ng-scope open']/ul[@class='dropdown-menu']//a[@ui-sref='beams.group.devices({groupid: activeGroupId()})']")
    _lnkMMembers = (By.XPATH, "//div[@class='btn-group dropdown header-buttons ng-scope open']/ul[@class='dropdown-menu']//a[@ui-sref='beams.group.members({groupid: activeGroupId()})']")
    _lnkMAccess = (By.XPATH, "//div[@class='btn-group dropdown header-buttons ng-scope open']/ul[@class='dropdown-menu']//a[@ui-sref='beams.group.access({groupid: activeGroupId()})']")
    _lnkMReservations = (By.XPATH, "//div[@class='btn-group dropdown header-buttons ng-scope open']/ul[@class='dropdown-menu']//a[@ui-sref='beams.group.reservations({groupid: activeGroupId()})']")
    _lnkMSettings = (By.XPATH, "//div[@class='btn-group dropdown header-buttons ng-scope open']/ul[@class='dropdown-menu']//a[@ui-sref='beams.group.settings({groupid: activeGroupId()})']")
                     
class AdminBeamsCommonPage(AdminTemplatePage):
    """
    @description: This is page object class that contains all common controls/methods used across all Beams pages.
        This class is ONLY for inheriting.
    @page: Beam All Devices page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lblHeader)
    @property
    def _btnBeamContent(self):
        return Element(self._driver, *_AdminBeamsPageLocator._btnBeamContent)
    @property
    def _lnkDevices(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkDevices)
    @property
    def _lnkMembers(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkMembers)
    @property
    def _lnkAccessTimes(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkAccessTimes)
    @property
    def _lnkReservations(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkReservations)
    @property
    def _lnkSettings(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkSettings)
    @property
    def _btnAllBeams(self):
        return Element(self._driver, *_AdminBeamsPageLocator._btnAllBeams)
    @property
    def _lnkCreateDeviceGroup(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkCreateDeviceGroup)
    @property
    def _lnkHelp(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkHelp)
        
    def _ddlDeviceInAllBeams(self, device_group_name):
        return Element(self._driver, *_AdminBeamsPageLocator._ddlDeviceInAllBeams(device_group_name))


    """MOBILE UI"""
    @property
    def _btnMNarvigation(self):
        return Element(self._driver, *_AdminBeamsPageLocator._btnMNarvigation)
    @property
    def _lstMNarvigation(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lstMNarvigation)
    @property
    def _lnkMDevices(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkMDevices)
    @property
    def _lnkMMembers(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkMMembers)
    @property
    def _lnkMAccess(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkMAccess)
    @property
    def _lnkMReservations(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkMReservations)
    @property
    def _lnkMSettings(self):
        return Element(self._driver, *_AdminBeamsPageLocator._lnkMSettings)
    
    
    """    Methods      """    
    def __init__(self, driver):        
        """      
        @summary: Constructor method   
        @param driver: Web driver 
        @author: Thanh Le    
        @created_date: August 08, 2016     
        """
        AdminTemplatePage.__init__(self, driver)


    def _open_naviagtion_on_moble(self):
        """      
        @summary: Open narvigation on mobile
        @author: Tan Le    
        @created_date: January 19, 2018     
        """
        self._btnMNarvigation.click()
        self._lstMNarvigation.wait_until_displayed()
        return self
        
    def goto_devices_tab(self):
        """      
        @summary:  Go to 'Devices' sub tab of a device group    
        @return: AdminBeamsDevicesPage: Devices tab
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.wait_untill_success_msg_disappeared()
            self._open_naviagtion_on_moble()._lnkMDevices.click()
        else:
            self._lnkDevices.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_devices_page import AdminBeamsDevicesPage
        return AdminBeamsDevicesPage(self._driver)
    
    
    def goto_setting_tab(self):
        """      
        @summary: Go to Settings tab of a device group   
        @return: AdminBeamsDevicesPage: Settings tab
        @author: Thanh Le  
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.wait_untill_success_msg_disappeared()
            self._open_naviagtion_on_moble()._lnkMSettings.click()
        else:
            self._lnkSettings.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_settings_page import AdminBeamsSettingsPage
        return AdminBeamsSettingsPage(self._driver)
    
    
    def goto_accesstimes_tab(self):
        """      
        @summary: Go to Access Times tab of a device group  
        @return: AdminBeamsDevicesPage: Access Times tab
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.wait_untill_success_msg_disappeared()
            self._open_naviagtion_on_moble()._lnkMAccess.click()
        else:
            self._lnkAccessTimes.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_access_times_page import AdminBeamAccessTimesPage
        return AdminBeamAccessTimesPage(self._driver)


    def goto_members_tab(self):
        """      
        @summary: Go to Members tab of a device group 
        @return: AdminBeamsDevicesPage: Members tab
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.wait_untill_success_msg_disappeared()
            self._open_naviagtion_on_moble()._lnkMMembers.click()
        else:
            self._driver.scroll_up_to_top()
            self._lnkMembers.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_members_page import AdminBeamsMembersPage
        return AdminBeamsMembersPage(self._driver)


    def goto_reservations_tab(self):
        """      
        @summary: Go to Reservations tab of a device group   
        @return: AdminBeamsDevicesPage: Reservations tab
        @author: Thanh Le         
        @created_date: August 08, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.wait_untill_success_msg_disappeared()
            self._open_naviagtion_on_moble()._lnkMReservations.click()
        else:
            self._lnkReservations.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_reservations_page import AdminReservationsPage
        return AdminReservationsPage(self._driver)
    
    
    def open_beam_content_dialog(self):
        """
        @summary: Method to open Manage Beam Content dialog
        @return: BeamContentDialog: This is 'Manage Beam Content' dialog
        @author: Thanh le
        @created_date: April, 2017
        """
        self._btnBeamContent.scroll_to().wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.beam_content_dialog import BeamContentDialog
        beam_content_dialog = BeamContentDialog(self._driver)
        if not beam_content_dialog._btnContinue.is_displayed(3):
            self._btnBeamContent.jsclick()
        return beam_content_dialog
    

    def open_help_dialog(self):
        """
        @summary: Method to open Help dialog
        @return: AdminBeamsDevicesPage
        @author: Khoi Ngo
        @created_date: October, 2017
        """
        self._lnkHelp.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
        return DialogBase(self._driver)

