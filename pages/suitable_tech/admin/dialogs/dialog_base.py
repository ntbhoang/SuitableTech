from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element


class _DialogBaseLocaltor(object):
    _icnLoading = (By.XPATH, "//div[@class='modal-content']//div[@class='loading-indicator']/span")
    _btnCancel = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='back($event)' or @ng-click='cancel()' or @ng-click='cancelFn()' or @ng-click='dismiss()']")
    _btnSubmitChanges = (By.XPATH, "//div[@class='modal-content']//button[@type='submit']")
    _dialog = (By.XPATH, "(//div[@class='modal-content'])[1]")
    _btnCloseHelpDialog = (By.XPATH,"//button[@ng-click=\"$close('cancel')\"]")
  
   
class DialogBase(object):
    """
    @description: This is page object class of dialog base. This class is ONLY for inheriting.
    @page: Dialog Base
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _icnLoading(self):
        return Element(self._driver, *_DialogBaseLocaltor._icnLoading)
    @property
    def _btnCancel(self):
        return Element(self._driver, *_DialogBaseLocaltor._btnCancel)
    @property
    def _btnSubmitChanges(self):
        return Element(self._driver, *_DialogBaseLocaltor._btnSubmitChanges)
    @property
    def _dialog(self):
        return Element(self._driver, *_DialogBaseLocaltor._dialog)
    @property
    def _btnCloseHelpDialog(self):
        return Element(self._driver, *_DialogBaseLocaltor._btnCloseHelpDialog)
    
    
    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """             
        self._driver = driver
        self._wait_for_dialog_appeared()
    
    
    def submit(self, wait_for_completed=True):
        """
        @summary: This action is used to click submit button
        @author: Thanh Le
        @parameter: wait_for_completed: boolean value to decide wait or not
        """
        self._btnSubmitChanges.wait_until_clickable()
        self._btnSubmitChanges.jsclick()
        if(wait_for_completed):
            self._wait_for_dialog_disappeared()
    
    
    def cancel(self):
        """
        @summary: This action is used to click cancel button
        @author: Thanh Le
        """
        self._btnCancel.click_element()
        self._wait_for_dialog_disappeared()
    
    
    def is_dialog_displayed(self, timeout=None):
        return self._dialog.is_displayed(timeout)
    
    
    def _wait_for_dialog_appeared(self):
        """
        @summary: This action is used to wait for dialog appeared
        @author: Thanh Le
        """
        self._dialog.wait_until_displayed()
    
    
    def _wait_for_dialog_disappeared(self):
        """
        @summary: This action is used to wait for dialog disappeared
        @author: Thanh Le
        """
        self._dialog.wait_until_disappeared()   
    
    
    def _wait_for_loading_completed(self):
        """
        @summary: This action is used to wait for loading completed
        @author: Thanh Le
        """
        self._icnLoading.wait_until_disappeared()


    def close_help_dialog(self):
        """
        @summary: Method to close Help dialog
        @return: AdminBeamsDevicesPage
        @author: Khoi Ngo
        @created_date: October, 2017
        """
        self._btnCloseHelpDialog.wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_devices_page import AdminBeamsDevicesPage
        return AdminBeamsDevicesPage(self._driver)

