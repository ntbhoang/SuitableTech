from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_base import ElementBase
from common.stopwatch import Stopwatch
from common.constant import Browser, Platform
from core.webdriver.elements.element_list import ElementList
from core.webdriver.exceptions import ElementIsNone


class DropdownList(ElementBase):
    
    def __init__(self, driver, by=By.XPATH, value=None):       
        ElementBase.__init__(self, driver, by, value)


    def select_by_text(self, text, click=True):
        """      
        @summary: select an item in SuitableTech dropdown list by text        
        @param text: Text of an item which to be selected
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Select by " + text
        self._print_action()
        self._select_element(self._get_child_item(by="text", value=text), click)


    def select_by_partial_text(self, text):
        """      
        @summary: select an item in SuitableTech dropdown list by partial text        
        @param text: Partial text of an item which to be selected
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Select by " + text
        self._print_action()
        self._select_element(self._get_child_item_by_partial_text(text))
    
    
    def select_by_href(self, value):
        """      
        @summary: select an item in SuitableTech dropdown list by text        
        @param text: Text of an item which to be selected
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Select by href"
        self._print_action()
        self._select_element(self._get_child_item(by="href", value=value))
    
    
    def is_item_existed(self, text):
        """      
        @summary: return True if item exists. Otherwise, return False.       
        @param text: Text of an item which to be checked
        @return: Boolean value True/False
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Is item existed"
        self._print_action()
        is_item_existed = False
        
        self.click()
        
        itemlist = ElementList(self._driver, By.XPATH, "{}//ul[@class='dropdown']//li".format(self._value))
        elements = itemlist.get_all_elements()
        if elements and len(elements) > 0:
            for w_elem in elements:
                displayed_text = w_elem.find_element(By.XPATH, "//a").text
                if displayed_text == text:
                    is_item_existed = True
                    break
        
        if not is_item_existed:
            self.jsmouse_to()
            self.jsclick()
            is_item_existed = self._get_child_item(value=text).is_displayed()
        
        return is_item_existed


    def is_item_not_existed(self, text):
        """      
        @summary: return True if item Not exists. Otherwise, return False.       
        @param text: Text of an item which to be checked
        @return: Boolean value True/False
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Is item Not existed"
        self._print_action()
        if(self._driver.driverSetting.browser_name == Browser.IE 
           or self._driver.driverSetting.browser_name == Browser.Edge):
            self.jsmouse_to()
            self.jsclick()
        else:
            self.mouse_to()
            self.click()
        return self._get_child_item(value=text).is_disappeared()
    
    
    def get_text(self):
        """      
        @summary: return Text currently displays in SuitableTech dropdown list     
        @return: string
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Get dropdown list's text"
        self._print_action()
        elem = Element(self._driver, By.XPATH, u"{}".format(self._value))
        elem.wait_until_displayed()
        return elem.text


    def get_selected_item(self):
        """      
        @summary: return Text of selected item in SuitableTech dropdown list     
        @return: string
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        self._current_action = "Get selected item"
        self._print_action()
        return Element(self._driver, By.XPATH, u"{}/a".format(self._value)).text
    
    
    def _get_child_item(self, by="text", value=""):
        """
        @param by: "text", "href"
        @return: the child element
        @created_date: August 5, 2016
        """
        child_xpath = u""
        if by == "text":
            child_xpath = u"{}//li//a[.=\"{}\"]".format(self._value, value)
        elif by == "href":
            child_xpath = u"{}//a[@href='{}']".format(self._value, value)
            
        return Element(self._driver, By.XPATH, child_xpath)
    
    
    def _get_child_item_by_partial_text(self, text):
        return Element(self._driver, By.XPATH, u"{}//li//a[contains(., \"{}\")]".format(self._value, text))


    def _select_element(self, element):
        _browser_name = self._driver.driverSetting.browser_name
        if _browser_name == Browser.IE or _browser_name == Browser.Safari or _browser_name == Browser.Edge or self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._select_element_js(element)
        else:
            self._select_element_sel(element)

    
    def _select_element_js(self, element):
        """
        @summary: This method allows select a item in dropdownlist by js
        @param element: element that need to be selected
        @author: Thanh Le
        @created_date: August 5, 2016
        """
        is_dropdown_displayed = self.is_displayed()
        sw = Stopwatch()
        sw.start()
        
        if is_dropdown_displayed:
            
            while sw.elapsed().total_seconds() < self._timeout:
                self.jsmouse_to()
                self.click()
                
                while (not element.is_displayed(5)) and (sw.elapsed().total_seconds() < self._timeout):
                    self.mouse_to()
                    self.click()
                
                if element.is_clickable(1):
                    element.jsmouse_to()
                    element.jsclick()
                    return
                    
            raise ElementIsNone(self._driver, "Select dropdownlist item", element._locator)
        else:
            raise ElementIsNone(self._driver, "Select dropdownlist", self._locator) 
    
    
    def _select_element_sel(self, element):
        """
        @summary: This method allows select a item in dropdownlist by selenium
        @param element: element that need to be selected
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        is_dropdown_displayed = self.is_displayed()
        sw = Stopwatch()
        sw.start()
        
        if is_dropdown_displayed:
            while sw.elapsed().total_seconds() < self._timeout:
                self.mouse_to()
                self.click()
                
                while (not element.is_displayed(5)) and (sw.elapsed().total_seconds() < self._timeout):
                    self.mouse_to()
                    self.click()

                if element.is_clickable(1):
                    self.mouse_to()
                    element.click()
                    
                    return
                    
            raise ElementIsNone(self._driver, "Cannot select dropdownlist item", element._locator)
        else:
            raise ElementIsNone(self._driver, "Cannot select dropdownlist", self._locator)            


    def _select_element_pyautogui(self, element, click=True):
        """
        @summary: This method allows select a item in dropdownlist by pyautogui
        @param element: element that need to be selected
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        is_dropdown_displayed = self.is_displayed()
        sw = Stopwatch()
        sw.start()
         
        if is_dropdown_displayed:
            can_be_clicked = False
             
            while can_be_clicked is False and sw.elapsed().total_seconds() < self._timeout:
                
                self.pyautogui_click()
                self.pyautogui_mouse_to()
                
                can_be_clicked = element.is_clickable(1)
                
                if can_be_clicked:
                    element.pyautogui_mouse_to()
                    can_be_clicked = element.is_clickable(1)
                    if can_be_clicked:
                        element.jsclick()
                        return
                    
            raise ElementIsNone(self._driver, "Select dropdownlist item", element._locator)
        else:
            raise ElementIsNone(self._driver, "Select dropdownlist", self._locator)


