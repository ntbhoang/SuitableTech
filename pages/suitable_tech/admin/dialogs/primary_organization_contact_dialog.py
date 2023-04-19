from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from time import sleep
from common.stopwatch import Stopwatch
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase


class _PrimaryOrganizationContactDialogLocator(object):
    """popup Primary Org Contact"""
    _popupPrimaryOrgContact = (By.XPATH, "//div[@class='organization ng-scope']")
    _btnDismissOrgContact = (By.XPATH, "//div[@class='organization ng-scope']//button[contains(@ng-click,'dismiss')]")
    _btnSaveOrgContact = (By.XPATH, "//div[@class='organization ng-scope']//button[contains(@ng-click,'save')]")
    _txtFirstName = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.first_name']")
    _txtLastName = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.last_name']")
    _txtCompanyName = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.company_name']")
    _txtJobTitle = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.job_title']")
    _txtEmail = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.email']")
    _txtPhone = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.phone']")
    _txtAddress1 = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.address_line_1']")
    _txtAddress2 = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.address_line_2']")
    _txtCity = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.city']")
    _txtPostalCode = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.postal_code']")
    _lblSuccessMessage = (By.XPATH, "//div[@class='alert alert-success']//span[@ng-bind-html='message.content']")
    _txtState = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.state']")
    _txtCountry = (By.XPATH, "//input[@ng-model='organizationSettings.contact_info.country']")


class PrimaryOrganizationContactDialog(DialogBase):
    """    Properties    """  
    @property
    def _lblSuccessMessage(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._lblSuccessMessage)
    @property
    def _popupPrimaryOrgContact(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._popupPrimaryOrgContact)
    @property
    def _btnDismissOrgContact(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._btnDismissOrgContact)
    @property
    def _btnSaveOrgContact(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._btnSaveOrgContact)
    @property
    def _txtFirstName(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtFirstName)
    @property
    def _txtLastName(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtLastName)
    @property
    def _txtCompanyName(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtCompanyName)
    @property
    def _txtJobTitle(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtJobTitle)
    @property
    def _txtEmail(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtEmail)
    @property
    def _txtPhone(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtPhone)
    @property
    def _txtAddress1(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtAddress1)
    @property
    def _txtAddress2(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtAddress2)
    @property
    def _txtCity(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtCity)
    @property
    def _txtPostalCode(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtPostalCode)
    @property
    def _txtState(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtState)
    @property
    def _txtCountry(self):
        return Element(self._driver, *_PrimaryOrganizationContactDialogLocator._txtCountry)
    
    """    Methods    """
    def __init__(self, driver):   
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """      
        self._driver = driver
        self._popupPrimaryOrgContact.wait_until_displayed()
        self._btnDismissOrgContact.wait_until_displayed()
        self._btnSaveOrgContact.wait_until_displayed()   
        
    
    def submit_primary_org_contact_info (self, info):
        if self.is_primary_organization_contact_displayed(2):
            self._txtFirstName.type(info['first_name'])
            self._txtLastName.type(info['last_name'])
            self._txtCompanyName.type(info['company_name'])
            self._txtJobTitle.type(info['job_title'])
            self._txtEmail.type(info['email'])
            self._txtPhone.type(info['phone'])
            self._txtAddress1.type(info['address_line_1'])
            self._txtAddress2.type(info['address_line_2'])
            self._txtCity.type(info['city'])
            self._txtPostalCode.type(info['postal_code'])
            self._txtState.type(info['state'])
            self._txtCountry.type(info['country'])
            self._btnSaveOrgContact.click()
            self.wait_untill_success_msg_disappeared()
        return self
    
    
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
        
    
    def close_primary_org_contact_info (self):
        if self.is_primary_organization_contact_displayed(2):
            self._btnDismissOrgContact.wait_until_displayed(5)
            self._btnDismissOrgContact.click()
            self._popupPrimaryOrgContact.wait_until_disappeared(5)
        return self
    
    
    def is_primary_organization_contact_displayed(self, timeout=None):
        """      
        @summary: Check if the primary org contact is displayed in setting or not      
        @return: True: the primary org is displayed
                False: the primary org is not displayed
        @author: Thanh le
        """
        return  self._popupPrimaryOrgContact.is_displayed(timeout)
        
    
    def wait_page_ready(self):
        """
        @summary: This action use to wait a page ready
        @author: Thanh Le
        """
        try:
            sw = Stopwatch()
            sw.start()
            timeout=30
            while(timeout > 0):
                page_state = self._driver.execute_script('return document.readyState;')
                if page_state == 'complete':
                    break
                timeout -= sw.elapsed().total_seconds()
        except Exception as ex:
            raise ex    
        