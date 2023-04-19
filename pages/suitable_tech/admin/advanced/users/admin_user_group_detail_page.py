from time import sleep
from selenium.webdriver.common.by import By
from common.application_constants import ApplicationConst
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.users.admin_users_common_page import AdminUsersCommonPage
from pages.suitable_tech.admin.dialogs.choose_users_dialog import ChooseUsersDialog
from core.webdriver.elements.element_list import ElementList
from core.suitabletechapis.user_api import UserAPI
from core.webdriver.elements.editable_combobox import EditableCombobox


class _AdminUserGroupDetailPageLocator(object):
    _lblPageHeader = (By.XPATH, "//h3[@class='detail-heading ng-binding']")
    _btnDeleteGroup = (By.XPATH, "//button[@ng-click='delete()']")
    _btnEditGroup = (By.XPATH, "//button[@ng-click='edit()']")
    _btnAddUsers = (By.XPATH, "//button[@ng-click='addUsers()']")
    _lnkChangeIcon = (By.XPATH, "//span[@class='change-picture-icon fa fa-pencil']")
    _lstUserGroupProfileCards = (By.XPATH, "//div[@for='usergroup']//a")
    _ddlAddUser = (By.XPATH, "//button[@data-toggle=\"dropdown\"]")
    _lstAddedUser = (By.XPATH, "//div[@class='gallery-content']//div[@ng-repeat='user in users']")
    _lstUserProfileCards = (By.XPATH, "//div[@class='row master-detail']//div[@class='gallery-group']//div[@class='profile-card ng-isolate-scope']")
    _lblDeviceGroups = (By.CSS_SELECTOR, ".dl-horizontal.item-details dd")
    _ecbxDeviceGroups = (By.XPATH, "//div[@class='modal-content']//div[@class='host']")
    _txtSearch = (By.XPATH, "//div[@class='row master-detail']//input[@type='search']")
    _iconListView = (By.XPATH, "//div[@class='row master-detail']//span[@class='glyphicon glyphicon-th-list']/..")

    """User Profile Card"""
    _lstUserName = (By.XPATH, '''(//div[@class="row master-detail"]//div[@ng-class="{'content-loading': usersContentLoading}"]//div[contains(@class,"profile-title")])''')

    @staticmethod
    def _btnRemoveUser(value):
        return (By.XPATH, u"//div[@class='profile-title ng-binding' and normalize-space(.)=\"{}\"]/..//div[@ng-if='canRemove']".format(value))
    @staticmethod
    def _lblUserGroupName(value):
        return (By.XPATH, u"//section[@class='ng-scope']//h3[contains(.,\"{}\")]".format(value))
    @staticmethod
    def _pnlUser(displayed_name):
        return (By.XPATH, u"//div[@class='gallery-content']//div[contains(@class, 'profile-title') and .=\"{}\"]/preceding-sibling::div[@class='profile-image-container']".format(displayed_name))
    @staticmethod
    def _itemAddUserMenu(value):
        return (By.XPATH, u"//div[button[@data-toggle=\"dropdown\"]]//a[text()=\"{}\"]".format(value))
    @staticmethod
    def _lnkDeviceGroupName(value):
        return (By.XPATH, u"//div[@class='row']//a[.='{}']".format(value))


