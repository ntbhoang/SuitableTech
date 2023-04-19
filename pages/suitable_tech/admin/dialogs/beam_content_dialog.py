from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from time import sleep
import pyautogui
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
pyautogui.FAILSAFE = False
from common.constant import Platform, Browser
from threading import Thread

class _BeamContentDialogLocator(object):
    _btnChooseFile = (By.XPATH, "//div[@class='modal-content']//form[@data-file-upload='fileUploadOptions']/span[not(contains(@class,'ng-hide')) and not(@style='')]")
    _txtChooseFile = (By.XPATH, "//input[@name='files[]']")
    _btnContinue = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='close(content)']")
    _iconLoading = (By.XPATH, "//div[@class='modal-content']//div[@class='col-xs-12'][@ng-show='isLoading']")
    _iconDeleteImg = (By.XPATH, "//a[@ng-click='delete(item)']/..[not(contains(@class,'ng-hide'))]")
    _btnDone = (By.CSS_SELECTOR, '.btn.btn-primary.ng-scope')
    
    @staticmethod
    def _iconRecycleBin(image_name):
        return (By.XPATH, u"//div[.=\"{}\"]//a".format(image_name))
    @staticmethod
    def _imageBeam(image_name):
        return (By.XPATH, u"//div[.=\"{}\"]//img".format(image_name))  
    
