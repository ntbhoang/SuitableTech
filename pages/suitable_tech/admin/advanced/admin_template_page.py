from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_list import ElementList
from core.webdriver.elements.dropdownlist import DropdownList
from common.constant import Browser, Platform, Constant, Language
from time import sleep
from core.utilities.utilities import Utilities
from common.application_constants import ApplicationConst
from dateparser import parse

        
class _AdminTemplateLocator(object):
    """    Top bar left section    """
    _lnkBeam = (By.XPATH, "//a[@class='navbar-brand']")
    _lnkDismissWelcomeBlock = (By.XPATH, "//dismissible[@class='ng-isolate-scope' and @key='dashboard-advanced']//div[@class='dismissPerm' and @ng-click='doNotShowAgain()']/div")
    _lnkDashboard = (By.XPATH, "//a[@href='#/dashboard/']")
    _lnkBeams = (By.XPATH, "//a[@href='#/beams/all/']")
    _lnkUsers = (By.XPATH, "//a[@href='#/contacts/']")
    _lnkActivity = (By.XPATH, "//a[@href='#/activity/']")
    _lblSuccessMessage = (By.XPATH, "//div[@class='alert alert-success']//span[@ng-bind-html='message.content']")
    _lblErrorMessage = (By.XPATH, "//li[@class='ng-toast__message' or @class='ng-toast__message ']//div[@class='alert alert-danger alert-dismissible']//span[@ng-bind-html='message.content']")
    _btnSetting = (By.XPATH, "//ul[@class='nav navbar-nav navbar-right']//a[@href='#/settings/']")
    _iconLoading = (By.XPATH, "//div[@class='loading-indicator']/span")
    _btnDismissMsg =  (By.XPATH, "//button[@ng-if='message.dismissButton']")
    """    Top bar right section    """
    _ddlAdminMenu = (By.XPATH, "//span[@class='glyphicon glyphicon-user']/ancestor::li[contains(@class,'dropdown')]")
    _linkOrgInAdminMenu = (By.XPATH, "//ul[@class='dropdown-menu']//li[@ng-repeat='org in organizations']")
    _lnkOrganizationSettings = (By.XPATH, "//div[@class='hidden-xs ng-scope']//a[@href='#/organization/']")
    _ddlOrganization = (By.XPATH, "//ul[@class='nav navbar-nav navbar-right']/li[@ng-if='organizations.length > 1']")
    _ddlMOrganization = (By.XPATH, "//ul[@class='nav navbar-nav']/li[@ng-show='organizations.length > 1']")
    
    """popup Primary Org Contact"""
    _popupPrimaryOrgContact = (By.XPATH, "//div[@class='organization ng-scope']")
    _btnDismissOrgContact = (By.XPATH, "//div[@class='organization ng-scope']//button[contains(@ng-click,'dismiss')]")
    _btnSaveOrgContact = (By.XPATH, "//div[@class='organization ng-scope']//button[contains(@ng-click,'save')]")
    _ddlSimplifiedSwitchOrgs = (By.XPATH, "//ul[@class='dropdown-menu org-switcher']/..")
    
    """Image icon"""
    _imgUserIcon = (By.XPATH, "//div[@class='profile-image-container ng-isolate-scope editable']//img")
    _btnRemoveImageIcon = (By.XPATH, "//button[@ng-click='removeImage()']")    
    _lnkChangeImage = (By.XPATH, "//span[@class='change-picture-icon fa fa-pencil']/..")

    _iconIconView = (By.XPATH, "//span[@class='glyphicon glyphicon-th-large']/..")
    _iconListView = (By.XPATH, "//span[@class='glyphicon glyphicon-th-list']/..")
    _lstUserIconMode = (By.XPATH, "//div[@class='row ng-scope']//div[@ng-repeat='user in users']")
    _lstUserListMode = (By.XPATH, "//table[@ng-switch-when='list']//tr[@ng-repeat='user in users']")

    _ddlShow = (By.XPATH, "//div[contains(@ng-if, 'showGroups')]")

    @staticmethod
    def _clsActiveTab(tab):
        return (By.XPATH, u"//li[contains(@ng-class,'{}')][@class='active']".format(tab))
    
    """MOBILE UI"""
    _lnkMDashboard = (By.XPATH, "//div[@class='visible-xs ng-scope']//a[@href='#/dashboard/']")
    _lnkMBeams = (By.XPATH, "//div[@class='visible-xs ng-scope']//a[contains(text(),'Beam') and @href='#/beams/all/']")
    _lnkMUsers = (By.XPATH, "//div[@class='visible-xs ng-scope']//a[@href='#/contacts/']")
    _lnkMOrganization = (By.XPATH, "//div[@class='visible-xs ng-scope']//a[@href='#/organization/']")
    _lnkMActivity = (By.XPATH, "//div[@class='visible-xs ng-scope']//a[@href='#/activity/']")
    _lnkMLogout = (By.XPATH, "//ul[@class='nav navbar-nav']//a[@href='/accounts/logout']")
    _lnkMAccountSetting = (By.XPATH, "//ul[@class='nav navbar-nav']//a[@ui-sref='account.settings']")
    _lnkMSwitchOrganization= (By.XPATH,"//a[@ng-model='showOrgs']/..")
    
    @staticmethod
    def _lnkOrganization(org):
        return (By.XPATH, u"//a[@ng-model='showOrgs']/../ul/li//*[contains(., '{}') and @class='ng-binding']".format(org))

