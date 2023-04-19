from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from core.webdriver.elements.element_list import ElementList
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from core.webdriver.elements.editable_combobox import EditableCombobox
from selenium.webdriver.common.keys import Keys

class _EditDeviceDlgLocator(object):
    _txtDeviceName = (By.XPATH, "//input[@ng-model='device.name']")
    _txtBeamLocation = (By.XPATH, "//div[@class='modal-content']//input[@name='location' and @type='text']")
    _txtBeamLabel = (By.XPATH, "//div[@class='modal-content']//input[@ng-model='newTag.text']")
    _lnkRemoveTagLabel = (By.XPATH, "//div[@class='modal-content']//a[@ng-click='$removeTag()']")
    _liBeamLabelTags = (By.XPATH, "//div[@class='modal-content']//li[@class='tag-item ng-scope']//span")
    _btnUnlinkDevice = (By.XPATH, "//div[@class='modal-content']//button[@ng-click='setShowUnlink(true)']")
    _ecbxDeviceGroups = (By.XPATH, "//div[@class='modal-content']//div[@ng-model='device.device_group.id']//span[@aria-label='Select box activate']")
    _ecbxReservations = (By.XPATH, "//div[@ng-model='device.reservations']//span[@aria-label='Select box activate']//i[1]")
    _txtWarningMsg = (By.XPATH, "//div[@class='modal-content']//span[@class='text-danger']")
    _txtReservations = (By.XPATH, "//div[@ng-model='device.reservations']/input[1]")
    _lstReservationPermission = (By.XPATH, ".//div[@ng-bind='opt.title']")
    _cbbReservationSelectedValue = (By.XPATH, "//span[@class='btn btn-default form-control ui-select-toggle']//span[@ng-bind='$select.selected.title']")
    
    @staticmethod
    def _cbbReservationVaules(value):
        return (By.XPATH, u"//div[@class='ng-binding ng-scope' and @ng-bind='opt.title' and .=\"{}\"]".format(value))
    
    @staticmethod
    def _lnkRemoveLabel(value):
        return (By.XPATH, u"//li[@class='tag-item ng-scope']//ng-include//span[text()=\"{}\"]/..//a".format(value))
    
