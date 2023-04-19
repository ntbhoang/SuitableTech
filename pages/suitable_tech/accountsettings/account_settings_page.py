from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.accountsettings.account_setting_common_page import AccountSettingsCommonPage
from common.application_constants import ApplicationConst
from pages.suitable_tech.user.password_change_page import PasswordChangePage
from time import sleep
from common.constant import Language
from core.webdriver.elements.editable_combobox import EditableCombobox


class _AccountSettingsPageLocator(object):
    _lnkSetting = (By.XPATH, "//li[@class='active']/a/span[@class='ng-scope']")
    _btnDisconectGoogle = (By.XPATH, "//div[@ng-class='googleAuth.provider']")
    _lbkChangeYourPassword = (By.XPATH, "//a[@href='/accounts/password_change']")
    _lnkChangeDefaultUserIcon = (By.XPATH, "//div[@can-remove='defaultImage']//a[@ng-click='changeImage()']")
    _btnRemoveDefaultUserIcon = (By.XPATH, "//div[@can-remove='defaultImage']//button[@ng-click='removeImage()']")
    _ecbxLanguage = (By.XPATH, "//div[@ng-model='settings.language']//span[@aria-label='Select box activate']")
    _btnSave = (By.XPATH, "//button[@ng-click='save()']")
    _txtFirstName = (By.XPATH, "//input[@ng-model='settings.first_name']")
    _txtLastName = (By.XPATH, "//input[@ng-model='settings.last_name']")
    _lblHeader = (By.XPATH, "//h2[@class='heading']")
    _btnShowAllHelpMessages = (By.XPATH, ".//button[@ng-click='resetHelp()']")

    @staticmethod
    def _lblOrgTitle(value):
        return (By.XPATH, u"//div[@ng-repeat='organization in organizations']/h5[.=\"{}\"]".format(value))
    @staticmethod
    def _chkDisplayURLConnectInvitation():
        return (By.XPATH, u"//section[@class='settings-section ng-scope'][.//h4[text()='{}']]//input[@ng-change='patchModel()']".format(ApplicationConst.LBL_GROUP_PROPERTY))
    @staticmethod
    def _lnkChangeOrgUserIcon(org_name):
        return (By.XPATH, u"//h5[.=\"{}\"]/..//a[@ng-click='changeImage()']".format(org_name))
    
    
