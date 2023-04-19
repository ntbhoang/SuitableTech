from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_list import ElementList
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from pages.suitable_tech.admin.dialogs.choose_users_dialog import ChooseUsersDialog
from common.application_constants import ApplicationConst
from core.suitabletechapis.user_api import UserAPI

class _AdminBeamsMembersPageLocator(object):
    _btnAddUsers = (By.XPATH, "//button[@ng-click='addMember()']")
    _btnAddUsersFn = (By.XPATH, "//button[@ng-click='addContactsFn()']")
    _txtSearch = (By.XPATH, "//input[@type='search']")
    
    """User Profile Card"""
    _lstUserName = (By.XPATH,'''(//div[@ng-class="{'content-loading': usersContentLoading}"]//div[contains(@class,"profile-title")])''')

    @staticmethod
    def _iconUsersLoading():
        return (By.XPATH, u"//h4[.=\"{}\"]/ancestor::div[@ng-show='includeGroups']//div[@class='loading-indicator']/span".format(ApplicationConst.LBL_BEAMS_MEMBERS_USERS))
    @staticmethod
    def _iconUserGroupsLoading():
        return (By.XPATH, u"//h4[.=\"{}\"]/ancestor::div[@class='contacts-gallery']//div[@class='loading-indicator']/span".format(ApplicationConst.LBL_BEAMS_MEMBERS_USER_GROUPS))
    @staticmethod
    def _btnRemoveGroup(group_name):
        return (By.XPATH, u"//div[@class='profile-title ng-binding' and normalize-space(.)=\"{}\"]/preceding-sibling::div//button".format(group_name)) 
    @staticmethod
    def _btnRemoveUser(displayed_name):
        return (By.XPATH, u"//div[normalize-space(.)=\"{}\"]/preceding-sibling::div[@class='profile-image-container']//button[translate[.=\"{}\"]]".format(displayed_name, ApplicationConst.LBL_BEAMS_MEMBERS_REMOVE_USER))
    @staticmethod
    def _pnlUser(email_address):
        return (By.XPATH, u"//h4[.=\"{}\"]/../following-sibling::div//div[normalize-space(.)=\"{}\"]".format(ApplicationConst.LBL_BEAMS_MEMBERS_USERS, email_address))
    @staticmethod
    def _pnlUserGroup(group_name):
        return (By.XPATH, u"//h4[.=\"{}\"]/../following-sibling::div//div[normalize-space(.)=\"{}\"]".format(ApplicationConst.LBL_BEAMS_MEMBERS_USER_GROUPS, group_name))
    @staticmethod
    def _pnlProfileCard(profile_title):
        return (By.XPATH, u"//div[@class='profile-title ng-binding' and normalize-space(.)=\"{}\"]/..".format(profile_title))


class AdminBeamsMembersPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam Members page.
        This page will be opened after clicking Members tab on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/beams/787/members/ for more details.
    @page: Beam Members page
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _btnAddUsers(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._btnAddUsers)
    @property
    def _btnAddUsersFn(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._btnAddUsersFn)
    @property
    def _btnCreateDeviceGroup(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._btnCreateDeviceGroup)
    @property
    def _btnCreateUserGroup(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._btnCreateUserGroup)
    @property
    def _txtSearch(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._txtSearch)
    @property
    def _iconUsersLoading(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._iconUsersLoading())
    @property
    def _iconUserGroupsLoading(self):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._iconUserGroupsLoading())
    
    """User Profile Card"""
    @property
    def _lstUserName (self):
        return ElementList(self._driver, *_AdminBeamsMembersPageLocator._lstUserName)

    def _pnlUser(self, email_address):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._pnlUser(email_address))
    def _pnlUserGroup(self, group_name):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._pnlUserGroup(group_name))
    def _btnRemoveGroup(self, group_name):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._btnRemoveGroup(group_name))
    def _btnRemoveUser(self, user):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._btnRemoveUser(user))
    def _pnlProfileCard(self, value):
        return Element(self._driver, *_AdminBeamsMembersPageLocator._pnlProfileCard(value))
    
    """    Methods      """    
    def __init__(self, driver):        
        """      
        @summary: Constructor method        
        @param driver: Web driver
        @author: Thanh Le 
        @created_date: October 10, 2016 
        """
        AdminBeamsCommonPage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        self._wait_for_loading()
        
    
    def add_user_to_device_group(self, user):
        """      
        @summary: Add a user to a device group  
        @param user: user would like to add to device group
        @return: AdminBeamsMembersPage
        @author: Thanh Le      
        @created_date: October 10, 2016  
        """
        self._btnAddUsers.wait_until_clickable().click_element()
        ChooseUsersDialog(self._driver).choose_user(user.email_address)
        self._wait_for_loading()
        return self    
    
    
    def add_user_group_to_device_group(self, group_name):
        """      
        @summary: Add a user group to a device group
        @param group_name: user group would like to add to device group
        @return: AdminBeamsMembersPage
        @author: Thanh Le     
        @created_date: October 10, 2016 
        """
        self._btnAddUsers.wait_until_clickable().click_element()
        choose_user_dialog = ChooseUsersDialog(self._driver)
        choose_user_dialog.choose_user(group_name)
        return self
    

    def remove_user(self, displayed_name):
        """      
        @summary: Remove a user by displayed name
        @param displayed_name: full name of user would like to be removed 
        @return: AdminBeamsMembersPage
        @author: Thanh Le
        @created_date: October 10, 2016 
        """
        self.click_remove_user(displayed_name)
        self.accept_remove_user_dialog()
        self._pnlUser(displayed_name).wait_until_disappeared()
        return self    
    
    
    def click_remove_user(self, displayed_name):      
        """      
        @summary: Click Remove button on user icon by displayed name
        @param displayed_name: full name of user would like to be removed 
        @return: AdminBeamsMembersPage
        @author: Thanh Le  
        @created_date: October 10, 2016  
        """  
        self.search_user(displayed_name)
        self._btnRemoveUser(displayed_name).wait_until_displayed()
        self._btnRemoveUser(displayed_name).wait_until_clickable().click_element()
        return self
    
    
    def accept_remove_user_dialog(self):
        """      
        @summary: Click Ok button on remove user confirmation pop-up
        @return: AdminBeamsMembersPage
        @author: Thanh Le   
        @created_date: October 10, 2016    
        """
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        return self
    
    
    def reject_remove_user_dialog(self):
        """      
        @summary: Click Ok button on remove user confirmation pop-up       
        @return: AdminBeamsMembersPage
        @author: Thanh Le     
        @created_date: October 10, 2016  
        """
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).cancel()
        return self
    
    
    def get_toast_msg(self, continue_dialog=True):
        """      
        @summary: Get message 'Are you sure you want to remove this member
                 from the '<device group's name>' device group?' 
        @param close_dialog: close the confirm message or not 
        @return: AdminBeamsMembersPage
        @author: Thanh Le   
        @created_date: October 10, 2016 
        """
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        return ConfirmActionDialog(self._driver).get_dialog_message(continue_dialog)
        
    
    def is_user_disappeared(self, search_value, check_value=None, wait_time_out=None):
        """      
        @summary: Check if a user disappears or not    
        @param search_value: user would like to be checked
        @param check_value: value used to compare
        @param wait_time_out: time to wait for user disappears
        @return: True: the user disappears, False: the user still appears
        @author: Thanh Le
        @created_date: October 10, 2016 
        """
        self.search_user(search_value)
        if(check_value==None):
            return self._pnlUser(search_value).is_disappeared(wait_time_out)
        else:
            return self._pnlUser(check_value).is_disappeared(wait_time_out)
        
    
    def is_user_existed(self, search_value, check_value=None, wait_time_out=None):
        """      
        @summary: Check if a user is existed or not  
        @param search_value: user would like to be checked
        @param check_value: value used to compare
        @param wait_time_out: time to wait for user displays
        @return: True: the user is existed, False: the user is not existed
        @author: Thanh Le 
        @created_date: October 10, 2016 
        """
        self.search_user(search_value)
        if(check_value==None):
            return self._pnlUser(search_value).is_displayed(wait_time_out)
        else:
            return self._pnlUser(check_value).is_displayed(wait_time_out)
    
    
    def is_user_group_removable(self, group_name, wait_time_out=None):
        """      
        @summary: Check if a user can be removed or not (The red Remove button displays on user group)   
        @param  group_name: the name of user group would like to check
        @param wait_time_out: time to wait for the Remove button displays
        @return: True: The Remove button displays, False: The Remove button is not displayed
        @author: Thanh Le 
        @created_date: October 10, 2016 
        """
        self.search_user(group_name)
        return self._btnRemoveGroup(group_name).is_displayed(wait_time_out)
    
    
    def is_user_group_disappeared(self, group_name, wait_time_out=None):
        """      
        @summary: Check if a user group disappears or not  
        @param group_name: name of user group would like to check
        @param wait_time_out: time to wait for a user group disappears
        @return: True: the user group disappears, False: the user group appears
        @author: Thanh Le    
        @created_date: October 10, 2016  
        """
        self.search_user(group_name)
        return self._pnlUserGroup(group_name).is_disappeared(wait_time_out)
    
    
    def is_user_group_existed(self, group_name, wait_time_out=None):
        """      
        @summary: Check if a user group is existed or not    
        @param group_name: name of user group would like to check
        @param wait_time_out: time out to wait for a user group is displayed
        @return: True: the user group is existed, False: the user group is not existed
        @author: Thanh Le 
        @created_date: October 10, 2016 
        """
        self.search_user(group_name)
        return self._pnlUserGroup(group_name).is_displayed(wait_time_out)
    

    def remove_user_group(self, group_name):
        """      
        @summary: Remove a user group by group name 
        @param group_name: name of user group would like to remove
        @return: AdminBeamsMembersPage
        @author: Thanh Le
        @created_date: October 10, 2016 
        """
        self.search_user(group_name)
        self._btnRemoveGroup(group_name).wait_until_clickable()
        from time import sleep
        sleep(3)
        self._btnRemoveGroup(group_name).click_element()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        return self
    
    
    def search_user(self, search_value):
        """      
        @summary: Search for a user based on a search criteria    
        @param search_value: keyword used for searching
        @return: AdminBeamsMembersPage: user matched with searched value displays
        @author: Thanh Le
        @created_date: October 10, 2016 
        """
        self._txtSearch.type(search_value)
        self._wait_for_loading()
        return self
    
    
    def _wait_for_loading(self, timeout=5):
        """      
        @summary: Wait for user icon loading completely
        @param timeout: time to wait for user icon loads completely
        @return: AdminBeamsMembersPage
        @author: Thanh Le  
        @created_date: October 10, 2016 
        """
        self._iconUsersLoading.wait_until_displayed(timeout)
        self._iconUserGroupsLoading.wait_until_displayed(timeout)
        self._iconUsersLoading.wait_until_disappeared(timeout)        
        self._iconUserGroupsLoading.wait_until_disappeared(timeout)


    def goto_user_group_detail_page(self, group_name):
        """      
        @summary: Go to detail page of a user group         
        @param group_name: name of user group would like to go detail page
        @return: detail page of user group
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self._txtSearch.wait_until_displayed().type(group_name)
        self._wait_for_loading()
        return self.select_user_group(group_name)


    def select_user_group(self, group_name):
        """      
        @summary: Select a user by user's group name
        @param group_name: name of user group would like to select
        @return: Admin User Group Detail Page
        @author: Thanh Le
        @created_date: August 16, 2016
        """ 
        self._pnlProfileCard(group_name).wait_until_clickable().jsclick()
        from pages.suitable_tech.admin.advanced.users.admin_user_group_detail_page import AdminUserGroupDetailPage
        return AdminUserGroupDetailPage(self._driver)


    def check_search_user_work_correctly(self, user):
        """
        @summary: Check search function for user work
        @return: True if Search returns correct values, Fail if Search returns incorrect values
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """

        self.search_user(user.email_address)
        number_user = self._lstUserName.get_all_elements()
        if len(number_user) != 1:
            print("Search incorrectly, it returns more than 1 value")
            return False
        username = UserAPI.get_displayed_name(user)
        search_return = number_user[0].text
        if search_return == username:
            self._txtSearch.clear()
            self.wait_for_loading(5)
            return True
        else:
            False


    def check_sort_by_work_correctly(self):
        """
        @summary: Check Sort By ddl can sort with each label
        @return: True if Sort By ddl can sort with all label when click for each, Fail if Sort By ddl can not sort
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """

        btn_sort_by_xpath = "//div[@is-open='sortDropdownOpen']/button"
        return self.check_sort_by_work(btn_sort_by_xpath, page= "Users")


    def check_table_users_can_sort(self):
        """
        @summary: Check table can sort with each label
        @return: True if table can sort with all label when click for each, Fail if table can not sort
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """
        xpath_table = "//div[contains(@ng-class,'usersContentLoading')]//table[@class='table table-hover ng-scope']"
        return self.check_sort_table_work(xpath_table)
