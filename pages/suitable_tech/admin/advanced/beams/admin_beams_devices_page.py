from selenium.webdriver.common.by import By
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from core.webdriver.elements.element import Element
from common.application_constants import ApplicationConst
from time import sleep


class _AdminBeamsDevicesPageLocator(object):
    _btnAddDevices = (By.XPATH, "//button[@type='button' and @ng-click='addDevices()']")
    _iconIconView = (By.XPATH, "//span[@class='glyphicon glyphicon-th-large']/..")
    _iconListView = (By.XPATH, "//span[@class='glyphicon glyphicon-th-list']/..")
    _imgListViewDeviceItem = (By.XPATH, "//div[@class='img-responsive small profile-image-container ng-isolate-scope']")
    _lblDevicesGroupName = (By.XPATH, "//h3[@class='detail-heading']")
    _txtSearchBeams = (By.XPATH, "//input[@type='search']")
    
    @staticmethod
    def _lblDeviceCard(value):
        return (By.XPATH, u"//div[@class='profile-title' and @title=\"{}\"]/a".format(value))
    @staticmethod
    def _lnkDeviceToChoose(device_name):
        return (By.XPATH, u"//div[@class='modal-content']//h5[normalize-space(.)=\"{}\"]/../..".format(device_name))
    @staticmethod
    def _pnlIconViewDeviceItem(panel_value):
        return (By.XPATH, u"//div[contains(@class, 'profile-title') and normalize-space(.)=\"{}\"]/..//div[@class='profile-image-container ng-isolate-scope']".format(panel_value))
    @staticmethod
    def _pnlListViewDeviceItem(panel_value):
        return (By.XPATH, u"//td[.=\"{}\"]/preceding-sibling::td/div".format(panel_value))
    
    
class AdminBeamsDevicesPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam Devices page.
        This page will be opened after clicking Devices tab on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/beams/787/ for more details.
    @page: Beam Devices page
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _txtSearchBeams(self):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._txtSearchBeams)    
    @property
    def _btnAddDevices(self):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._btnAddDevices)
    @property
    def _lblDevicesGroupName(self):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._lblDevicesGroupName)
    @property
    def _iconIconView(self):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._iconIconView)
    @property
    def _iconListView(self):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._iconListView)
    
    def _pnlIconViewDeviceItem(self, panel_value):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._pnlIconViewDeviceItem(panel_value))
    def _pnlListViewDeviceItem(self, panel_value):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._pnlListViewDeviceItem(panel_value))
    def _lblDeviceCard(self, value):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._lblDeviceCard(value))
    def _lnkDeviceToChoose(self, device_name):
        return Element(self._driver, *_AdminBeamsDevicesPageLocator._lnkDeviceToChoose(device_name))
    
    """    Methods    """
    def __init__(self, driver, wait_for_loading=True):        
        """      
        @summary: Constructor method
        @param driver: Web driver
        @param wait_for_loading: time to wait the page loading successfully  
        @author: Thanh Le      
        @created_date: August 08, 2016   
        """
        if(wait_for_loading):
            AdminBeamsCommonPage.__init__(self, driver)
            self._lblHeader.wait_until_displayed()
            self.wait_for_loading()
        else:
            self._driver = driver
            
    
    def add_devices(self, devices=[], wait_for_completed=True):
        """      
        @summary: Add a device to a device group         
        @param devices: device would like to add to device group
        @param wait_for_completed: time to wait for add devices completely
        @return: AdminBeamsDevicesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._btnAddDevices.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.create_device_group import CreateDeviceGroupDialog                
        dialog = CreateDeviceGroupDialog(self._driver)
        
        for device_name in devices:
            dialog._select_a_device(device_name)   
              
        dialog.submit(wait_for_completed)
        if(wait_for_completed):
            self.wait_for_loading()
            
        return self
    
    
    def select_a_device(self, device_name):
        """      
        @summary: Select a device with device name         
        @param device_name: name of device would like to select
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._txtSearchBeams.type(device_name)
        sleep(2)
        self._lblDeviceCard(device_name).wait_until_clickable().click_element()
        from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage
        return AdminBeamDetailPage(self._driver, device_name)

    
    def switch_to_icon_view(self):
        """      
        @summary: Switch to icon view         
        @return: AdminBeamsDevicesPage
        @author:  Thanh Le   
        @created_date: August 08, 2016   
        """
        self._iconIconView.click()
        self.wait_for_loading(5)
        return self
    
    
    def get_device_group_name(self):
        """      
        @summary: Get device group name         
        @return: device group name 
        @author: Thanh Le    
        @created_date: August 08, 2016
        """
        header_detail = self._lblDevicesGroupName.text
        return header_detail.replace(ApplicationConst.LBL_BEAMS_DEVICES_PAGE_HEADER, "").strip()
    
    
    def switch_to_list_view(self):
        """      
        @summary: Switch to list view  
        @return: AdminBeamsDevicesPage
        @author: Thanh Le  
        @created_date: August 08, 2016
        """
        self._iconListView.click()
        self.wait_for_loading(5)
        return self
    
    
    def get_item_size_in_icon_view(self, panel_value):
        """      
        @summary: Get size of device group icon in icon view
        @param panel_value: panel value
        @return: size of device group icon in icon view
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        try:
            return int(self._pnlIconViewDeviceItem(panel_value).get_attribute("imgsize"))
        except Exception:
            return 0
    
    
    def get_item_size_in_list_view(self, panel_value):
        """      
        @summary: Get size of device group icon in list view  
        @param panel_value: panel value
        @return: size of device group icon in list view
        @author: Thanh Le 
        @created_date: August 08, 2016
        """
        try:
            return int(self._pnlListViewDeviceItem(panel_value).get_attribute("imgsize"))
        except Exception as ex:
            raise Exception('Beam does not display ' + str(ex))        
    
    def is_device_existed(self, search_value, check_value=None):
        """      
        @summary: Check if a device is existed or not  
        @param search_value: the device to be checked
        @param check_value: criteria to search
        @return: True: The device is existed, False: The device is not existed
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        sleep(1)
        self._txtSearchBeams.type(search_value)
        if(check_value != None):
            return self._lblDeviceCard(check_value).is_displayed()
        else:
            return self._lblDeviceCard(search_value).is_displayed()
    
    
    def is_device_not_existed(self, search_value, check_value=None):
        """      
        @summary: Check if the device is not existed    
        @param search_value: the device to be checked
        @pama check_value: criteria to search
        @return: True: The device is not existed, False: The device is existed
        @author: Thanh Le 
        @created_date: August 08, 2016        
        """
        self._txtSearchBeams.type(search_value)
        if(check_value != None):
            return self._lblDeviceCard(check_value).is_disappeared()
        else:
            return self._lblDeviceCard(search_value).is_disappeared()


    def is_add_devices_button_display(self):
        """
        @summary: check Add Devices button
        @author: Thanh le
        @created_date: September 28, 2017
        """
        return self._btnAddDevices.is_displayed()