class AccountSettingsPage(AccountSettingsCommonPage):
    """
    @description: This is page object class for Account Settings page.
        This page will be opened after clicking Your Account link in Admin dropdown menu on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/account/settings/ for more details.
    @page: Account Settings page
    @author: Thanh Le
    """

    """    Properties    """
    @property
    def _lblHeader(self):
        return Element(self._driver, *_AccountSettingsPageLocator._lblHeader)
    @property
    def _lbkChangeYourPassword(self):
        return Element(self._driver, *_AccountSettingsPageLocator._lbkChangeYourPassword)
    @property
    def _lnkChangeDefaultUserIcon(self):
        return Element(self._driver, *_AccountSettingsPageLocator._lnkChangeDefaultUserIcon)
    @property
    def _btnRemoveDefaultUserIcon(self):
        return Element(self._driver, *_AccountSettingsPageLocator._btnRemoveDefaultUserIcon)
    @property
    def _ecbxLanguage(self):
        return EditableCombobox(self._driver, *_AccountSettingsPageLocator._ecbxLanguage)
    @property
    def _btnSave(self):
        return Element(self._driver, *_AccountSettingsPageLocator._btnSave)
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_AccountSettingsPageLocator._txtFirstName)
    @property
    def _txtLastName(self):
        return Element(self._driver, *_AccountSettingsPageLocator._txtLastName)
    @property
    def _btnShowAllHelpMessages(self):
        return Element(self._driver, *_AccountSettingsPageLocator._btnShowAllHelpMessages)

    def _lblOrgTitle(self, value):
        return Element(self._driver, *_AccountSettingsPageLocator._lblOrgTitle(value))
    def _lnkChangeOrgUserIcon(self, org_name):
        return Element(self._driver, *_AccountSettingsPageLocator._lnkChangeOrgUserIcon(org_name))
    def _btnDisconectGoogle(self):
        return Element(self._driver, *_AccountSettingsPageLocator._btnDisconectGoogle)

    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method         
        @param driver: Web Driver
        @author: Thanh Le
        """
        AccountSettingsCommonPage.__init__(self, driver)
        self._lblHeader.wait_until_displayed()
        
        
    def is_org_title_displayed(self, orgtitle, timeout=5):
        """      
        @summary: Check if an Organization's name displays or not        
        @param orgtitle: organization's name 
        @return: True: org name displays, False: org name does not display
        @author: Thanh Le
        """
        return self._lblOrgTitle(orgtitle).is_displayed(timeout)
    
    
    def disconect_from_google(self):
        """      
        @summary:  Method to disconnect from GSSO by clicking the 'Disconnect from Google' button on Account Settings page
                the 'Disconnect Successful' page displays       
        @return: DisassociationCompletedPage: This is 'Disconnect Successful' page
        @author: Duy Nguyen
        """
        self._btnDisconectGoogle().click_element()
        from pages.suitable_tech.user.disassociation_complete_page import DisassociationCompletedPage
        return DisassociationCompletedPage(self._driver)
    
    
    def goto_change_password_page(self):
        """      
        @summary: Go to Change Password page by clicking on Change Your Password link       
        @return: PasswordChangePage page
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        self._lbkChangeYourPassword.click()
        return PasswordChangePage(self._driver)

    
    def change_user_icon(self, image_path, org_name=""):
        """      
        @summary: Method to change user icon's image      
        @param:
            - image_path: local image file path
            - left | top | width | height : the boundary of crop-tracker element  
        @return: AccountSettingsPage: Account Settings page still displays after changing user's icon image successfully
        @author: Quang Tran      
        """
        if org_name:
            self._lnkChangeOrgUserIcon(org_name).scroll_to().wait_until_clickable().click()
        else:
            self._lnkChangeDefaultUserIcon.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.upload_image_dialog import UploadImageDialog
        dialog = UploadImageDialog(self._driver)
        dialog.choose_file(image_path)
        dialog.move_crop_tracker()
        dialog.submit()
        
        #wait for updating new icon
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
            ico_url = self.get_icon_link()
            ext = ico_url.rsplit('.', 1)
        
        return self
    
    
    def remove_user_icon(self):
        """      
        @summary: Remove the icon image of a user
        @return: AccountSettingsPage: Account Settings page still displays after removing user's icon image successfully
        @author: Quang Tran 
        """
        btn_remove = self._btnRemoveDefaultUserIcon
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
    
    
    def is_disconnect_google_button_displayed(self, wait_time = 2):
        """
        @summary: check if disconnect google button displayed
        @return: True: the disconnect google button is displayed
                False: the disconnect google button is not displayed
        @author: Duy Nguyen
        """
        return self._btnDisconectGoogle().is_displayed(wait_time)
    
    
    def set_user_language(self, user):
        """
        @summary: set user's language in Account setting page. The language is get from setting run time 
        @param user: user that you want to set language 
        @author: THanh Le
        """
        
        self.set_first_last_name(user).set_language(self._driver.driverSetting.language).save_change()
        return self
    
    
    def set_first_last_name(self, user):
        if user.first_name:
            self._txtFirstName.type(user.first_name)
            print("set first name : {}".format(user.first_name))
        if user.last_name:
            self._txtLastName.type(user.last_name)
            print("set last name : {}".format(user.last_name))
        return self
    
    
    def set_language(self, language=Language.ENGLISH):
        """
        @summary: set user language
        @return: True: the disconnect google button is displayed
                False: the disconnect google button is not displayed
        @author: Duy Nguyen
        """
        
        if(language == Language.ENGLISH):
            language = "English"
        elif(language == Language.FRENCH):
            language = u"Français"
        elif(language == Language.JAPANESE):
            language = u"日本語"
        
        self._ecbxLanguage.select(language, xpath_ext="//div[@ng-model='settings.language']")        
        return self
        
        
    def save_change(self, wait_for_completed=True):
        """
        @summary: click on button 'Save Change' in Account setting page
        @param wait_for_completed: need to wait for saving complete or not
        @author: Thanh Le
        """
        self._btnSave.wait_until_clickable().click_element()    
        if wait_for_completed:
            self.wait_untill_success_msg_disappeared()
        return self
        
        
    def is_contact_info_correct(self,user):
        """      
        @summary: Check if an Organization's name displays or not        
        @param user: user information 
        @return: True: contact info displays correct, False: contact info displays not correct
        @author: Thanh Le
        """
        return user.first_name == self._txtFirstName.get_attribute("value") and user.last_name == self._txtLastName.get_attribute("value")


    def show_all_help_messages(self):
        """
        @summary: Show all help messages
        @author: Thanh Le
        """
        self._btnShowAllHelpMessages.wait_until_clickable().scroll_to().click()
        return self

