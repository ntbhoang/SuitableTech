from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pyautogui
pyautogui.FAILSAFE = False
from common.constant import Platform, Browser
from threading import Thread


class _UploadImageDialogLocator(object):
    _btnChooseFile = (By.XPATH, "//div[@class='modal-content']//form[@id='profileimage-upload']/span")
    _txtChooseFile = (By.XPATH, "//input[@name='files[]']")
    _btnSubmit = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='ok()']")
    _lblCropTracker = (By.XPATH, "//div[@ng-show='previewUrl']/h4/span")
    _pnlCropTracker = (By.XPATH, ".//form[@id='profileimage-upload']//div[@class='jcrop-tracker' and contains(@style, 'cursor: move')]")
    _pnlCropTracker_Container = (By.XPATH, ".//form[@id='profileimage-upload']//div[@class='jcrop-tracker' and contains(@style, 'cursor: crosshair')]")
    _pnlHandleResizeCropTracker = (By.XPATH, ".//form[@id='profileimage-upload']//div[@class='ord-se jcrop-handle']")
    _pnlUploadProgress = (By.XPATH, "//div[@class='modal-content']//div[@class='progress-bar progress-bar-success']")
    _lblCropMessage = (By.XPATH, "//div[@class='modal-content']//div[@ng-show='previewUrl']//h4")
    _icnUpload = (By.XPATH, "//*[@id='profileimage-upload']//span[@class='i fa fa-spin fa-spinner']")
    
   
class UploadImageDialog(DialogBase):
    """
    @description: This is page object class for Upload Image Dialog. You need to init it before using in page class.
    @page: Upload Image Dialog
    @author: Thanh Le
    """
    

    """    Properties    """
    @property
    def _txtChooseFile(self):
        return Element(self._driver, *_UploadImageDialogLocator._txtChooseFile)
    @property
    def _btnChooseFile(self):
        return Element(self._driver, *_UploadImageDialogLocator._btnChooseFile)
    @property
    def _lblCropTracker(self):
        return Element(self._driver, *_UploadImageDialogLocator._lblCropTracker)
    @property
    def _pnlCropTracker(self):
        return Element(self._driver, *_UploadImageDialogLocator._pnlCropTracker)
    @property
    def _pnlCropTracker_Container(self):
        return Element(self._driver, *_UploadImageDialogLocator._pnlCropTracker_Container)
    @property
    def _pnlHandleResizeCropTracker(self):
        return Element(self._driver, *_UploadImageDialogLocator._pnlHandleResizeCropTracker)
    @property
    def _pnlUploadProgress(self):
        return Element(self._driver, *_UploadImageDialogLocator._pnlUploadProgress)
    @property
    def _btnSubmit(self):
        return Element(self._driver, *_UploadImageDialogLocator._btnSubmit)
    @property
    def _lblCropMessage(self):
        return Element(self._driver, *_UploadImageDialogLocator._lblCropMessage)
    @property
    def _icnUpload(self):
        return Element(self._driver, *_UploadImageDialogLocator._icnUpload)
    
    
    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """      
        DialogBase.__init__(self, driver)
        self._btnChooseFile.wait_until_displayed()


    def choose_file(self, file_path):
        
        if((self._driver.driverSetting.browser_name in [Browser.Chrome, Browser.Firefox, Browser.IE]) or self._driver.driverSetting.run_locally == False):
            elem = self._driver.find_hidden_element(*_UploadImageDialogLocator._txtChooseFile)
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


    def is_crop_tracker_displayed(self, wait_time_out = 5):
        """
        @summary: Check if crop tracker display is displayed or not
        @parameter: wait_time_out: waiting time
        @return: True: the drop tracker is displayed
                False: the drop tracker is not displayed
        @author: Thanh Le
        """
        return self._pnlCropTracker_Container.is_displayed(wait_time_out)
    
    
    def get_crop_tracker_message(self):
        """
        @summary: This action is used to get crop tracker message
        @return: The message of drop-tracker
        @author: Thanh Le
        """
        return self._lblCropMessage.text
    
    
    def get_crop_tracker_dimension(self):
        """
        @summary: This action is used to get crop tracker dimension
        @return: dimensions of drop tracker
        @author: Thanh Le
        """
        tracker = self._pnlCropTracker_Container
        style = tracker.get_attribute("style")
        
        attributes = {}
        if style:
            style_items = style.split(";")        
            for item in style_items:
                entry = item.split(":")
                if len(entry) > 1:
                    attributes[ entry[0].strip() ] = entry[1].strip()
        
        left = 0
        top = 0
        width = 0
        height = 0
        
        if "left" in attributes:            
            left = int(attributes["left"].strip().replace('px',''))
        if "top" in attributes:            
            top = int(attributes["top"].strip().replace('px',''))
        if "width" in attributes:            
            width = int(attributes["width"].strip().replace('px',''))
        if "height" in attributes:            
            height = int(attributes["height"].strip().replace('px',''))
        
        return [left, top, width, height]
    
    
    def move_crop_tracker(self):
        """
        @summary: This action is used to move crop tracker to middle of image 
        @author: Tan Le
        """
        self._pnlCropTracker_Container.wait_until_displayed()
        ActionChains(self._driver.wrapped_driver).drag_and_drop(self._pnlCropTracker.native_element, self._pnlCropTracker_Container.native_element).perform()
        return self
        
    
    def resize_crop_tracker(self):
        """
        @summary: This action is used to resize crop tracker 
        @author: Tan Le
        """
        self._pnlCropTracker_Container.wait_until_displayed()
        ActionChains(self._driver.wrapped_driver).drag_and_drop(self._pnlHandleResizeCropTracker.native_element, self._pnlCropTracker_Container.native_element).perform()
        return self
        
    def submit(self, wait_for_completed=True):
        """
        @summary: This action is used to click on submit button to crop image
        @author: Thanh Le
        """
        if self._driver.driverSetting.browser_name == Browser.Edge:
            th1 = SubmitThread(self._driver)
            th1.daemon = False
            th1.start()
            th1.join(3)
        else:
            self._btnSubmit.click()
            if(wait_for_completed):
                self._wait_for_dialog_disappeared()
                       
                       
    def _wait_for_loading_completed(self):
        """
        @summary: This action is used to wait image loading
        @author: Thanh Le
        """
        progress_bar = self._pnlUploadProgress
        progress_bar.wait_until_displayed(5)
        if progress_bar.is_displayed():
            self._pnlUploadProgress.wait_until_disappeared()
        

class OpenFileDialogThread(Thread):
    def __init__(self, driver):
        Thread.__init__(self)
        self._driver = driver

    def run(self):
        el = Element(self._driver, *_UploadImageDialogLocator._btnChooseFile)
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
        #work arround for issue: lost focus
        # => click on screen before typing.
        x,y = pyautogui.size()
        # click on the middle of browser to work-around for issue: select dropdown list failed when mouse into screen
        pyautogui.click(x=x/2, y=170)
        # focus Cancel button
        pyautogui.press('tab')
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
        
