import os
from selenium import webdriver
from common.constant import Browser
from common.helper import Helper


class Driver_MAC():
    executable_path = Helper.base_dir() + "/libs/remote_execution/"
        
    @staticmethod
    def get_driver(driverSetting):    
        """
        @Author: return driver based on data setting
        :param driverSetting:
        :return:
        """

        if driverSetting.browser_name == Browser.Firefox:
            file_path = Driver_MAC.executable_path + "geckodriver"
            return webdriver.Firefox(executable_path=file_path)
        elif driverSetting.browser_name == Browser.Safari:
            return webdriver.Safari()
        elif driverSetting.browser_name == Browser.Chrome:
            file_path = Driver_MAC.executable_path + "macchromedriver"
            options = webdriver.ChromeOptions()
            options.add_argument("--kiosk")
            options.add_argument("--safebrowsing-disable-download-protection")
            dir_name = Helper.base_dir() + "/data/download"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            prefs = {"download.default_directory": dir_name, "download.prompt_for_download": False, "safebrowsing.enabled": "true"}
            options.add_experimental_option("prefs", prefs)
            return webdriver.Chrome(executable_path=file_path, chrome_options=options)
        
        return None 