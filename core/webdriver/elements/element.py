from selenium.webdriver.common.by import By
from core.webdriver.elements.element_base import ElementBase
from selenium.common.exceptions import StaleElementReferenceException
from common.stopwatch import Stopwatch
from core.webdriver.exceptions import ElementIsNone
from time import sleep
from common.constant import Browser


class Element(ElementBase):
    
    """ Methods """
    def __init__(self, driver, by=By.XPATH, value=None):       
        ElementBase.__init__(self, driver, by, value) 


    def submit(self):
        """
        @summary: this method to submit a form, dialog
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Submit"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                elem.submit()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
            
    def clear(self):
        """
        @summary: This method allows clear data of a textbox or combobox
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Clear"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                elem.clear()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
            
    def send_keys(self, *value):
        """
        @summary: This method allows send keys to textbox or combobox
        @param value: the text need to be send
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Send keys"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                elem.send_keys(*value)
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
            
    def check(self):
        """
        @summary: This method allows check a checkbox
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Check"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                if(elem.is_selected() == False):
                    elem = self.jsclick()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
        
         
    def uncheck(self):
        """
        @summary: This method allows uncheck a checkbox
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "UnCheck"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                if(elem.is_selected() == True):
                    if self._driver._driverSetting.browser_name == Browser.Safari:
                        self._driver.execute_script("arguments[0].click();", elem)
                    else:
                        elem.click()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
            
    def type(self, *value):
        """
        @summary: This method to clear and send keys to textbox or combobox
        @param value: the text that need to be type
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self.clear()
        self.send_keys(*value)
    
    
    def slow_type(self, value):
        """
       @summary: This method to clear and send keys to textbox or combobox. This method have sleep after each key sent
       @param value: the text that need to be type
       @author: Thanh Le
       @created_date: August 5, 2016
       """
        self._current_action = "Slow type"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                self.clear()
                length = len(value)
                number_of_fast_chars = round(length * 0.0) 
                fast_chars = value[:number_of_fast_chars]
                slow_chars = value[number_of_fast_chars:]
                self.send_keys(fast_chars)
                
                for char in slow_chars:
                    self.send_keys(char)
                    sleep(0.1)
                    
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
    
    def get_attribute(self, name):
        """
        @summary: This method allows get attribute (style, class, id, ...) of element
        @param name: attribute of element (style, class, ...)
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Get {} attribute".format(name)
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                return elem.get_attribute(name)
            except ElementIsNone:
                return None
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()
            
    
    def is_selected(self):
        """
        @summary: This method is used to check checkbox is selected
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Is selected"
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._timeout
        
        while(timeleft > 0):
            try:
                elem = self._get_element(timeleft)
                return elem.is_selected()
            except ElementIsNone:
                return None
            except StaleElementReferenceException:
                self.wait_until_clickable(2)
            except Exception as ex:
                self._driver.save_screenshot()
                raise ex
            timeleft -= sw.elapsed().total_seconds()

