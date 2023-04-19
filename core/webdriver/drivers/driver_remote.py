from common.constant import Browser, Remote_Type, Platform
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from core.webdriver.drivers.desired_capabilities import BrowserStackDesiredCapabilities,\
    SauceLabsDesiredCapabilities
from common.helper import Helper


class Driver_Remote():
    grid_platform_cap_info = [{"platformKey": Platform.WINDOWS, "platformValue": "WINDOWS"},
                              {"platformKey": Platform.MAC, "platformValue": "MAC"},
                              {"platformKey": Platform.ANY, "platformValue": "ANY"}]
    
    
    browserstack_platform_cap_info = [{"platformKey": Platform.WINDOWS, "platformValue": "Windows"},
                                      {"platformKey": Platform.MAC, "platformValue": "OS X"},
                                      {"platformKey": Platform.ANY, "platformValue": "Not supported"}]

    
    saucelabs_platform_cap_info = [{"platformKey": Platform.WINDOWS, "platformValue": "Windows"},
                                      {"platformKey": Platform.MAC, "platformValue": "OS X"},
                                      {"platformKey": Platform.ANY, "platformValue": "Not supported"}]

    @staticmethod
    def get_driver(driverSetting, tc_name = None):
        """
        @Author: Thanh Le
        get driver based on data setting data
        :param driverSetting:
        :return:
        """

        desired_cap = Driver_Remote.get_desired_cap(driverSetting, tc_name)
        _driver = webdriver.Remote(command_executor=driverSetting.hub_url, desired_capabilities=desired_cap)
        return _driver
    
    @staticmethod
    def get_desired_cap(driverSetting, name = None):
        """
        @Author: Thanh Le
        get desired capabilities based on setting data
        :param driverSetting:
        :return:
        """

        desired_cap = None
        root_desired_cap = None
        
        #Get Base Cap
        if driverSetting.remote_type == Remote_Type.GRID:
            root_desired_cap = DesiredCapabilities
        elif driverSetting.remote_type == Remote_Type.BROWSERSTACK:
            root_desired_cap = BrowserStackDesiredCapabilities
        elif driverSetting.remote_type == Remote_Type.SAUCELABS:
            root_desired_cap = SauceLabsDesiredCapabilities
        
        #Get Browser Cap
        if driverSetting.browser_name == Browser.Firefox:
            desired_cap = root_desired_cap.FIREFOX.copy()
        elif driverSetting.browser_name == Browser.IE:
            desired_cap = root_desired_cap.INTERNETEXPLORER.copy()
        elif driverSetting.browser_name == Browser.Edge:
            desired_cap = root_desired_cap.EDGE.copy()
        elif driverSetting.browser_name == Browser.Safari:
            desired_cap = root_desired_cap.SAFARI.copy()
        elif driverSetting.browser_name == Browser.Chrome:
            desired_cap = root_desired_cap.CHROME.copy()
        
        #Configure to match expected settings
        if driverSetting.remote_type == Remote_Type.GRID:
            desired_cap['platform'] = Helper.get_dict_value(Driver_Remote.grid_platform_cap_info, "platformKey", driverSetting.platform, "platformValue")
        elif driverSetting.remote_type == Remote_Type.BROWSERSTACK:
            desired_cap['os'] = Helper.get_dict_value(Driver_Remote.browserstack_platform_cap_info, "platformKey", driverSetting.platform, "platformValue")
        elif driverSetting.remote_type == Remote_Type.SAUCELABS:
            desired_cap['platform'] = Helper.get_dict_value(Driver_Remote.saucelabs_platform_cap_info, "platformKey", driverSetting.platform, "platformValue") + " " + driverSetting.platform_version
            desired_cap['idleTimeout'] = 180
            if name is not None: 
                desired_cap['name'] = name
                
                
        return desired_cap
