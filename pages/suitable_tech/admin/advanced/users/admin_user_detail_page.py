from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.users.admin_users_common_page import AdminUsersCommonPage
from pages.suitable_tech.admin.dialogs.edit_user_dialog import EditUserDialog
from core.webdriver.elements.element_list import ElementList
from common.application_constants import ApplicationConst


class _AdminUserDetailPageLocator(object):
    _lblPageHeader = (By.XPATH, "//h3[@class='detail-heading ng-binding']")
    _btnRemoveFromOrg = (By.XPATH, "//button[@ng-click='delete()']")
    _btnEditUser = (By.XPATH, "//button[@ng-click='edit()']")
    _btnResendInvitation = (By.CSS_SELECTOR, "button[ng-click='resendInvitation()']")
    _btnInviteThisUser = (By.CSS_SELECTOR, "button[ng-click='inviteToJoin()']")
    _lblTempUser = (By.CSS_SELECTOR,"span[ng-if='user.is_temporary'] translate")

    @staticmethod
    def _lblAdministratesGroup():
        return (By.XPATH, u"//dt[.=\"{}\"]/following-sibling::dd[1]//span[@class='ng-scope']/a".format(ApplicationConst.LBL_ADMINISTERS_GROUPS))
    @staticmethod
    def _lblUserGroups():
        return (By.XPATH, u"//dt[.=\"{}\"]/following-sibling::dd[1]//span[@class='ng-scope']/a".format(ApplicationConst.LBL_USER_GROUPS))
    @staticmethod
    def _lblDeviceGroups():
        return (By.XPATH, u"//dt[.=\"{}\"]/following-sibling::dd[1]//span[@class='ng-scope']/a".format(ApplicationConst.LBL_DEVICE_GROUPS_PROPERTY))
    @staticmethod
    def _lblUserTitle(value):
        return (By.XPATH, u"//h3[contains(., \"{}\")]".format(value))
    @staticmethod
    def _lblUserInformation(property_name):
        return (By.XPATH, u"//dt[.=\"{}\"]/following-sibling::dd[1]".format(property_name))
    @staticmethod
    def _lblAdministratorNotice(value):
        return (By.XPATH, u"//dd[contains(.,\"{}\") and contains(@ng-if,'user.is_admin')]".format(value))
    @staticmethod
    def _lblMilestone(index, value):
        return (By.XPATH, u".//div[@ng-controller='MilestoneAccordianCtl']/div[{}]/div[text()='{}']/..".format(index, value))
    @staticmethod
    def _lnkUserGroup(user_group_name):
        return (By.XPATH, u".//a[text()=\"{}\"]".format(user_group_name))
    
