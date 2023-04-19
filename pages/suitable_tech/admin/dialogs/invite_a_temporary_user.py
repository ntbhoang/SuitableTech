from datetime import datetime
from selenium.webdriver.common.by import By
from core.webdriver.elements.datepicker import DatePicker
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from common.application_constants import ApplicationConst
from time import sleep

class _TemporaryAccessTimeLocator():
    _txtInviteUserEmail = (By.CSS_SELECTOR, "form[name='tempAccessForm'] input[name='email']")
    _txtInviteUserFirstName = (By.XPATH, "//label[@for='first_name']//following-sibling::input")
    _txtInviteUserLastName = (By.XPATH, "//label[@for='last_name']//following-sibling::input")
    _chkALinkToBeamSoftware = (By.CSS_SELECTOR, "#show_installer_link")
    _chkRequireSessionAnswer = (By.CSS_SELECTOR, "#answer_required")
    _chkTheDefaultInvitationMessage = (By.CSS_SELECTOR, "#use_default_invite_message")
    _elmStartTime = (By.XPATH, "//div[@class='modal-content']//label[@for='start_date']/following-sibling::div//ul")
    _elmEndTime = (By.XPATH, "//div[@class='modal-content']//label[@for='end_date']/following-sibling::div//ul")    
    _txtStartingDate = (By.XPATH, "//div[@class='modal-content']//label[@for='start_date']/following-sibling::div//input")
    _txtStartingHour = (By.CSS_SELECTOR, "div[ng-model='accessTime.start_time'] input[ng-model='hours']")
    _txtStartingMinute = (By.CSS_SELECTOR, "div[ng-model='accessTime.start_time'] input[ng-model='minutes']")
    _btnStartingMeridian = (By.CSS_SELECTOR, "div[ng-model='accessTime.start_time'] button[ng-click='toggleMeridian()']")
    _btnStartingDatePicker = (By.XPATH, "//div[@class='modal-content']//label[@for='start_date']/following-sibling::div/span[@class='input-group-btn']//button")
    _txtEndingDate = (By.XPATH, "//div[@class='modal-content']//label[@for='end_date']/following-sibling::div//input")
    _txtEndingHour = (By.CSS_SELECTOR, "div[ng-model='accessTime.end_time'] input[ng-model='hours']")
    _txtEndingMinute = (By.CSS_SELECTOR, "div[ng-model='accessTime.end_time'] input[ng-model='minutes']")
    _btnEndingMeridian = (By.CSS_SELECTOR, "div[ng-model='accessTime.end_time'] button[ng-click='toggleMeridian()']")
    _btnEndingDatePicker = (By.XPATH, "//div[@class='modal-content']//label[@for='end_date']/following-sibling::div/span[@class='input-group-btn']//button")
    _btnDelete = (By.XPATH, "//button[@ng-click='delete()']")
    _txtEmailContact = (By.XPATH, "//label[@for='contact']//following-sibling::p")
    _ddlChooseDeviceGroup = (By.XPATH, "//div[@name='device_group' and @ng-model='accessTime.device_group']//li[@class='ui-select-choices-group']")
    _lblChooseDeviceGroup = (By.XPATH, "//span[@aria-label='Select box activate']")
    _txtChooseDeviceGroup = (By.XPATH, "//input[@type='search']")
    
    @staticmethod
    def _itmDeviceGroup(devicename):
        return (By.XPATH, u"//div[contains(@id,\"ui-select-choices\")]//span[text()=\"{}\"]".format(devicename))

