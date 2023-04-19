from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase


class _ConfirmActionDialogLocator(object):
    _btnContinue = (By.CSS_SELECTOR, ".modal-content .btn.btn-primary.ng-binding")
    _lblDialogMessage = (By.XPATH, "//div[@class='modal-content']//div[@ng-show='content']")
    
   
class ConfirmActionDialog(DialogBase):
    """
    @description: This is page object class for Confirm action Dialog. You need to init it before using in page class.
    @page: Confirm action Dialog
    @author: Thanh Le
    @created: Jan-06-2017
    """
    
    
    """    Properties    """
    @property
    def _btnContinue(self):
        return Element(self._driver, *_ConfirmActionDialogLocator._btnContinue)
    @property
    def _lblDialogMessage(self):
        return Element(self._driver, *_ConfirmActionDialogLocator._lblDialogMessage)
    
    
    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        @created: Jan-06-2017
        """      
        DialogBase.__init__(self, driver)
        self._btnContinue.wait_until_displayed()
    
    
    def get_dialog_message(self, continue_dialog=True):
        """      
        @summary: get dialog message  
        @param continue_dialog: the way close message
                True: Close dialog via click on continue button
                False: Close dialog via click on cancel button
        @return: dialog message
        @author: Thanh Le
        @created: Jan-06-2017
        """   
        self._lblDialogMessage.wait_until_displayed()
        msg = self._lblDialogMessage.text
        if(continue_dialog):
            self.continue_dialog(continue_dialog)
        else:
            self.cancel()
            
        return msg
    
    
    def continue_dialog(self, wait_for_dialog = True):
        """      
        @summary: clicking on continue button  
        @author: Thanh Le
        @created: Jan-06-2017
        """   
        self._btnContinue.click_element()
        if wait_for_dialog:
            self._wait_for_dialog_disappeared()

