from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.users.admin_users_common_page import AdminUsersCommonPage
from core.webdriver.elements.dropdownlist import DropdownList
from core.webdriver.elements.element_list import ElementList
from common.application_constants import ApplicationConst
from pages.basepage import BasePage
from time import sleep
import re
from core.utilities.utilities import Utilities
from core.suitabletechapis.user_api import UserAPI
from data_test.dataobjects.user import User


class _AdminUsersPageLocator(object):
    _txtSearch = (By.XPATH, "//input[@type='search']")
    _btnClearSearch = (By.XPATH, "//span[contains(@class, 'clear')]")
    _lblProfileCard = (By.XPATH, "//div[@for='user']//div[@class='profile-title ng-binding']")
    _iconDelete = (By.XPATH, "//span[@class='clear-input glyphicon glyphicon-remove form-control-feedback text-muted']")
    _lblNoUsersFoundMessage = (By.XPATH, "//div[@ng-hide='users.length || usersContentLoading']//span[@class='ng-scope']//span")
    _lstUserProfileCards = (By.XPATH, "//div[@for='user']//a")
    _lstUserGroupProfileCards = (By.XPATH, "//div[@for='usergroup']//a")
    _ddlItems = (By.XPATH, "//div[contains(@is-open, 'itemsDropdownOpen')]")
    _btnsTopPagination = (By.XPATH, "//div[@ng-show='includeGroups']/div/div[@ng-model='pagination.groupsCurrentPage']")
    _lstTopPaginationPage = (By.XPATH, "//div[@ng-show='includeGroups']/div/div/li/a[@ng-click='selectPage(page.number, $event)']")
    _tblUserGroup= (By.CSS_SELECTOR, "div[ng-show='includeGroups']")
    
    """User Profile Card"""
    _lstUserName = (By.XPATH, '''//div[@ng-class="{'content-loading': usersContentLoading}"]//div[contains(@class,"profile-title")]''')

    @staticmethod
    def _lblUserProfileCard(value):
        return (By.XPATH, u"//h4[.=\"{}\"]/following::div[@ng-repeat='user in users']//div[@class='profile-title ng-binding' and contains(.,\"{}\")]".format(ApplicationConst.LBL_ADMIN_USERS_SECTION_USERS, value))
    @staticmethod
    def _lblUserIconMode(email, icon_type):
        return (By.XPATH, u"//*[.='{}']/..//span[contains(@ng-if,\"{}\") or contains(@is-visible,\"{}\")]".format(email, icon_type, icon_type))
    @staticmethod
    def _lblUserTitle(value):
        return (By.XPATH, u"//h3[.=\"{}\"]".format(value))
    @staticmethod
    def _pnlProfileCard(profile_title):
        return (By.XPATH, u"//div[@class='profile-title ng-binding' and normalize-space(.)=\"{}\"]/..".format(profile_title))    
    @staticmethod
    def _pnlProfileCardIcon(profile_title):
        return (By.XPATH, u"//div[@class='profile-title ng-binding' and normalize-space(.)=\"{}\"]/..//div[@class='profile-image-container ng-isolate-scope']".format(profile_title))
    @staticmethod
    def _pnlProfileRowIcon(profile_title):
        return (By.XPATH, u"//td[@class='ng-binding' and normalize-space(.)=\"{}\"]/parent::tr//div[@class='img-responsive small profile-image-container ng-isolate-scope']".format(profile_title))
    @staticmethod
    def _imgUserGroupIcon(user_group_name):
        return (By.XPATH,u"//div[@for='usergroup']//div[.=\"{}\"]/preceding-sibling::div//img".format(user_group_name))
    @staticmethod
    def _titleUserGroup(user_group_name):
        return (By.XPATH,u"//div[@for='usergroup'][.//div[contains(.,\"{}\")]]//div[@class='profile-detail']//span".format(user_group_name))
    @staticmethod
    def _icnGuestUser(display_name):
        return (By.XPATH,u"//div[text()=\"{}\"]/..//span[@uib-tooltip='Temporary User']".format(display_name))
 
    
