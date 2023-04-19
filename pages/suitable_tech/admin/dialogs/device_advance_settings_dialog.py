from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from core.webdriver.elements.element_list import ElementList
from common.application_constants import ApplicationConst

class _DeviceAdvanceSettingLocator(object): 
    
    _lblLinkedBy = (By.XPATH, "//div[@ng-show = 'device.linked_by']//dd")
    _lblLinkedOn = (By.XPATH, "//div[@ng-show = 'device.linked_on']//dd")
    _sectionNetworks = (By.XPATH, "//dl[@ng-repeat='interface in device.network_info.interfaces']")
    _tabSettings = (By.XPATH, "//a[@ng-click=\"setSubview($event, 'settings')\"]")
    _btnRestart = (By.XPATH, "//button[@class='btn btn-warning dropdown-toggle']")
    _btnShutDown = (By.XPATH, "//button[@class='btn btn-danger dropdown-toggle']")
    _lnkRestartImmediately = (By.XPATH, "//a[@ng-click=\"shutdown($event, 'power_cycle', 'now')\"]")
    _lnkRestartWhenIdle = (By.XPATH, "//a[@ng-click=\"shutdown($event, 'power_cycle', 'when_idle')\"]")
    _lnkShutDownImmediately = (By.XPATH, "//a[@ng-click=\"shutdown($event, 'power_off', 'now')\"]")
    _lnkShutDownWhenIdle = (By.XPATH, "//a[@ng-click=\"shutdown($event, 'power_off', 'when_idle')\"]")
    
    @staticmethod
    def _lblSystemInfo(value):
        return (By.XPATH, u"//h4[contains(.,\"{}\")]/..//dt".format(value))
    @staticmethod
    def _lblCurrentNetworkInfo(value):
        return (By.XPATH, u"//h4[contains(.,\"{}\")]/..//dl[@class='dl-horizontal item-details']/dt".format(value))
    @staticmethod
    def _lblRelayServerInfo(value):
        return (By.XPATH, u"//h4[contains(.,\"{}\")]/..//dl[@ng-if='device.state.relay_server']/dt".format(value))
        
        
