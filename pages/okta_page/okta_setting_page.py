from pages.basepage import BasePage
from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By
from time import sleep

class _OktaSettingPageLocator(object):
    _btnEditPersonInfo = (By.ID, "person_info.edit_link")
    _txtPersonInfoFirstName = (By.ID, "person_info.firstName")
    _txtPersonInfoLastName = (By.ID, "person_info.lastName")
    _btnPersonInfoSave = (By.ID, "person_info.button.submit")
    _ifrSetting = (By.ID, "//div[@id='main-content']//iframe")
    _txtPersonInfoOldPass = (By.ID, "change_password.oldPassword")

class OktaSettingPage(BasePage):
    """
    @description: This is page object class for OneLogin Page
    @page: One Login Page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _btnEditPersonInfo(self):
        return Element(self._driver, *_OktaSettingPageLocator._btnEditPersonInfo)
    @property
    def _txtPersonInfoFirstName(self):
        return Element(self._driver, *_OktaSettingPageLocator._txtPersonInfoFirstName)
    @property
    def _txtPersonInfoLastName(self):
        return Element(self._driver, *_OktaSettingPageLocator._txtPersonInfoLastName)
    @property
    def _btnPersonInfoSave(self):
        return Element(self._driver, *_OktaSettingPageLocator._btnPersonInfoSave)
    @property
    def _ifrSetting(self):
        return Element(self._driver, *_OktaSettingPageLocator._ifrSetting)
    @property
    def _txtPersonInfoOldPass(self):
        return Element(self._driver, *_OktaSettingPageLocator._txtPersonInfoOldPass)


    """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method
        @parameter: driver: Web Driver
        @author: Thanh Le
        """
        BasePage.__init__(self, driver)
        
        
    def update_personal_information(self,user):
        """
        @summary: update personal information
        @param user: user information
        @author: Thanh Le
        """
        self.wait_page_ready()
        #for stable on chrome
        sleep(0.3)
        self._driver.switch_to_frame("settings-frame")
        self._txtPersonInfoOldPass.wait_until_displayed()
        self._btnEditPersonInfo.wait_until_clickable().jsclick()
        self._txtPersonInfoFirstName.type(user.first_name)
        self._txtPersonInfoLastName.type(user.last_name)
        self._btnPersonInfoSave.wait_until_clickable().click_element()
        sleep(1)
        if self._btnPersonInfoSave.is_displayed(1):
            self._btnPersonInfoSave.click_element()
        self._btnPersonInfoSave.wait_until_disappeared()
        return self

