from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_list import ElementList
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from time import sleep
from core.webdriver.elements.editable_combobox import EditableCombobox
import pyautogui
from common.constant import Platform, Browser
from threading import Thread

class _ImportUsersDialogLocator(object):
    _txbCSVFile = (By.XPATH, "//div[@class='modal-content']//input[@name='csvfile']")
    _ecbxDeviceGroups = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='invitationDetails.selectedDeviceGroupIds']")
    _ecbxUserGroups = (By.XPATH, "//div[@class='modal-content']//div[contains(@ng-model, 'invitationDetails.selectedUserGroupIds')]")
    _btnNext = (By.XPATH, "//div[@class='modal-content']//form[@ng-submit='stepOne()']//button[@type='submit']")
    _btnConfirm = (By.XPATH, "//div[@class='modal-content']//form[@ng-submit='stepTwo()']//button[@type='submit']")
    _btnBrowse = (By.XPATH,"//input[@type='file']")
    _txtBrowseFile = (By.XPATH, "//input[@name='csvfile']")
    
    @staticmethod
    def _spanSelectedItem(name):
        return (By.XPATH, u"//span[text()='{}']".format(name))


class ImportUsersDialog(DialogBase):
    """
    @description: This is page object class for Import Users Dialog. You need to initialize it before using in class.
    @page: Import Users Dialog
    """
    

    """    Properties    """
    @property
    def _btnBrowse(self):
        return Element(self._driver, *_ImportUsersDialogLocator._btnBrowse)
    
    @property
    def _txbCSVFile(self):
        return Element(self._driver, *_ImportUsersDialogLocator._txbCSVFile)
    @property
    def _ecbxDeviceGroups(self):
        return EditableCombobox(self._driver, *_ImportUsersDialogLocator._ecbxDeviceGroups)
    @property
    def _ecbxUserGroups(self):
        return EditableCombobox(self._driver, *_ImportUsersDialogLocator._ecbxUserGroups)
    @property
    def _btnNext(self):
        return Element(self._driver, *_ImportUsersDialogLocator._btnNext)
    @property
    def _btnConfirm(self):
        return Element(self._driver, *_ImportUsersDialogLocator._btnConfirm)
    @property
    def _txtBrowseFile(self):
        return Element(self._driver, *_ImportUsersDialogLocator._txtBrowseFile)
    
    def _spanSelectedItem(self, name):
        return Element(self._driver, *_ImportUsersDialogLocator._spanSelectedItem(name)) 
    
    """    Methods    """
    def __init__(self, driver):    
        """      
        @summary: Constructor method   
        @param driver: Web Driver
        @author: Thanh Le        
        """    
        DialogBase.__init__(self, driver)
    
    
    def get_number_of_users_in_table(self):
        """
        @summary: Get number of users in table
        @return: number of users 
        @author: Thanh Le
        """
        user_list = ElementList(self._driver, By.XPATH, "//div[@class='contacts-import-wrapper']/table/tbody/tr")
        return user_list.count(5)
    
    
    def submit_users_from_file(self, data_file_path, new_device_group, new_user_group):
        """      
        @summary: This action is used to submit users from apart file
        @parameter: data_file_path: file path
                    new_device_group: new device group
                    new_user_group: new user group.
        @return: Dashboard page
        @author: Thanh Le
        """    
        self._submit_file(data_file_path)
        if self._driver.driverSetting.browser_name == Browser.Safari:
            sleep(2)
            self._btnNext.click_element()
        number_users = self.get_number_of_users_in_table()
        
        if(new_device_group != None):
            self._ecbxDeviceGroups.select(new_device_group)
            if(not self._spanSelectedItem(new_device_group).is_displayed(2)):
                self._ecbxDeviceGroups.select(new_device_group)
                if(not self._spanSelectedItem(new_device_group).is_displayed(2)):
                    self._driver.screenshot()
            
        if(new_user_group != None):
            self._ecbxUserGroups.select(new_user_group, "//div[@ng-model='invitationDetails.selectedUserGroupIds']")
            if(not self._spanSelectedItem(new_user_group).is_displayed(2)):
                self._ecbxUserGroups.select(new_user_group)
                if(not self._spanSelectedItem(new_user_group).is_displayed(2)):
                    self._driver.screenshot()
        
        if number_users > 0:
            self._btnConfirm.wait_until_clickable().jsclick()
        else:
            self.cancel()
            
        self._wait_for_dialog_disappeared()
        return self

    
    def submit_users_from_invalid_file(self, data_file_path):
        """      
        @summary: This action is used to submit users from invalid apart file
        @parameter: data_file_path: file path
        @return: Dashboard page
        @author: Thanh Le
        """
        self._submit_file(data_file_path)
        if self._driver.driverSetting.browser_name == Browser.Safari:
            self._btnNext.click_element()
        return self
    
    
    def _submit_file(self, data_file_path):
        if self._driver.driverSetting.browser_name == Browser.Edge or \
            self._driver.driverSetting.browser_name == Browser.Safari:
            th1 = OpenFileDialogThread(self._driver)
            th1.daemon = False
            th1.start()
            th1.join(3)
            
            th2= SendKeysThread(self._driver, data_file_path+'\n')
            th2.daemon = False
            th2.start()
            th2.join(3)
        else:
            self._txtBrowseFile.send_keys(data_file_path)
        
        self._btnNext.wait_until_clickable().click()

        

class OpenFileDialogThread(Thread):
    def __init__(self, driver):
        Thread.__init__(self)
        self._driver = driver

    def run(self):
        el = Element(self._driver, *_ImportUsersDialogLocator._txtBrowseFile)
        el.click()
        

class SendKeysThread(Thread): 
    def __init__(self, driver, text):
        Thread.__init__(self)
        self._driver = driver
        self._text = text

    def run(self):
        #work arround for issue: lost focus
        # => click on screen before typing.
        x,y = pyautogui.size()
        pyautogui.click(x=x/2, y=5)
        sleep(2)
        
        pyautogui.typewrite(self._text)
        sleep(2)
        
        if self._driver.driverSetting.platform == Platform.MAC:
            pyautogui.keyDown('return')
            pyautogui.keyUp('return')
        else:
            pyautogui.keyDown('enter')
            pyautogui.keyUp('enter')
        
        pyautogui.moveTo(2, y)
        sleep(2)


