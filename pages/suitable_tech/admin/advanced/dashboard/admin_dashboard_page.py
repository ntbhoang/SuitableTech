from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.admin_template_page import AdminTemplatePage
from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
from common.constant import Language, Constant, Browser
from core.webdriver.elements.element_list import ElementList
from core.webdriver.elements.notification_records import NotificationRecords
from time import sleep
from common.application_constants import ApplicationConst
from core.suitabletechapis.user_api import UserAPI

class _AdminDashboardPageLocator(object):
    _btnInviteANewUser = (By.XPATH, "//button[@ng-click='inviteContact()']")
    _btnInviteATempUser = (By.XPATH, "//button[@ng-click='createTemporaryAccess()']")
    _btnImportUsers = (By.XPATH, "//button[@ng-click='importContacts()']")
    _lnkAddABeam = (By.XPATH, ".//dismissible//ng-transclude//h4[@ng-if='currentUser.is_admin']/a")
    _lnkDownloadtheBeamDesktopSoftware = (By.XPATH,".//dismissible//ng-transclude//h4/a[@href='/installers/']")
    _lnkYourAccount = (By.XPATH, "//ul[@class='dropdown-menu']/li/a[@href='#/account/settings/']/span[@class='ng-scope']")
    _lblPageTitle = (By.XPATH, "//h3//translate")
    _btnsReject = (By.XPATH, "//button[@ng-click='rejectAccessRequest(request.secret)']")
    _lblHeader = (By.XPATH, "//div[@class='row secondary-nav']//h3")
    _lblAccessRequestRecord = (By.XPATH, "//div[@ng-repeat='request in accessRequests']")
    _imgBeam = (By.XPATH, "//img[@src='//dm92u2vspm71b.cloudfront.net/static/site_admin_frontend/img/addBeam.svg']")
    _blckWelcomeToBeamContent = (By.XPATH, ".//dismissible/div[@class='dismissible']/ng-transclude/div")
    _btnHelp = (By.XPATH, ".//a[@href='https://support.suitabletech.com/']")

    @staticmethod
    def _btnRejectRequestedAccess(user_email):
        return (By.XPATH, u"//div[@ng-repeat='request in accessRequests']//em[contains(text(),'{}')]/../../..//button[@ng-click='rejectAccessRequest(request.secret)']".format(user_email))   
    @staticmethod
    def _btnApproveRequestAccess(user_email):
        return (By.XPATH, u"//div[@ng-repeat='request in accessRequests']//em[contains(text(),'{}')]/../../..//button[@ng-click='approveAccessRequest(request.secret)']".format(user_email)) 
    @staticmethod
    def _btnRejectRequestedReservation(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::div[@ng-repeat='request in reservationRequests']//button[@class='btn btn-danger']".format(username))
    @staticmethod
    def _btnAddABeam(orgsinfo):
        return (By.XPATH, u"//a[@href=\"/setup/link?o={}\"]/button".format(orgsinfo))

class AdminDashboardPage(AdminTemplatePage):
    """
    @description: This is page object class for Admin Dashboard page.
        This page will be opened after clicking signning in as Administrator.
        Please visit https://staging.suitabletech.com/manage/#/dashboard/ for more details.
    @page: Admin Dashboard page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_AdminDashboardPageLocator._lblHeader)
    @property
    def _btnInviteANewUser(self):
        return Element(self._driver, *_AdminDashboardPageLocator._btnInviteANewUser)
    @property
    def _btnInviteATempUser(self):
        return Element(self._driver, *_AdminDashboardPageLocator._btnInviteATempUser)
    @property
    def _btnImportUsers(self):
        return Element(self._driver, *_AdminDashboardPageLocator._btnImportUsers)
    @property
    def _lnkYourAccount(self):
        return Element(self._driver, *_AdminDashboardPageLocator._lnkYourAccount)
    @property
    def _lnkAddABeam(self):
        return Element(self._driver, *_AdminDashboardPageLocator._lnkAddABeam)
    @property
    def _lnkDownloadtheBeamDesktopSoftware(self):
        return Element(self._driver, *_AdminDashboardPageLocator._lnkDownloadtheBeamDesktopSoftware)
    @property
    def _lblPageTitle(self):
        return Element(self._driver, *_AdminDashboardPageLocator._lblPageTitle)
    @property
    def _btnsReject(self):
        return ElementList(self._driver, *_AdminDashboardPageLocator._btnsReject)
    @property
    def _lblAccessRequestRecord(self):
        return NotificationRecords( self._driver, *_AdminDashboardPageLocator._lblAccessRequestRecord)  
    @property
    def _imgBeam(self):
        return Element( self._driver, *_AdminDashboardPageLocator._imgBeam)
    @property
    def _blckWelcomeToBeamContent(self):
        return Element( self._driver, *_AdminDashboardPageLocator._blckWelcomeToBeamContent)
    @property
    def _btnHelp(self):
        return Element( self._driver, *_AdminDashboardPageLocator._btnHelp)
    
    def _btnRejectRequestedReservation(self, username):
        return Element(self._driver, *_AdminDashboardPageLocator._btnRejectRequestedReservation(username))   
    def _btnAddABeam(self, orgsinfo):
        return Element(self._driver, *_AdminDashboardPageLocator._btnAddABeam(orgsinfo))
    def _btnApproveRequestAccess(self, user_email):
        return Element(self._driver, *_AdminDashboardPageLocator._btnApproveRequestAccess(user_email))
    
    """    Methods    """
    def __init__(self, driver):        
        """      
        @summary: Constructor method      
        @param driver: Web driver
        @author: Thanh Le 
        """
        AdminTemplatePage.__init__(self, driver)      
#         self._lblHeader.wait_until_displayed()
    
    
    def open_invite_a_new_user_dialog(self):
        """      
        @summary: Open the Invite a New User form by click 'Invite a New User' button
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        self._btnInviteANewUser.wait_until_clickable().click_element()
        return self
        
    
    def enter_invite_user_info(self, user):
        """      
        @summary:  Fill out user info on Invite New User form 
        @param user: user would like to invite
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        invite_user_dialog = InviteNewUserDialog(self._driver)        
        invite_user_dialog.enter_invite_information(user)
        return self
    
    
    def is_invite_user_button_disabled(self):
        """      
        @summary: Check if the Invite User button is disabled or not
        @return: True: the Invite User button is disabled, False: the Invite User button is enabled
        @author: Thanh Le
        """
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        return InviteNewUserDialog(self._driver).is_invite_user_button_disabled()      
    
    
    def cancel_invite_user_dialog(self):
        """      
        @summary: Cancel on the Invite a New User form
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        InviteNewUserDialog(self._driver).cancel()
    
    
    def invite_new_user(self, user, wait_for_completed=True):
        """      
        @summary:  Invite a new user       
        @param user: user would like to invite
        @param wait_for_completed: time to wait for complete inviting
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        self.open_invite_a_new_user_dialog()
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        invite_user_dialog = InviteNewUserDialog(self._driver)        
        invite_user_dialog.submit_invite_information(user, wait_for_completed)
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
        
        return self


    def invite_new_device_group_admin_user(self, user, wait_for_completed=True):
        """      
        @summary: Invite a new device group admin user  
        @param user: user who would like to invite
        @param wait_untill_success_msg_disappeared: dismiss the successful message or not
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        return self.invite_new_user(user, wait_for_completed)\
            .goto_settings_tab_of_a_device_group(user.device_group)\
            .add_administrator(user, wait_for_completed)
    
    
    def get_page_title(self):
        """      
        @summary: Get title of a page     
        @return: Title of page
        @author: Thanh Le
        """
        return self._lblPageTitle.text
    

    def get_organization_name(self):
        """      
        @summary: Get title of a page     
        @return: Title of page
        @author: Thanh Le
        """
        return self.get_page_title().replace(ApplicationConst.LBL_DASHBOARD_TEXT, "")
    
    
    def import_users(self, data_file_path, new_device_group, new_user_group, wait_message=True, jsclick=False):
        """      
        @summary: Import users    
        @param 
            - data_file_path: file path of imported file
            - new_device_group: device group would like to add imported user to
            - new_user_group: user group would like to add imported user to
        @return: AdminDashboardPage
        @author: Thanh Le
        """
        if self._driver.driverSetting.browser_name == Browser.Edge:
            jsclick = False
            sleep(1)

        if jsclick:
            sleep(1)
            self._btnImportUsers.jsclick()
        else:
            self._btnImportUsers.wait_until_clickable().click_element()
        
        from pages.suitable_tech.admin.dialogs.import_users_dialog import ImportUsersDialog
        ImportUsersDialog(self._driver).submit_users_from_file(data_file_path, new_device_group, new_user_group)
        if wait_message:
            self.wait_untill_success_msg_disappeared()
        
        return self
    
    
    def import_users_expecting_error(self, data_file_path):
        """      
        @summary: Import an invalid user file   
        @param data_file_path: path to imported file
        @return: AdminDashboardPage
        """
        self._btnImportUsers.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.dialogs.import_users_dialog import ImportUsersDialog
        ImportUsersDialog(self._driver).submit_users_from_invalid_file(data_file_path)
        return self
    
    
    def invite_temporary_user(self, user, start_date=None, end_date=None, link_to_beam_sofware=None, default_invitation=None, require_session_answer=None, device_group=None):
        """
        @summary: Invite a temporary user        
        @param user: The temporary user
        @param start_date: Staring date
        @param end_date: Ending date
        @param link_to_beam_sofware: Include a link to the Beam software checkbox [True/False]
        @param default_invitation: Include the default invitation message checkbox [True/False]
        @param require_session_answer: Require session answer checkbox [True/False]        
        @return: AdminBeamAccessTimesPage
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._btnInviteATempUser.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.dialogs.invite_a_temporary_user import InviteTempUserDialog
        InviteTempUserDialog(self._driver).submit_invite_information(user, start_date, end_date, link_to_beam_sofware, default_invitation, require_session_answer, device_group)
        return self
    
    
    def  goto_link_a_beam_page(self, org_info=Constant.OrgsInfo[Constant.AdvancedOrgName]):
        """
        @summary: click on 'Add a Beam' in admin dashboard page to open 'Link A Beam With Your Account' Dialog
        @return: LinkABeamWithYourAccountDialog
        @author: Thanh Le
        @created_date: August 17, 2016
        """        
        self._btnAddABeam(org_info).wait_until_clickable().click_element()
        from pages.suitable_tech.admin.link_a_beam_with_your_account_page import LinkABeamWithYourAccountPage
        if not LinkABeamWithYourAccountPage(self._driver)._btnLinkYourBeam.is_displayed(3):
            self._btnAddABeam.jsclick()
        return LinkABeamWithYourAccountPage(self._driver)
        

    def is_page_displayed(self, time_out=None):
        """
        @summary: Check if a page is displayed or not
        @param time_out: time out to wait
        @return: True: the page is displayed, False: the page is not displayed    
        @author: Duy Nguyen
        @created_date: August 17, 2016
        """
        return self._lblHeader.is_displayed(time_out)


    def _set_user_language(self):
        """
        @summary: Set language for new User. This is a workarround for defect BUG_35
        @return: WelcomeToBeamPage    
        @author: Thanh Le
        @created_date: Sep 21, 2016
        """
        if(self._driver._driverSetting.language == Language.ENGLISH):
            return WelcomeToBeamPage(self._driver)
        else:
            #welcome_to_beam_url = self._driver.current_url
            WelcomeToBeamPage(self._driver).goto_account_settings_page_by_menu_item()\
                .set_language(self._driver._driverSetting.language).save_change()
            
            self._driver.get(Constant.SuitableTechWelcomeURL)
            return WelcomeToBeamPage(self._driver)
    
    
    def is_access_request_displayed(self, user):
        """
        @summary: Check whether the access request recoded is displayed or not
        @param user: User object
        @return: True if found. Otherwise, return False    
        @author: Thanh Le
        @created_date: Sep 21, 2016
        """
        return self._lblAccessRequestRecord.does_record_exist(user)
    
    
    def reject_a_requested_reservation(self, user):
        """
        @summary: Reject a requested reservation
        @param user: User object
        @return: AdminDashboardPage    
        @author: Thanh Le
        @created_date: March 23, 2017
        """
        self._btnRejectRequestedReservation(UserAPI.get_displayed_name(user)).wait_until_clickable().click()
        if not self._btnRejectRequestedReservation(UserAPI.get_displayed_name(user)).is_disappeared(2):
            self._btnRejectRequestedReservation(UserAPI.get_displayed_name(user)).jsclick()
        return self
        
        
    def reject_all_access_requests(self):
        """
        @summary: Reject all existing access requests
        @return: AdminDashboardPage    
        @author: Thanh Le
        @created_date: Otc 05, 2016
        """
        all_reject_buttons = self._btnsReject.get_all_elements()
        if(len(all_reject_buttons) > 0):
            for _ in range(len(all_reject_buttons)):
                reject_button = self._btnsReject.get_element_at(0)
                reject_button.click()
                self.wait_untill_success_msg_disappeared()

    
    def is_access_request_existed(self, wait_time_out=5):
        """
        @summary: check access request access in Beam dashboard/Notification 
        @param wait_time_out: time to wait
        @return: True/False
        @author: Thanh Le
        @created_date: Otc 05, 2016
        """
        return (self._btnsReject.get_all_elements(wait_time_out) != [])
        
    
    def submit_primary_org_contact_info(self, info):
        from pages.suitable_tech.admin.dialogs.primary_organization_contact_dialog import PrimaryOrganizationContactDialog
        PrimaryOrganizationContactDialog(self._driver).submit_primary_org_contact_info(info)
        return self


    def open(self):
        """
        @summary: This action use to navigate ST page
        @return AdminDashboardPage page object
        @author: Thanh Le
        """
        self._driver.get(Constant.SuitableTechURL)
        self._lblPageTitle.wait_until_displayed()
        return self

    def is_welcome_to_beam_block_image_display(self):
        """
        @summary: Check if the Welcome To Beam block image displays or not
        @return: True: the Welcome To Beam block image displays, False: the Welcome To Beam block image does not display
        @author: Thanh Le
        """
        if self._imgBeam.is_displayed():
            return True
        return False


    def get_welcome_to_beam_block_content(self):
        """
        @summary: Get content of Welcome To Beam block
        @return: Content of Welcome To Beam block
        @author: Thanh Le
        """
        return self._blckWelcomeToBeamContent.text


    def  goto_download_page(self):
        """
        @summary: click on 'Download' in admin dashboard page to open 'Beam Software Installers' page
        @author: Thanh Le
        """
        self._lnkDownloadtheBeamDesktopSoftware.wait_until_clickable().click_element()
        sleep(3)

    def  goto_link_a_beam_page_by_link(self):
        """
        @summary: click on 'Link a new Beam' in admin dashboard page to open 'Link a Beam' page
        @author: Thanh Le
        """
        self._lnkAddABeam.wait_until_clickable().click_element()
        sleep(3)

    def  goto_beam_help_center(self):
        """
        @summary: click on 'Help' button in admin dashboard page to open 'Beam help center' page
        @author: Thanh Le
        """
        self._btnHelp.wait_until_clickable().click_element()
        self._btnHelp.wait_until_disappeared()
        return self


    def is_add_a_beam_button_display(self, orgsinfo=Constant.OrgsInfo[Constant.AdvancedOrgName]):
        """
        @summary: Check if the Add A Beam button displays or not
        @return: True: the Add A Beam button displays, False: the Add A Beam button does not display
        @author: Thanh Le
        """
        return self._btnAddABeam(orgsinfo).is_displayed()


    def approve_request_access_device_group(self, user_name):
        """
        @summary: Approve request access to device group
        @author: Quang Tran
        """
        self._btnApproveRequestAccess(user_name).wait_until_clickable().click()
        return self

