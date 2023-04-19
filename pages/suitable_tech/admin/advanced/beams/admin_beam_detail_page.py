from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage
from pages.suitable_tech.admin.dialogs.edit_device_dialog import EditDeviceDialog
from time import sleep
from common.application_constants import ApplicationConst
from core.webdriver.elements.element_list import ElementList
from core.suitabletechapis.user_api import UserAPI
from common.constant import Platform


class _AdminBeamDetailPageLocator(object):
    _btnEdit = (By.XPATH, "//button[@type='button' and @ng-click='edit()']")
    _btnBeamAdvance = (By.XPATH, "//button[@class='btn btn-default' and @ng-click='showAdvanced()']")    
    _btnReserveThisBeam = (By.XPATH, "//button[@class='btn btn-default ng-scope']")
    _lnkChangeDeviceIcon = (By.XPATH, "//span[@class='change-picture-icon fa fa-pencil']/..")  
    _lblBeamLocation = (By.XPATH, "//dl[@class='dl-horizontal item-details']//span[@ng-show='device.location' or @ng-hide='device.location']")
    _lblBeamLabel = (By.XPATH, "//dl[@class='dl-horizontal item-details']//span[@ng-show='device.tagString()' or @ng-hide='device.tagString()']")
    _lblActivitiesOnRecentActivity = (By.XPATH, "//div[@class='ng-isolate-scope']/div[@class='tab-content']//div[@class='media activity-item ng-scope']")
    _btnShowMore = (By.XPATH, "//div[@class='ng-isolate-scope']/div[@class='tab-content']//button[@class='btn btn-xs btn-default' and @ng-click='loadMore()']")
   
    @staticmethod
    def _lblBeamGroup():
        return (By.XPATH, u"//dt[text()=\"{}\"]/following-sibling::dd[1]/span[not(@class='ng-hide')]".format(ApplicationConst.LBL_GROUP_PROPERTY))
    @staticmethod
    def _lblBeamName(device_name):
        return (By.XPATH, u"//h3[.=\"{}\"]".format(device_name))
    @staticmethod
    def _tabReservation():
        return (By.XPATH, u"//li[@heading='{}'][not(contains(@class,'active'))]/a".format(ApplicationConst.LBL_RESERVATION_TAB))
    @staticmethod
    def _lblStartTimeHeader(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::table/../h4".format(username))
    @staticmethod
    def _tblReservationData(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::tr".format(username))
    @staticmethod
    def _btnEditReservation(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::tr//button[@ng-if=\"reservation.status == 'requested' || reservation.status == 'confirmed'\"]".format(username))
    @staticmethod
    def _btnRejectReservation(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::tr//button[@ng-click=\"rejectReservation($event, reservation)\"]".format(username))
    @staticmethod
    def _btnApproveReservation(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::tr//button[@ng-click=\"approveReservation($event, reservation)\"]".format(username))
    @staticmethod
    def _lblReservationStatus(username):
        return (By.XPATH, u"//a[.=\"{}\"]/ancestor::tr//div[@class='reservation-status ng-binding']".format(username))

    """Mobile UI"""
    _btnMRejectReservation = (By.XPATH, "//button[@ng-click='rejectRequest()']")
    _btnMApproveReservation = (By.XPATH, "//button[@ng-if=\"editing && reservation.status == 'requested'\" and @type='submit']")

    @staticmethod
    def _btnMEditReservation(username):
        return (By.XPATH, u"//span[@for='reservation.user']/span[.='{}']/../../../div[@class='media-left media-middle']".format(username))


class AdminBeamDetailPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Beam Details page.
        This page will be opened after clicking Beam panel on Beams page.
        Please visit https://staging.suitabletech.com/manage/#/beams/787/beam/beam135909030/ for more details.
    @page: Beam Detail page
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _btnEdit(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnEdit)
    @property
    def _lblBeamLabel(self):
        return ElementList(self._driver, *_AdminBeamDetailPageLocator._lblBeamLabel)
    @property
    def _lblBeamLocation(self):
        return ElementList(self._driver, *_AdminBeamDetailPageLocator._lblBeamLocation)
    @property
    def _btnBeamAdvance(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnBeamAdvance)
    def _lblBeamName(self, beam_name):
        return Element(self._driver, *_AdminBeamDetailPageLocator._lblBeamName(beam_name))
    @property
    def _lblBeamGroup(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._lblBeamGroup())
    @property
    def _btnReserveThisBeam(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnReserveThisBeam)
    @property
    def _lnkChangeDeviceIcon(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._lnkChangeDeviceIcon)
    @property
    def _tabReservation(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._tabReservation())
    @property
    def _lblActivitiesOnRecentActivity(self):
        return ElementList(self._driver, *_AdminBeamDetailPageLocator._lblActivitiesOnRecentActivity)
    @property
    def _btnShowMore(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnShowMore)   
    def _tblReservationData(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._tblReservationData(username))
    def _lblStartTimeHeader(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._lblStartTimeHeader(username))
    def _btnEditReservation(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnEditReservation(username))
    def _btnRejectReservation(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnRejectReservation(username))   
    def _btnApproveReservation(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnApproveReservation(username)) 
    def _lblReservationStatus(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._lblReservationStatus(username))

    """Mobile UI"""
    def _btnMEditReservation(self, username):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnMEditReservation(username))

    @property
    def _btnMRejectReservation(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnMRejectReservation)
    @property
    def _btnMApproveReservation(self):
        return Element(self._driver, *_AdminBeamDetailPageLocator._btnMApproveReservation)
    
    """    Methods    """
    def __init__(self, driver, beam_name_to_wait_for=None):
        """      
        @summary: Constructor method    
        @param driver: Web Driver 
        @param beam_name_to_wait_for: time to wait a available beam
        @author: Thanh Le
        @created_date: August 15, 2016
        """     
        AdminBeamsCommonPage.__init__(self, driver)
        
        #This is to make sure the page is loaded completely
        if(beam_name_to_wait_for!=None):
            self._lblBeamName(beam_name_to_wait_for).wait_until_displayed()
            self._lnkChangeDeviceIcon.wait_until_displayed()
        
        
    def is_beam_name_displayed(self, beam_name):
        """      
        @summary: Check if a Beam displays or not     
        @param beam_name: name of beam device
        @return: True: The Beam displays, False: The Beam does not display
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        return self._lblBeamName(beam_name).is_displayed() 
    
    
    def get_beam_labels(self):
        """      
        @summary: Get all labels of a Beam device from Beam detail page
        @return: String of labels
        @author: Duy Nguyen
        @created_date: August 05, 2016
        """
        returnList = []
        label_tag_list = self._lblBeamLabel.get_all_elements()
        for tag in label_tag_list:
            returnList.append(tag.text)
        return returnList       
    
    
    def is_any_label_existed(self):
        """
        @summary: Check label of Beam is existed or not     
        @return: True: The Beam's label is existed, False: The Beam's label is not existed
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        
        lst_beam_label = self.get_beam_labels()
        is_not_existed = True
        for e in lst_beam_label:
            if e != 'None':
                if len(e) >= 1:
                    is_not_existed = False
                    break
        return is_not_existed
    
    
    def is_beam_label_existed(self, label):
        """      
        @summary: Check if a label of Beam is existed or not     
        @param label: The label which would like to be checked
        @return: True: The label is existed, False: The label is not existed
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        lbs = self.get_beam_labels()
        for lbl in lbs:
            lbl = lbl.replace("\ue003","").replace("\ue007","")
            if( lbl.strip() == label):
                return True
        return False
        
    
    def is_beam_able_to_unlink(self):
        """      
        @summary: Check if the 'Unlink This Device' button displays or not       
        @return: True: The 'Unlink This Device' button displays, False: The 'Unlink This Device' button does not display
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """           
        dialog = self.open_edit_dialog()
        can_unlink = dialog.is_button_unlink_displayed()
        dialog.cancel()
        return can_unlink
    
    
    def get_beam_label_tag_list(self):
        """      
        @summary: Get all Beam labels from the Edit Device form 
        @return: label_tag_list: list of all Beam labels
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """        
        dialog = self.open_edit_dialog()
        label_tag_list = dialog.get_all_beam_labels()
        dialog.cancel()
        return label_tag_list
    
    
    def get_beam_location(self):
        """      
        @summary: Get location of Beam device  
        @return: String of Beam location
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        location = self._lblBeamLocation
        return location.get_element_at(0).text


    def set_beam_name(self, device_name):
        """      
        @summary: Set new name for a Beam  
        @param device_name: The new name would like to reset 
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dlg = self.open_edit_dialog()
        dlg.set_beam_name(device_name)
        dlg.submit()
        
        self.wait_untill_success_msg_disappeared()
        return self

    
    def set_beam_label(self, beam_label,wait_for_completed=True):
        """      
        @summary: Set new label for a Beam
        @param beam_label: The new label would like to set for a Beam 
        @param wait_for_completed: time to wait setting completely  
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dlg = self.open_edit_dialog()
        dlg.set_beam_label(beam_label)
        dlg.submit()
        if (wait_for_completed == True):
            self.wait_untill_success_msg_disappeared()
        return self
    
    
    def remove_beam_label(self, beam_label):
        """      
        @summary: Remove label from a Beam
        @param beam_label: The label would like to remove from Beam 
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Thanh Le
        @created_date: March 06, 2017
        """
        dlg = self.open_edit_dialog()
        dlg.remove_beam_label(beam_label)
        dlg.submit()
        return self
        
    
    def remove_all_beam_labels(self):
        """      
        @summary: Remove all beam labels of a Beam         
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dlg = self.open_edit_dialog()
        dlg.remove_all_beam_labels()
        dlg.submit()
        return self

    
    def set_beam_label_tag_list(self, beam_label_tag_list):
        """      
        @summary: Set new labels for a Beam after removing all existing ones      
        @param beam_label_tag_list: The new label would like to set for Beam
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dlg = self.open_edit_dialog()
        dlg.remove_all_beam_labels()
        for label in beam_label_tag_list:
            dlg.add_beam_label(label)
        
        dlg.submit()
        self.wait_untill_success_msg_disappeared()
        return self
    
    
    def set_beam_location(self, beam_location):
        """      
        @summary: Set new location for a Beam 
        @param beam_location: The new location would like to set for a Beam 
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dlg = self.open_edit_dialog()
        dlg.set_beam_location(beam_location)
        dlg.submit()
        self.wait_untill_success_msg_disappeared()
        return self 
    
    
    def set_beam_group(self, device_group, wait_for_completed=True):
        """      
        @summary: Select new device group for a Beam     
        @param device_group: The new device group would like to set for a Beam 
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        dlg = self.open_edit_dialog()
        dlg.set_beam_group(device_group)
        dlg.submit(wait_for_completed)
        if(wait_for_completed):
            self.wait_untill_success_msg_disappeared()
        return self
    
    
    def set_beam_reservations(self, reservation):
        """      
        @summary: Set reservation for the Beam 
        @param reservation: reservation types (Allowed, By Request, By Administrators Only or Not Allowed)
        @return: AdminBeamDetailPage: The Beam detail page displays after doing save from Edit Device form
        @author: Tan Le
        @created_date: September 16, 2017
        """
        dlg = self.open_edit_dialog()
        if dlg.get_beam_reservation() == reservation:
            dlg.cancel()
        else:
            dlg.set_beam_reservation(reservation)
            dlg.submit()
        return self
        
        
    def open_edit_dialog(self):
        """      
        @summary: Method to open 'Edit Device' form
        @return: EditDeviceDialog: This is 'Edit Device' form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        self._btnEdit.wait_until_clickable().click_element()
        dlg = EditDeviceDialog(self._driver)
        if not dlg.is_dialog_displayed(1):
            self._btnEdit.jsclick()
        return dlg
    
    
    def open_create_a_reservation_dialog(self):
        """      
        @summary: Method to open 'Create a reservation' form
        @return: reserve_beam_dialog: This is 'Create a reservation' form
        @author: Thanh Le
        @created_date: March 14, 2017
        """
        self._btnReserveThisBeam.wait_until_clickable().click_element()
        from pages.suitable_tech.admin.dialogs.reserve_beam_dialog import ReserveABeamDialog
        return ReserveABeamDialog(self._driver)
    
    
    def reserve_a_beam(self, start_time, end_time, normal_user):
        """      
        @summary: Method to create a reservation
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: March 14, 2017
        """
        self.open_create_a_reservation_dialog().reserve_a_beam(start_time, end_time, normal_user)
        return self
    
    def goto_beam_advance_setting(self):
        """      
        @summary: Open 'Advanced Settings' of a Beam        
        @return: DeviceAdvanceSettingsDialog: This is 'Advance Settings' form
        @author: Duy Nguyen
        @created_date: August 15, 2016
        """
        self._btnBeamAdvance.wait_until_clickable().click()
        from pages.suitable_tech.admin.dialogs.device_advance_settings_dialog import DeviceAdvanceSettingsDialog
        return DeviceAdvanceSettingsDialog(self._driver)
  
  
    def get_beam_group(self):
        """      
        @summary: Get group name of a Beam
        @return: String of group name of Beam
        @author: Tham Nguyen
        @created_date: August 15, 2016
        """
        return self._lblBeamGroup.text


    def open_reservation_tab(self): 
        """      
        @summary: Open reservation tab   
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: February 20, 2017
        """        
        self._tabReservation.click()
        if self._tabReservation.is_displayed(2):
            self._tabReservation.jsclick() 
        return self
    
    
    def update_reservation(self, user, start_time, end_time):
        """      
        @summary: Edit a reservation 
        @param user: user reserves beam
        @param start_time: new start time needs to update
        @param end_time: new end time needs to update   
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: February 20, 2017
        """            
        self.open_edit_reservation_dialog(user).reserve_a_beam(start_time, end_time)
        return self
    
    
    def delete_reservation(self, user):
        """      
        @summary: Delete a reservation 
        @param user: user reserves beam 
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: February 20, 2017
        """     
        return self.open_edit_reservation_dialog(user).delete_the_reservation()
    
    
    def reject_a_requested_reservation(self, user):
        """      
        @summary: Reject a requested reservation 
        @param user: user reserves beam 
        @return: AdminBeamDetailPage
        @author: Thanh Le
        @created_date: February 22, 2017
        """        
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMEditReservation(UserAPI.get_displayed_name(user)).scroll_to().click()
            self._btnMRejectReservation.scroll_to().click()
            if self._btnMRejectReservation.is_displayed(2):
                self._btnMRejectReservation.jsclick()
        else:
            btn_reject_request = self._btnRejectReservation(UserAPI.get_displayed_name(user))
            btn_reject_request.scroll_to().wait_until_clickable().click()
            if not btn_reject_request.is_disappeared(10):
                btn_reject_request.jsclick()
        return self
          
    
    def approve_a_requested_reservation(self, user):
        """      
        @summary: Approve a requested reservation 
        @param user: user reserves beam 
        @return: AdminBeamDetailPage
        @author: Tan Le
        @created_date: September 21, 2017
        """        
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMEditReservation(UserAPI.get_displayed_name(user)).scroll_to().click()
            self._btnMApproveReservation.scroll_to().jsclick()
        else:
            self._btnApproveReservation(UserAPI.get_displayed_name(user)).jsclick()
        return self
    
    
    def open_edit_reservation_dialog(self, user):
        """      
        @summary: Open the edit reservation dialog
        @param user: user reserves beam 
        @return: ReserveABeamDialog
        @author: Thanh Le
        @created_date: March 20, 2017
        """     
        sleep(2)
        from pages.suitable_tech.admin.dialogs.reserve_beam_dialog import ReserveABeamDialog
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMEditReservation(UserAPI.get_displayed_name(user)).scroll_to().click()
            if not ReserveABeamDialog(self._driver).is_dialog_displayed(2):
                self._btnMEditReservation(UserAPI.get_displayed_name(user)).scroll_to().jsclick()
        else:
            self._btnEditReservation(UserAPI.get_displayed_name(user)).scroll_to().click()
            if not ReserveABeamDialog(self._driver).is_dialog_displayed(2):
                self._btnEditReservation(UserAPI.get_displayed_name(user)).scroll_to().jsclick()
        ReserveABeamDialog(self._driver)._dialog.wait_until_displayed()
        return ReserveABeamDialog(self._driver)
    
    
    def get_reservation_data(self, user):
        try:
            displayed_name = UserAPI.get_displayed_name(user)
            start_time_header = str(self._lblStartTimeHeader(displayed_name).text)
            start_time_header.strip()
            reservation_data = self._tblReservationData(displayed_name).text
            
            start_time_and_end_time = reservation_data.split('\n')
            return start_time_header + start_time_and_end_time[0][:-3].strip() + start_time_and_end_time[1][:-4].strip()
        
        except Exception as ex:
            raise Exception("Reservation does not display!" + str(ex))
    

    def get_reservation_status(self, user):
        """      
        @summary: Get reservation status
        @param user: user reserves beam 
        @return: Reservation status string
        @author: Thanh Le
        @created_date: March 21, 2017
        """   
        try:
            return self._lblReservationStatus(UserAPI.get_displayed_name(user)).text
        except Exception as ex:
            raise Exception("Reservation does not display!" + str(ex))
        
    
    def is_reservation_deleted(self, user):
        """      
        @summary: Is reservation deleted
        @param user: user reserves beam 
        @return: ReserveABeamDialog
        @author: Thanh Le
        @created_date: March 21, 2017
        """     
        return self._btnEditReservation(UserAPI.get_displayed_name(user)).is_disappeared()
    
    
    def are_activities_shown_in_recent_activity_tab(self):
        return self._lblActivitiesOnRecentActivity.count()>0
        
        
    def is_show_more_button_displayed_in_recent_activity_tab(self):
        return self._btnShowMore.is_displayed(1)
    