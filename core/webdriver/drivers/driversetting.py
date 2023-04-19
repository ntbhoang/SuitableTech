import os
import json
from common.constant import Browser
import threading
from common.stopwatch import Stopwatch

RLOCK = threading.RLock()
LOAD_SETTING_TIMEOUT = 60


class DriverSetting(object):
    
    def __init__(self):
        self.browser_name = None
        self.browser_version = None
        self.platform = None
        self.platform_version = None
        self.element_wait_timeout = None
        self.page_wait_timeout = None
        self.email_wait_timeout = None
        self.language = None
        self.run_locally = True
        self.hub_url = None
        self.remote_type = None
        self.mobile_emulation = None

    @staticmethod
    def load():
        with RLOCK:
            from common.helper import Helper
            sw = Stopwatch()
            sw.start()
            driverSetting = DriverSetting()
            # Read execution setting info from ExecutionSetting.json
            data = None
            while not data and sw.elapsed().total_seconds() < LOAD_SETTING_TIMEOUT:
                file_path = Helper.base_dir() + "\\data_test\\setting".replace("\\", os.path.sep)
                file_read = open(file_path + "\\ExecutionSettings.json".replace("\\", os.path.sep), "r")
                data = file_read.read()
                file_read.close()
                
            execution_info = json.loads(data)
            setting_file = open(file_path + os.path.sep + execution_info["environmentFile"], "r")
            data = setting_file.read()
            setting_file.close()
            settings = json.loads(data.replace(r"\n\t", ""))
            
            if settings["browser"].upper() == Browser.IE:
                driverSetting.browser_name = Browser.IE
            else:
                driverSetting.browser_name = settings["browser"].capitalize()
            
            driverSetting.browser_version = settings["browserVerion"]
            driverSetting.platform = settings["platform"].upper()
            driverSetting.platform_version = settings["platformVersion"]
            driverSetting.element_wait_timeout = settings["elementWaitTimeout"]
            driverSetting.page_wait_timeout = settings["pageWaitTimeout"]
            driverSetting.email_wait_timeout = settings["emailWaitTimeout"]
            driverSetting.language = execution_info["language"].upper()
            driverSetting.run_locally = settings["runLocally"]
            driverSetting.remote_type = settings["remoteSetting"]["remote_type"].upper()
            driverSetting.hub_url = settings["remoteSetting"]["hub_url"]
            driverSetting.mobile_emulation = settings["mobileEmulation"]
        
            return driverSetting
