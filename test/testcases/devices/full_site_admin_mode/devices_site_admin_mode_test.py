from common.helper import Helper
from pages.suitable_tech.user.login_page import LoginPage
from common.application_constants import ApplicationConst
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from common.constant import Constant
from test.testbase import TestBase
from data_test.dataobjects import beam

class DevicesSiteAdminMode_Tests(TestBase):   
    
    def test_c11272_can_change_device_name_1_x(self):
        """            
        @author: Duy.Nguyen
        @date: 7/26/2016
        @precondition:
        Login as the Org Admin
        
        @steps:
        1) Go to "Beams" under the "Manage your Beams" Dashboard
        2) Click on a device under the "Devices" tab
        3) Click on the "Edit" box
        4) change "Name" and then "Save Changes"
        
        @expected:
        when the page refreshes, the device name should change
        """
        try:
            # Pre-condition
            device_random_name = Helper.generate_random_string()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            # Test Case Section
            admin_all_beam_device_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()
            
            beam_detail_page = admin_all_beam_device_page.select_a_device(beam_name)\
                .set_beam_name(device_random_name)
            
            beam_reselect_detail_page = beam_detail_page.goto_beams_tab()\
                .select_a_device(device_random_name)
            
            self.assertTrue(beam_reselect_detail_page.is_beam_name_displayed(device_random_name),
                            "Assertion Error: Edited Beam name is not correct")
        finally:
            # post-condition
            TestCondition.restore_advanced_beam_name(beam)
            TestCondition.release_a_beam(beam)
            
        
    def test_c10957_can_add_device_group_1_x(self):
        """            
        @author: Duy.Nguyen
        @date: 7/26/2016
        @summary: Can Add Device Group (1.X)
        @precondition:
        Login as the Org Admin
        
        @steps:
        1) Go to "Beams" under the "Manage your Beams" Dashboard
        2) click on "Create Device Group" box (Or.. click on the drop-down menu "All Beams" and click "Create Device Group" from there")
        3) Fill out device names, click on "Choose devices to add to this group" if desired, and finally click "Create Device Group"

        @expected:
        Device group can be seen under the "Beams" tab from step 1
        """
        try:
            # Pre-condition
            
            device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            # steps            
            admin_beam_all_devices_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .create_new_device_group(device_group_name, [beam_name])\
                .goto_beams_tab().switch_to_icon_view()
            
            # verify point
            self.assertTrue(admin_beam_all_devices_page.is_device_group_existed(device_group_name),
                            "Assertion Error: Device Group is not existed")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name])
      
          
    def test_c10958_can_change_device_group_1_x(self):
        """            
        @author: Quang Tran
        @date: 08/09/2016
        @precondition:
            There is an existing Beam (Beam1) added to a device group (DeviceGroupA).
            Add another device group (DeviceGroupB)
        
        @steps:
        1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
        2. Go to "Beams" tab and select a device (Beam1)
        3. Click "Edit" button
        4. Select another device group (DeviceGroupB) in the "Group" list
        5. Select "Save Changes" button to save changes
        6. Go to "Beams" tab and search for the device (Beam1) and select it
        7. go to the detail page of device

        @expected:
            (4) The message "Warning! If you move this device to a different group, members of this group will no longer be able to access it."
            (5)
            _Message "The device was saved successfully."
            _The device (Beam1) was removed from the device group (DeviceGroupA).
            (7). Verify that new group is displayed in "Group" field. (DeviceGroupB)

        """
        try:
            # pre-condition
            device_group_name_1 = Helper.generate_random_device_group_name()
            device_group_name_2 = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            TestCondition.create_device_group(device_group_name_1, [beam_name])
            TestCondition.create_device_group(device_group_name_2)
            
            # steps            
            admin_beams_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                    .select_a_device(beam_name)
            
            dlg = admin_beams_detail_page.open_edit_dialog()
            dlg.set_beam_group(device_group_name_2)
            warning_msg = dlg.get_warning_message()
            dlg.submit(False)
            success_msg = admin_beams_detail_page.get_msg_success()
            
            admin_beams_detail_page.wait_untill_success_msg_disappeared()
            
            # verify points
            self.assertEqual(warning_msg, ApplicationConst.WARN_MSG_CHANGE_DEVICE_GROUP_NAME, \
                "No warning message displayed when modifying the Device Group of device {}".format(beam_name))
            
            self.assertEqual(success_msg, ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL, \
                "No message displayed after modifying the Device Group of device {} successful.".format(beam_name))    
            
            admin_beams_detail_page = admin_beams_detail_page.goto_beams_tab().select_a_device(beam_name)
            
            self.assertEqual(admin_beams_detail_page.get_beam_group(), device_group_name_2, 'The new group {} does not display in Group field'.format(device_group_name_2))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name_1, device_group_name_2])
    
    
    def test_c11271_change_device_label_1_x(self):
        """
        @author: Tham.Nguyen
        @date: 08/09/2016
        @summary: Change device Label [1.X]
        @precondition:           
            Devices-Mod-Label
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Login to Suitabletech with Org admin
            Add a device (Beam1)
        @steps:
            1) Go to Dashboard page by selecting Manage Your Beams from the user dropdown menu
            2) Go to "Beams" tab and select a device (Beam1)
            3) Click "Edit" button
            4) Enter new label to "Labels" field
            5) Select "Save Changes" button to save changes
            6) Select "Edit" button again
            7) Delete all in "Labels" field
            8) Select "Save Changes" button to save changes
        
        @expected:          
            (5). 
            _The "Device was saved successfully" message appears.
            _The entered label was saved in "Labels" field of Beam detail page.
            (8). 
            _The "Device was saved successfully" message appears.
            _The entered label field displays as "None" in Beam detail page.
        """
        try:
            # pre-condition
            new_label_name = Helper.generate_random_label_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            device_name = beam.beam_name
            
            # step
            detailed_beam_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_a_device(device_name)\
                .set_beam_label(new_label_name, False)
            
            # verify points
            actual_alert_msg = detailed_beam_page.get_msg_success()
             
            self.assertEqual(actual_alert_msg, ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL,
                             "Assertion Error: Expected alert message '{}' doesn't match actual alert message '{}'".format(ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL, actual_alert_msg))
                                                                                                                                            
            detailed_beam_page = detailed_beam_page.goto_beams_tab().select_a_device(device_name)
            lst_beam_label = detailed_beam_page.get_beam_labels()
           
            self.assertTrue((new_label_name in lst_beam_label),
                            "Assertion Error: The entered label '{}' was not saved in 'Labels' field of '{}' Beam".format(new_label_name, device_name))
            
            detailed_beam_page = detailed_beam_page.goto_beams_tab().select_a_device(device_name).remove_all_beam_labels()
            
            actual_alert_msg = detailed_beam_page.get_msg_success()
            self.assertEqual(actual_alert_msg, ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL,
                             "Assertion Error: Expected alert message '{}' doesn't match actual alert message '{}'".format(ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL, actual_alert_msg))
            
            detailed_beam_page = detailed_beam_page.goto_beams_tab().select_a_device(device_name)
            lst_beam_label = detailed_beam_page.get_beam_labels()
                
            self.assertTrue(ApplicationConst.LBL_NONE_PROPERTY in lst_beam_label, "Assertion Error: The entered label field of beam '{}' doesn't display as 'None' in Beam detail page".format(device_name))
        finally:
            TestCondition.release_a_beam(beam)
    
  
    def test_c11270_change_device_location_1_X(self):
        """
        @author: Duy Nguyen
        @date: 08/17/2016
        @summary: Change device location [1.X]
        @precondition:           
            Devices-Mod-Location
            
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1) Select Beams, Device (N/A: Group or All Beams)
            2) Select a Beam
            3) Edit Location parameter by clicking on the field and typing (New/Modify/Delete) information
            4) All Changes are saved after completion
        
        @expected:          
            Verify All Changes are saved by exiting and reentering menu
        """
        try:
            # precondition:
            new_location_name = Helper.generate_random_string()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            # steps:
            detailed_beam_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_a_device(beam_name)\
            
            old_location_name = detailed_beam_page.get_beam_location()
            detailed_beam_page.set_beam_location(new_location_name)
            
            # verify points:
            self.assertEqual(detailed_beam_page.get_beam_location(), new_location_name, "Assertion Error: The Location Information is not correct")
            
        finally:
            TestCondition.restore_advanced_beam_location(beam, old_location_name)
            TestCondition.release_a_beam(beam)
            
            
    def test_c11638_enter_out_of_bonds_linking_code_when_add_a_beam_device(self):
        """
        @author: Duy Nguyen
        @date: 08/17/2016
        @summary: Enter out of bonds Linking code when add A Beam device
        @precondition:           
            1. From your organization's Site Admin 2.0 Dashboard.
            2. Select the "Beam" drop down menu, then select the "all beams" link
            3. Select any Beam
            4. Select the "Edit" button above the beam image
            5. Select the "Unlink this Device.." button
            6. Confirm your selection
            7. Verify that this Beam is no longer searchable within the organization.
        @steps:
        Steps To Complete Task: To Link a Beam Device
            1) From your organization's Site Admin 2.0 Dashboard.
            2) Select the "Add A Beam" button
            3) Enter a 6 digit invalid linking code:
            4) select "Link your Beam"
        
        @expected:          
            Verify that the form displays invalid data message in the fields, and the beam was not linked.
        """
        try:
            # steps:
            link_a_beam_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_link_a_beam_page().link_a_beam('LGVN Testing', '@$#$%^', '')
            
            # verify point
            self.assertEqual(link_a_beam_page.get_error_message(), ApplicationConst.LBL_LINKING_CODE_ERROR, 'The error message does not display or it does not localize')
        
        finally:
            pass

    def test_c33900_cannot_add_device_group_that_already_existed(self):
        """
        @author: Khoi Ngo
        @date: 10/13/2017
        @summary: Verify that admin cannot add Device Group that already existed
        @steps:
            1. Login as org admin
            2. Go to Beams page
            3. Click Create Device Group button
            4. Enter name then click Create Device Group button
            5. Go to Beams page
            6. Create Device Group with the same name at step 4
        @expected:
            (6) 'A device group with that name already exists.' message displays.
        """

        try:
            device_group_name = Helper.generate_random_device_group_name()
            # steps
            device_group_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_beams_tab()\
                .create_new_device_group(device_group_name)\
                .goto_beams_tab()\
                .create_new_device_group(device_group_name, wait_for_completed = False)

            actual_msg = device_group_detail_page.get_error_message()
            self.assertTrue(device_group_detail_page.is_error_msg_displayed(), "Error message doesn't display")
            self.assertEqual(actual_msg, ApplicationConst.INFO_MSG_DEVICE_GROUP_EXISTED, "Error message content is not correct")
        finally:
            TestCondition.delete_device_groups([device_group_name])
        
