from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase


class _CreateDeviceGroupDlgLocator(object):
    _txtGroupName = (By.XPATH, "//div[@class='modal-content']//input[@ng-model='devicegroup.name']")
    _btnChooseDevices = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='setChooseDevices()']")
    _txtSearchBeams = (By.XPATH, "//div[@class='modal-content']//input[@type='search']")
   
    @staticmethod
    def _lnkDeviceToChoose(device_name):
        return (By.XPATH, u"//div[@class='modal-content']//h5[normalize-space(.)=\"{}\"]/ancestor::a[not(contains(@class,'active'))]".format(device_name))
    
    
class CreateDeviceGroupDialog(DialogBase):
    """
    @description: This is page object class for Create Device Group Dialog. You need to init it before using in page class.
    @page: Create Device Group Dialog
    @author: Thanh Le
    """
    
    
    """    Properties    """   
    @property
    def _txtGroupName(self):
        return Element(self._driver, *_CreateDeviceGroupDlgLocator._txtGroupName)
    @property
    def _btnChooseDevices(self):
        return Element(self._driver, *_CreateDeviceGroupDlgLocator._btnChooseDevices)
    @property
    def _txtSearchBeams(self):
        return Element(self._driver, *_CreateDeviceGroupDlgLocator._txtSearchBeams)
    
    def _lnkDeviceToChoose(self, device_name):
        return Element(self._driver, *_CreateDeviceGroupDlgLocator._lnkDeviceToChoose(device_name))
    
    
    """    Methods    """   
    def __init__(self, driver):        
        """      
        @summary: Constructor method 
        @param driver: web driver
        @author: Thanh Le         
        """
        DialogBase.__init__(self, driver)
    
    
    def _select_a_device(self, device_name):
        """      
        @summary: Select a device by device name 
        @param device_name: name of device would like to select
        @return: CreateDeviceGroupDialog
        @author: Thanh Le
        """
        self._txtSearchBeams.wait_until_displayed().type(device_name)
        self._wait_for_loading_completed()
        self._lnkDeviceToChoose(device_name).wait_until_clickable().click_element()
        if self._lnkDeviceToChoose(device_name).is_displayed(2):
            self._lnkDeviceToChoose(device_name).click_element()
        return self
    
    
    def submit_device_group_info(self, device_group_name, devices=None, wait_for_completed=True):
        """      
        @summary: Submit information on Create Device Group form         
        @param 
            - device_group_name: name of device group would like to create
            - devices: device to add to device group
            - wait_for_completed: time wait for completing creating device group
        @return: self
        @author: Thanh Le
        """
        self._txtGroupName.wait_until_displayed().type(device_group_name)
        if(devices != None):
            self._btnChooseDevices.click()
            self._wait_for_loading_completed()
            
            for device_name in devices:
                self._select_a_device(device_name)
            
        self.submit(wait_for_completed)
        return self
    