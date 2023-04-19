from core.webdriver.elements.element import Element
from selenium.webdriver.common.by import By
from common.constant import Browser
from common.stopwatch import Stopwatch
from selenium.webdriver.common.keys import Keys
import urllib


class BasePage(object):
    """
    @description: This class is ONLY for inheriting.
    @page: Base of all pages
    @author: Thanh Le
    """


    """    Chat box    """
    @property
    def _lblChatboxHeader(self):
        if self._driver._driverSetting.browser_name == Browser.Safari:
            return Element(self._driver, By.XPATH, "//div[@id='olark']")
        return Element(self._driver, By.XPATH, "//div[@id='olark-wrapper']/button")
    
    """Narvigation bar on Mobile"""
    @property
    def _btnMNarBar(self):
        return Element(self._driver, By.XPATH, "//button[@class='navbar-toggle']")


    def __init__(self, driver):
        """
        @summary: Constructor method  
        @parameter: <driver> : web driver
        @author: Thanh Le
        """
        self._driver = driver


    def get_dialog_message(self, close_dialog=True):
        """
        @summary: This action use to get web driver dialog message
        @parameter: <close_dialog>: close or keep dialogs with Boolean value
        @author: Thanh Le    
        @return: dialog message
        """
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        return ConfirmActionDialog(self._driver).get_dialog_message(close_dialog)


    def goto_request_access_page(self, request_access_link):
        """
        @summary: This action use to go to Request Beam Access page
        @parameter: <request_access_link>: url link to go Request Beam Access Page
        @author: Thanh Le
        @return: RequestBeamAccessPage     
        """
        self._driver.get(request_access_link)
        from pages.suitable_tech.user.request_beam_access import RequestBeamAccessPage
        return RequestBeamAccessPage(self._driver)


    def wait_page_ready(self, timeout=30):
        """
        @summary: This action use to wait a page ready
        @author: Thanh Le
        """
        try:
            sw = Stopwatch()
            sw.start()
            while(timeout > 0):
                page_state = self._driver.execute_script('return document.readyState;')
                if page_state == 'complete':
                    break
                timeout -= sw.elapsed().total_seconds()
        except Exception as ex:
            raise ex


    def get_clip_board_value(self):
        """
        @summary: This action use to get system clipboard
        @author: Thanh Le
        """
        self._driver.execute_script("var para = document.createElement('input'); para.setAttribute('id','logigear_input'); document.body.appendChild(para);")
        ele = self._driver.find_element(value = 'logigear_input')
        ele.send_keys(Keys.CONTROL, 'v')
        return str(ele.get_attribute('value'))


    def get_status_code(self, link):
        """
        @summary: get status code
        @return: return status code, example 200 for successful
        @author: Thanh Le
        """
        try:
            return urllib.request.urlopen(link).code
        except Exception as ex:
            return (str(ex))

