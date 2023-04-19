from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By
from core.webdriver.elements.element_list import ElementList
from common.constant import Language, Platform
from time import sleep
from builtins import staticmethod


class _AdminActivityPageLocator(object):
    _lblHeader = (By.XPATH, "//div[@class='row secondary-nav']//h3")
    _lblSummary = (By.XPATH, "//div[@ng-controller='ActivityTimelineCtrl']//p[@translate-n='numPilots']")
    _btnRangeDate = (By.XPATH, "//button[@options='datepickerOptions']")
    _txtStartDate = (By.XPATH, "//div[contains(@style,'display: block')]//input[@name='daterangepicker_start']")
    _txtEndDate = (By.XPATH, "//div[contains(@style,'display: block')]//input[@name='daterangepicker_end']")
    _btnApply = (By.XPATH, "//div[contains(@style,'display: block')]//button[@class='applyBtn btn btn-sm btn-success']")
    _btnStatus = (By.XPATH, "//div[contains(@class,'secondary-content')]//button[@class='btn btn-default dropdown-toggle']")
    _txtSearch = (By.CSS_SELECTOR, "input[type='search']")
    _lnkCustomRange = (By.XPATH, "//div[contains(@style,'display: block')]//div[@class='ranges']//ul//li[last()]")
    _lstStatusState = (By.XPATH, "//div[contains(@class,'secondary-content')]//li[contains(@class,'select-item')]")
    _btnExportCSV = (By.CSS_SELECTOR, "button[ng-click='exportCsv()']")
    _iconLoading = (By.CSS_SELECTOR, '.fa.fa-2x.fa-spin.fa-circle-o-notch')
    _lstActivityItem = (By.CSS_SELECTOR, '.item-title')
    _iconActivityItem = (By.XPATH, "(//div[@class='item-title']/../..)[1]")
    _tooltipActivity = (By.XPATH, "//div[@class='tooltip-inner ng-binding']/div")

    '''Mobile UI'''
    _lblMSummary = (By.XPATH, "//div[@ng-show='!devices.length']/div[@class='col-xs-10']")
    _btnMRangeDate = (By.XPATH, "//div[@class='row filters']//button[@options='datepickerOptions']")
    _lstMStatusState = (By.XPATH, "//div[contains(@class,'activity-timeline-mobile')]//li[contains(@class,'select-item')]")
    _btnMStatus = (By.XPATH, "//div[contains(@class,'activity-timeline-mobile')]//button[@class='btn btn-default dropdown-toggle']")
    _lstMSelectDevice = (By.XPATH, "(//div[@ng-click='selectDevice(device)'])")
    _btnMBackToDevices = (By.XPATH, "//div[@ng-click='backToDevices()']")
    _lstMActivityItem = (By.XPATH, "//div[@ng-repeat='activityGroup in deviceActivities']/div[contains(@class,'item')]")
    _iconMLoading = (By.XPATH, "//span[@class='fa fa-spin fa-circle-o-notch']")
    
    @staticmethod
    def _lstSelectedActivity(status):
        return (By.XPATH, u"//div[@class='foreground']//div[@class='group']/div[contains(@class,'{}')]".format(status))

    @staticmethod
    def _lstMSelectedActivity(status):
        return (By.XPATH, u"//div[contains(@class,'activity-timeline-mobile')]//div[contains(@class,'{}')]".format(status))

    @staticmethod
    def _itemStatus(index):
        return (By.XPATH, "//div[contains(@class,'secondary-content')]//li[{}]".format(index + 1))

