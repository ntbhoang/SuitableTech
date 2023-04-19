from selenium.webdriver.common.by import By
from core.webdriver.elements.element_list import ElementList
from common.application_constants import ApplicationConst
from core.webdriver.exceptions import ElementIsNone


class NotificationRecords(ElementList):
    
    def __init__(self, driver, by=By.XPATH, locator_value=None):
        ElementList.__init__(self, driver, by, locator_value)
        
    @staticmethod
    def does_contain_text(array_text, container):
        """
        @summary: This method returns False if the text is not in container ( message displays in notification record )
        @param array_text: array text
        @param container: message display
        @return: False if the text is not in container
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        for text in array_text:
            if text is not None and not (text in container):
                return False
        return True

    def does_record_exist(self, user):
        """
        @summary: This method returns True if exist a notification records
        @param user: user instance
        @return: True if exists record, if not return False
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        try:
            elements = self._get_elements()
            if elements is None:
                raise ElementIsNone(self._driver, "Get request records", self._locator_value) 
            else:
                for w_elem in elements:
                    if user.first_name == None and user.last_name == None:
                        displayed_text = w_elem.find_element(By.XPATH, ".//div[@class='media-body']//p[not(@class='ng-hide')]//translate").text
                    else:
                        displayed_text = w_elem.find_element(By.XPATH, ".//div[@class='media-body']//translate").text
            
                    temp = [ApplicationConst.LBL_ACCESS_REQUEST_RECORD_MESSAGE, user.email_address]
                    if self.does_contain_text(temp, displayed_text):
                        return True
                    
        except Exception as ex:
            raise Exception("Element is not found. Error: {}".format(ex))
        
        return False
