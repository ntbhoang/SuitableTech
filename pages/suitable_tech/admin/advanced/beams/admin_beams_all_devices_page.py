from selenium.webdriver.common.by import By
from common.application_constants import ApplicationConst
from core.webdriver.elements.dropdownlist import DropdownList
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_list import ElementList
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from time import sleep
from common.constant import Browser, Platform
from dateparser import parse


class _AdminBeamsAllDevicePageLocator(object):
    _btnCreateDeviceGroup = (By.XPATH, "//div[@class='row secondary-nav']//button[@ng-click='createDeviceGroup()' and @type='button']")
    _btnCreateDeviceGroupInAllBeams = (By.XPATH, "//div[@class='dropdown header-buttons device-group-dropdown open']//button[@ng-click='createDeviceGroup()']")
    _iconIconView = (By.XPATH, "//span[@class='glyphicon glyphicon-th-large']/..")
    _iconListView = (By.XPATH, "//span[@class='glyphicon glyphicon-th-list']/..")
    _txtSearchBeams = (By.XPATH, "//input[@type='search']")
    _lblOffline = (By.XPATH, "//div[@class='text-muted']/span[2]")
    _lblAvailable = (By.XPATH, "//div[@class='text-success']/span[2]")
    _btnAddDevices = (By.XPATH, "//button[@type='button' and @ng-click='addDevices()']")
    _cbxAllBeams = (By.XPATH,"//div[contains(@class,'device-group-dropdown')]/button[@aria-haspopup='true' and @aria-expanded='false']")

    """Device Profile Card"""
    _lstDeviceName = (By.XPATH, "//div[contains(@class,'profile-title')]/*[1]")
    _lstDeviceGroupName = (By.XPATH, "//div[contains(@class,'profile-title')]/span/a")
    _lstStatus = (By.XPATH, "//div[@ng-class='device.stateColor()']//span[@class='ng-binding']")
    _lstLocation = (By.XPATH, "//span[@ng-show='device.location']")
    _lstLastUsed = (By.XPATH, "//span[@ng-show='device.last_call']")

    '''Mobile UI'''
    _btnMCreateDeviceGroup = (By.XPATH, "//div[@class='btn-group']//button[@ng-click='createDeviceGroup()']")
    _cbxMAllBeams = (By.XPATH,"//div[contains(@class,'group dropdown header')]/button[@aria-haspopup='true' and @aria-expanded='false']")

    @staticmethod
    def _lstDeviceGroups():
        return (By.XPATH, u"//h4[.=\"{}\"]/../..//div[@class='gallery-item ng-scope']".format(ApplicationConst.LBL_DEVICE_GROUPS))
    @staticmethod
    def _imgDeviceGroupIcon(device_group_name):
        return (By.XPATH,u"//div[@for='deviceGroup']//div[.=\"{}\"]/preceding-sibling::div//img".format(device_group_name))
    @staticmethod
    def _lnkDeviceGroup(device_group_name):
        return (By.XPATH, u"//div[@class='profile-title ng-binding' and .=\"{}\"]/..".format(device_group_name))
    @staticmethod
    def _lnkFirstDeviceGroup(device_group_name):
        return (By.XPATH, u"(//div[@for='deviceGroup'])[1]//div[.=\"{}\"]/..".format(device_group_name))
    @staticmethod
    def _lnkDevice(device_name):
        return (By.XPATH, u"//a[.=\"{}\" and @class='ng-binding ng-scope']".format(device_name))
    @staticmethod
    def _lnkFirstDevice(device_name):
        return (By.XPATH, u"(//div[@for='device'])[1]//a[.=\"{}\"]".format(device_name))
    @staticmethod
    def _lnkDeviceID(device_id):
        return (By.XPATH, u"//div[@class='profile-title']//a[contains(@href,'{}')]".format(device_id))

class AdminBeamsAllDevicesPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam All Devices page.
        This page will be opened after clicking Beams tab on Dashboard page.
        From this page, user can view all device or device group. 
        Please visit https://staging.suitabletech.com/manage/#/beams/all/ for more details.
    @page: Beam All Devices page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _btnCreateDeviceGroup(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._btnCreateDeviceGroup)
    
    @property
    def _btnMCreateDeviceGroup(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._btnMCreateDeviceGroup)
    
    @property
    def _btnCreateDeviceGroupInAllBeams(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._btnCreateDeviceGroupInAllBeams)
    @property
    def _cbxDeviceGroup(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._cbxDeviceGroup)
    @property
    def _txtSearchBeams(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._txtSearchBeams)
    @property
    def _lstDeviceGroups(self):
        return ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lstDeviceGroups())
    @property
    def _iconIconView(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._iconIconView)
    @property
    def _iconListView(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._iconListView)
    @property
    def _btnAddDevices(self):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._btnAddDevices)
    @property
    def _cbxAllBeams(self):
        return DropdownList(self._driver, *_AdminBeamsAllDevicePageLocator._cbxAllBeams)
    @property
    def _cbxMAllBeams(self):
        return DropdownList(self._driver, *_AdminBeamsAllDevicePageLocator._cbxMAllBeams)

    """Device Profile Card"""
    @property
    def _lstDeviceName(self):
        return ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lstDeviceName)
    @property
    def _lstDeviceGroupName(self):
        return ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lstDeviceGroupName)
    @property
    def _lstStatus(self):
        return ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lstStatus)
    @property
    def _lstLocation(self):
        return ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lstLocation)
    @property
    def _lstLastUsed(self):
        return ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lstLastUsed)

    def _lnkDeviceGroup(self, device_group_name):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._lnkDeviceGroup(device_group_name))
    def _lnkFirstDeviceGroup(self, device_group_name):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._lnkFirstDeviceGroup(device_group_name))
    def _lnkDevice(self, device_name):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._lnkDevice(device_name))
    def _lnkFirstDevice(self, device_name):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._lnkFirstDevice(device_name))
    def _imgDeviceGroupIcon(self, device_group_name):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._imgDeviceGroupIcon(device_group_name))
    def _lnkDeviceID(self, device_id):
        return Element(self._driver, *_AdminBeamsAllDevicePageLocator._lnkDeviceID(device_id))

    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web driver
        @author: Thanh le      
        @created_date: August 08, 2016
        """
        AdminBeamsCommonPage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        self.wait_for_loading()
        
        
    def is_add_devices_button_display(self):
        """      
        @summary: check Add Devices button     
        @author: Thanh le      
        @created_date: March 09, 2017
        """
        return self._btnAddDevices.is_displayed()
    
    
    def create_new_device_group(self, device_group_name, devices=None, wait_for_completed=True):
        """      
        @summary: Create new device group         
        @param device_group_name: name of device group would like to create
        @param devices: Beam device would like to add to device group
        @param wait_for_completed: wait for the 'Create Device Group' form completely submitted
        @return: AdminBeamsDevicesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        
        self.click_create_device_group_button()
        
        from pages.suitable_tech.admin.dialogs.create_device_group import CreateDeviceGroupDialog
        create_device_group_dialog = CreateDeviceGroupDialog(self._driver)
   
        if not create_device_group_dialog.is_dialog_displayed():
            self.click_create_device_group_button(True)
            
        create_device_group_dialog.submit_device_group_info(device_group_name, devices, wait_for_completed)
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
        
        from pages.suitable_tech.admin.advanced.beams.admin_beams_devices_page import AdminBeamsDevicesPage
        return AdminBeamsDevicesPage(self._driver, wait_for_completed)
    
    
    def click_create_device_group_button(self, js=False):
        """
        @summary: Click on '+ Create Device Group' button
        @author: Thanh Le
        @return: Admin beams all devices page
        @created_date: August 08, 2016
        """
        
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_all_beams_dropdown()
            self._btnMCreateDeviceGroup.wait_until_displayed()
            self._btnMCreateDeviceGroup.wait_until_clickable().click()
        else:
            self._btnCreateDeviceGroup.wait_until_displayed()
            if js:
                self._driver.execute_script("$('.btn.btn-default.pull-right.ng-scope').click();")
            else:
                self._btnCreateDeviceGroup.wait_until_clickable().click()
            
        return self

    
    def is_device_group_existed(self, device_group_name, wait_time_out=None):
        """      
        @summary: Check if a device group is existed or not   
        @param device_group_name: name of device group would like to check
        @param wait_time_out: time out to wait for device group is displayed
        @return: True: The device group is existed, False: The device group is not existed
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self.search(device_group_name)
        return self._lnkDeviceGroup(device_group_name).is_displayed(wait_time_out)
    
    
    def is_device_group_not_existed(self, device_group_name, wait_time_out=None):
        """      
        @summary: Check if a device group is not existed
        @param device_group_name: name of device group would like to check
        @param wait_time_out: time out to wait for a device group is disappeared
        @return: True: The device group is not existed, False: The device group is existed
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self.search(device_group_name)
        return self._lnkDeviceGroup(device_group_name).is_disappeared(wait_time_out)
    
    
    def select_a_device(self, device_name):
        """      
        @summary: Select a device
        @param device_name: name of device would like to select
        @return: Admin Beam Detail Page
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self.search(device_name)
        sleep(2)
        self._lnkDevice(device_name).click_element()
        self.wait_for_loading()
        if self._lnkDevice(device_name).is_displayed(5):
            self._lnkDevice(device_name).jsclick()
        from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage
        return AdminBeamDetailPage(self._driver, device_name)


    def goto_beam_details_page_by_id(self, device_id):
        """      
        @summary: Select a device
        @param device_name: name of device would like to select
        @return: Admin Beam Detail Page
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        beamname = self._lnkDeviceID(device_id).text
        self._lnkDeviceID(device_id).wait_until_displayed()
        lnk = self._lnkDeviceID(device_id).get_attribute('href')
        self._driver.get(lnk)
        self._lnkDeviceID(device_id).wait_until_disappeared()
        from pages.suitable_tech.admin.advanced.beams.admin_beam_detail_page import AdminBeamDetailPage
        return AdminBeamDetailPage(self._driver, beamname)
    
    
    def select_device_group(self, device_group_name):
        """      
        @summary: Select a device group   
        @param device_group_name: name of device group would like to select 
        @return: AdminBeamsDevicesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self.search(device_group_name)
        self._lnkFirstDeviceGroup(device_group_name).wait_until_clickable().jsclick()     
        if(self._driver._driverSetting.browser_name == Browser.Safari):
            sleep(2)    
        from pages.suitable_tech.admin.advanced.beams.admin_beams_devices_page import AdminBeamsDevicesPage
        return AdminBeamsDevicesPage(self._driver)
    
    
    def get_device_group_icon_url(self, device_group_name):
        """      
        @summary: Get url of device group icon        
        @param device_group_name: name of device would like to get url of icon
        @return: url of device group icon
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self.search(device_group_name)
        image_element = self._imgDeviceGroupIcon(device_group_name)
        image_element.wait_until_displayed()
        
        return image_element.get_attribute("src")
    
    
    def remove_all_device_groups(self, keyword = "LGVN Group"):
        """      
        @summary: Remove all created device groups 
        @param keyword: criteria for removing device group
        @return: AdminBeamsDevicesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self.search(keyword)
        self.wait_for_loading()
        lst_device_group_cards = self._lstDeviceGroups
        count = lst_device_group_cards.count()
        while(count > 0):
            for i in range(0, count):
                web_elem = lst_device_group_cards.get_element_at(i)
                if web_elem and web_elem.text:
                    web_elem.click()
                    from pages.suitable_tech.admin.advanced.beams.admin_beams_devices_page import AdminBeamsDevicesPage
                    AdminBeamsDevicesPage(self._driver).goto_setting_tab().delete_device_group()
            
            self.search(keyword)
            self.wait_for_loading()
            lst_device_group_cards = self._lstDeviceGroups
            count = lst_device_group_cards.count()
        
        return self
    
    
    def switch_to_icon_view(self):
        """      
        @summary: Switch to icon view mode
        @return: AdminBeamsDevicesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._iconIconView.wait_until_clickable().click()
        return self
    
    
    def switch_to_list_view(self):
        """      
        @summary: Switch to list view mode
        @return: AdminBeamsDevicesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._iconListView.wait_until_clickable().click()
        return self
    
    
    def search(self, search_item):
        """      
        @summary: Search for a Beam 
        @param search_item: keyword used for search
        @return: Beam device matched with searched keyword
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._txtSearchBeams.type(search_item)
        self.wait_for_loading()
        return self
    
    
    def _get_device_status_list(self):
        """      
        @summary: Get device status
        @return: List of device status
        @author: Thanh Le 
        @created_date: March 10, 2017        
        """        
        offline_list = ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lblOffline).get_all_elements()
        available_list = ElementList(self._driver, *_AdminBeamsAllDevicePageLocator._lblAvailable).get_all_elements()
        
        device_status_list = []
        for i in offline_list:
            device_status_list.append(i.text)
            
        for j in available_list:
            device_status_list.append(j.text)
            
        return device_status_list
            
    
    def are_offline_available_text_localized(self):
        """      
        @summary: Are offline and available text localized
        @language: Language is selected
        @return: True if the text is localized
                 False if the text is not localized
        @author: Thanh Le 
        @created_date: March 10, 2017        
        """
        device_status_list = self._get_device_status_list()
        for i in device_status_list:
            if i != ApplicationConst.LBL_BEAM_OFFLINE_STATUS and i != ApplicationConst.LBL_BEAM_AVAILABLE_STATUS:
                return False
        return True


    def is_create_device_group_button_display(self):
        """
        @summary: check Create Device Group button displays or not
        @author: Khoi Ngo
        @created_date: Oct 23, 2017
        """
        return self._btnCreateDeviceGroup.is_displayed()


    def open_all_beams_dropdown(self):
        """
        @summary: open All Beams dropdown menu
        @author: Khoi Ngo
        @created_date: Oct 23, 2017
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._cbxMAllBeams.click()
        else:
            self._cbxAllBeams.click()
        return self


    def is_create_device_group_button_in_all_beams_display(self):
        """
        @summary: check Create Device Group button displays or not
        @author: Khoi Ngo
        @created_date: Oct 23, 2017
        """
        return self._btnCreateDeviceGroupInAllBeams.is_displayed()


    def is_device_displayed(self, device_name):
        """
        @summary: Check if a device is displayed or not
        @param device_name: name of device would like to check
        @return: Admin Beam Detail Page
        @author: Khoi Ngo
        @created_date: Oct 24, 2017
        """
        return self._lnkDevice(device_name).is_displayed()


    def check_table_devices_can_sort(self):
        """
        @summary: Check table can sort with each label
        @return: True if table can sort with all label when click for each, Fail if table can not sort
        @author: Khoi Ngo
        @created_date: Oct 30, 2017
        """
        xpath_table = "//div[@class='gallery-group']//h4[@class='gallery-group-title ng-scope']/../following-sibling::table"
        return self.check_sort_table_work(xpath_table)


    def get_device_sort_by_data_list(self, sort_by):
        """
        @summary: Get list of device sorting by
        @return: list of data
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """

        if sort_by == "name":
            elements = self._lstDeviceName.get_all_elements()

        elif sort_by == "devicegroup":
            elements = self._lstDeviceGroupName.get_all_elements()

        elif sort_by == "location":
            elements = self._lstLocation.get_all_elements()

        elif sort_by == "status":
            elements = self._lstStatus.get_all_elements()

        elif sort_by == "lastused":
            elements = self._lstLastUsed.get_all_elements()

        data_list=[]
        for i in range (len(elements)):
            if sort_by == "status":   
                data = elements[i].text
            
            elif sort_by == "lastused":
                data = elements[i].text
                if data == "":
                    continue
                else:
                    data = parse(parse(data).strftime('%m %d %y'))
            
            else:
                data = elements[i].text.lower()
            
            

            data_list.append(data)

        return data_list


    def check_sort_by_work_correctly(self):

        btn_sort_by_xpath = "//div[@is-open='sortDropdownOpen']/button"
        return self.check_sort_by_work(btn_sort_by_xpath, page= "Beams")
