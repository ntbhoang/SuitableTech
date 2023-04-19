from pages.suitable_tech.user.user_template_page import UserTemplatePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from common.application_constants import ApplicationConst


class _WelcomeToBeamPageLocator(object):
    _lblWelcomeMessage = (By.XPATH, "//div[@class='alert-box success']")  
    _chkAcceptRisks = (By.ID, "id_accept_risks")
    _btnPlayVideo = (By.XPATH, "//button[@aria-label='Play']")
    _lblHeader = (By.XPATH, "//section[@class='masthead info']//h2") 
    _btnSetting = (By.XPATH, "//button[@aria-label='Settings']")
    _btnSpeed = (By.XPATH, "//span[.='1x']/../../button[@class='w-accordion__item__head w-css-reset-button-important w-vulcan-v2-button']")
    _btnSpeedx2 = (By.XPATH, "//button[.='2x']")
    _txtFirstName = (By.XPATH, "//input[@id='id_first_name']")
    _txtLastName = (By.XPATH, "//input[@id='id_last_name']")
    
    @staticmethod
    def _btnContinue():
        return (By.XPATH, u"//button[@id='submit' and contains (.,'{}')]".format(ApplicationConst.LBL_PLAY_VIDEO_CONTINUE))
    
class WelcomeToBeamPage(UserTemplatePage):
    """
    @description: This is page object class for Welcome To Beam page. 
        This page will be opened after setting up password for new User.
        Please visit https://staging.suitabletech.com/welcome/ for more details.
    @page: Welcome To Beam page
    @author: Thanh Le
    @created: Jan-06-2017
    """
    
    
    """    Properties    """    
    @property
    def _txtLastName(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._txtLastName)  
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._txtFirstName)  
    @property
    def _lblHeader(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._lblHeader)    
    @property
    def _lblWelcomeMessage(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._lblWelcomeMessage)  
    @property
    def _chkAcceptRisks(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._chkAcceptRisks)  
    @property
    def _btnContinue(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._btnContinue())  
    @property
    def _btnPlayVideo(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._btnPlayVideo)
    @property
    def _btnSetting(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._btnSetting)
    @property
    def _btnSpeed(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._btnSpeed)
    @property
    def _btnSpeedx2(self):
        return Element(self._driver, *_WelcomeToBeamPageLocator._btnSpeedx2)
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver 
        @author: Thanh Le
        @created: Jan-06-2017
        """         
        UserTemplatePage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        #This is to make sure the page loads complete. Please consider when removing.
        self._btnPlayVideo.wait_until_displayed()
        
                        
    def is_welcome_user_page_displayed(self, wait_time = None):
        """
        @summary: Check if welcome user page is displayed
        @parameter:<wait_time>: waiting time
        @return: True if welcome user page is displayed, False for vice versa
        @author: Thanh Le
        @created: Jan-06-2017
        """
        return (self._lblHeader.is_displayed(wait_time) and self._btnPlayVideo.is_displayed(wait_time))
    
    
    def get_welcome_message(self):
        """
        @summary: This action use to get welcome message text
        @author: Thanh Le
        @return: welcome message
        @created: Jan-06-2017
        """
        return self._lblWelcomeMessage.text.split('\n')[1]
    
    
    def watch_video(self, user, simplified=False, had_name=True):
        """
        @summary: This action use to run introduction video
        @author: Thanh Le
        @return: AdminDashboardPage or SimplifiedDashboardPage page object
        @created: Jan-06-2017
        """
        self._driver.scroll_down_to_bottom()
        self._chkAcceptRisks.click_element()
        self.set_double_speed()
        self._btnPlayVideo.click_element()
        
        if not had_name:
            self._txtFirstName.wait_until_displayed()
            self._txtFirstName.type(user.first_name)
            self._txtLastName.click_element()
            self._txtLastName.type(user.last_name)
        
        self._btnContinue.wait_until_clickable(300).click()
               
        if simplified:
            from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
            return SimplifiedDashboardPage(self._driver)
        from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
        return AdminDashboardPage(self._driver)
    
    
    def set_double_speed(self):
        """
        @summary:set double speed for video at welcome page 
        @author: Thanh Le
        @created: Jan-06-2017
        """
        try:
            self._btnSetting.wait_until_clickable()
            self._btnSetting.click()
            self._btnSpeed.click()
            self._btnSpeedx2.click_element()
        except:
            raise('Cannot set double speed.')
        return self

