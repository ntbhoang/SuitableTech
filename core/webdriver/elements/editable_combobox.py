"""
Created on Jun 15, 2016

@description: This is a wrapper class for the DIV element that represents an editable combobox. 
    When using this class, make sure that you select the correct DIV element, where it contains the 'input' 
    and 'listbox' element.
@author: thanh.viet.le
"""

from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_list import ElementList
from time import sleep
from common.constant import Browser


class EditableCombobox(Element):
    
    def __init__(self, driver, by=By.XPATH, value=None):       
        Element.__init__(self, driver, by, value)
    
    
    def select(self, search_value, xpath_ext=""):
        """
        @summary: This method allows select a item of editable combobox
        @param search_value: value that need to be selected
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._current_action = "Select item"
        self._print_action()

        # Sleep to action select combobox more stable 
        sleep(2)  
        
        self.click_element()
        search_input = Element(self._driver, By.XPATH, xpath_ext+"//input[@type='search' or @type='text']")
        if search_input.is_enabled(2):
            search_input.type(search_value)
            sleep(1)

        options = ElementList(self._driver, self._by, xpath_ext+"//ul//div[@role='option'] | //ng-include[@class='ng-scope']")
        elements = options.get_all_elements()
        if elements and len(elements) > 0:
            for w_elem in elements:
                displayed_text = w_elem.find_element(By.XPATH, ".//span").text
                if displayed_text == search_value:
                    if self._driver._driverSetting.browser_name == Browser.Safari:
                        self._driver.execute_script("arguments[0].click();", w_elem)
                    else:
                        w_elem.click()
                    break
        else:
            search_input.type(search_value)
            item_to_be_selected = Element(self._driver, By.XPATH, u"(//div[@role='option'])[1]//span[.='{}']".format(search_value))
            item_to_be_selected.wait_until_displayed()
            item_to_be_selected.click_element()
    
    
    def select_value_that_search_value_is_different_displayed_value(self, search_value, displayed_value, xpath_ext = ""):
        """
        @summary: This method allows select a item of editable user combobox 
        @param search_value: value that need to be selected
        @param displayed_value: displayed value
        @author: Thanh Le
        @created_date: March 14, 2017
        """
        # Sleep to action select combobox more stable 
        sleep(2)  
        
        self.click_element()
        search_input = Element(self._driver, By.XPATH, xpath_ext+"//input[@type='search']")
        if search_input.is_enabled(2):
            search_input.slow_type(search_value)
            #Sleep to handle rearching username too slowly  
            sleep(20)

        options = ElementList(self._driver, self._by, xpath_ext+"//ul//div[@role='option']")
        elements = options.get_all_elements()
        if elements and len(elements) > 0:
            for w_elem in elements:
                displayed_text = w_elem.find_element(By.XPATH, ".//span").text
                if displayed_text == displayed_text:
                    if self._driver._driverSetting.browser_name == Browser.Safari:
                        self._driver.execute_script("arguments[0].click();", w_elem)
                    else:
                        w_elem.click()