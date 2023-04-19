from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from core.webdriver.elements.element_list import ElementList
from pages.suitable_tech.admin.dialogs.reserve_beam_dialog import ReserveABeamDialog 
from common.constant import Browser, Platform


class SimplifiedDashboardPageLocator(object):
    _lblHeader = (By.XPATH, "//h2[@class='heading ng-binding']")
    _lstDevices = (By.CSS_SELECTOR, ".device-details-container")
    _iconLoading = (By.XPATH, "//div[@class='loading-indicator']/span")
    _lblBeamStatus = (By.XPATH, "//div[@class='text-muted' or @class='text-success']")
    _lnkDownloadtheBeamDesktopSoftware = (By.XPATH, "//div[@class='icon-link-icon']/a[@href='/installers/']") 
    _lblBeamsName = (By.CSS_SELECTOR, '.beam-gallery h3')
    _lnkGetHelp = (By.CSS_SELECTOR, ".icon-link-icon a[href='/support/']")
    _lnkAddABeam = (By.CSS_SELECTOR, "//div[@class='icon-link-icon']/a[@href[starts-with(., '/setup/link')]]")
    _imgBeam = (By.XPATH, "//img[@src='//dm92u2vspm71b.cloudfront.net/static/site_admin_frontend/img/addBeam.svg']")
    _blckWelcomeToBeam = (By.CSS_SELECTOR, "dismissible[key='dashboard-advanced']")
    _blckWelcomeToBeamContent = (By.XPATH, ".//dismissible/div[@class='dismissible']/ng-transclude/div")
    _btnAddABeam = (By.XPATH, "//div[@ng-if='user.is_admin']//a/img/..")

    @staticmethod
    def _btnManagebyId(value):
        return (By.XPATH, u"//a[@class='btn btn-block btn-primary hidden-xs ng-scope' and @href='#/devices/{}/']".format(value))
    @staticmethod
    def _lblDeviceTitle(value):
        return (By.XPATH, u"//h3[@class='device-title ng-binding'][.=\"{}\"]".format(value))
    @staticmethod
    def _btnReserveThisBeam(value):
        return (By.XPATH, u"//h3[@class='device-title ng-binding' and .=\"{}\"]/..//button[@ng-click='createReservation(device)']".format(value))
    @staticmethod
    def _btnAddUser(beam_name):
        return (By.XPATH, u"//h3[text()=\"{}\"]/..//button[@ng-click='addSelectedUser()']".format(beam_name))
    @staticmethod
    def _btnMAddUser(beam_name):
        return (By.XPATH, u"//h3[text()='{}']/../../..//div[@class='row visible-xs ng-scope']//button[@ng-click='addSelectedUser()']".format(beam_name))
    @staticmethod
    def _txtInvitedEmail(beam_name):
        return (By.XPATH, u"//h3[text()=\"{}\"]/..//input[@ng-model='userToAdd']".format(beam_name))
    @staticmethod
    def _txtMInvitedEmail(beam_name):
        return (By.XPATH, u"//h3[text()='{}']/../../following-sibling::div[@class='row visible-xs ng-scope']//input[@class='form-control ng-pristine ng-untouched ng-valid ng-empty']".format(beam_name))
    @staticmethod
    def _lstUserDisplay(user_email):
        return (By.XPATH,u"//li[@role='option' and contains(normalize-space(),\"{}\")]".format(user_email))

    """MOBILE UI"""
    @staticmethod
    def _btnMManagebyId(value):
        return (By.XPATH, u"//a[@class='btn btn-primary visible-xs ng-scope' and @href='#/devices/{}/']".format(value))
    
