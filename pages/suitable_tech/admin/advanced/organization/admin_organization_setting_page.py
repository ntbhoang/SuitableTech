from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.organization.admin_organization_common_page import OrganizationCommonPage
from asyncio.tasks import sleep

class _OrganizationSettingsPageLocator(object):
    _txtOrganizationName = (By.XPATH, "//input[@ng-model='organizationSettings.name']")
    _txtEmailNotifications = (By.XPATH, "//input[@ng-model='organizationSettings.notification_from_name']")
    _btnSaveSettings = (By.XPATH, "//form[@name='organizationSettingsForm']//input[@type='submit']")
    _txtDefaultInviteMessage = (By.XPATH, "//textarea[@ng-model='organizationSettings.default_invite_message']")
    _sectionBeamContent = (By.XPATH, "//section[contains(@ng-if,'showBeamContent')]")
    _btnManageBeamContent = (By.XPATH, "//button[@ng-click='manageBeamContent()']")

    """Primary Org Contact"""
    _txtFirstName = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.first_name']")
    _txtLastName = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.last_name']")
    _txtCompanyName = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.company_name']")
    _txtJobTitle = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.job_title']")
    _txtEmail = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.email']")
    _txtPhone = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.phone']")
    _txtAddress1 = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.address_line_1']")
    _txtAddress2 = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.address_line_2']")
    _txtCity = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.city']")
    _txtPostalCode = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.postal_code']")
    _txtState = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.state']")
    _txtCountry = (By.XPATH, "//input[@ng-model='primaryContact.contact_info.country']")
    _btnSaveSettingsPriOrgContact = (By.XPATH, "//form[@name='primaryContactForm']//input[@type='submit']")
    
    
class OrganizationSettingsPage(OrganizationCommonPage):
    """
    @description: This is page object class for Admin Organization Authentication page.
        This page will be opened after clicking Settings tab on Organization page.
        Please visit https://stg1.suitabletech.com/manage/129/#/organization/ for more details.
    @page: Admin Organization Settings page
    @author: thanh.viet.le
    """

    """    Properties    """
    @property
    def _btnManageBeamContent(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._btnManageBeamContent)
    @property
    def _sectionBeamContent(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._sectionBeamContent)
    @property
    def _txtOrganizationName(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtOrganizationName)
    @property
    def _txtEmailNotifications(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtEmailNotifications)
    @property
    def _btnSaveSettings(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._btnSaveSettings)
    @property
    def _txtDefaultInviteMessage(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtDefaultInviteMessage)
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtFirstName)
    @property
    def _txtLastName(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtLastName)
    @property
    def _txtCompanyName(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtCompanyName)
    @property
    def _txtJobTitle(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtJobTitle)
    @property
    def _txtEmail(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtEmail)
    @property
    def _txtPhone(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtPhone)
    @property
    def _txtAddress1(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtAddress1)
    @property
    def _txtAddress2(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtAddress2)
    @property
    def _txtCity(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtCity)
    @property
    def _txtPostalCode(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtPostalCode)
    @property
    def _txtState(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtState)
    @property
    def _txtCountry(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._txtCountry)
    @property
    def _btnSaveSettingsPriOrgContact(self):
        return Element(self._driver, *_OrganizationSettingsPageLocator._btnSaveSettingsPriOrgContact)
    
    
    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web driver 
        @author: Khoi Ngo       
        """      
        OrganizationCommonPage.__init__(self, driver)
        self.wait_for_loading()

    
    def is_beam_content_section_displayed(self):
        """      
        @summary: Check if beam content section is displayed or not    
        @return: True: Beam Content section is displayed
        @author: Thanh Le
        """        
        return self._sectionBeamContent.is_displayed()

    
    def submit_email_notifications_name(self, name):
        """
        @summary: This action use to input value to Email Notifications text-box
        @param: name: title of notification email
        @return: OrganizationSettingsPage
        @author: Duy Nguyen
        """
        from time import sleep
        sleep(1)
        self._txtEmailNotifications.type(name)
        sleep(1)
        self._btnSaveSettings.click()
        self.wait_untill_success_msg_disappeared()
        return self
    
    
    def get_email_notifications_name(self):
        """
        @summary: This action use to get value of Email Notifications text-box
        @return: OrganizationSettingsPage
        @author: Duy Nguyen
        """
        return self._txtEmailNotifications.get_attribute("value")


    def set_default_invite_message(self, default_text):
        """      
        @summary: The method to set Default Invite Message
        @param default_text: default text
        @return: OrganizationSettingsPage
        @author: Thanh Le
        @created_date: March 09, 2017
        """
        from time import sleep
        sleep(1)
        self._txtDefaultInviteMessage.type(default_text)
        sleep(1)
        self._btnSaveSettings.click()
        self.wait_untill_success_msg_disappeared()
        return self


    def open_beam_content_dialog(self):        
        """
        @summary: The method to open beam content dialog
        @return: BeamContentDialog
        @author: Thanh Le
        @created_date: May 04, 2017
        """
        self._btnManageBeamContent.scroll_to().wait_until_clickable().click()  
        if self._btnManageBeamContent.is_displayed(5):
            self._driver.refresh()
            self._btnManageBeamContent.jsclick()
        from pages.suitable_tech.admin.dialogs.beam_content_dialog import BeamContentDialog
        beam_content_dialog = BeamContentDialog(self._driver)
        if not beam_content_dialog._btnContinue.is_displayed(3):
            self._btnBeamContent.scroll_to().jsclick()
        return beam_content_dialog
    
    
    def is_data_of_primary_org_contact_correct(self, contact_info):
        """      
        @summary: The method to check data of primary org contact 
        @return: True/False
        @author: Thanh Le
        @created_date: May 04, 2017
        """
        print('Check contact info at Org Settings page')
        if not self._txtFirstName.get_attribute('value') == contact_info['first_name']:
            print('Frist Name info is incorrect.')
            return False
        if not self._txtLastName.get_attribute('value') == contact_info['last_name']:
            print('Last Name info is incorrect.')
            return False
        if not self._txtCompanyName.get_attribute('value') == contact_info['company_name']:
            print('Company Name info is incorrect.')
            return False
        if not self._txtJobTitle.get_attribute('value') == contact_info['job_title']:
            print('Job Title info is incorrect.')
            return  False
        if not self._txtEmail.get_attribute('value') == contact_info['email']:
            print('Email info is incorrect.')
            return  False
        if not self._txtPhone.get_attribute('value') == contact_info['phone']:
            print('Phone info is incorrect.')
            return False
        if not self._txtAddress1.get_attribute('value') == contact_info['address_line_1']:
            print('Address 1 info is incorrect.')
            return False
        if not self._txtAddress2.get_attribute('value') == contact_info['address_line_2']:
            print('Address 2 info is incorrect.')
            return False
        if not self._txtCity.get_attribute('value') == contact_info['city']:
            print('City info is incorrect.')
            return False
        if not self._txtPostalCode.get_attribute('value') == contact_info['postal_code']:
            print('Postal code info is incorrect.')
            return False
        if not self._txtState.get_attribute('value') == contact_info['state']:
            print('State info is incorrect.')
            return False
        if not self._txtCountry.get_attribute('value') == contact_info['country']:
            print('Country info is incorrect.')
            return False
        
        return True