class DeviceAdvanceSettingsDialog(DialogBase):
    """
    @description: This is page object class for Device Advance Settings Dialog. You need to init it before using in page class.
    @page: Device Advance Settings Dialog
    @author: Thanh Le
    """
    
    """    Properties    """
    
    @property
    def _lblLinkedBy(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._lblLinkedBy)
    @property
    def _lblLinkedOn(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._lblLinkedOn)
    @property
    def _sectionNetworks(self):
        return ElementList(self._driver, *_DeviceAdvanceSettingLocator._sectionNetworks)
    @property
    def _tabSettings(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._tabSettings)
    @property
    def _btnRestart(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._btnRestart)
    @property
    def _btnShutDown(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._btnShutDown)
    @property
    def _lnkRestartImmediately(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._lnkRestartImmediately)
    @property
    def _lnkRestartWhenIdle(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._lnkRestartWhenIdle)
    @property
    def _lnkShutDownImmediately(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._lnkShutDownImmediately)
    @property
    def _lnkShutDownWhenIdle(self):
        return Element(self._driver, *_DeviceAdvanceSettingLocator._lnkShutDownWhenIdle)
    
    def _lblSystemInfo(self):
        return ElementList(self._driver, *_DeviceAdvanceSettingLocator._lblSystemInfo(ApplicationConst.LBL_SYSTEM)) 
    
    def _lblCurrentNetworkInfo(self):
        return ElementList(self._driver, *_DeviceAdvanceSettingLocator._lblCurrentNetworkInfo(ApplicationConst.LBL_NETWORK))  
    
    def _lblRelayServerInfo(self):
        return ElementList(self._driver, *_DeviceAdvanceSettingLocator._lblRelayServerInfo(ApplicationConst.LBL_NETWORK))    
    
    """    Methods    """
    def __init__(self, driver): 
        """      
        @summary: Constructor method
        @param driver: web driver
        @author: Thanh Le         
        """        
        self._driver = driver
        self._wait_for_loading_completed()
    
    def get_linked_by_infomation(self):
        """      
        @summary: Get user who linked it is available in the Beam Manager
        @return: user email
        @author: Thanh Le
        @created_date: May 03, 2017
        """
        return self._lblLinkedBy.text 
    
    
    def get_link_date_infomation(self):
        """      
        @summary: Get the date of linking device 
        @return: date string
        @author: Thanh Le
        @created_date: May 03, 2017
        """
        return self._lblLinkedOn.text
    
    
    def does_system_info_display_fully(self, system_info):
        """      
        @summary: The method is to check system info display fully
        @param system_info: array displayed info 
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        sytem_lables_list = []
        self._wait_for_loading_completed()
        lable_element_list = self._lblSystemInfo().get_all_elements()
        for lable in lable_element_list:
            sytem_lables_list.append(lable.text)
        return sorted(sytem_lables_list)==sorted(system_info)
    
    
    def does_current_network_info_display_fully(self, current_network_info):
        """      
        @summary: The method is to check current network info display fully
        @param current_network_info: array current network info
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        current_network_lables_list = []
        lable_element_list = self._lblCurrentNetworkInfo().get_all_elements()
        for lable in lable_element_list:
            current_network_lables_list.append(lable.text)
        return sorted(current_network_lables_list)==sorted(current_network_info)
    
    
    def does_relay_server_info_display_fully(self, relay_server_info):
        """      
        @summary: The method is to check relay server info display fully
        @param relay_server_info: array relay server info
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        relay_server_lables_list = []
        lable_element_list = self._lblRelayServerInfo().get_all_elements()
        for lable in lable_element_list:
            relay_server_lables_list.append(lable.text)
        return sorted(relay_server_lables_list)==sorted(relay_server_info)
    
    
    def does_network_types_info_display_fully(self, network_info):
        """      
        @summary: The method is to check network types info display fully
        @param network_element: network_element
        @param relay_server_info: array network info
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        network_element_list = self._sectionNetworks.get_all_elements()
        if len(network_element_list)==0:
            print("There is no section network in Beam Advance Settings") 
        else:
            for network_element in network_element_list:
                relay_server_lables_list = []
                lable_element_list = network_element.find_elements(by=By.CSS_SELECTOR, value='dt')
                for lable in lable_element_list:
                    relay_server_lables_list.append(lable.text)
                if sorted(relay_server_lables_list)!=sorted(network_info):
                    return False
            
        return True
    
    
    def does_network_info_display_fully(self, current_network_info, network_info, relay_server_info):
        """
        @summary: The method is to  network info display fully infomation
        @param current_network_info: array current network info
        @param network_info: array network type info
        @param relay_server_info: array relay server info
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        if not self.does_current_network_info_display_fully(current_network_info):
            print('Current network does not display full infomation')
            return False
        if not self.does_network_types_info_display_fully(network_info):
            print('Network type sections do not display full infomation')
            return False            
        if not self.does_relay_server_info_display_fully(relay_server_info):
            print('Relay server does not display full infomation')
            return False    
        return True             
                
                
    def enter_settings_tab(self):
        """
        @summary: The method is enter Settings tab
        @return: Device Advance Settings Dialog
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        self._tabSettings.click()
        return self
    
    
    def does_restart_button_display_corectly(self):
        """
        @summary: The method is to check Restart button and its dropdown
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        if self._btnRestart.is_displayed(1):
            self._btnRestart.click()
            if self._lnkRestartImmediately.is_displayed(1) and self._lnkRestartWhenIdle.is_displayed(1):
                return True
        return False
    

    def does_shutdown_button_display_corectly(self):
        """
        @summary: The method is to check Shutdown button and its dropdown
        @return: True/False
        @author: Tan Le
        @created_date: Sept 29, 2017
        """
        if self._btnShutDown.is_displayed(1):
            self._btnShutDown.click()
            if self._lnkShutDownImmediately.is_displayed(1) and self._lnkShutDownWhenIdle.is_displayed(1):
                return True
        return False
    
    
    def does_settings_tab_display_correctly(self):
        return self.does_restart_button_display_corectly() and self.does_shutdown_button_display_corectly()