class SimplifiedDashboardPage(AdminTemplatePage):
    """
    @description: This is page object class for Simplified DashBoard Page.
    This page appear when logging by Simplified User and go to Dashboard page
    @page:  Simplified DashBoard Page
    @author: Thanh Le
    """
    
    
    """    Properties    """
    def _btnManagebyId(self, value):
        return Element(self._driver, *SimplifiedDashboardPageLocator._btnManagebyId(value))
    def _lstDevices(self):
        return ElementList(self._driver, *SimplifiedDashboardPageLocator._lstDevices)
    def _lblBeamsName(self):
        return ElementList(self._driver, *SimplifiedDashboardPageLocator._lblBeamsName)
    def _btnReserveThisBeam(self, beam_name):
        return Element(self._driver, *SimplifiedDashboardPageLocator._btnReserveThisBeam(beam_name))
    def _btnAddUser(self, beam_name):
        return Element(self._driver, *SimplifiedDashboardPageLocator._btnAddUser(beam_name))
    def _btnMAddUser(self, beam_name):
        return Element(self._driver, *SimplifiedDashboardPageLocator._btnMAddUser(beam_name))
    def _txtInvitedEmail(self, beam_name):
        return Element(self._driver, *SimplifiedDashboardPageLocator._txtInvitedEmail(beam_name))
    def _txtMInvitedEmail(self, beam_name):
        return Element(self._driver, *SimplifiedDashboardPageLocator._txtMInvitedEmail(beam_name))
    @property
    def _lnkGetHelp(self):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lnkGetHelp)
    @property
    def _lnkAddABeam(self):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lnkAddABeam)            
    @property
    def _lblHeader(self):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lblHeader)
    @property
    def _lblBeamStatus(self):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lblBeamStatus)
    @property
    def _lnkDownloadtheBeamDesktopSoftware(self):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lnkDownloadtheBeamDesktopSoftware)
    @property
    def _imgBeam(self):
        return Element( self._driver, *SimplifiedDashboardPageLocator._imgBeam)
    @property
    def _blckWelcomeToBeamContent(self):
        return Element( self._driver, *SimplifiedDashboardPageLocator._blckWelcomeToBeamContent)
    @property
    def _blckWelcomeToBeam(self):
        return Element( self._driver, *SimplifiedDashboardPageLocator._blckWelcomeToBeam)
    @property
    def _btnAddABeam(self):
        return Element(self._driver, *SimplifiedDashboardPageLocator._btnAddABeam)

    def _lblDeviceTitle(self, value):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lblDeviceTitle(value))
    
    def _lstUserDisplay(self, user_email):
        return Element(self._driver, *SimplifiedDashboardPageLocator._lstUserDisplay(user_email))

    """MOBILE UI"""
    def _btnMManagebyId(self, beamID):
        return Element(self._driver, *SimplifiedDashboardPageLocator._btnMManagebyId(beamID))       
        
        
    """    Methods    """
    def __init__(self, driver, wait_for_loading_completely = True):    
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        AdminTemplatePage.__init__(self, driver)
        self._lnkDownloadtheBeamDesktopSoftware.wait_until_displayed()
        if wait_for_loading_completely:
            self._lblBeamStatus.wait_until_displayed()
    
    
    def can_manage_device(self, beam_id):
        """
        @summary: check that 'Manage' button for a beam exist or not
        @return: Return True if Manage button exit otherwise return False
        @author: Thanh Le        
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            return self._btnManagebyId(beam_id).is_displayed()
        else:
            return self._btnManagebyId(beam_id).is_displayed()
    
    
    def get_number_of_devices_displayed(self):
        """
        @summary: get the number of device in dashboard page by getting all 'Manage' buttons 
        @return: return all Manage buttons in dashboard page
        @author: Thanh Le
        """
        return self._lstDevices().count(10)    
        
    
    def goto_manage_beam_page(self, beam_id):
        """
        @summary: This action is used to go to manage beam page   
        @author: Thanh Le
        @parameter: <beam_name>: beam name string
        @return SimplifiedBeamDetailPage page object
        """
        try:
            if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
                self._btnMManagebyId(beam_id).wait_until_displayed(15)
                self._btnMManagebyId(beam_id).scroll_to()
                self._btnMManagebyId(beam_id).wait_until_clickable().click_element()
                self._btnMManagebyId(beam_id).wait_until_disappeared()
                if self._btnMManagebyId(beam_id).is_displayed(5):
                    self._btnMManagebyId(beam_id).click_element()
            else:    
                self._btnManagebyId(beam_id).wait_until_displayed(15)
                self._btnManagebyId(beam_id).scroll_to()
                self._btnManagebyId(beam_id).wait_until_clickable().click_element()
                self._btnManagebyId(beam_id).wait_until_disappeared()
                self._iconLoading.wait_until_disappeared()
                if self._btnManagebyId(beam_id).is_displayed(5):
                    self._btnManagebyId(beam_id).click_element()
            from pages.suitable_tech.admin.simplified.beams.simplified_beam_detail_page import SimplifiedBeamDetailPage
            SimplifiedBeamDetailPage(self._driver)._btnEdit.wait_until_displayed(10)
            return SimplifiedBeamDetailPage(self._driver)
        except Exception as ex:
            self._driver.save_screenshot()
            raise ex


    def is_page_displayed(self, time_out=None):
        """
        @summary: Check if a page is displayed or not
        @param time_out: time out to wait
        @return: True: the page is displayed, False: the page is not displayed    
        @author: Thanh Le
        @created_date: 8/17/2016
        """
        return (self._lnkDownloadtheBeamDesktopSoftware.is_displayed(time_out) and self._lnkGetHelp.is_displayed(time_out))

    
    def is_beam_displayed(self, beam_name):
        list_beams = self._lblBeamsName().get_all_elements()
        for item in list_beams:
            if item.text == beam_name:
                return True
        return False    
        
    
    def open_beam_help_center_page(self):
        """
        @summary: This action is used to go Beam Help Center page
        @author: Thanh Le
        @return: BeamHelpCenterPage page object
        """
        self._lnkGetHelp.click()
        from time import sleep
        sleep(5)
        self._driver.switch_to_window(1)
        self._driver.maximize_window()
        from pages.suitable_tech.user.beam_help_center_page import BeamHelpCenterPage
        return BeamHelpCenterPage(self._driver)
    
    
    def is_device_title_displayed(self, device_title, wait_time_out=5):
        """
        @summary: Check if device title is displayed
        @author: Thanh Le
        @parameter: <device_title>: string device title
                    <wait_time_out>: waiting time
        @return: True if device title displayed, False for vice versa
        """
        return self._lblDeviceTitle(device_title).is_displayed(wait_time_out)


    def is_btn_reserve_this_beam_displayed(self, beam_name, wait_time_out=5):
        """
        @summary: Check if Reserve This Beam button displays for specific beam 
        @author: Tan Le
        @parameter: <beam_name>: string device name
                    <wait_time_out>: waiting time
        @return: True if dReserve This Beam button displays, False for vice versa
        """
        return self._btnReserveThisBeam(beam_name).is_displayed(wait_time_out)


    def is_welcome_to_beam_block_display(self):
        """
        @summary: Check if the Welcome To Beam block displays or not
        @return: True: the Welcome To Beam block displays, False: the Welcome To Beam block does not display
        @author: Thanh Le
        """
        return self._blckWelcomeToBeam.is_displayed()


    def is_welcome_to_beam_block_image_display(self):
        """
        @summary: Check if the Welcome To Beam block image displays or not
        @return: True: the Welcome To Beam block image displays, False: the Welcome To Beam block image does not display
        @author: Thanh Le
        """
        return self._imgBeam.is_displayed()


    def get_welcome_to_beam_block_content(self):
        """
        @summary: Get content of Welcome To Beam block
        @return: Content of Welcome To Beam block
        @author: Thanh Le
        """
        return self._blckWelcomeToBeamContent.text


    def goto_download_page(self):
        """
        @summary: click on 'Download' in simplified dashboard page to open 'Beam Software Installers' page
        @author: Thanh Le
        """
        self._lnkDownloadtheBeamDesktopSoftware.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.simplified.dashboard.beam_software_installers_page import BeamSoftwareInstallersPage
        return BeamSoftwareInstallersPage(self._driver)
        
    def is_welcome_to_beam_block_dismiss(self):
        """
        @summary: Check if the Welcome To Beam block dismisses or not
        @return: True: the Welcome To Beam block dismisses, False: the Welcome To Beam block still displays
        @author: Thanh Le
        """
        return not self._blckWelcomeToBeam.is_displayed(2)
    
    def open_reserve_beam_dialog(self, beam_name):
        """
        @summary: Open Reserve Beam dialog 
        @author: Tan Le
        @parameter: <beam_name>: string device name
        @return: True if Reserve This Beam button displays, False for vice versa
        @author: Tan Le
        @created_date: 9/19/2017
        """
        self._btnReserveThisBeam(beam_name).wait_until_clickable().click()
        dlg = ReserveABeamDialog(self._driver)
        if not dlg.is_dialog_displayed(2):
            self._btnReserveThisBeam(beam_name).jsclick()
        return dlg
    
    
    def reserve_a_beam(self, reservation):
        reserve_beam_dialog = self.open_reserve_beam_dialog(reservation.beam_name)
        reserve_beam_dialog.reserve_a_beam(reservation.start_time, reservation.end_time)
        return self


    def add_user(self, user, beam_name, wait_for_completed=True, wait_user_display=False):
        """
        @summary: This action is used to add user
        @param: user: user object
        @param beam_name: name of beam is used to invite user
        @return: SimplifiedBeamDetailPage
        @author: Khoi Ngo
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._txtMInvitedEmail(beam_name).send_keys(user.email_address)
            self._btnMAddUser(beam_name).click()
        else:
            if(self._driver._driverSetting.browser_name == Browser.Safari):
                self._txtInvitedEmail(beam_name).type(user.email_address)
            else:
                self._txtInvitedEmail(beam_name).slow_type(user.email_address)

                if (wait_user_display):
                    self._lstUserDisplay(user.email_address).is_displayed(20)
                    self._lstUserDisplay(user.email_address).click()

            self._btnAddUser(beam_name).click()

        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared(60)

        return self


    def is_add_a_beam_button_display(self):
        """
        @summary: Check if the Add A Beam button displays or not
        @return: True: the Add A Beam button displays, False: the Add A Beam button does not display
        @author: Thanh Le
        """
        return self._btnAddABeam.is_displayed()