class EditDeviceDialog(DialogBase):
    """
    @description: This is page object class for Edit Device Dialog. You need to init it before using in page class.
    @page: Edit Device Dialog
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _txtDeviceName(self):
        return Element(self._driver, *_EditDeviceDlgLocator._txtDeviceName)
    @property
    def _txtBeamLocation(self):
        return Element(self._driver, *_EditDeviceDlgLocator._txtBeamLocation)
    @property
    def _txtBeamLabel(self):
        return Element(self._driver, *_EditDeviceDlgLocator._txtBeamLabel)
    @property
    def _liBeamLabelTags(self):
        return ElementList(self._driver, *_EditDeviceDlgLocator._liBeamLabelTags)
    @property
    def _lnkRemoveTagLabel(self):
        return ElementList(self._driver, *_EditDeviceDlgLocator._lnkRemoveTagLabel)
    @property
    def _btnUnlinkDevice(self):
        return Element(self._driver, *_EditDeviceDlgLocator._btnUnlinkDevice)
    @property
    def _ecbxDeviceGroups(self):
        return EditableCombobox(self._driver, *_EditDeviceDlgLocator._ecbxDeviceGroups)
    @property
    def _ecbxReservations(self):
        return EditableCombobox(self._driver, *_EditDeviceDlgLocator._ecbxReservations)
    @property
    def _txtWarningMsg(self):
        return Element(self._driver, *_EditDeviceDlgLocator._txtWarningMsg)
    @property
    def _txtReservations(self):
        return Element(self._driver, *_EditDeviceDlgLocator._txtReservations)
    @property
    def _lstReservationPermission(self):
        return ElementList(self._driver, *_EditDeviceDlgLocator._lstReservationPermission)
    @property
    def _cbbReservationSelectedValue(self):
        return Element(self._driver, *_EditDeviceDlgLocator._cbbReservationSelectedValue)
    
    def _lnkRemoveLabel(self, value):
        return Element(self._driver, *_EditDeviceDlgLocator._lnkRemoveLabel(value))
    
    def _cbbReservationVaules(self, value):
        return Element(self._driver, *_EditDeviceDlgLocator._cbbReservationVaules(value))
    
    """    Methods    """
    def __init__(self, driver):     
        """      
        @summary: Constructor method    
        @param driver: Web Driver
        @author: Thanh Le
        """        
        DialogBase.__init__(self, driver)
    
    
    def add_beam_label(self, beam_label):
        """
        @summary: This action is used to add beam label
        @parameter: beam_label: beam label string
        @author: Thanh Le
        """
        if(beam_label != None):
            self._wait_for_dialog_appeared()
            self._txtBeamLabel.send_keys(beam_label)
            self._txtBeamLabel.send_keys(Keys.ENTER)
            self._txtDeviceName.click() # work arround for typing "Enter" problem
            
    
    def is_button_unlink_displayed(self):
        """
        @summary: Check if button unlink is displayed or not
        @return: True: the Unlink this device button is displayed
                False: the Unlink this device button is not displayed
        @author: Thanh Le
        """
        self._wait_for_dialog_appeared()
        return self._btnUnlinkDevice.is_displayed(5)
    
    
    def is_button_unlink_disappeared(self):
        """
        @summary: Check if button unlink is disappeared or not
        @return: True: the Unlink this device button disappears
                False: the Unlink this device button appears
        @author: Thanh Le
        """
        self._wait_for_dialog_appeared()
        return self._btnUnlinkDevice.is_disappeared(5)
    
    
    def set_beam_name(self, value):
        """
        @summary: This action is used to set beam name
        @return: EditDeviceDialog
        @parameter: value: beam name
        @author: Thanh Le
        """
        self._txtDeviceName.wait_until_displayed().type(value)
        return self
    
    
    def is_device_group_cbx_disabled(self):
        """
        @summary: Check if device group chekbox is disabled
        @return: True: the device group checkbox is disabled
                False: the device group checkbox is enabled
        @author: Thanh Le
        """
        is_disabled  = self._ecbxDeviceGroups.get_attribute("disabled")
        if is_disabled != None:
            return True
        return False
    
    
    def get_all_beam_labels(self):
        """
        @summary: This action is used to get all beam labels
        @return: all labels of beam
        @author: Thanh Le
        """
        self._wait_for_dialog_appeared()
        returnList = []
        taglist = self._liBeamLabelTags
        count = taglist.count(5) 
        if(count > 0):
            label_tag_list = taglist.get_all_elements()
            for tag in label_tag_list:
                returnList.append(tag.text)
        return returnList       
     
        
    def remove_all_beam_labels(self):
        """
        @summary: This action is used to remove all beam labels
        @return: EditDeviceDialog
        @author: Thanh Le
        """
        for _ in range(self._lnkRemoveTagLabel.count(5) * 2):
            self._txtBeamLabel.send_keys(Keys.BACKSPACE)
        
        return self
    
        
    def set_beam_label(self, beam_label):
        """
        @summary: This action is used to set beam label
        @return: EditDeviceDialog
        @parameter: beam_label: beam label string
        @author: Thanh Le
        """
        if(beam_label != None):
            self._wait_for_dialog_appeared()
            self.remove_all_beam_labels()
            self.add_beam_label(beam_label)
        return self
    
    
    def remove_beam_label(self, beam_label):
        """
        @summary: This action is used to set beam label
        @return: EditDeviceDialog
        @parameter: beam_labels: beam labels array
        @author: Thanh Le
        """
        if(beam_label != None):
            self._wait_for_dialog_appeared()
            self._lnkRemoveLabel(beam_label).wait_until_displayed()\
            .click() # work arround for typing "Enter" problem
        return self
    
    def set_beam_location(self, beam_location):
        """
        @summary: This action is used to set beam location
        @return: EditDeviceDialog
        @parameter: beam_location: beam location string
        @author: Thanh Le
        """
        if(beam_location != None):
            self._wait_for_dialog_appeared()
            if self._txtBeamLocation.is_enabled(2):
                self._txtBeamLocation.type(beam_location)
        return self
    
    
    def clear_beam_location(self):
        """
        @summary: This action is used to clear beam location
        @return: EditDeviceDialog
        @author: Thanh Le
        """
        self._wait_for_dialog_appeared()
        self._txtBeamLocation.wait_until_displayed().clear()
        return self

    
    def set_beam_group(self, group_name):
        """
        @summary: This action is used to set beam group name
        @parameter: group_name: group name string
        @return: EditDeviceDialog
        @author: Thanh Le
        """
        self._wait_for_dialog_appeared()
            
        if group_name:
            self._ecbxDeviceGroups.wait_until_displayed().select(group_name, "//label[@for='device_group']/..")
        return self
    
    
    def get_warning_message(self):
        """
        @summary: This action is used to get warning message.
        @return: warning message text content
        @author: Thanh Le
        """
        txt_warning = self._txtWarningMsg
        if txt_warning.is_displayed(5):
            return txt_warning.text
        return None
    
    
    def search_reservations_permission(self, permission):
        self._ecbxReservations.wait_until_clickable().click()
        self._txtReservations.type(permission)
        return self
        
        
    def get_reservation_permission_name_at_the_first(self):
        return self._lstReservationPermission.get_element_at(0).text
        

    def get_beam_reservation(self):
        """
        @summary: This action is to get current reservation value of beam.
        @return: Reservation value
        @author: Tan Le
        @created_date: September 18, 2017
        """
        return self._cbbReservationSelectedValue.text
    
    
    def set_beam_reservation(self, reservation):
        """
        @summary: This action is to set beam reservation.
        @param: reservation: value of reservation that user wants to set 
        @return: EditDeviceDialog
        @author: Tan Le
        @created_date: September 18, 2017
        """
        self._cbbReservationSelectedValue.click()
        self._cbbReservationVaules(reservation).wait_until_clickable().click()
            
        return self
        
            
            