class AdminUserDetailPage(AdminUsersCommonPage):
    """
    @description: This is page object class for Admin Users Details page.
        This page will be opened after clicking Users link.
        Please visit https://staging.suitabletech.com/manage/#/contacts/c10930@mailinator.com/ for more details.
    @page: Admin Users Details page
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _lblPageHeader(self):
        return Element(self._driver, *_AdminUserDetailPageLocator._lblPageHeader)
    @property
    def _btnRemoveFromOrg(self):
        return Element(self._driver, *_AdminUserDetailPageLocator._btnRemoveFromOrg)
    @property
    def _lblAdministratesGroup(self):
        return ElementList(self._driver, *_AdminUserDetailPageLocator._lblAdministratesGroup())   
    @property
    def _btnEditUser(self):
        return Element(self._driver, *_AdminUserDetailPageLocator._btnEditUser)
    @property
    def _btnResendInvitation(self):
        return Element(self._driver, *_AdminUserDetailPageLocator._btnResendInvitation)
    @property
    def _btnInviteThisUser(self):
        return Element(self._driver, *_AdminUserDetailPageLocator._btnInviteThisUser)
    @property
    def _lblTempUser(self):
        return Element(self._driver, *_AdminUserDetailPageLocator._lblTempUser)
    @property
    def _lblUserGroups(self):
        return ElementList(self._driver, *_AdminUserDetailPageLocator._lblUserGroups())
    @property
    def _lblDeviceGroups(self):
        return ElementList(self._driver, *_AdminUserDetailPageLocator._lblDeviceGroups())
    
    def _lblAdministratorNotice(self, value):
        return Element(self._driver, *_AdminUserDetailPageLocator._lblAdministratorNotice(value))
    def _lblUserTitle(self, value):
        return Element(self._driver, *_AdminUserDetailPageLocator._lblUserTitle(value))
    def _lblUserInformation(self, property_name):
        return Element(self._driver, *_AdminUserDetailPageLocator._lblUserInformation(property_name))
    def _lblMilestone(self, index, value):
        return Element(self._driver, *_AdminUserDetailPageLocator._lblMilestone(index, value))
    def _lnkUserGroup(self, user_group_name):
        return Element(self._driver, *_AdminUserDetailPageLocator._lnkUserGroup(user_group_name))
    
    """    Methods    """
    def __init__(self, driver):      
        """      
        @summary: Constructor method
        @param driver: Web driver 
        @author: Thanh Le   
        @created_date: October 03, 2016       
        """  
        AdminUsersCommonPage.__init__(self, driver)
        self._wait_for_loading()


    def get_user_info(self, property_name):
        """      
        @summary: Get user information  
        @param property_name: name of user would like to get property
        @return: information of user
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        from time import sleep
        self._lblUserInformation(property_name).is_displayed(15)
        sleep(2)        
        return str(self._lblUserInformation(property_name).text)        
    
    def get_user_administers_groups(self):
        """      
        @summary: Get admin user group      
        @return: list of user group of admin
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        lst_groups = []
        lst_elements = self._lblAdministratesGroup.get_all_elements()
        for e in lst_elements:
            lst_groups.append(e.text)
        return lst_groups
    
    
    def is_user_removable(self):
        """      
        @summary: Check if the Remove button is enable for a user or not         
        @return: True: the Remove button is displayed, False: the Remove button is not displayed
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        return self._btnRemoveFromOrg.is_disappeared(5)
    

    def remove_user_from_organization(self, wait_for_completed=True):
        """      
        @summary: Remove a user form an organization 
        @param wait_for_completed: time to wait for complete removing
        @return: AdminUserDetailPage
        @author: Thanh Le     
        @created_date: October 03, 2016    
        """
        self._btnRemoveFromOrg.click()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
        return self
    
    
    def is_user_page_displayed(self, user_displayed_name):
        """      
        @summary: Check if user detail page is displayed or not       
        @param user_displayed_name: user would like to be checked
        @return: True: user page is displayed, False: user page is not displayed
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        return self._lblUserTitle(user_displayed_name).is_displayed()


    def edit_user(self, verified_domain_user = False, first_name = None, last_name = None, add_user_groups=[], add_device_groups=[], remove_user_groups=[], remove_device_groups=[], allow_administer=False, wait_for_completed=True, cancel=False):
        """      
        @summary: Edit user on edit user dialog
        @param: user_groups: add user to these user groups
        @param device_groups: add user to these device groups
        @param allow_administer: allow user to administer or not
        @param wait_for_completed: wait for action completed or not
        @param cancel: cancel changes or not
        @author: Khoi Ngo
        @created_date: October 10, 2017
        """
        self.open_edit_user_dialog()\
            ._wait_for_dialog_appeared()
        EditUserDialog(self._driver).edit_user(verified_domain_user, first_name, last_name, add_user_groups, add_device_groups, remove_user_groups, remove_device_groups, allow_administer, cancel)
        if wait_for_completed:
            self.wait_untill_success_msg_disappeared(2)
        return self
    
    
    def is_allow_user_to_administrater_org_enabled(self):
        """      
        @summary: Check if the 'Allow this user to administer this organization' checkbox is enabled or  not
        @return: True: the checkbox is enable, False: the checkbox is disabled
        @author: Thanh Le   
        @created_date: October 03, 2016      
        """

        edit_user_dialog = EditUserDialog(self._driver)
        result = self.open_edit_user_dialog().is_allow_user_to_administrater_org_enabled()
        edit_user_dialog.cancel()
        return result
    
    
    def is_administator_label_notice(self, option, wait_time=2):
        """      
        @summary: Check if a user is administrator or not
        @param: option: yes or no (the user is admin or not)
        @param: wait_time: time to wait for notice
        @return: True: the Administrator field is Yes, False: the Administrator field is No
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        return self._lblAdministratorNotice(option).is_displayed(wait_time)
    
    
    def get_user_groups(self):
        """      
        @summary: Get list of user group of a user     
        @return: list of user groups
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        lst_user_groups = []
        lst_elements = self._lblUserGroups.get_all_elements()
        for e in lst_elements:            
            lst_user_groups.append(e.text)
        return lst_user_groups
    
    
    def get_device_groups(self):
        """      
        @summary: Get list of device group of a user         
        @return: list of device groups
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        lst_devices = []
        lst_elements = self._lblDeviceGroups.get_all_elements()
        for e in lst_elements:
            lst_devices.append(e.text)
        return lst_devices
   
    
    def wait_for_page_displayed(self, user_displayed_name):
        """      
        @summary: Wait for user detail page displays         
        @param user_displayed_name: name of user would like to check
        @return: AdminUserDetailPage
        @author: Thanh Le  
        @created_date: October 03, 2016    
        """
        self._lblUserTitle(user_displayed_name).wait_until_displayed()
        return self


    def is_milestones_filled_correctly(self, completed_milestones_number):
        """
        @summary: Check if milestone is filled completed or not
        @param completed_milestones_number: number of completed milestones
        @return: AdminUserDetailPage
        @author: Thanh Le
        @created_date: September 20, 2017
        """
        milestones_list = ApplicationConst.LST_MILESTONES.split(',')
        for num in range(len(milestones_list)):
            if num <= completed_milestones_number-1:
                if not 'completed' in self._lblMilestone(num+1, milestones_list[num]).get_attribute("class"):
                    return False
            else:
                if 'completed' in self._lblMilestone(num+1, milestones_list[num]).get_attribute("class"):
                    return False
        return True


    def open_edit_user_dialog(self):
        """
        @summary: Open edit user dialog
        @return: EditUserDialog
        @author: Khoi Ngo
        @created_date: October 09, 2017
        """
        self._btnEditUser.wait_until_clickable().click()
        return EditUserDialog(self._driver)


    def goto_user_group_detail(self, user_group_name):
        """
        @summary: Go to user group by link
        @return: AdminUserGroupDetailPage
        @author: Khoi Ngo
        @created_date: October 10, 2017
        """
        self._lnkUserGroup(user_group_name).wait_until_clickable().click()
        from pages.suitable_tech.admin.advanced.users.admin_user_group_detail_page import AdminUserGroupDetailPage
        return AdminUserGroupDetailPage(self._driver)


    def resend_invitation(self):
        """
        @summary: re-send invitation
        @return: AdminUserDetailPage
        @author: Khoi Ngo
        @created_date: October 11, 2017
        """
        self._btnResendInvitation.wait_until_clickable().click()
        return self


    def invite_user(self, user):
        """
        @summary: invite temporary user to guess user
        @return: AdminUserDetailPage
        @author: Khoi Ngo
        @created_date: October 20, 2017
        """
        self._btnInviteThisUser.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        InviteNewUserDialog(self._driver).submit_invite_information(user)
        return self


    def is_temporary_user_label_displayed(self):
        """
        @summary: invite temporary user to guess user
        @return: AdminUserDetailPage
        @author: Khoi Ngo
        @created_date: October 20, 2017
        """
        self.wait_untill_success_msg_disappeared()
        return self._lblTempUser.is_displayed()