class AdminTemplatePage(BasePage):    
    """
    @description: This is page object class that contains all controls and methods shared across all Admin pages.
        This class is ONLY for inheriting.
    @page: Admin Template Page
    @author: Thanh Le
    """

    """    Properties    """ 
    @property
    def _lnkBeam(self):
        return Element( self._driver, *_AdminTemplateLocator._lnkBeam)
    @property
    def _lnkDismissWelcomeBlock(self):
        return Element( self._driver, *_AdminTemplateLocator._lnkDismissWelcomeBlock) 
    @property
    def _popupPrimaryOrgContact(self):
        return Element(self._driver, *_AdminTemplateLocator._popupPrimaryOrgContact)
    @property
    def _btnDismissOrgContact(self):
        return Element(self._driver, *_AdminTemplateLocator._btnDismissOrgContact)
    @property
    def _btnSaveOrgContact(self):
        return Element(self._driver, *_AdminTemplateLocator._btnSaveOrgContact)
    def _clsActiveTab(self, tab):
        return Element(self._driver, *_AdminTemplateLocator._clsActiveTab(tab))
    @property
    def _lnkActivity(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkActivity)
    @property
    def _btnDismissMsg(self):
        return Element(self._driver, *_AdminTemplateLocator._btnDismissMsg)
    @property
    def _iconLoading(self):
        return Element(self._driver, *_AdminTemplateLocator._iconLoading)
    @property
    def _btnSetting(self):
        return Element(self._driver, *_AdminTemplateLocator._btnSetting)
    @property
    def _lblSuccessMessage(self):
        return Element(self._driver, *_AdminTemplateLocator._lblSuccessMessage)
    @property
    def _lblErrorMessage(self):
        return Element(self._driver, *_AdminTemplateLocator._lblErrorMessage)
    @property
    def _lnkBeams(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkBeams)
    @property
    def _lnkDashboard(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkDashboard)
    @property
    def _lnkUsers(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkUsers)
    @property
    def _lnkOrganizationSettings(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkOrganizationSettings)
    @property
    def _ddlOrganization(self):
        return DropdownList(self._driver, *_AdminTemplateLocator._ddlOrganization)
    @property
    def _ddlMOrganization(self):
        return DropdownList(self._driver, *_AdminTemplateLocator._ddlMOrganization)
    @property
    def _ddlAdminMenu(self):
        return DropdownList(self._driver, *_AdminTemplateLocator._ddlAdminMenu)
    @property
    def _ddlSimplifiedSwitchOrgs(self):
        return DropdownList(self._driver, *_AdminTemplateLocator._ddlSimplifiedSwitchOrgs)
    @property
    def _hrefYourAccount(self):
        return "#/account/settings/"
    @property
    def _hrefSignOut(self):
        return "/accounts/logout"

    
    """    Top bar right section    """
    @property
    def _lnkBeamMenuItem(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkBeamMenuItem)

    """Image icon"""
    @property
    def _imgUserIcon(self):
        return Element(self._driver, *_AdminTemplateLocator._imgUserIcon)
    @property
    def _btnRemoveImageIcon(self):
        return Element(self._driver, *_AdminTemplateLocator._btnRemoveImageIcon) 
    @property
    def _lnkChangeImage(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkChangeImage)

    @property
    def _iconIconView(self):
        return Element(self._driver, *_AdminTemplateLocator._iconIconView)
    @property
    def _iconListView(self):
        return Element(self._driver, *_AdminTemplateLocator._iconListView)
    @property
    def _lstUserIconMode(self):
        return ElementList(self._driver, *_AdminTemplateLocator._lstUserIconMode)
    @property
    def _lstUserListMode(self):
        return ElementList(self._driver, *_AdminTemplateLocator._lstUserListMode)

    @property
    def _ddlShow(self):
        return DropdownList(self._driver, *_AdminTemplateLocator._ddlShow)

    """MOBILE UI"""
    @property
    def _lnkMDashboard(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMDashboard)
    @property
    def _lnkMBeams(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMBeams)
    @property
    def _lnkMUsers(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMUsers)
    @property
    def _lnkMOrganization(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMOrganization)
    @property
    def _lnkMActivity(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMActivity)
    @property
    def _lnkMLogout(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMLogout)
    @property
    def _lnkMAccountSetting(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMAccountSetting)
    @property
    def _lnkMSwitchOrganization(self):
        return Element(self._driver, *_AdminTemplateLocator._lnkMSwitchOrganization)

    def _lnkOrganization(self, org):
        return Element(self._driver, *_AdminTemplateLocator._lnkOrganization(org))

    """    Methods      """
    def __init__(self, driver):
        """      
        @summary: Constructor method     
        @param driver: web driver
        @author: Thanh Le
        """
        BasePage.__init__(self, driver)