class AdminUserGroupDetailPage(AdminUsersCommonPage):
    """
    @description: This is page object class for Admin Users Group Details page.
        This page will be opened after clicking Users link.
        Please visit https://staging.suitabletech.com/manage/#/contacts/groups/325/ for more details.
    @page: Admin Users Group Details page
    @author: Thanh Le
    """

    """    Properties    """ 
    @property
    def _lblPageHeader(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._lblPageHeader)
    @property
    def _btnDeleteGroup(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._btnDeleteGroup)
    @property
    def _btnEditGroup(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._btnEditGroup)
    @property
    def _btnAddUsers(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._btnAddUsers)
    @property
    def _lnkChangeIcon(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._lnkChangeIcon)
    @property
    def _lstAddedUser(self):
        return ElementList(self._driver, *_AdminUserGroupDetailPageLocator._lstAddedUser)
    @property
    def _ddlAddUser(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._ddlAddUser)
    @property
    def _lstUserProfileCards(self):
        return ElementList(self._driver, *_AdminUserGroupDetailPageLocator._lstUserProfileCards)
    @property
    def _lblDeviceGroups(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._lblDeviceGroups)
    @property
    def _ecbxDeviceGroups(self):
        return EditableCombobox(self._driver, *_AdminUserGroupDetailPageLocator._ecbxDeviceGroups)
    @property
    def _txtSearch(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._txtSearch)
    @property
    def _iconListView(self):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._iconListView)

    """User Profile Card"""
    @property
    def _lstUserName (self):
        return ElementList(self._driver, *_AdminUserGroupDetailPageLocator._lstUserName)


    def _itemAddUserMenu(self,value):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._itemAddUserMenu(value))
    def _lblUserGroupName(self, group_name):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._lblUserGroupName(group_name))
    def _pnlUser(self, displayed_name):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._pnlUser(displayed_name))
    def _btnRemoveUser(self, value):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._btnRemoveUser(value))
    def _lnkDeviceGroupName(self, value):
        return Element(self._driver, *_AdminUserGroupDetailPageLocator._lnkDeviceGroupName(value))

    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: web driver
        @author: Thanh Le       
        @created_date: October 03, 2016      
        """     
        AdminUsersCommonPage.__init__(self, driver)
        
        
    def is_user_group_name_displayed(self, group_name, wait_time_out=None):
        """      
        @summary: Check if a user group is displayed or not by name      
        @param: group_name: name of user group would like to check
        @param: wait_time_out: time to wait for user group displays
        @return: True: user group is displayed, False: user group is not displayed
        @author: Thanh Le
        @created_date: October 03, 2016    
        """        
        return self._lblUserGroupName(group_name).is_displayed(wait_time_out)
    
    
    def is_change_icon_link_displayed(self):
        """      
        @summary: Check if icon link of a user group is displayed or not      
        @return: True: the icon link is displayed, False; the icon link is not displayed
        @author: Thanh Le  
        @created_date: October 03, 2016    
        """
        return self._lnkChangeIcon.is_displayed(10)


    def add_user_to_group(self, email_address):
        """      
        @summary: Add a user to user group by user's email         
        @param email_address: email of user would like to add to user group
        @return: AdminUserGroupDetailPage
        @author: Thanh Le     
        @created_date: October 03, 2016    
        """
        self._btnAddUsers.wait_until_displayed()
        self._btnAddUsers.click()
        ChooseUsersDialog(self._driver).choose_user(email_address)
        return self


    def open_add_user_dialog(self):
        """      
        @summary: Add a user to user group by user's email         
        @param email_address: email of user would like to add to user group
        @return: AdminUserGroupDetailPage
        @author: Thanh Le     
        @created_date: March 08, 2017  
        """  
        self._btnAddUsers.wait_until_displayed()
        self._btnAddUsers.click()
        return ChooseUsersDialog(self._driver)


    def get_property(self, value):
        """      
        @summary: Get property of a device group
        @param value: property of a device group
        @return: property of a device group
        @author: Thanh Le
        @created_date: October 03, 2016
        """
        self.wait_untill_success_msg_disappeared()
        if value == ApplicationConst.LBL_DEVICE_GROUPS_PROPERTY:
            return self._lblDeviceGroups.text


    def delete_user_group(self, wait_for_completed=True):
        """      
        @summary: Delete a user group      
        @param wait_for_completed: time wait for completing delete
        @return: Admin User Group Detail Page
        @author: Thanh Le    
        @created_date: October 03, 2016    
        """
        self._btnDeleteGroup.click()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        
        # check succeed message
        if wait_for_completed:
            self.wait_untill_success_msg_disappeared()
        
        from pages.suitable_tech.admin.advanced.users.admin_users_page import AdminUsersPage
        return AdminUsersPage(self._driver, wait_for_completed)    
    
    
    def is_user_existed(self, displayed_name, wait_time_out=None):
        """      
        @summary: Check if a user is existed or not by full name
        @param displayed_name: full name of user would like to check
        @param wait_time_out: time to wait for use panel displaying
        @return: True: the user is existed, False: the user is not existed
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        return self._pnlUser(displayed_name).is_displayed(wait_time_out)
    
    
    def is_user_not_existed(self, displayed_name, wait_time_out=None):
        """      
        @summary: Check if a user is existed or not by full name
        @param displayed_name: full name of user would like to check
        @param wait_time_out: time to wait for use panel disappearing
        @return: True: the user is existed, False: the user is not existed
        @author: Thanh Le
        @created_date: October 03, 2016    
        """
        return self._pnlUser(displayed_name).is_disappeared(wait_time_out)
    
    
    def remove_user(self, user_name):
        """      
        @summary: Remove a user by user name    
        @param user_name: the user would like to remove
        @return: AdminUserGroupDetailPage
        @author: Thanh Le  
        @created_date: October 03, 2016    
        """
        self._btnRemoveUser(user_name).click()
        self.wait_for_loading()
        self._pnlUser(user_name).wait_until_disappeared(5)
        return self


    def change_group_name(self, new_group_name):
        """      
        @summary: Change name of user group  
        @param new_group_name: new name would like to set for user group
        @return: Admin User Group Detail Page
        @author:  Thanh le 
        @created_date: October 03, 2016          
        """
        self._btnEditGroup.click()
        from pages.suitable_tech.admin.dialogs.edit_user_group_dialog import EditUserGroupDialog
        dialog = EditUserGroupDialog(self._driver)
        dialog.change_user_group_name(new_group_name)
        return self 


    def goto_user_detail_page(self, user):
        """
        @summary: Go to user detail page
        @param user: user would like to view detail
        @return: Admin User Detail Page
        @author: Quang Tran
        @created_date: October 03, 2016    
        """
        self._lblUserProfileCard(user.get_displayed_name()).wait_until_clickable().click()
        self._lblUserProfileCard(user.get_displayed_name()).wait_until_disappeared()
        from pages.suitable_tech.admin.advanced.users.admin_user_detail_page import AdminUserDetailPage   
        return AdminUserDetailPage(self._driver)


    def remove_user_from_organization(self, user):
        """      
        @summary: Remove a user from org
        @param user: user who would like to remove
        @return: Admin User Group Detail Page
        @author: Quang Tran  
        @created_date: October 03, 2016    
        """
        user_displayed_name = user.get_displayed_name()
        self.goto_user_detail_page(user).remove_user_from_organization()
        self._lblUserProfileCard(user_displayed_name).wait_until_disappeared()
        from pages.suitable_tech.admin.advanced.users.admin_users_page import AdminUsersPage
        return AdminUsersPage(self._driver)


    def wait_for_page_displayed(self, user_group_name):
        """      
        @summary: wait for a page displays
        @param user_group_name: user group would like to wait for display
        @return: Admin User Group Detail Page
        @author: Thanh Le      
        @created_date: October 03, 2016       
        """
        self._lblUserGroupName(user_group_name).wait_until_displayed()
        return self


    def get_users_goup_title(self, user_group):
        """      
        @summary: return number user of user group    
        @author: Thanh Le     
        @created_date: June 02, 2017
        """
        return self._titleUserGroup(user_group).text


    def click_add_user_button_and_select(self, value):
        """      
        @summary: Select add all user menu  
        @author: Tan Le     
        @created_date: July 10, 2017
        """
        self._ddlAddUser.click()
        self._itemAddUserMenu(value).click()
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        sleep(2)
        return self


    def is_all_users_added(self, organization):
        """      
        @summary: Select add all user menu  
        @author: Tan Le     
        @created_date: July 10, 2017
        """
        expected_users = len(UserAPI.get_list_users(organization))
        actual_users = self._lstAddedUser.count()
        print("Expected users:" + str(expected_users) + ", Actual users:" + str(actual_users))
        return expected_users == actual_users


    def get_all_users_in_group(self):
        return self._lstUserProfileCards.count()


    def add_device_group_to_user_group(self, device_group_name):
        """      
        @summary: Add device group to group  
        @author: Tan Le
        @param device_group_name: add device group has name device_group_name into user group    
        @created_date: Oct 19, 2017
        """
        from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
        self._btnEditGroup.wait_until_clickable(20)
        self._btnEditGroup.click()
        self._ecbxDeviceGroups.select(device_group_name, self._ecbxDeviceGroups._value)
        DialogBase(self._driver).submit()
        return self


    def goto_device_group_detail_page(self, device_group_name):
        """      
        @summary: Go to device group detail page
        @author: Tan Le
        @param device_group_name: go to device group has name is device_group_name
        @created_date: Oct 19, 2017
        """
        self._lnkDeviceGroupName(device_group_name).wait_until_clickable(20)
        self._lnkDeviceGroupName(device_group_name).click()
        from pages.suitable_tech.admin.advanced.beams.admin_beams_devices_page import AdminBeamsDevicesPage
        return AdminBeamsDevicesPage(self._driver)


    def is_add_user_button_displayed(self, wait_time_out=None):
        """      
        @summary: Check button Add User is displayed or not
        @author: Tan Le
        @created_date: Nov 20, 2017
        """
        return self._btnAddUsers.is_displayed(wait_time_out)

    def check_sort_by_work_correctly(self):
        """
        @summary: Check Sort By ddl can sort with each label
        @return: True if Sort By ddl can sort with all label when click for each, Fail if Sort By ddl can not sort
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """

        btn_sort_by_xpath = "//div[@class='row master-detail']//div[@is-open='sortDropdownOpen']/button"
        return self.check_sort_by_work(btn_sort_by_xpath, page = "Usergroup details")


    def get_users_sort_by_data_list(self, sort_by):
        """
        @summary: Get list of users after select a label of Sort By ddl
        @param sort_by: a label in Sort By ddl
        @return: list of users
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """

        elements = self._lstUserName.get_all_elements()

        data_list=[]
        for i in range (len(elements)):
            data = elements[i].text
            if sort_by == "first_name" or sort_by == "last_name":
                if "@" in data:
                    data = ""
            if sort_by == "first_name":
                data = data[:11]
            if sort_by == "last_name":
                data = data[12:]

            data_list.append(data)

        return data_list


    def search_for_user(self, search_value):
        """
        @summary: Search for a user
        @param search_value: criteria for searching a user
        @return: Admin Users Page
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """
        self._txtSearch.wait_until_displayed().type(search_value)
        self._wait_for_loading(20)
        return self


    def check_search_user_work_correctly(self, user):
        """
        @summary: Check search function for user work
        @return: True if Search returns correct values, Fail if Search returns incorrect values
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """

        self.search_for_user(user.email_address)
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


    def check_table_users_can_sort(self):
        """
        @summary: Check table can sort with each label
        @return: True if table can sort with all label when click for each, Fail if table can not sort
        @author: Khoi Ngo
        @created_date: Mar 05, 2018
        """
        xpath_table = "//div[@class='gallery-group']//table[@class='table table-hover ng-scope']"
        return self.check_sort_table_work(xpath_table)


    def switch_to_list_view(self):
        """
        @summary: Switch to list view
        @return: User Group details page
        @author: Thanh Le
        @created_date: August 08, 2016
        """
        self._iconListView.click()
        self.wait_for_loading(5)
        return self