class BeamContentDialog(DialogBase):
    """
    @description: This is page object class of dialog base. This class is ONLY for inheriting.
    @page: Dialog Base
    @author: Thanh Le
    """
    
    """    Properties    """
    @property
    def _iconDeleteImg(self):
        return Element(self._driver, *_BeamContentDialogLocator._iconDeleteImg)
    @property
    def _txtChooseFile(self):
        return Element(self._driver, *_BeamContentDialogLocator._txtChooseFile)
    @property
    def _btnChooseFile(self):
        return Element(self._driver, *_BeamContentDialogLocator._btnChooseFile)
    @property
    def _btnDone(self):
        return Element(self._driver, *_BeamContentDialogLocator._btnDone)
    @property
    def _btnContinue(self):
        return Element(self._driver, *_BeamContentDialogLocator._btnContinue)
    @property
    def _iconLoading(self):
        return Element(self._driver, *_BeamContentDialogLocator._iconLoading)
    def _iconRecycleBin(self, image_name):
        return Element(self._driver, *_BeamContentDialogLocator._iconRecycleBin(image_name))
    def _imageBeam(self, image_name):
        return Element(self._driver,*_BeamContentDialogLocator._imageBeam(image_name))
    
    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """      
        self._driver = driver
        self._iconLoading.wait_until_disappeared()
        self._btnContinue.wait_until_displayed()
        
    
    def is_image_displays(self, image_name, timeout= None):
        """
        @summary: Check if image displays
        @author: Thanh Le
        @return: True if image displays, False for vice versa
        """  
        return self._imageBeam(image_name).is_displayed(timeout)
        
    
    def is_icon_delete_image_displays(self, timeout= None):
        """
        @summary: Check if icon Delete image displays
        @author: Thanh Le
        @return: True if icon Delete image displays, False for vice versa
        """  
        return self._iconDeleteImg.is_displayed(timeout)
    
    
    def is_choose_file_button_displays(self, timeout= None):
        """
        @summary: Check if Choose file button displays
        @author: Thanh Le
        @return: True if Choose file button displays, False for vice versa
        """  
        return self._btnChooseFile.is_displayed(timeout)


    def choose_file(self, file_path):
        if((self._driver.driverSetting.browser_name in [Browser.Chrome, Browser.Firefox, Browser.IE]) or self._driver.driverSetting.run_locally == False):
            elem = self._driver.find_hidden_element(*_BeamContentDialogLocator._txtChooseFile)
            elem.send_keys(file_path)
        else:
            th1 = OpenFileDialogThread(self._driver)
            th1.daemon = False
            th1.start()
            th1.join(3)
             
            th2= SendKeysThread(self._driver, file_path+'\n')
            th2.daemon = False
            th2.start()
            th2.join(3)
             
            self._wait_for_loading_completed()
             
        return self
        
    
    def _wait_for_loading_completed(self):
        """
        @summary: This action is used to wait image loading
        @author: Thanh Le
        """
        loading_icon = self._iconLoading
        loading_icon.wait_until_displayed(2)
        if loading_icon.is_displayed():
            self._iconLoading.wait_until_disappeared()
            
        
    def click_continue_button(self, wait_for_completed=True):
        """
        @summary: This action is used to click on Continue button
        @author: Thanh Le
        """
        self._btnContinue.scroll_to().click()
        if(wait_for_completed):
            if self._btnContinue.is_displayed(3):
                self._btnContinue.jsclick()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_settings_page import AdminBeamsSettingsPage
        return AdminBeamsSettingsPage(self._driver)
         
            
    def click_done(self):
        """
        @summary: This action is used to click on Continue button
        @author: Thanh Le
        """
        self._btnDone.wait_until_clickable().click()
        if self._btnDone.is_displayed(3):
            self._btnDone.jsclick()
        return self
        

    def click_cancel_button(self):
        """
        @summary: This action is used to click on Cancel button
        @author: Thanh Le
        """
        self._btnCancel.click()
        if not self._dialog.is_disappeared(4):
            self._btnCancel.jsclick()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_settings_page import AdminBeamsSettingsPage
        return AdminBeamsSettingsPage(self._driver)
    
    
    def delete_image_beam_content(self, image_name, wait_for_completed=True):
        """      
        @summary: Delete an image in Manage Beam Content
        @parameter: <image_name>: name of image
        @return: self
        @author: Thanh Le
        """        
        self.click_delete_image_icon(image_name).continue_dialog(wait_for_completed)
        
        #wait for removing
        self._imageBeam(image_name).wait_until_disappeared()
        self._iconRecycleBin(image_name).wait_until_disappeared()
        
        return self
        
        
    def click_delete_image_icon(self, image_name):
        """      
        @summary: Click trash icon on an image 
        @parameter: <image_name>: name of image
        @return: ConfirmActionDialog
        @author: Thanh Le
        """   
        self._iconRecycleBin(image_name).wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        return ConfirmActionDialog(self._driver)
        
    
    def choose_beam_content_image(self, image_name):
        if self.is_image_displays(image_name, 10):
            self._imageBeam(image_name).click()            
            self.click_continue_button()
        if self._btnContinue.is_displayed(3):
            self.click_continue_button()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_settings_page import AdminBeamsSettingsPage
        return AdminBeamsSettingsPage(self._driver)
        
        
class OpenFileDialogThread(Thread):
    def __init__(self, driver):
        Thread.__init__(self)
        self._driver = driver

    def run(self):
        el = Element(self._driver, *_BeamContentDialogLocator._btnChooseFile)
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
        # click on the middle of browser to work-around for issue: select dropdown list failed when mouse into screen
        pyautogui.click(x=x/2, y=5)                     
        sleep(2)
        
        pyautogui.typewrite(self._text)
        sleep(2)
        
        if self._driver.driverSetting.platform == Platform.MAC:
            pyautogui.keyDown('return')
            pyautogui.keyUp('return')
        
        pyautogui.moveTo(x/2, y=5) # move to the middle of browser to work-around for issue: select dropdown list failed when mouse into screen
        sleep(2)
        

class SubmitThread(Thread):
    def __init__(self, driver):
        Thread.__init__(self)
        self._driver = driver

    def run(self):
        # focus Cancel button
        pyautogui.keyDown('tab')
        pyautogui.keyUp('tab')
        sleep(1)
        #focus Submit button
        pyautogui.keyDown('tab')
        pyautogui.keyUp('tab')
        sleep(1)
        # press spacebar
        pyautogui.keyDown(' ')
        pyautogui.keyUp(' ')
        sleep(1)