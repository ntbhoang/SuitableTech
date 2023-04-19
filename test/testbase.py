import unittest
from core.webdriver.drivers.driver import Driver
from core.utilities.test_condition import TestCondition
from core.webdriver.drivers.driversetting import DriverSetting
from sauceclient import SauceClient
from common.constant import Constant, Platform
import os

class TestBase(unittest.TestCase):
    
    def setUp(self):
        self._driver = Driver.get_driver(DriverSetting.load(), self._testMethodName)
        self._driver.maximize_window()
        self._driver.tc_name = self._testMethodName
        self.maxDiff = None
        self.passed = True
        
    
    def tearDown(self):
        TestCondition.force_log_out(self._driver)
        if self._driver._driverSetting.run_locally == False:
            if self._driver._driverSetting.remote_type == Constant.SauceLabs:
                if "traceback object at" in str(self._outcome.errors):
                    self.passed = False
                self.sauce_client = SauceClient(Constant.SauceLabsAuth['User'], Constant.SauceLabsAuth['Access Key'])
                if self.passed:
                    self.sauce_client.jobs.update_job(self._driver._driver.session_id, passed=True) 
                else:
                    self.sauce_client.jobs.update_job(self._driver._driver.session_id, passed=False)
        self._driver.quit()
        
        
    def assertTrue(self, expr, msg):
        try:
            unittest.TestCase.assertTrue(self, expr)
        except:
            self._driver.save_screenshot()
            self.passed = False
            self.fail(msg)
    
    
    def assertFalse(self, expr, msg):
        try:
            unittest.TestCase.assertFalse(self, expr)
        except:
            self._driver.save_screenshot()
            self.passed = False
            self.fail(msg)
            
    
    def assertEqual(self, first, second, msg):
        try:
            unittest.TestCase.assertEqual(self, first, second)
        except:
            print(first)
            print(second)
            self._driver.save_screenshot()
            self.passed = False
            self.fail(msg)
            
    
    def assertNotEqual(self, first, second, msg):
        try:
            unittest.TestCase.assertNotEqual(self, first, second)
        except:
            self._driver.save_screenshot()
            self.passed = False
            self.fail(msg)
            
    
    def assertIn(self, member, container, msg):
        try:
            unittest.TestCase.assertIn(self, member, container)
        except:
            self._driver.save_screenshot()
            self.passed = False
            self.fail(msg)
            
    
    def assertNotIn(self, member, container, msg):
        try:
            unittest.TestCase.assertNotIn(self, member, container, msg)
        except:
            self._driver.save_screenshot()
            self.sauce_client.jobs.update_job(self._driver._driver.session_id, passed=False) 
            self.fail(msg)
    
    
    def delete_temporary_files (self):
        if self._driver._driverSetting.run_locally == True and self._driver.driverSetting.platform == Platform.WINDOWS:
            tmp = os.environ.get("TMP")
            if tmp:
                for f in os.listdir(tmp):
                    name = os.path.join(tmp, f)
                    try:
                        if os.path.isfile(name):
                            os.remove(name)
                        elif os.path.isdir(name):
                            import shutil
                            shutil.rmtree(name)                            
                        else:
                            #os.rmdir(name) # to only remove empty directories.
                            # To remove the directory and all of its contents.
                            os.removedirs(name)                                                                          
                    except OSError:
                        # Specific exception handling could be done based on the 'errno'.
                        pass # skip files that are in use on Windows or otherwise cannot be removed.
        
            
    @staticmethod
    def is_html_tag_in_string(text):
        import re
        matches = re.search("/<[^<]+>/", text)
        return matches
        
if __name__ == "__main__":
    unittest.main()
