import os
from selenium import webdriver
from common.constant import Browser, Platform
from common.helper import Helper
from selenium.webdriver.chrome.options import Options


class Driver_Windows():
    executable_path = Helper.base_dir() + "\\libs\\remote_execution\\".replace("\\", os.path.sep)
    dir_name = Helper.base_dir() + "\\data_test\\download"

    @staticmethod
    def get_driver(driverSetting):
        _driver = None
        if not os.path.exists(Driver_Windows.dir_name):
            os.makedirs(Driver_Windows.dir_name)
        
        if driverSetting.browser_name == Browser.Firefox:
            file_path = Driver_Windows.executable_path + "geckodriver-v0.17.0.exe"
            firefox_option = webdriver.FirefoxProfile()
            firefox_option.set_preference("browser.tabs.remote.autostart.2", False)
            #Hide download dialog and set dir for file dowloaded 
            firefox_option.set_preference('browser.download.folderList', 2) 
            firefox_option.set_preference('browser.download.manager.showWhenStarting', False)
            firefox_option.set_preference('browser.download.dir', Driver_Windows.dir_name)
            firefox_option.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')            
            _driver = webdriver.Firefox(firefox_option, executable_path=file_path)
            
        elif driverSetting.browser_name == Browser.IE:
            file_path = Driver_Windows.executable_path + "IEDriverServer.exe"
            _driver = webdriver.Ie(file_path)
            
        elif driverSetting.browser_name == Browser.Safari:
            _driver = webdriver.Safari()
            
        elif driverSetting.browser_name == Browser.Chrome:
            file_path = Driver_Windows.executable_path + "chromedriver.exe"
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-logging")
            #Hide download dialog and set dir for file dowloaded 
            prefs = {"download.default_directory": Driver_Windows.dir_name, "download.prompt_for_download": False, "safebrowsing.enabled": "false", "credentials_enable_service": False}
            chrome_options.add_experimental_option("prefs", prefs)
            if driverSetting.platform == Platform.ANDROID:
                chrome_options.add_experimental_option("mobileEmulation", driverSetting.mobile_emulation)
            _driver = webdriver.Chrome(file_path, chrome_options=chrome_options)
            
        elif driverSetting.browser_name == Browser.Edge:
            file_path = Driver_Windows.executable_path + "MicrosoftWebDriver.exe"
            _driver = webdriver.Edge(file_path)
            _driver.desired_capabilities['elementScrollBehavior'] = '1'
            
        return _driver