class AdminActivityPage(AdminTemplatePage):
    """
    @description: This is page object class for Admin Activity page.
        This page will be opened after clicking Activity tab on Dashboard page.
        Please visit https://staging.suitabletech.com/manage/#/activity/ for more details.
    @page: Admin Activity page
    @author: Thanh Le
    """
    
    """    Properties """
    @property
    def _tooltipActivity(self):
        return Element(self._driver, *_AdminActivityPageLocator._tooltipActivity)
    @property
    def _iconActivityItem(self):
        return Element(self._driver, *_AdminActivityPageLocator._iconActivityItem)
    @property
    def _lblHeader(self):
        return Element(self._driver, *_AdminActivityPageLocator._lblHeader)
    @property
    def _lblSummary(self):
        return Element(self._driver, *_AdminActivityPageLocator._lblSummary)
    @property
    def _lblMSummary(self):
        return Element(self._driver, *_AdminActivityPageLocator._lblMSummary)
    @property
    def _btnRangeDate(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnRangeDate)
    @property
    def _btnMRangeDate(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnMRangeDate)
    @property
    def _txtStartDate(self):
        return Element(self._driver, *_AdminActivityPageLocator._txtStartDate)
    @property
    def _txtEndDate(self):
        return Element(self._driver, *_AdminActivityPageLocator._txtEndDate)
    @property
    def _btnApply(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnApply)
    @property
    def _btnStatus(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnStatus)
    @property
    def _btnMStatus(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnMStatus)
    @property
    def _lstStatusState(self):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstStatusState)
    @property
    def _lstMStatusState(self):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstMStatusState)
    @property
    def _txtSearch(self):
        return Element(self._driver, *_AdminActivityPageLocator._txtSearch)
    @property
    def _lnkCustomRange(self):
        return Element(self._driver, *_AdminActivityPageLocator._lnkCustomRange)
    @property
    def _btnExportCSV(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnExportCSV)
    @property
    def _iconLoading(self):
        return Element(self._driver, *_AdminActivityPageLocator._iconLoading)
    @property
    def _iconMLoading(self):
        return Element(self._driver, *_AdminActivityPageLocator._iconMLoading)
    @property
    def _lstActivityItem(self):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstActivityItem)
    @property
    def _lstMActivityItem(self):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstMActivityItem)
    @property
    def _lstMSelectDevice(self):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstMSelectDevice)
    @property
    def _btnMBackToDevices(self):
        return Element(self._driver, *_AdminActivityPageLocator._btnMBackToDevices)
    def _lstSelectedActivity (self, status):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstSelectedActivity(status))
    def _lstMSelectedActivity (self, status):
        return ElementList(self._driver, *_AdminActivityPageLocator._lstMSelectedActivity(status))
    def _itemStatus (self, index):
        return Element(self._driver, *_AdminActivityPageLocator._itemStatus(index))

    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method
        @param driver: web driver
        @author: Thanh Le
        @created_date: August 05, 2016
        """     
        AdminTemplatePage.__init__(self, driver)
#         self._lblHeader.wait_until_displayed()
    
    
    def get_summary_text(self):
        """      
        @summary: Get summary label
        @param driver: web driver
        @author: Thanh Le
        @created_date: March 13, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:   
            self._lblMSummary.wait_until_displayed()
            return self._lblMSummary.text
        else:
            self._lblSummary.wait_until_displayed()
            return self._lblSummary.text
    
    
    def search_activity(self, date_range=False, status=False, keyword=False, export_csv=False):
        if date_range:
            if self._driver._driverSetting.language == Language.ENGLISH:
                from_date = date_range['from_date']['mm'] + '/' + date_range['from_date']['dd'] + '/' + date_range['from_date']['yyyy']
                to_date = date_range['to_date']['mm'] + '/' + date_range['to_date']['dd'] + '/' + date_range['to_date']['yyyy']
            elif self._driver._driverSetting.language == Language.FRENCH:
                from_date = date_range['from_date']['dd'] + '/' + date_range['from_date']['mm'] + '/' + date_range['from_date']['yyyy']
                to_date = date_range['to_date']['dd'] + '/' + date_range['to_date']['mm'] + '/' + date_range['to_date']['yyyy']
            else:
                from_date = date_range['from_date']['yyyy'] + '/' + date_range['from_date']['mm'] + '/' + date_range['from_date']['dd']
                to_date = date_range['to_date']['yyyy'] + '/' + date_range['to_date']['mm'] + '/' + date_range['to_date']['dd']

            if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
                self._btnMRangeDate.click()
            else:
                self._btnRangeDate.click()
            self._lnkCustomRange.click()
            self._txtStartDate.type(from_date)
            self._txtEndDate.type(to_date)
            self._btnApply.click()
            
        if status:
            self.click_status_dropdown()
            all_elements = self._lstStatusState.get_all_elements()
            for i in range(len(all_elements)):
                if((all_elements[i].get_attribute('class') == 'select-item') and (all_elements[i].text.strip() in status))\
                    or ((all_elements[i].get_attribute('class') == 'select-item selected') and (all_elements[i].text.strip() not in status)):
                    all_elements[i].click()
                    self._iconLoading.wait_until_disappeared(20)
                    self.click_status_dropdown()
        
        if keyword:      
            self._txtSearch.type(keyword)
            
        self._iconLoading.wait_until_disappeared(20)
        
        if export_csv:
            self._btnExportCSV.click()
            
        return self
            
            
    def get_list_activity_items(self):

        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            all_select_devices = self._lstMSelectDevice.get_all_elements()
            len_activity = 0
            for i in range (len(all_select_devices)):
                self._lstMSelectDevice.get_element_at(i).click()
                all_activity = len(self._lstMActivityItem.get_all_elements())
                len_activity = len_activity + all_activity
                self._btnMBackToDevices.click()
            return len_activity
        else:
            all_activity_items = self._lstActivityItem.get_all_elements()
        return len(all_activity_items)
    
    
    def click_activity_item(self):                
        items = self._lstActivityItem.get_all_elements()
        if len(items) > 0:
            sleep(2)
            self._iconActivityItem.wait_until_clickable().click()
        else:
            print("There is no activity item to click")
        return self
    

    def get_content_tooltip_displays(self):
        """
        @summary: Check if tooltip displays
        @author: Thanh Le
        @return: True if tooltip displays, False for vice versa
        """ 
        return self._tooltipActivity.text


    def _get_list_of_selected_activity (self, status):
        
        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            all_select_devices = self._lstMSelectDevice.get_all_elements()
            len_selected_activity = 0
            for i in range (len(all_select_devices)):
                self._lstMSelectDevice.get_element_at(i).click()
                all_selected_activity = len(self._lstMSelectedActivity(status).get_all_elements())
                len_selected_activity = len_selected_activity + all_selected_activity
                self._btnMBackToDevices.click()
            return len_selected_activity
        else:
            selected_activity = self._lstSelectedActivity(status).get_all_elements()
            return len(selected_activity)


    def click_status_dropdown (self):
        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            return self._btnMStatus.click()
        else:
            return self._btnStatus.click()


    def _select_status(self, index):
        if self._driver.driverSetting.platform == Platform.ANDROID or self._driver.driverSetting.platform == Platform.IOS:
            all_status_elements = self._lstMStatusState.get_all_elements()
            all_status_elements[index].click()
            self._iconMLoading.wait_until_disappeared(10)   
        else:
            self._lstStatusState.click(index)
            self._iconLoading.wait_until_disappeared(10)
        return self


    def check_activity_status_work_correctly(self, date_range):

        self.search_activity(date_range=date_range, status=False, keyword=False, export_csv=False)
        all_status_elements = self._lstStatusState.get_all_elements()
        check_status = True
        for item in range (len(all_status_elements)):
            item_attribute = all_status_elements[item].get_attribute('ng-class')
            status = item_attribute[20:].replace("}", "")

            selected_items = self._get_list_of_selected_activity(status)
            total_items = self.get_list_activity_items()
            
            if selected_items != total_items:
                check_status = False
                return check_status

            # select the next status and de-select the check status
            if item != (len(all_status_elements) - 1):
                for index in (item + 1, item):
                    self.click_status_dropdown()
                    self._select_status(index)

                selected_items = self._get_list_of_selected_activity(status)
                if selected_items != 0:
                    check_status = False
                    return check_status

            else:  # for last status item
                for index in (item, item - 1):
                    self.click_status_dropdown()
                    self._select_status(index)

                selected_items = self._get_list_of_selected_activity(status)
                if selected_items != 0:
                    check_status = False
                    return check_status
                break

        return check_status
