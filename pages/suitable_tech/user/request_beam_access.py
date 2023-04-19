from pages.suitable_tech.user.user_template_page import UserTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element


class _RequestBeamAccessPageLocator(object):
    _txtEmail = (By.ID, "id_email")
    _txtFirstName = (By.ID, "id_first_name")
    _txtLastName = (By.ID, "id_last_name")
    _txtMessage = (By.ID, "id_message")
    _btnSend = (By.ID, "submit-id-send")
    _lblSuccessMsg = (By.XPATH, "//div[@class='alert-box success']")
    

class RequestBeamAccessPage(UserTemplatePage):
    """
    @description: This is page object class for Request Beam Access page . 
        Please visit https://staging.suitabletech.com/r/7WS9NE/ for more details
    @page: Request Beam Access page
    @author: Thanh Le
    """
    
    
    """    Properties    """
    @property
    def _txtEmail(self):
        return Element(self._driver, *_RequestBeamAccessPageLocator._txtEmail)
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_RequestBeamAccessPageLocator._txtFirstName)
    @property
    def _txtLastName(self):
        return Element(self._driver, *_RequestBeamAccessPageLocator._txtLastName)
    @property
    def _txtMessage(self):
        return Element(self._driver, *_RequestBeamAccessPageLocator._txtMessage)
    @property
    def _btnSend(self):
        return Element(self._driver, *_RequestBeamAccessPageLocator._btnSend)
    @property
    def _lblSuccessMsg(self):
        return Element(self._driver, *_RequestBeamAccessPageLocator._lblSuccessMsg)


    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """         
        UserTemplatePage.__init__(self, driver)

    
    def send_request_beam_access(self, user, message=None):
        """
        @summary: This action use to send request beam access
        @parameter: <user>: user object
                    <message>: message text
        @return: Request Beam Access page
        @author: Thanh Le
        """
        self._txtEmail.type(user.email_address)
        if(user.first_name!=None):
            self._txtFirstName.type(user.first_name)
        if(user.last_name!=None):
            self._txtLastName.type(user.last_name)
        if(message!=None):
            self._txtMessage.type(message)
        
        self._btnSend.click_element()
        self._lblSuccessMsg.wait_until_displayed()
        return self


    def get_request_success_message(self):
        """
        @summary: This action use to get message text
        @return: success message text
        @author: Thanh Le
        """
        return self._lblSuccessMsg.text
    
