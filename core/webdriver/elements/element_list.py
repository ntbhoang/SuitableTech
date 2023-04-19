from selenium.webdriver.common.by import By
from common.stopwatch import Stopwatch
from selenium.common.exceptions import StaleElementReferenceException,\
    WebDriverException

class ElementList(object):
    _current_action = ""

    def __init__(self, driver, by=By.XPATH, locator_value=None):
        self._by = by
        self._value = locator_value
        self._locator = "{{By: {}, Value: {}}}".format(by, locator_value)
        self._driver = driver
        self._time_left = self._driver.driverSetting.element_wait_timeout
        self._elements = []


    def _print_action(self):
        separator = "                              "
        print(" " + (self._current_action + separator)[:27] + ">>  " + self._locator)


    def _get_elements(self, wait_time_out=None):
        """
        @summary: get list elements
        @param wait_time_out: time to waiting for elements
        @return: elements
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        elements = self._driver.find_elements(self._by, self._value, wait_time_out)
        
        self._elements.clear()
        
        if elements is None:
            return []

        for element in elements:
            self._elements.append(element)
             
        return self._elements


    def count(self, wait_time_out=None):
        """
        @summary: count number element in list
        @param wait_time_out: time to waiting for elements
        @return: number of elements or 0 if doesn't have any elements
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        try:
            elements = self._get_elements(wait_time_out)
            return 0 if elements is None else len(elements)
        except Exception as ex:
            raise Exception("Cannot count ElementList. Error: {}".format(ex))


    def get_all_elements(self, wait_time_out=None):
        """
        @summary: get all elements
        @param wait_time_out: time to waiting for elements
        @return: elements
        @author: Thanh Le
        @created_date: August 5, 2016
        """
        try:
            elements = self._get_elements(wait_time_out)
            if elements is None:
                raise Exception("Element list is not found!")
            
            return elements
        except Exception as ex:
            raise Exception("Cannot count ElementList. Error: {}".format(ex))


    def get_element_at(self, index):
        """
        @summary: get specific element based on index
        @param index: element's index
        @return: element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        try:
            elements = self._get_elements()
            if elements is None:
                raise Exception("Element list is not found!")
            else:
                if index < len(elements):
                    return elements[index]
                else:
                    raise Exception("Index is out of range")
        except Exception as ex:
            raise Exception("Element is not found. Error: {}".format(ex))


    def wait_until_clickable(self, wait_time_out=None, index=None):
        """
        @summary: wait until elementlist or element of list is clickable
        @param wait_time_out: time to waiting for element
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Wait until clickable"
        self._print_action()
        
        if(wait_time_out == None):
            wait_time_out = self._time_left
        if index == None:
            self._driver.wait_for_element_clickable(self._by, self._value, wait_time_out)
        else:
            self._driver.wait_for_element_clickable(self._by, self._value[index], wait_time_out)
        return self


    def click(self, index):
        """
        @summary: click element at index by selenium
        @author: Thanh Le
        @created_date: June 13, 2018
        """
        self._current_action = "Click at [{}] of Elementlist".format(index)
        self._print_action()
        sw = Stopwatch()
        sw.start()
        timeleft = self._time_left
        message = []

        while(timeleft > 0):
            try:
                elements = self._get_elements(timeleft)
                elements[index].click()
                break
            except StaleElementReferenceException:
                self.wait_until_clickable(5, index)
            except WebDriverException as wdex:
                if ("Element is obscured" in str(wdex)) or ("Unknown error" in str(wdex)) or ("Other element would receive the click" in str(wdex)):
                    self.wait_until_clickable(5, index)
                else:
                    message.append(wdex)
            except Exception as ex:
                message.append(ex)
                raise ex

        timeleft -= sw.elapsed().total_seconds()

        if message:
            self._driver.save_screenshot()
            print(message)

