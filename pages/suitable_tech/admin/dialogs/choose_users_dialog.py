from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from core.webdriver.elements.element_list import ElementList


class _ChooseUsersDialogLocator(object):
    _txbSearchUser = (By.XPATH, "//div[@class='modal-content']//input[@type='search']")
    _btnAddSelectedUser = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='ok()']")
    _btnInviteUser = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='createContact()']")
    _lstSelectedUser = (By.CSS_SELECTOR, "div[class= 'selected-user']")
    
    @staticmethod
    def _lblAvailableUser(search_value):
        return (By.XPATH, u"//div[@ng-repeat='contact in availableContacts']//*[.=\"{}\"]".format(search_value))
    @staticmethod
    def _lblSelectedUser(select_value):
        return (By.XPATH, u"//div[@class='selected-contacts contacts-list']//*[.=\"{}\"]".format(select_value))
    @staticmethod
    def _btnRemoveUser(display_name):
        return (By.XPATH, u"//h5[text()=\"{}\"]/ancestor::div[@class='selected-user']//div[contains(@class, 'remove-button')]".format(display_name))
class ChooseUsersDialog(DialogBase):
    """
    @description: This is page object class for Choose Users Dialog. You need to init it before using in page class.
    @page: Choose Users Dialog
    @author: Thanh Le
    """
    

    """    Properties    """
    @property
    def _txbSearchUser(self):
        return Element(self._driver, *_ChooseUsersDialogLocator._txbSearchUser)
    @property
    def _btnAddSelectedUser(self):
        return Element(self._driver, *_ChooseUsersDialogLocator._btnAddSelectedUser)    
    @property
    def _btnInviteUser(self):
        return Element(self._driver, *_ChooseUsersDialogLocator._btnInviteUser)
    @property
    def _lstSelectedUser(self):
        return ElementList(self._driver, *_ChooseUsersDialogLocator._lstSelectedUser)

    def _lblAvailableUser(self, search_value):
        return Element(self._driver, *_ChooseUsersDialogLocator._lblAvailableUser(search_value))
    def _lblSelectedUser(self,select_value):
        return Element(self._driver, *_ChooseUsersDialogLocator._lblSelectedUser(select_value))
    def _btnRemoveUser(self, display_name):
        return Element(self._driver, *_ChooseUsersDialogLocator._btnRemoveUser(display_name))
        
    
    """    Methods    """
    def __init__(self, driver):    
        """      
        @summary: Constructor method
        @param driver: web driver
        @author: Thanh Le         
        """    
        DialogBase.__init__(self, driver)
    
    
    def select_user(self, search_value):
        """      
        @summary: Select a user by searched value   
        @param search_value: value use to search for selecting user
        @return: User detail page
        @author: Thanh Le
        """
        self._wait_for_dialog_appeared()
        self.search_user(search_value = search_value, wait = True)
        self._lblAvailableUser(search_value).scroll_to().click_element()
        self._lblSelectedUser(search_value).wait_until_displayed()
        return self
    
        
    def search_user(self, search_value, wait = False):
        """      
        @summary: Select a user by searched value   
        @param search_value: value use to search for selecting user
        @return: User detail page
        @author: Thanh Le
        """
        self._txbSearchUser.wait_until_displayed(5)
        self._txbSearchUser.type(search_value)
        if wait:
            self._lblAvailableUser(search_value).wait_until_displayed()
    
    
    def invite_new_user(self, user):
        """      
        @summary: Invite a new user
        @param user: user would like to invite
        @return: ChooseUsersDialog
        @author: Thanh Le
        """
        self._btnInviteUser.scroll_to().click()
        from pages.suitable_tech.admin.dialogs.invite_new_user_dialog import InviteNewUserDialog
        simple_invite_new_user_dialog = InviteNewUserDialog(self._driver)
        simple_invite_new_user_dialog.submit_invite_information_for_simple_form(user)
        return self
    
    
    def choose_user(self, search_value):
        """      
        @summary: Choose user by search value
        @param search_value: value to search for choosing user
        @return: ChooseUsersDialog
        @author: Thanh Le     
        """
        self.select_user(search_value)
        self._btnAddSelectedUser.click_element()
        self._wait_for_dialog_disappeared()
        return None
    
    
    def add_selected_user(self):
        """      
        @summary: click Add Selected User button
        @return: ChooseUsersDialog
        @author: Khoi Ngo
        """
        self._btnAddSelectedUser.click_element()
        self._wait_for_dialog_disappeared()
        from pages.suitable_tech.admin.advanced.users.admin_user_group_detail_page import AdminUserGroupDetailPage
        return AdminUserGroupDetailPage(self._driver)
    
    
    def is_remove_user_button_displayed(self, user):
        """      
        @summary: Check if Remove User button displays or not
        @param email_address: email of user is checked remove button
        @return: ChooseUsersDialog
        @author: Thanh Le       
        """
        return self._btnRemoveUser(user.get_displayed_name()).is_displayed()


    def is_user_displayed_in_selected_list(self, email_address):
        """
        @summary: Check if user displays in selected list or not
        @param email_address: email_address of user would like to check
        @return: ChooseUsersDialog
        @author: Khoi Ngo
        """
        selected_user_list = self._lstSelectedUser.get_all_elements()
        for user in selected_user_list:
            if email_address in user.text:
                return True
        return False