class AdminUsersPage(AdminUsersCommonPage):
    """
    @description: This is page object class for Admin Users page.
        This page will be opened after clicking Users on Dashboard page.
        Please visit https://staging.suitabletech.com/manage/#/contacts/ for more details.
    @page: Admin Users page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _txtSearch(self):
        return Element(self._driver, *_AdminUsersPageLocator._txtSearch)
    @property
    def _btnClearSearch(self):
        return Element(self._driver, *_AdminUsersPageLocator._btnClearSearch)
    @property
    def _ddlItems(self):
        return DropdownList(self._driver, *_AdminUsersPageLocator._ddlItems)
    @property
    def _btnCreateDeviceGroup(self):
        return Element(self._driver, *_AdminUsersPageLocator._btnCreateDeviceGroup)
    @property
    def _lblProfileCard(self):
        return Element(self._driver, *_AdminUsersPageLocator._lblProfileCard)
    @property
    def _lstUserProfileCards(self):
        return ElementList(self._driver, *_AdminUsersPageLocator._lstUserProfileCards)
    @property
    def _lstUserGroupProfileCards(self):
        return ElementList(self._driver, *_AdminUsersPageLocator._lstUserGroupProfileCards)
    @property
    def _btnsTopPagination(self):
        return Element(self._driver, *_AdminUsersPageLocator._btnsTopPagination)
    @property
    def _lstTopPaginationPage(self):
        return ElementList(self._driver, *_AdminUsersPageLocator._lstTopPaginationPage)
    @property
    def _iconDelete(self):
        return Element(self._driver, *_AdminUsersPageLocator._iconDelete)
    @property
    def _lblNoUsersFoundMessage(self):
        return Element(self._driver, *_AdminUsersPageLocator._lblNoUsersFoundMessage)
    @property
    def _tblUserGroup(self):
        return Element(self._driver, *_AdminUsersPageLocator._tblUserGroup)

    def _lblUserIconMode(self, email, icon_type):
        return Element(self._driver, *_AdminUsersPageLocator._lblUserIconMode(email, icon_type))
    def _lblUserTitle(self, value):
        return Element(self._driver, *_AdminUsersPageLocator._lblUserTitle(value))
    def _pnlProfileCard(self, value):
        return Element(self._driver, *_AdminUsersPageLocator._pnlProfileCard(value))
    def _lblUserProfileCard(self, value):
        return Element(self._driver, *_AdminUsersPageLocator._lblUserProfileCard(value))
    def _pnlProfileCardIcon(self, value):
        return Element(self._driver, *_AdminUsersPageLocator._pnlProfileCardIcon(value))
    def _pnlProfileRowIcon(self, value):
        return Element(self._driver, *_AdminUsersPageLocator._pnlProfileRowIcon(value))
    def _imgUserGroupIcon(self, group_name):
        return Element(self._driver, *_AdminUsersPageLocator._imgUserGroupIcon(group_name))
    def _pnlListViewDeviceItem(self, panel_value):
        return Element(self._driver, *_AdminUsersPageLocator._pnlListViewDeviceItem(panel_value))
    def _titleUserGroup(self, usergroup):
        return Element(self._driver, *_AdminUsersPageLocator._titleUserGroup(usergroup))
    def _icnGuestUser(self, display_name):
        return Element(self._driver, *_AdminUsersPageLocator._icnGuestUser(display_name))

    """User Profile Card"""
    @property
    def _lstUserName(self):
        return ElementList(self._driver, *_AdminUsersPageLocator._lstUserName)


    """    Methods    """
    def __init__(self, driver, wait_for_loading=True):       
        """      
        @summary: Constructor method    
        @param driver: web driver
        @author: Thanh Le         
        """
        if(wait_for_loading):
            AdminUsersCommonPage.__init__(self, driver)
            self.wait_for_loading()
        else:
            BasePage.__init__(self, driver)
            
    
    def is_user_existed(self, search_value, check_value=None, wait_time_out=None):
        """      
        @summary: Check if a user is existed or not         
        @param search_value: user would like to check
        @param check_value: value used to check
        @param wait_time_out: time wait for user exists  
        @return: True: user is existed, False: user is not existed
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self.search_for_user(search_value)
        if(check_value != None):
            return self._lblUserProfileCard(check_value).is_displayed(wait_time_out)
        else:
            return self._lblUserProfileCard(search_value).is_displayed(wait_time_out)
    
    
    def is_user_not_existed(self, search_value, check_value=None, wait_time_out=None):
        """      
        @summary: Check if user is not existed
        @param search_value: user would like to check
        @param check_value: value used to check
        @param wait_time_out: time wait for user is not existed  
        @return: True: user is not existed, False: user is existed
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self.search_for_user(search_value)
        if(check_value != None):
            return self._lblUserProfileCard(check_value).is_disappeared(wait_time_out)
        else:
            return self._lblUserProfileCard(search_value).is_disappeared(wait_time_out)


    def click_items_button_and_select(self, value):
        """      
        @summary: Click Items button and select item in show dropdown list   
        @param value: item would like to select
        @return: Admin Users Page
        @author: Thanh Le     
        @created_date: October 03, 2016 
        """
        self._driver.refresh()
        self._ddlItems.select_by_partial_text(value)
        self._iconLoading.wait_until_disappeared()
        return self
    
        
    def is_user_group_existed(self, search_value, check_value = None, wait_time_out=None):
        """      
        @summary: Check if a user group is existed or not     
        @param search_value: user group would like to check
        @param check_value: criteria for searching
        @param wait_time_out: time out to wait for completing searching
        @return: True: the user group is existed, False: the user group is not existed
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self._txtSearch.wait_until_displayed().type(search_value)
        self._wait_for_loading()
        if(check_value != None):
            return self._pnlProfileCard(check_value).is_displayed(wait_time_out)
        else:
            return self._pnlProfileCard(search_value).is_displayed(wait_time_out)
    
    
    def is_user_group_not_existed(self, search_value, check_value = None, wait_time_out=None):
        """      
        @summary: Check if a user group is not exist  
        @param search_value: user group would like to check
        @param check_value: criteria for searching
        @param wait_time_out: time out to wait for completing searching
        @return: True: the user group is not existed, False: the user group is existed
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self._txtSearch.wait_until_displayed().type(search_value)
        self._wait_for_loading()
        if(check_value != None):
            return self._pnlProfileCard(check_value).is_disappeared(wait_time_out)
        else:
            return self._pnlProfileCard(search_value).is_disappeared(wait_time_out)
        
    
    def goto_user_detail_page(self, user):
        """      
        @summary: Go to detail page of a user 
        @param user: user would like to go to detail page
        @return: detail page of user
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self.search_for_user(user.email_address)
        return self.select_user(user.get_displayed_name())


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
            

    def search_for_user(self, search_value):
        """      
        @summary: Search for a user       
        @param search_value: criteria for searching a user
        @return: Admin Users Page
        @author: Thanh Le      
        @created_date: October 03, 2016 
        """
        self._txtSearch.wait_until_displayed().type(search_value)
        self._wait_for_loading(20)
        return self
     
    
    def remove_user_group_from_organization(self, group_name):
        """      
        @summary: Remove a user group form organization
        @param group_name: name of user group
        @return: Admin Users Page
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self.goto_user_group_detail_page(group_name).delete_user_group()
        self._pnlProfileCard(group_name).wait_until_disappeared()
        return self
    
    
    def remove_user_from_organization(self, user):
        """      
        @summary: Remove a user from an organization         
        @param user: user would like to remove
        @return: Admin Users Page
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self.goto_user_detail_page(user).remove_user_from_organization()
        return self
    
        
    def remove_all_test_users(self, keyword = "logigear1+user"):
        """      
        @summary: Remove all existing user matched searched keyword       
        @param keyword: criteria to remove user
        @return: Admin Users Page
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        from pages.suitable_tech.admin.advanced.users.admin_user_detail_page import AdminUserDetailPage   
        self.search_for_user(keyword)
        lst_user_profile_cards = self._lstUserProfileCards
        count = lst_user_profile_cards.count()
        while(count > 0):
            for i in range(0, count):
                web_elem = lst_user_profile_cards.get_element_at(i)
                if web_elem:
                    self._driver.execute_script("arguments[0].click();", web_elem)  
                    dialog = AdminUserDetailPage(self._driver)
                    dialog.remove_user_from_organization()
            
            self.search_for_user(keyword)
            # update runtime object
            lst_user_profile_cards = self._lstUserProfileCards
            count = lst_user_profile_cards.count(10)
                    
        return self
    
    
    def remove_all_test_user_groups(self, keyword = "LGVN"):
        """      
        @summary: Remove all existing users matched with searched criteria
        @param keyword: criteria for searching
        @return: Admin Users Page
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        from pages.suitable_tech.admin.advanced.users.admin_user_group_detail_page import AdminUserGroupDetailPage
        self.search_for_user(keyword)
        
        lst_user_group_profile_cards = self._lstUserGroupProfileCards   
        count = lst_user_group_profile_cards.count()
        while(count > 0):
            for i in range(0, count):
                web_elem = lst_user_group_profile_cards.get_element_at(i)
                if web_elem and web_elem.text:
                    self._driver.execute_script("arguments[0].click();", web_elem)   
                        
                    dialog = AdminUserGroupDetailPage(self._driver)
                    dialog.delete_user_group()
            
            self.search_for_user(keyword)        
            count = lst_user_group_profile_cards.count()
        
        return self
       
       
    def is_icon_delete_in_search_textbox_existed(self):
        """      
        @summary:  Check if the delete 'x' button is displayed or not       
        @return: True: 'x' button is display in search textbox, False: 'x' button is not displayed in search textbox
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        return self._iconDelete.is_displayed(2)  
    
    
    def get_no_users_found_message(self):
        """      
        @summary: Get 'No users match your search.' message
        @return: The message 'No users match your search.'
        @author: Thanh Le
        @created_date: October 03, 2016 
        """
        self._lblNoUsersFoundMessage.wait_until_displayed(5)
        return self._lblNoUsersFoundMessage.text
    

    def get_item_size_in_icon_view(self, value):
        """      
        @summary: Get the "imgsize" of the profile icon          
        @param value is the Name of User Group or User        
        @return: number type integer
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        try:
            return int(self._pnlProfileCardIcon(value).get_attribute("imgsize"))
        except Exception:
            return 0
    
    
    def get_item_size_in_list_view(self, value):
        """      
        @summary: Get the "imgsize" of the profile icon          
        @param value: the Name of User Group or User        
        @return: number type integer
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        try:
            return int(self._pnlProfileRowIcon(value).get_attribute("imgsize"))
        except Exception:
            return 0
        
        
    def get_user_group_icon_url(self, user_group_name):
        """      
        @summary: Get url of a user group       
        @param: user_group_name: name of user group would like to get url
        @return: user group's icon url
        @author: Thanh Le
        """
        self._txtSearch.type(user_group_name)
        image_element = self._imgUserGroupIcon(user_group_name)
        image_element.wait_until_displayed()
        
        return image_element.get_attribute("src")
     
     
    def is_item_displayed_in_list_mode(self, value):
        """      
        @summary: Get the "imgsize" of the profile icon          
        @param value: the Name of User Group or User or the email of the user        
        @return: True if item is displayed, and False if not
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        return self._pnlProfileRowIcon(value).is_displayed(5)
    
    
    def select_user(self, user_displayed_name):
        """      
        @summary: Select a user by user's full name
        @param user_displayed_name: name of user would like to select
        @return: Admin User Detail Page
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        # on Safari and Chrome: cannot click on element so using the jsclick
        self._pnlProfileCard(user_displayed_name).wait_until_displayed()
        sleep(1)
        self._pnlProfileCard(user_displayed_name).jsclick() 
        from pages.suitable_tech.admin.advanced.users.admin_user_detail_page import AdminUserDetailPage   
        return AdminUserDetailPage(self._driver)
    
    
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
    
    
    def are_users_existed(self, all_emails):
        """      
        @summary: Check if users are existed or not     
        @param all_emails: emails of users would like to check
        @return: True: the users are existed, False: the users are not existed
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        for email in all_emails:
            
            self.search_for_user(email)
            count = self._lstUserProfileCards.count(10)
            if count < 1:
                return False
            
        return True
        
    
    def remove_all_users_in_list(self, all_emails):
        """      
        @summary: Remove all existing users in list   
        @param all_emails: emails of users would like to remove
        @return: Admin Users Page
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        from pages.suitable_tech.admin.advanced.users.admin_user_detail_page import AdminUserDetailPage
        
        for email in all_emails:
            
            self.search_for_user(email)
            lst_user_profile_cards = self._lstUserProfileCards
            count = lst_user_profile_cards.count()
            while(count > 0):
                for i in range(0, count):
                    web_elem = lst_user_profile_cards.get_element_at(i)
                    if web_elem:
                        self._driver.execute_script("arguments[0].click();", web_elem)  
                        dialog = AdminUserDetailPage(self._driver)
                        dialog.remove_user_from_organization()
                count = lst_user_profile_cards.count(3)
                
        return self


    def get_number_users(self):
        """      
        @summary: return number of all user    
        @return: number all user
        @author: Thanh Le     
        @created_date: June 02, 2017
        """
        return self._lstUserProfileCards.count()
    
    
    def get_users_goup_title(self, user_group):
        """      
        @summary: return number user of user group    
        @author: Thanh Le     
        @created_date: June 02, 2017
        """
        return self._titleUserGroup(user_group).text


    def is_pagination_displayed(self):
        """
        @summary: Check if pagination displays or not
        @author: Khoi Ngo
        @created_date: October 19, 2017
        """
        return self._btnsTopPagination.is_displayed()


    def is_page_display_user_groups_number_correctly(self, usergroups_number):
        """
        @summary: Check if each page displays number of usergroup correctly or not
        @author: Khoi Ngo
        @created_date: October 19, 2017
        """
        page_number = self._lstTopPaginationPage.count()
        usergroup_number = self._lstUserGroupProfileCards.count()

        last_page = self._lstTopPaginationPage.get_element_at(page_number-1)
        last_page.click()
        if int(re.search('\d+', usergroups_number).group()) > usergroup_number:
            return False

        pagination_pages = self._lstTopPaginationPage.get_all_elements()
        for index, pagination_page in enumerate(pagination_pages):
            if index < page_number:
                pagination_page.click()
                if int(re.search('\d+', usergroups_number).group()) != usergroup_number:
                    return False
        return True


    def check_users_display_with_icon(self, list_email_user, icon_type, display=True):
        """
        @summary: Check if temporary user icon display or not
        @param list_email_user: list user wanna check
        @param icon_type:  icon type
        @author: Khoi Ngo
        @created_date: October 20, 2017
        """
        #sleep for more stable
        sleep(1)
        user = User()
        if display:
            for email in list_email_user:
                user.email_address= email
                display_name = UserAPI.get_displayed_name(user)
                if not self._lblUserIconMode(display_name, icon_type).is_displayed():
                    return False
            return True
        else:
            for email in list_email_user:
                user.email_address= email
                display_name = UserAPI.get_displayed_name(user)
                if self._lblUserIconMode(display_name, icon_type).is_displayed(4):
                    return True
            return False


    def is_temporary_user_icon_display(self, display_name):
        """
        @summary: Check if temporary user icon display or not
        @author: Khoi Ngo
        @created_date: October 20, 2017
        """
        return self._icnGuestUser(display_name).is_displayed()


    def is_user_group_table_displayed(self):
        return self._tblUserGroup.is_displayed()


    def export_csv_file(self):
        """
        @summary: Export file csv from admin users page
        @author: Quang Tran
        @created_date: Jan 29, 2018
        """
        self._btnTools.wait_until_clickable().click()
        self._lnkExportUser.wait_until_clickable().click()
        from core.webdriver.drivers.driver_windows import Driver_Windows
        Utilities.wait_for_file_is_downloaded(Driver_Windows.dir_name+"\\users.csv")
        return self


    def get_list_email_users_from_CSV_exported(self):
        """
        @summary: Get all email of users from file CSV exported
        @author: Quang Tran
        @created_date: Jan 29, 2018
        """
        from core.utilities.utilities import CSV_Utilities
        from core.webdriver.drivers.driver_windows import Driver_Windows

        list_email = CSV_Utilities.find_all_users_in_csv(Driver_Windows.dir_name+"\\users.csv")
        del list_email[0]
        return list_email


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