class TemporaryAccessTime(DialogBase):
    """
    @description: This class is used for working on Access Time dialog
    @author: Quang Tran
    """
    
    
    """    Properties    """    
    def _itmDeviceGroup(self,devicename):
        return Element(self._driver, *_TemporaryAccessTimeLocator._itmDeviceGroup(devicename))
    @property
    def _txtChooseDeviceGroup(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtChooseDeviceGroup)
    @property
    def _lblChooseDeviceGroup(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._lblChooseDeviceGroup)
    @property
    def _ddlChooseDeviceGroup(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._ddlChooseDeviceGroup)
    @property
    def _txtStartingDate(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtStartingDate)
    @property
    def _txtStartingHour(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtStartingHour)
    @property
    def _txtStartingMinute(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtStartingMinute)
    @property
    def _btnStartingMeridian(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._btnStartingMeridian)
    @property
    def _txtEndingDate(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtEndingDate)
    @property
    def _txtEndingHour(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtEndingHour)
    @property
    def _txtEndingMinute(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtEndingMinute)
    @property
    def _btnEndingMeridian(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._btnEndingMeridian)    
    @property
    def _btnStartingDatePicker(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._btnStartingDatePicker)
    @property
    def _btnEndingDatePicker(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._btnEndingDatePicker)
    @property
    def _chkALinkToBeamSoftware(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._chkALinkToBeamSoftware)
    @property
    def _chkTheDefaultInvitationMessage(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._chkTheDefaultInvitationMessage)
    @property
    def _chkRequireSessionAnswer(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._chkRequireSessionAnswer)
    
    
    """    Methods    """
    def __init__(self, driver):
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        DialogBase.__init__(self, driver)


    def select_starting_date(self, start_date):
        """
        @summary: This action is used to select starting date for access time when inviting a temporary user
        @parameter: start_date: starting date
        @author: Thanh Le
        """
        self._btnStartingDatePicker.click()
        date_picker = DatePicker(self._driver, *_TemporaryAccessTimeLocator._elmStartTime)
        if not date_picker.is_displayed(3):
            self._btnStartingDatePicker.jsclick()
        date_picker.select_day(start_date.day, start_date.month, start_date.year)
    
    
    def select_ending_date(self, end_date):
        """
        @summary: This action is used to select ending date for access time when inviting a temporary user
        @parameter: end_date: ending date
        @author: Thanh Le
        """
        self._btnEndingDatePicker.click_element()
        date_picker = DatePicker(self._driver, *_TemporaryAccessTimeLocator._elmEndTime)
        if not date_picker.is_displayed(3):
            self._btnEndingDatePicker.jsclick()
        date_picker.select_day(end_date.day, end_date.month, end_date.year)
    
    
    def enter_time_range(self, start_date=None, end_date=None):
        """
        @summary: This action is used to enter time range for access time when inviting a temporary user
        @parameter: start_date: starting date
                    end_date: ending date
        @author: Thanh Le
        """
        if(start_date != None):
            self.select_starting_date(start_date)
            
            meridian = ApplicationConst.get_date_time_label(datetime.strftime(start_date, "%p"))
            if(self._btnStartingMeridian.text != meridian):
                self._btnStartingMeridian.click_element()         
            
            self._txtStartingHour.type(datetime.strftime(start_date, "%I"))
            self._txtStartingMinute.type(datetime.strftime(start_date, "%M"))
            
            
        if(end_date != None):
            self.select_ending_date(end_date)

            meridian = ApplicationConst.get_date_time_label(datetime.strftime(end_date, "%p"))
            if(self._btnEndingMeridian.text != meridian):
                self._btnEndingMeridian.click_element()

            self._txtEndingHour.type(datetime.strftime(end_date, "%I"))
            self._txtEndingMinute.type(datetime.strftime(end_date, "%M"))
        
            

    def checkbox_all(self, link_to_beam_sofware=None, default_invitation=None, require_session_answer=None):
        """
        @summary: This action is used to check all check-boxes on Invite a Temporary User form
        @parameter: link_to_beam_sofware: link to beam software checkbox
                    default_invitation: default invitation checkbox
                    require_session_answer: require session answer checkbox
        @author: Thanh Le
        """
        # checkbox include a link to beam software
        self.checkbox_link_to_beam_software(link_to_beam_sofware)
        # checkbox include the default invitation message
        self.checkbox_default_invitation(default_invitation)
        # checkbox require session answer
        self.checkbox_require_session_anwser(require_session_answer)
    
    
    def checkbox_link_to_beam_software(self, chk_link_to_beam_sofware):
        """
        @summary: This action is used to check the link to beam software check-box
        @parameter: chk_link_to_beam_sofware: link to beam software check-box
        @author: Thanh Le
        """
        if chk_link_to_beam_sofware != None:
            if chk_link_to_beam_sofware:
                self._chkALinkToBeamSoftware.check()
            else:
                self._chkALinkToBeamSoftware.uncheck()


    def checkbox_default_invitation(self, chkTheDefaultInvitationMessage):
        """
        @summary: This action is used to check the default invitation check-box
        @parameter: chkTheDefaultInvitationMessage: default invitation check-box
        @author: Thanh Le
        """
        if chkTheDefaultInvitationMessage != None:
            if chkTheDefaultInvitationMessage:
                self._chkTheDefaultInvitationMessage.check()
            else:
                self._chkTheDefaultInvitationMessage.uncheck()
    
    
    def checkbox_require_session_anwser(self, chkRequireSessionAnswer):
        """
        @summary: This action is used to check the require session answer checkbox
        @parameter: chkRequireSessionAnswer: require session answer checkbox
        @author: Thanh Le
        """
        if chkRequireSessionAnswer != None:
            if chkRequireSessionAnswer:
                self._chkRequireSessionAnswer.check()
            else:
                self._chkRequireSessionAnswer.uncheck()
    

