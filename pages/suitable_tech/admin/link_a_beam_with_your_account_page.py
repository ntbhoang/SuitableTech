from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.basepage import BasePage


class _LinkABeamWithYourAccountPage(object):
    _txtDeviceName = (By.CSS_SELECTOR, '#id_device_name')
    _txtLinkingCode = (By.CSS_SELECTOR, '#id_claim_key')
    _btnLinkYourBeam = (By.CSS_SELECTOR, '#submit-id-submitbtn')
    _lblErrorMessage = (By.CSS_SELECTOR, '.compact>li')
    

class LinkABeamWithYourAccountPage(BasePage):
    """
    @description: This is page object class for Link a Beam with your account page.
        This page will be opened after clicking on Add a Beam button.
        Please visit https:https://stg1.suitabletech.com/setup/link/?o=130 for more details.
    @page: Link A Beam With Your Account page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _txtDeviceName(self):
        return Element(self._driver, *_LinkABeamWithYourAccountPage._txtDeviceName)
    @property
    def _txtLinkingCode(self):
        return Element(self._driver, *_LinkABeamWithYourAccountPage._txtLinkingCode)
    @property
    def _btnLinkYourBeam(self):
        return Element(self._driver, *_LinkABeamWithYourAccountPage._btnLinkYourBeam)
    @property
    def _lblErrorMessage(self):
        return Element(self._driver, *_LinkABeamWithYourAccountPage._lblErrorMessage)

    """    Methods    """
    def __init__(self, driver):        
        """      
        @summary: Constructor method      
        @param driver: Web driver
        @author: Thanh Le 
        """
        BasePage.__init__(self, driver)      
#         self._lblChatboxHeader.wait_until_displayed()
    
    
    def link_a_beam(self, device_name, linking_code, organization):
        self._txtDeviceName.type(device_name)
        self._txtLinkingCode.type(linking_code)
        self._btnLinkYourBeam.click()
        return self
        
        
    def get_error_message(self):
        return self._lblErrorMessage.text
    
        
    def does_link_your_beam_button_display(self):
        return True if self._btnLinkYourBeam.is_displayed() else False
        
        