#         self._lblChatboxHeader.wait_until_displayed()
        
    
    def goto_activity_tab(self):
        """      
        @summary: Click Notifications link to go to Notifications tab        
        @return: AccountNotificationsPage page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()._lnkMActivity.click()
        else:
            self._driver.scroll_up_to_top()
            self._lnkActivity.click_element()
        self.wait_for_loading()
        from pages.suitable_tech.admin.advanced.activity.admin_activity_page import AdminActivityPage 
        return AdminActivityPage(self._driver)
    
    
    def goto_beams_tab(self):
        """      
        @summary: Go to Beams tab         
        @return: All Beams device page
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()
            self._lnkMBeams.click()
        else:
            self._driver.scroll_up_to_top()
            self._lnkBeams.wait_until_clickable().click_element()
            self._clsActiveTab('beams').wait_until_displayed()
        if 'beams/all' not in self._driver.current_url:
            if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
                self._lnkMBeams.jsclick()
            else:
                self._lnkBeams.jsclick()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_all_devices_page import AdminBeamsAllDevicesPage
        return AdminBeamsAllDevicesPage(self._driver)
    

    def is_error_msg_displayed(self, close = True, wait_time = None):
        """      
        @summary: Check if the error message is displayed or not    
        @return: True: the error message is displayed
        @author: Thanh Le
        """
        show = self._lblErrorMessage.is_displayed(wait_time)
        if close and show:
            self._btnDismissMsg.click()
        return show
        
    
    def is_success_msg_displayed(self, wait_time=None):
        """      
        @summary: Check if the successful message is displayed or not    
        @return: True: the successful message is displayed
        @author: Thanh Le
        """
        return self._lblSuccessMessage.is_displayed(wait_time)
    
    
    def get_msg_success(self):
        """      
        @summary: Get content of successful message 
        @return: message 'Device group settings were saved successfully'
        @author: Thanh Le
        """
        self._lblSuccessMessage.wait_until_displayed(5)
        return self._lblSuccessMessage.text


    def get_error_message(self):
        """      
        @summary: Get text on the red warning message
        @return: text
        @author: Thanh Le
        """
        return self._lblErrorMessage.text


    def goto_org_setting_page(self):
        """      
        @summary: Go to setting page of an organization     
        @return: Setting page of org
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()._lnkMOrganization.click()
        else:
            self._driver.scroll_up_to_top()
            self._lnkOrganizationSettings.click()
        from pages.suitable_tech.admin.advanced.organization.admin_organization_setting_page import OrganizationSettingsPage
        return OrganizationSettingsPage(self._driver)
    
    
    def wait_untill_success_msg_disappeared(self, timeout=10):
        """      
        @summary: Wait untill the success message is disappeared     
        @return: AdminTemplatePage
        @author: Thanh Le
        """
        self._lblSuccessMessage.wait_until_displayed(timeout).wait_until_disappeared(timeout)
        if(self._lblSuccessMessage.is_displayed(2)):
            self._driver.execute_script('location.reload();')
            sleep(3)
        self.wait_page_ready()
        return self
    
    
    def goto_dashboard_tab(self):
        """      
        @summary: Go to dashboard tab        
        @return: Dashboard page
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()._lnkMDashboard.click()  
        else:
            self._driver.scroll_up_to_top()
            self._lnkDashboard.click()        
        from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
        return AdminDashboardPage(self._driver)
    
    
    def goto_users_tab(self):
        """      
        @summary: Go to Users tab     
        @return: Users page
        @author: Thanh Le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()._lnkMUsers.click()
        else:
            self._driver.scroll_up_to_top()
            if self._driver._driverSetting.browser_name == Browser.Safari:
                sleep(2)
            self._lnkUsers.wait_until_clickable().click_element()
        self.wait_for_loading()
        from pages.suitable_tech.admin.advanced.users.admin_users_page import AdminUsersPage
        return AdminUsersPage(self._driver)
    
    
    def goto_members_tab_of_a_device_group(self, device_group_name):
        """      
        @summary: Go to Members tab of a device group     
        @param device_group_name: name of device group would like to go to Members tab
        @return: Members tab of device group page
        @author: Thanh Le 
        """
        beamsAllDevicePage = self.goto_beams_tab().select_device_group(device_group_name)
        return beamsAllDevicePage.goto_members_tab()
    
    
    def goto_reservations_tab_of_a_device_group(self, device_group_name):
        """      
        @summary: Go to Reservations tab of a device group  
        @param device_group_name: name of device group would like go to Reservations tab
        @return: Reservations tab of a device group page
        @author: Thanh Le
        """
        beamsAllDevicePage = self.goto_beams_tab().select_device_group(device_group_name)
        return beamsAllDevicePage.goto_reservations_tab()
    
    
    def goto_settings_tab_of_a_device_group(self, device_group_name):
        """      
        @summary: Go to Settings tab of a device group   
        @param device_group_name: name of device group would like to go to Settings tab
        @return: Settings tab of device group
        @author: Thanh Le
        """
        return self.goto_beams_tab().select_device_group(device_group_name).goto_setting_tab()
    
    
    def goto_access_times_tab_of_a_device_group(self, device_group_name):
        """      
        @summary: Go to Access Times tab of a device group   
        @param device_group_name: name of device group would like to go to Access Times tab
        @return: Access Times tab of device group
        @author: Thanh Le
        """
        return self.goto_beams_tab().select_device_group(device_group_name).goto_accesstimes_tab()
    
     
    def logout(self):
        """      
        @summary: Log out from Suitable Tech     
        @return: Home page object
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()
            self._lnkMLogout.wait_until_clickable().click()
            if self._lnkMLogout.is_displayed(2) or self._lnkBeam.is_displayed(2):
                self._lnkMLogout.jsclick()
        else:
            self._driver.scroll_up_to_top()
            self.wait_untill_success_msg_disappeared(5)
            self._ddlAdminMenu.wait_until_clickable()
        
            self._ddlAdminMenu.select_by_href(self._hrefSignOut)
        from pages.suitable_tech.user.signout_complete_page import SignoutCompletePage
        return SignoutCompletePage(self._driver, True)
    
    
    def goto_your_account(self):
        """      
        @summary: Go to Your Account page  
        @return: Your account page
        @author: Thanh Le
        """
        # TODO: work around due bug INFR-2446
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.open_narbar_on_mobile()
            self._lnkMAccountSetting.click()
        else: 
            try:
                self._driver.execute_script('$("dismissible[key=\'dashboard-advanced\'] .glyphicon.glyphicon-remove.dismiss").click();')
            except:
                pass
            self._ddlAdminMenu.select_by_href(self._hrefYourAccount) 
     
        from pages.suitable_tech.accountsettings.account_settings_page import AccountSettingsPage
        return AccountSettingsPage(self._driver)
    
    
    def goto_another_org(self, org_name, dissmiss=True, from_simplified_organization=False):
        """      
        @summary: Go to another org (LogiGear Test, LogiGear Test 2, LogiGear Test 3)
        @return: Your account page
        @author: Thanh Le
        """
        self.wait_page_ready()
        if self._lblSuccessMessage.is_displayed(0):
            self._lblSuccessMessage.click()

        if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
            if from_simplified_organization:
                self._ddlSimplifiedSwitchOrgs.select_by_partial_text(org_name)
            else:
                self._ddlAdminMenu.select_by_partial_text(org_name)
                self.wait_page_ready(3)
        else:
            self.open_narbar_on_mobile()
            self._lnkMSwitchOrganization.click()
            self._lnkOrganization(org_name).click()
            self.wait_page_ready(3)

        if self._btnDismissOrgContact.is_displayed(3) and dissmiss:
            self._btnDismissOrgContact.click()

        if org_name == Constant.SimplifiedOrgName:
            from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
            return SimplifiedDashboardPage(self._driver)

        from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
        return AdminDashboardPage(self._driver)


    def logout_and_login_again(self, email_address, password, loginAgainAsNormalUser=False):
        """      
        @summary: Log out from Suitable Tech and then login again       
        @param email_address: Email address of admin user that used to login
        @param password: Password of admin user that used to login
        @return: AdminDashboardPage if user is admin, SimplifiedDashboardPage if user isn't admin
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        return self.logout().goto_login_page().login(email_address, password, loginAgainAsNormalUser)
    
    
    def logout_and_login_again_as_unwatched_video_user(self, email_address, password):
        """      
        @summary: Log out from Suitable Tech and then login again       
        @param email_address: Email address of admin user that used to login
        @param password: Password of admin user that used to login
        @return: AdminDashboardPage if user is admin, SimplifiedDashboardPage if user isn't admin
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        return self.logout().goto_login_page().login(email_address, password)

    
    def get_selected_organization(self):
        """      
        @summary: Get the organization item in drop-down list
        @return: Selected org
        @author: Thanh Le
        """
        return self._ddlOrganization.get_selected_item()
    
    
    def is_organization_dropdown_displayed(self, timeout=None):
        """
        @summary: Check if the org is displayed in org drop-down list or not
        @return: True: the org is displayed
                False: the org is not displayed
        @author: Thanh le
        """
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self.wait_untill_success_msg_disappeared()
            self.open_narbar_on_mobile()
            return self._ddlMOrganization.is_displayed(timeout)
        else:
            return self._ddlOrganization.is_displayed(timeout)


    def does_dropdown_contain_multi_orgs(self, timeout=None):
        """      
        @summary: Check if the multi orgs are displayed in admin drop-down list or not      
        @return: True: the org is displayed
                False: the org is not displayed
        @author: Thanh le
        """
        count = ElementList(self._driver, *_AdminTemplateLocator._linkOrgInAdminMenu).count()
        if count > 1:
            return True
        return False
    
    
    def wait_for_loading(self, timeout=3):
        """      
        @summary: wait for page loads completely        
        @param timeout: time to wait for loading completely
        @author: Thanh Le
        """
        if(timeout==None):
            timeout = 0
        self._iconLoading.wait_until_displayed(timeout)
        self._iconLoading.wait_until_disappeared(timeout)


    def is_primary_organization_contact_displayed (self, timeout=None):
        """      
        @summary: Check if the primary org contact is displayed in setting or not      
        @return: True: the primary org is displayed
                False: the primary org is not displayed
        @author: Thanh le
        """
        return  self._popupPrimaryOrgContact.is_displayed(timeout)
    
    
    def is_organization_menu_displayed(self, timeout = None):
        """      
        @summary: Check if the organization menu is displayed or not      
        @return: True: the organization menu is displayed
                False: the organization menu is not displayed
        @author: Thanh le
        """
        return self._lnkOrganizationSettings.is_displayed(timeout)
    
    
    def submit_primary_org_contact_info(self, info):
        from pages.suitable_tech.admin.dialogs.primary_organization_contact_dialog import PrimaryOrganizationContactDialog
        return PrimaryOrganizationContactDialog(self._driver).submit_primary_org_contact_info(info)
    
    
    def wait_until_username_display(self):
        """
        @summary: wait until username display
        @author: Tan Le
        """       
        sleep(3)
        try:
            timeout = 1
            while(timeout <= 60):
                try:
                    username = self._driver.execute_script("return $('.dropdown-header.ng-binding').text()")
                    if username != '':
                        break
                    else:
                        timeout += 1
                        sleep(1)
                except:
                    pass
        except Exception as ex:
            raise ex


    def get_icon_link(self):
        """
        @summary: Get user icon link of a user
        @return: file_url: correct user icon link
        @author: Quang Tran
        """
        self.wait_page_ready()
        file_url = self._imgUserIcon.get_attribute("src")
        return Utilities.correct_link(file_url)


    def remove_image_icon(self):
        """      
        @summary: remove the icon of this group
        @return: Admin User Common Page
        @author: Thanh Le  
        """
        btn_remove = self._btnRemoveImageIcon
        if btn_remove.is_displayed(5):
            btn_remove.click()
            from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
            ConfirmActionDialog(self._driver).continue_dialog()
            
            #wait for removing
            sleep(3)
            ico_url = self.get_icon_link()
            ext = ico_url.rsplit('.', 1)
            tried = 0
            while tried < 10:
                if len(ext) > 1 and ext[1] == 'svg':
                    sleep(2)
                    return self
                tried += 1
                sleep(2)
                ico_url = self.get_icon_link()
                ext = ico_url.rsplit('.', 1)  
        return self  
        
        
    def set_image_icon(self, image_path, resize_tracker = False, wait_for_completed = True):
        """      
        @summary: Change icon   
        @param image_path: path to  new image file
        @param wait_for_completed: time wait for complete changing
        @return: Admin User Group Detail Page
        @author: Quang Tran 
        @created_date: October 03, 2016    
        """
        dialog = self.open_upload_image_dialog()
        dialog.choose_file(image_path)
        self.wait_for_loading(20)
        if resize_tracker:
            dialog.resize_crop_tracker()
        else:
            dialog.move_crop_tracker()
        dialog.submit()
            
        #wait for updating new icon
        if wait_for_completed:
            self.wait_for_icon_updated()
        
        return self
    
    
    def change_image_icon(self, image_path, resize_tracker = False, wait_for_completed = True):
        return self.remove_image_icon().set_image_icon(image_path, resize_tracker, wait_for_completed)
        
    
    def wait_for_icon_updated(self):
        """      
        @summary: Wait for icon mage is completely updated
        @return: Admin User Group Detail Page
        @author: Quang Tran
        @created_date: October 03, 2016    
        """  
        sleep(3)
        ico_url = self.get_icon_link()
        ext = ico_url.rsplit('.', 1)
        tried = 0
        while tried < 10:
            if len(ext) > 1 and ext[1] != 'svg':
                sleep(2)
                return self
            tried += 1
            sleep(2)
            ico_url = self.get_group_icon_link()
            ext = ico_url.rsplit('.', 1)
            
        return self
    

    def open_upload_image_dialog(self):
        """      
        @summary: Method to open upload image dialog
        @return: UploadImageDialog: This is 'Upload Image' dialog
        @author: Thanh le
        @created_date: March 7, 2017
        """
        self._lnkChangeImage.wait_until_displayed(5)
        self._lnkChangeImage.wait_until_clickable().jsclick() 
        from pages.suitable_tech.admin.dialogs.upload_image_dialog import UploadImageDialog
        return UploadImageDialog(self._driver)


    def check_sort_table_work(self, xpath_table):
        """
        @summary: Check table can sort with each label
        @param xpath_table: xpath of table would like to check
        @return: True if table can sort with all label when click for each, Fail if table can not sort
        @author: Khoi Ngo
        @created_date: Oct 30, 2017
        """
        xpath_rows = xpath_table+"/tbody/tr"
        xpath_columns = xpath_table+"/thead/tr/th"
        numbers_rows = ElementList(self._driver, By.XPATH, xpath_rows).count()
        list_headers = ElementList(self._driver, By.XPATH, xpath_columns).get_all_elements()

        for index_td, header_can_sort in enumerate(list_headers):
            if 'pointer' in header_can_sort.get_attribute('class'):
                header_enable_click = Element(self._driver, By.XPATH, xpath_columns + "[{}]/span".format(index_td+1))
                name_header = header_can_sort.text
                print("Click on {}".format(name_header))
                for i in range (1, 3):
                    header_enable_click.jsclick()
                    xpath_sort_by = xpath_columns + "[{}]//span[@ng-if='isSortedBy']//span[not(contains(@class,'ng-hide'))]".format(index_td+1)
                    sort_by = Element(self._driver, By.XPATH, xpath_sort_by).get_attribute('class')
                    if not self._check_data_sort_correct(xpath_table, name_header, index_td, numbers_rows, sort_by):
                        print("Column {} sorts data incorrect".format(name_header))
                        return False
        return True


    def _check_data_sort_correct(self, xpath_table, name_header, index_td, numbers_rows, sort_by):
        """
        @summary: Check column of table can sort by desc or asc
        @param xpath_table: xpath of table contain column want to check
        @param name_header: header of column
        @param index_td: index of column want to check
        @param numbers_rows: numbers row of table
        @param sort_by: column is sorted by desc or asc
        @return: True if clumn can sort , Fail if clumn can not sort
        @author: Khoi Ngo
        @created_date: Oct 30, 2017
        """  
        data_row_list_actual = []
        data_row_list_expected = []
        data_row_list_expected_column_status = []
        index_td = index_td + 1
        name_header = name_header.strip()

        for i in range(1, numbers_rows+1):
            xpath_data = xpath_table + "/tbody/tr[{}]/td[{}]"
            xpath_data = xpath_data.format(i, index_td)
            elememt_row = Element(self._driver, By.XPATH, xpath_data)
            if not elememt_row.is_displayed(2) :
                continue
            else:
                if name_header == ApplicationConst.LBL_STATUS:
                    #Data change follow language and have 2 status, so get data from attribute "class" to sort and check
                    data_elememt_row = elememt_row.get_attribute("class").lower()
                    data_row_list_expected_column_status.append(data_elememt_row)
                else: 
                    if name_header == ApplicationConst.LBL_LAST_USED:
                        data_elememt_row = elememt_row.text
                        if data_elememt_row == "":
                            continue
                        else: 
                            data_elememt_row = parse(data_elememt_row)
                    else:
                        data_elememt_row = elememt_row.text.lower()
                        if data_elememt_row == "":
                            continue  
                    data_row_list_expected.append(data_elememt_row)
                data_row_list_actual.append(data_elememt_row)
        
        if len(data_row_list_expected) > 0:
            data_row_list_expected.sort()
        else:
            data_row_list_expected_column_status.sort()

        print("Compare data sorted actual with data sorted expected")
        if 'asc' in sort_by:
            data_row_list_expected_column_status.reverse()
            if (data_row_list_expected == data_row_list_actual or data_row_list_actual == data_row_list_expected_column_status):
                return True
            else:
                print('Column {} does not sort by asc'.format(name_header))
        else:
            data_row_list_expected.reverse()
            if (data_row_list_expected == data_row_list_actual or data_row_list_actual == data_row_list_expected_column_status):
                return True
            else:
                print('Column {} does not sort by desc'.format(name_header))


    def switch_to_icon_view(self):
        """      
        @summary: Switch to icon view         
        @return: AdminBeamsDevicesPage
        @author:  Thanh Le   
        @created_date: August 08, 2016   
        """
        self._iconIconView.click()
        self.wait_for_loading(5)
        return self


    def switch_to_list_view(self):
        """      
        @summary: Switch to list view  
        @return: AdminBeamsDevicesPage
        @author: Thanh Le  
        @created_date: August 08, 2016
        """
        self._iconListView.wait_until_clickable().click()
        self.wait_for_loading(5)
        return self


    def is_icon_displayed_at_each_users_on_table(self, icon_type):
        #sleep for more stable
        sleep(3)
        users = self._lstUserListMode.get_all_elements()
        for index in range(len(users)):
            icon = self._lstUserListMode.get_element_at(index).find_element_by_xpath(".//span[contains(@is-visible,\"{}\")]".format(icon_type))
            if not icon.is_displayed():
                return False
        return True


    def is_icon_displayed_at_each_users_on_icon_mode(self, icon_type):
        #sleep for more stable
        sleep(3)
        users = self._lstUserIconMode.get_all_elements()
        for index in range(len(users)):
            icon = self._lstUserIconMode.get_element_at(index).find_element_by_xpath(".//span[contains(@ng-if,\"{}\")]".format(icon_type))
            if not icon.is_displayed():
                return False
        return True


    def click_show_button_and_select(self, value):
        """      
        @summary: Click Show button and select item in show dropdown list   
        @param value: item would like to select
        @return: Admin Users Page
        @author: Thanh Le     
        @created_date: October 03, 2016 
        """
        self._ddlShow.select_by_partial_text(value)
        #close popup
        self._ddlShow.click()
        self.wait_for_loading(5)
        return self
    
    
    def open_narbar_on_mobile(self):
        """      
        @summary: Open Nar bar on mobile after login  
        @return: Admin Users Page
        @author: Tan Le
        @created_date: January 15, 2018
        """
        self.wait_untill_success_msg_disappeared()
        self._btnMNarBar.wait_until_clickable().click()
        #sleep for stable
        sleep(0.5)
        return self


    def dismiss_welcome_to_beam_block(self):
        """
        @summary: click on 'Dismiss and do not show again' in simplified dashboard page to dismiss 'Welcome to Beam' block
        @author: Thanh Le
        """
        self._lnkDismissWelcomeBlock.wait_until_clickable().click()
        self._lnkDismissWelcomeBlock.wait_until_disappeared(2)
        return self


    def check_sort_by_work (self, btn_sort_by_xpath, page):
        """
        @param btn_sort_by: button Sort By element
        """
        btn_sort_by = Element(self._driver, By.XPATH, btn_sort_by_xpath)
        labels_sort_by = ElementList(self._driver, By.XPATH, "(" + btn_sort_by_xpath + "/following-sibling::*/li/a)")
        sort_type = Element(self._driver, By.XPATH, btn_sort_by_xpath + "/../following-sibling::*/span")

        labels = labels_sort_by.get_all_elements()

        for i in range (len(labels)):
            btn_sort_by.click()
            labels_sort_by.click(i)
            self.wait_for_loading(3)

            ng_click_attr = labels_sort_by.get_element_at(i).get_attribute("ng-click")
            sort_by = ng_click_attr[14:].replace("')","")
            print("sort device icons by {}".format(sort_by))

            for i in range (1,3):
                data_list = self._sort_by_data(sort_by, page)
                class_attr = sort_type.get_attribute("class")
                if "arrow-up" in class_attr:
                    if not self._is_data_sorted(data_list, sort_by, ascending = True):
                        print("device icons are not sorted ascending by {}".format(sort_by))
                        return False
                else:
                    if not self._is_data_sorted(data_list, sort_by, ascending = False):
                        print("device icons are not sorted descending by {}".format(sort_by))
                        return False

                sort_type.click()

        return True


    def _sort_by_data(self, sort_by, page = "Beams"):

        if page == "Beams":
            from pages.suitable_tech.admin.advanced.beams.admin_beams_all_devices_page import AdminBeamsAllDevicesPage
            return AdminBeamsAllDevicesPage.get_device_sort_by_data_list(self, sort_by)

        if page == "Users":
            from pages.suitable_tech.admin.advanced.users.admin_users_page import AdminUsersPage
            return AdminUsersPage.get_users_sort_by_data_list(self, sort_by)

        if page == "Usergroup details":
            from pages.suitable_tech.admin.advanced.users.admin_user_group_detail_page import AdminUserGroupDetailPage
            return AdminUserGroupDetailPage.get_users_sort_by_data_list(self, sort_by)


    def _is_data_sorted(self, data_list, sort_by, ascending = True):

        if ascending:
            if sort_by == 'status' and self._driver._driverSetting.language == Language.JAPANESE:
                return True if sorted(data_list, reverse=True) == data_list else False
            else:
                return True if sorted(data_list) == data_list else False

        if not ascending:
            if sort_by == 'status' and self._driver._driverSetting.language == Language.JAPANESE:
                return True if sorted(data_list) == data_list else False
            else:
                return True if sorted(data_list, reverse=True) == data_list else False

