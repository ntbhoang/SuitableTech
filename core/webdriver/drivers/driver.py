from datetime import datetime
import platform
import os

from selenium.common.exceptions import TimeoutException, NoSuchWindowException,\
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from common.constant import Browser, Constant, Language, Platform
from common.helper import Helper, EmailDetailHelper
from common.stopwatch import Stopwatch
from core.webdriver.drivers.driver_mac import Driver_MAC
from core.webdriver.drivers.driver_windows import Driver_Windows
from core.webdriver.drivers.driver_remote import Driver_Remote
POLL_FREQUENCY = 1


class Driver(object):

    @staticmethod
    def get_driver(driverSetting, tc_name = None):
        if driverSetting.browser_name == Browser.Edge:
            return Driver_Edge(driverSetting, tc_name)
        elif driverSetting.browser_name == Browser.Safari:
            return Driver_Safari(driverSetting, tc_name)
        else:
            return Driver(driverSetting, tc_name)
        
       
    _driver = None
    _driverSetting = None
    _tc_name = None
    folder_screen_shot = ""
    sep = os.path.sep
    separator = "                              "
    
    def __init__(self, driverSetting, tc_name = None):
        self._print_action("Open browser")
        self._driverSetting = driverSetting
        if driverSetting.run_locally:  # CREATE LOCAL DRIVER
            if driverSetting.platform == Platform.MAC or driverSetting.platform == Platform.IOS:
                self._driver = Driver_MAC.get_driver(driverSetting)

            if driverSetting.platform == Platform.WINDOWS or driverSetting.platform == Platform.ANDROID:
                self._driver = Driver_Windows.get_driver(driverSetting)
        else:  # CREATE REMOTE DRIVER
            self._driver = Driver_Remote.get_driver(driverSetting, tc_name)
            
        self.set_page_load_timeout(driverSetting.page_wait_timeout)
        try:
            if driverSetting.browser_name != Browser.Safari:
                self.delete_all_cookies()
        except:
            pass
        
        from core.i18n.i18n_support import I18NSupport, I18NLanguage
        # set testing language
        if driverSetting.language == Language.JAPANESE:
            I18NSupport.set_language(I18NLanguage.ja_JP)
        elif driverSetting.language == Language.FRENCH:
            I18NSupport.set_language(I18NLanguage.fr_FR)
        else:
            I18NSupport.set_language(I18NLanguage.default)
            
        EmailDetailHelper.set_language(driverSetting.language)    
                    
        # Update run environment file at data\RunEnv.txt
        self._update_run_env(driverSetting)
        self._tc_name = tc_name


    """ Properties """
    @property
    def wrapped_driver(self):
        return self._driver
    @property
    def title(self):
        self._print_action("Get page title")
        return self._driver.title
    @property
    def current_url(self):
        return self._driver.current_url
    @property
    def window_handles(self):
        return self._driver.window_handles
    @property
    def driverSetting(self):
        return self._driverSetting
    
    """All Web_driver's methods"""
    def _update_run_env(self, driverSetting):
        # Get browser name & version
        machine_name = browser = ""
        
        if driverSetting.run_locally:
            machine_name = platform.node();
            browser = driverSetting.browser_name + ", version " + driverSetting.browser_version
        else:
            machine_name = driverSetting.remote_type
            sys_info = self.execute_script("return window.navigator.userAgent")
            try:
                keyword = driverSetting.browser_name + "/"
                if driverSetting.browser_name == Browser.IE:
                    keyword = "rv:"
                elif driverSetting.browser_name == Browser.Safari:
                    keyword = "Version/"
                    
                for item in sys_info.split(" "):
                    if keyword in item:
                        version = item.strip(keyword).strip(")")
                        break
            except:
                version = "Unknown"
            
            try:
                browser = driverSetting.browser_name + ", version " + version
            except:
                browser = "Unknown"
        # Write information
        self.write_information(machine_name, browser)


    def _print_action(self, action):
        print(">>>  " + action)
        

    def write_information(self, machine_name, browser):
        try:
            delim = "="
            new_line = "\n"        
            file_env_path = Helper.base_dir() + self.sep + Constant.RunEnvironmentFile
            if not os.path.exists(file_env_path):
                open(file_env_path, 'w').close()
                
            file_env = open(file_env_path, 'r+')
            if os.stat(file_env_path).st_size == 0:
                folder_name = "screen_shot_" + datetime.now().strftime('%b %d %Y %H-%M-%S')
                self.folder_screen_shot = Helper.base_dir() + "\\test\\test_run\\test_result\\".replace("\\", self.sep) + folder_name
                file_env.truncate()
                # file_env.write("os" + delim + os_name + new_line)
                file_env.write("machine" + delim + machine_name + new_line)
                file_env.write("browser" + delim + browser + new_line)
                file_env.write("language" + delim + self._driverSetting.language + new_line)
                file_env.write("platform" + delim + self._driverSetting.platform + new_line)
                file_env.write("screen_shot" + delim + self.folder_screen_shot)
            else:
                with file_env as fp:
                    for line in fp:
                        if "screen_shot=" in line:
                            self.folder_screen_shot = line.split("=")[1]
            file_env.close()
        except Exception as ex:
            raise ex
        

    def execute_script(self, script, *args):
        try:
            result = self._driver.execute_script(script, *args)
            return result
        except Exception as ex:
            self.save_screenshot()
            raise ex
        

    def get(self, url):
        try:
            self._driver.get(url)
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Navigate to " + url)


    def get_window_size(self):
        try:
            return self._driver.get_window_size()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        
    
    def get_window_position(self):
        try:
            return self._driver.get_window_position()
        except Exception as ex:
            self.save_screenshot()
            raise ex


    def find_element(self, by=By.ID, value=None, timeout=None):    
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        try:
            return WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            return None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex


    def find_hidden_element(self, by=By.ID, value=None, timeout=None):    
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
            
        try:
            return WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex
        

    def find_elements(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
            
        try:
            return WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.presence_of_all_elements_located((by, value)))                           
        except TimeoutException:
            return None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex
        

    def wait_for_element_invisible(self, by=By.ID, value=None, timeout=None):
        self.is_element_invisible(by, value, timeout)


    def wait_for_element_visible(self, by=By.ID, value=None, timeout=None):
        self.is_element_visible(by, value, timeout)


    def wait_for_element_clickable(self, by=By.ID, value=None, timeout=None):
        if self.driverSetting.browser_name == Browser.Edge:
            Driver_Edge.is_element_clickable(self, by, value, timeout)
        else:
            self.is_element_clickable(by, value, timeout)


    def is_element_visible(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        try:
            result = WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            result = None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex
        
        return result is not None
    

    def is_element_invisible(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        try:
            result = WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.invisibility_of_element_located((by, value)))
        except TimeoutException:
            result = None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex
        
        return result is True
    

    def is_element_clickable(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        try:
            result = WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.element_to_be_clickable((by, value)))
        except TimeoutException:
            result = None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex
        
        return result is not None


    def get_dialog_message(self, close_dialog=True):
        try:
            result = self._driver.switch_to_alert().text
            if close_dialog:
                self.handle_dialog(close_dialog)
            return result
            self._print_action("Get dialog message")
        except Exception as ex:
            self.save_screenshot()
            raise ex
        

    def handle_dialog(self, accept=False):
        timeout = self._driverSetting.element_wait_timeout
        try:
            alert = WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.alert_is_present())
            
            if accept:
                alert.accept()
                self._print_action("Accept dialog")
            else:
                alert.dismiss()
                self._print_action("Dismiss dialog")
            WebDriverWait(self._driver, 5, POLL_FREQUENCY).until_not(EC.alert_is_present())
        except Exception as ex:
            self.save_screenshot()
            raise ex
    
    
    def maximize_window(self):
        try:
            self._driver.maximize_window()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Maximize browser")
        

    def close(self):
        try:
            self._driver.close()
            if self.window_handles:
                self.switch_to_main_window()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Close browser")

        
    def refresh(self):
        try:
            self._driver.refresh()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Refresh browser")


    def quit(self):
        try:
            self._driver.quit()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Quit browser")

        
    def switch_to_alert(self):
        try:
            self._print_action("Switch to alert")
            return self._driver.switch_to.alert
        except Exception as ex:
            self.save_screenshot()
            raise ex
        
        
    def switch_to_main_window(self):
        try:
            self.switch_to_window(0)
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Switch to main window")
        
        
    def switch_to_window(self, index=0):
        try:
            self._driver.switch_to.window(self.window_handles[index])
            self.switch_to_default_content()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Switch to window with index = " + str(index))


    def switch_to_default_content(self):
        try:
            self._driver.switch_to.default_content()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Switch to default content")


    def switch_to_frame(self, frame_id):
        try:
            self._driver.switch_to.frame(frame_id)
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Switch to frame " + str(frame_id))
  

    def save_screenshot(self):
        try:
            if not hasattr(self, 'tc_name'):
                self.tc_name = "screenshot"
            file_name = self.folder_screen_shot + self.sep + self.tc_name + " " + datetime.now().strftime('%b %d %Y %H-%M-%S') + ".png"
            dir_name = os.path.dirname(file_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            
            self._driver.save_screenshot(file_name)
        except Exception as ex:
            raise ex
        self._print_action("Save screenshot")

    
    def set_page_load_timeout(self, time_to_wait):
        try:
            self._driver.set_page_load_timeout(time_to_wait)
        except Exception as ex:
            raise ex
        self._print_action("Set page load timeout to " + str(time_to_wait) + " seconds")

    
    def delete_all_cookies(self):
        try:
            self._driver.delete_all_cookies()
        except Exception as ex:
            raise ex
        self._print_action("Delete all cookies")
        
    
    def open_new_tab(self, url):
        try:
            self.execute_script("window.open('{}');".format(url))
            self.switch_to_window(1)
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Open new tab")

    
    def scroll_down_to_bottom(self):
        try:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Scroll down to bottom")

        
    def scroll_up_to_top(self):
        try:
            self.execute_script("window.scrollTo(0, 0)")
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Scroll up to top")


    def get_cookies(self):
        try:
            self._print_action("Get all cookies")
            return self._driver.get_cookies()
        except Exception as ex:
            raise ex
        
    
    def get_cookie(self, cookie_name):
        try:
            self._print_action("Get cookie with name " + cookie_name)
            return self._driver.get_cookie(cookie_name)
        except Exception as ex:
            raise ex


    def back(self):
        try:
            self._driver.back()
        except Exception as ex:
            self.save_screenshot()
            raise ex
        self._print_action("Back to previous page")


class Driver_Edge(Driver):
    
    def _scroll_to_find(self, by=By.ID, value=None, timeout=1):
        try:
            present_element = WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.presence_of_element_located((by, value)))
            if present_element:
                self.execute_script("arguments[0].scrollIntoView(true);", present_element)
        except TimeoutException:
            pass
        except StaleElementReferenceException:
            pass


    def find_element(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        sw = Stopwatch()
        sw.start()
        while timeout > 0:
            try:
                return WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.visibility_of_element_located((by, value)))
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return None


    def find_elements(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        sw = Stopwatch()
        sw.start()
        while timeout > 0:
            try:
                return WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.presence_of_all_elements_located((by, value)))                           
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return None


    def is_element_visible(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        sw = Stopwatch()
        sw.start()
        while timeout > 0 and result == None:
            try:
                result = WebDriverWait(self._driver, 1, POLL_FREQUENCY).until(EC.visibility_of_element_located((by, value)))
                break
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return result is not None


    def is_element_invisible(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        sw = Stopwatch()
        sw.start()
        while timeout > 0 and result == None:
            try:
                result = WebDriverWait(self._driver, 1, POLL_FREQUENCY).until(EC.invisibility_of_element_located((by, value)))
                break
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return result is True


    def is_element_clickable(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        sw = Stopwatch()
        sw.start()
        while timeout > 0 and result == None:
            try:
                result = WebDriverWait(self._driver, timeout, POLL_FREQUENCY).until(EC.element_to_be_clickable((by, value)))
                break
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return result is not None

class Driver_Safari(Driver):
    def is_element_visible(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        try:
            result = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            result = None
        except NoSuchWindowException:
            self.save_screenshot()
            raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
        except Exception as ex:
            self.save_screenshot()
            raise ex
        
        return result is not None

    def _scroll_to_find(self, by=By.ID, value=None, timeout=1):
        try:
            present_element = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((by, value)))
            if present_element:
                self.execute_script("arguments[0].scrollIntoView(true);", present_element)
        except TimeoutException:
            pass
        except StaleElementReferenceException:
            pass
        
        
    def find_element(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        sw = Stopwatch()
        sw.start()
        while timeout > 0:
            try:
                return WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((by, value)))
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return None
            
    
    def is_element_invisible(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        sw = Stopwatch()
        sw.start()
        while timeout > 0 and result == None:
            try:
                result = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((by, value)))
                break
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return result is True
    

    def is_element_clickable(self, by=By.ID, value=None, timeout=None):
        if timeout is None:
            timeout = self._driverSetting.element_wait_timeout
        
        result = None
        
        sw = Stopwatch()
        sw.start()
        while timeout > 0 and result == None:
            try:
                result = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((by, value)))
                break
            except TimeoutException:
                self._scroll_to_find(by, value, 1)
                timeout -= sw.elapsed().total_seconds()
            except NoSuchWindowException:
                self.save_screenshot()
                raise NoSuchWindowException("Error: Cannot interact with element {} when browser is closed.".format(self._locator))
            except Exception as ex:
                self.save_screenshot()
                raise ex
        
        return result is not None