class InviteTempUserDialog(TemporaryAccessTime):
    """
    @description: This class is used for working on Invite Temporary Use dialog
    @author: Quang Tran
    """
    
    
    """    Properties    """
    @property
    def _txtInviteUserEmail(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtInviteUserEmail)
    @property
    def _txtInviteUserFirstName(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtInviteUserFirstName)
    @property
    def _txtInviteUserLastName(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtInviteUserLastName)
    
    
    """    Methods    """
    def submit_invite_information(self, user, start_date=None, end_date=None, chk_link_to_beam_sofware=None\
                            , chk_default_invitation=None, chk_require_session_answer=None, device_group = None):
        """
        @summary: This action is used to submit invite information
        @parameter: user: user object
                    start_date: starting date
                    end_date: ending date
                    chk_link_to_beam_sofware: link to beam software checkbox
                    chk_default_invitation: default invitation checkbox
                    chk_require_session_answer: default invitation checkbox
                    device_group: device group name
        @author: Quang Tran
        """
        self.enter_invite_information(user.email_address, start_date, end_date\
                , chk_link_to_beam_sofware, chk_default_invitation, chk_require_session_answer, device_group)
        self.submit()      
        sleep(2)  

       
    def enter_invite_information(self, email_address=None\
                            , start_date=None, end_date=None, link_to_beam_sofware=None\
                            , default_invitation=None, require_session_answer=None, device_group = None):
        """
        @summary: This action is used to enter invite information
        @parameter: user: user object
                    start_date: starting date
                    end_date: ending date
                    chk_link_to_beam_sofware: link to beam software checkbox
                    chk_default_invitation: default invitation checkbox
                    chk_require_session_answer: default invitation checkbox
                    device_group: device group name
        @return: Dashboard page
        @author: Quang Tran        
        """
        if(email_address != None):
            self._txtInviteUserEmail.type(email_address)        
        if(device_group != None):
            self._lblChooseDeviceGroup.click()
            self._txtChooseDeviceGroup.type(device_group)
            self._itmDeviceGroup(device_group).click()
        
        self.enter_time_range(start_date, end_date)
        self.checkbox_all(link_to_beam_sofware, default_invitation, require_session_answer)
        
        return self


class EditTemporaryAccessTime(TemporaryAccessTime):
    """
    @description: This class is used for working on Edit Temporary Access Time dialog
    @author: Quang Tran
    """
    
    
    """    Properties    """    
    @property
    def _txtEmailContact(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._txtEmailContact)
    @property
    def _btnDelete(self):
        return Element(self._driver, *_TemporaryAccessTimeLocator._btnDelete)
    
    
    """    Methods    """
    def delete_accesstime(self):
        """
        @summary: This action is used to delete access time
        @author: Quang Tran
        """
        self._btnDelete.click()
    
    
    def edit_temporary_access_time(self, start_date=None, end_date=None, link_to_beam_sofware=None\
                            , default_invitation=None, require_session_answer=None):
        """
        @summary: This action is used to edit temporary access time
        @parameter: start_date: starting date
                    end_date: ending date
                    link_to_beam_sofware: link to beam software checkbox
                    default_invitation: default invitation checkbox
                    require_session_answer: default invitation checkbox
        @author: Quang Tran
        """
        self.enter_time_range(start_date, end_date)
        self.checkbox_all(link_to_beam_sofware, default_invitation, require_session_answer)
        self.submit()
        sleep(2)