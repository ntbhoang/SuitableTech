from common.application_constants import ApplicationConst
from common.helper import Helper
from pages.suitable_tech.user.login_page import LoginPage
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from common.constant import Constant
import random

class Devices_Test(TestBase):
    
    def test_c11600_change_device_location_1_x(self):
        """
        @author: Quang.Tran
        @date: 7/25/2016
        @summary: Change device location [1.X] 
        @precondition: 
            Devices-Mod-Location
            
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Login as the Device Group Admin
        
        @steps:
            1) go to the "Manage your Beams" dashboard and click on the "Beams" tab
            2) click on a device in the "Devices" section
            3) click on the "Edit" box above the device image
            4) the "Edit Device" box will open, change the location then click the "Save Changes" box
        @expected:
            Verify All Changes are saved by refreshing your browser; verify the Location tag is updated
        
        @note: Ready to automate
        """
        old_location = ""
        new_location = "1A Phan Xich Long, Phu Nhuan dist., HCMC, Vietnam"
        new_device_group_name = Helper.generate_random_device_group_name()
        beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
        beam_name = beam.beam_name
        
        admin_user = User()
        admin_user.generate_advanced_device_group_admin_data()
        admin_user.device_group = new_device_group_name
        
        try:
            # pre-condition 
            TestCondition.create_device_group(new_device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)

            beam_detail_page = admin_dashboard_page.goto_beams_tab().select_a_device(beam_name)
            old_location = beam_detail_page.get_beam_location()
            beam_detail_page.set_beam_location(new_location)
            
            # verify
            beam_detail_page.goto_dashboard_tab().goto_beams_tab().select_a_device(beam_name)
            self.assertEqual(beam_detail_page.get_beam_location(), new_location, \
                               "Assertion Error: Failed to change location of device %s" % (beam_name))
        finally:
            # post-condition
            TestCondition.restore_advanced_beam_location(beam, location=old_location)
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])


    def test_c11601_change_device_label_1_X(self):
        """
        @author: Quang.Tran
        @date: 7/25/2016
        @summary: Change device Label [1.X]
        @precondition: 
            Devices-Mod-Label
            
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Login as the Device Group Admin
        
        @steps:
            1) go to the "Manage your Beams" dashboard and click on the "Beams" tab
            2) click on a device in the "Devices" section
            3) click on the "Edit" box above the device image
            4) the "Edit Device" box will open, change the label or Add a label and then click the "Save Changes" box
        @expected:
            Verify All Changes are saved by refreshing your browser; verify the Label tag is updated
        """
        
        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            new_label = Helper.generate_random_string()   
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
                      
            TestCondition.create_device_group(new_device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)
               
            # steps
            beam_detail_page = admin_dashboard_page.goto_beams_tab().select_a_device(beam_name)
            old_label_tag_list = beam_detail_page.get_beam_label_tag_list()
            beam_detail_page.set_beam_label(new_label)
            
            beam_detail_page.goto_dashboard_tab().goto_beams_tab().select_a_device(beam_name)

            self.assertTrue(beam_detail_page.is_beam_label_existed(new_label), \
                            "Assertion Error: Failed to change the label of device %s" % (beam_name))
        finally:
            # restore the previous value
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])
            TestCondition.restore_advanced_beam_labels(beam, old_label_tag_list)


    def test_c11602_can_change_device_name_1_x(self):
        """
        @author: tham.nguyen
        @date: 7/22/2016
        @summary: Can change device name[1.X] 
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            1. Login as the Device Group Admin
        @steps:
            1. Go to "Beams" under the "Manage your Beams" Dashboard
            2. Click on a device under the "Devices" tab
            3. Click on the "Edit" box
            4. change "Name" and then "Save Changes"
        @expected:
            1. Verify All Changes are saved by refreshing your browser; verify the Name tag is updated
        """
        try:
            # pre-condition
            new_device_name = Helper.generate_random_device_name()
            new_device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
            
            TestCondition.create_device_group(new_device_group_name, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            admin_beam_detail = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab().select_a_device(beam_name)\
                .set_beam_name(new_device_name)
            
            admin_beam_detail.goto_dashboard_tab().goto_beams_tab().select_a_device(new_device_name)
            
            # verify points
            self.assertTrue(admin_beam_detail.is_beam_name_displayed(new_device_name),
                            "Assertion Error: New name of the device '{}' hasn't changed after it was edited from '{}'".format(new_device_name, beam_name))
        finally:
            # post-condition
            TestCondition.restore_advanced_beam_name(beam)
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([admin_user])
            TestCondition.delete_device_groups([new_device_group_name])

    
    def test_c11605_unlink_a_beam_device (self):
        """
        @author: Quang.Tran
        @date: 7/25/2016
        @summary: Unlink A Beam device 
        @precondition: 
            Login as the Device Group Admin
        
        @steps:
            1) go to the "Manage your Beams" dashboard and click on the "Beams" tab
            2) Click on a desired device
            3) Click on the "Edit" box above the device image
        @expected:
            Verify that the "Unlink This Device..." box is not there (i.e. Device Group Admins cannot unlink devices)
        
        @note: Ready to automate
        """
        
        try:
            # precondition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            new_device_group_name = Helper.generate_random_device_group_name()
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
            
            TestCondition.create_device_group(new_device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)
               
            # testcase's steps
            current_page = admin_dashboard_page.goto_beams_tab().select_a_device(beam_name)
            
            # verify
            self.assertFalse(current_page.is_beam_able_to_unlink(),
                             "Assertion Error: The 'Unlink This Device...' button is displayed in Device Group Admin page.")
        finally:
            # postcondition:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])


    def test_c11592_device_group_admin_removes_an_existing_device_group_admin_2_X(self):
        """
        @author: Duy.Nguyen
        @date: 8/5/2016
        @summary: C11592 - Device Group Admin Removes an existing Device Group Admin [2.X]
        @precondition:
        -two device group admins see previous test case
            
        @steps:
        1) Using a device group admin account (not an org admin account), click on the "Beams" tab under the "Manage your Beams" dashboard
        2) click on a device group, then click on the "Settings" tab
        3) Under the "Administrators" title in the "Settings" tab, click on the "X" next to device group admin you wish to remove 
        4) click the blue box "Save Changes" towards the top-left side of the browser
        5) Verify that a green pop up stating "device group settings were saved successfully" appears in the top right corner. 
            
        @expected:
        Confirm that the removed user is not a device group admin anymore
            1) Go to the "Users" tab under the "Manage your Beams" dashboard
            2) Click on the desired user that you are checking device admin privileges
            3) Next to the "Administrates Groups" string you should "none" where the name of the desired device group would be if they were a device group admin. 
        """        
        try:
            # pre-condition:
            device_group_name = Helper.generate_random_device_group_name()
            admin_user_1 = User()
            admin_user_1.generate_advanced_device_group_admin_data()
            admin_user_1.device_group = device_group_name
            admin_user_2 = User()
            admin_user_2.generate_advanced_device_group_admin_data()
            admin_user_2.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user_1, admin_user_2])
              
            # steps:            
            beams_settings_page = LoginPage(self._driver).open()\
                .login(admin_user_1.email_address, admin_user_1.password)\
                .goto_beams_tab()\
                .select_device_group(device_group_name)\
                .goto_setting_tab()\
                .remove_admin_user(admin_user_2.get_displayed_name(), False)
            
            # verify point:
            self.assertEqual(beams_settings_page.get_msg_success(), ApplicationConst.INFO_MSG_SAVE_DEVICE_GROUP_SETTING_SUCCESSFUL,
                            "Assertion Error: The message with expected content doesnot display")
            
            admin_user_detail_page = beams_settings_page.goto_users_tab().goto_user_detail_page(admin_user_2)
            
            self.assertEqual(admin_user_detail_page.get_user_administers_groups(), [],
                             "Assertion Error: The Administrates Information is not correct")
            
        finally:
            # post-condition
            TestCondition.delete_advanced_users([admin_user_1, admin_user_2])
            TestCondition.delete_device_groups([device_group_name])
            
            
    def test_c11705_device_advanced_info_page(self):
        """
        @author: Tan.Le
        @date: 09/28/2017
        @summary: C11705 - Device Advanced Info Page
        @precondition:
        1) Login as the Device Group Admin
            
        @steps: Steps To Complete Task: To view a Beam Device Advanced Info Page
        1) go to the "Manage your Beams" dashboard and click on the "Beams" tab
        2) Click on a desired device
        3) Click on the "Advanced" box above the device image
        
        @expected:
        Verify the following Device Advanced Settings Page Information
        
        """        
        try:
            # pre-condition:
            device_group_name = Helper.generate_random_device_group_name()
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            
            beam_name = random.choice([Constant.BeamProNameUTF8, Constant.BeamPlusName])
            beam = TestCondition.get_and_lock_a_physical_beam(beam_name)
            
            TestCondition.create_device_group(device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            system_info = [ApplicationConst.LBL_SERIAL_NUMBER, ApplicationConst.LBL_UID, ApplicationConst.LBL_SOFTWARE_VERSION, ApplicationConst.LBL_LINKED_BY, ApplicationConst.LBL_LINKED_ON]
            current_network_info = ['SSID', 'MAC', ApplicationConst.LBL_FREQUENCY]
            network_info = [ApplicationConst.LBL_TYPE, 'MAC', ApplicationConst.LBL_IP_ADDRESS]
            relay_server_info = [ApplicationConst.LBL_IP_ADDRESS]
              
            # steps:            
            infomation_tab = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_a_device(beam_name)\
                .goto_beam_advance_setting()
            
            self.assertTrue(infomation_tab.does_system_info_display_fully(system_info),\
                            "Assertion Error: Missing System information.")
            self.assertTrue(infomation_tab.does_network_info_display_fully(current_network_info, network_info, relay_server_info),\
                            "Assertion Error: Missing Network information.")
            
            settings_tab = infomation_tab.enter_settings_tab()
            
            self.assertTrue(settings_tab.does_settings_tab_display_correctly(),\
                            "Assertion Error: Settings tab display incorrectly.")
            
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group_name])


    def test_c11603_can_add_device_group(self):
        """
        @author: Khoi Ngo
        @date: 10/23/2017
        @summary: Verify that device group admin can't add device group
        @precondition:
            - Create a Device Group Admin

        @steps:
            1) Login as the Device Group Admin
            2) Go to "Manage your Beams" dashboard
            3) Click on the "Beams" tab at the top
            4) Click on drop-down menu "All Beams"
        @expected:
            (3) Verify the "+ Create a Device Group" Icon is not present
            (4) Verify the "Create Device Group" box is not present

        """
        try:
            # pre-condition:
            device_group_name = Helper.generate_random_device_group_name()

            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name


            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            # steps:
            admin_devices_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab()
            self.assertFalse(admin_devices_page.is_create_device_group_button_display(), "Verify the '+ Create a Device Group' Icon is present")

            all_beams_menu = admin_devices_page.open_all_beams_dropdown()
            self.assertFalse(all_beams_menu.is_create_device_group_button_in_all_beams_display(), "Verify the 'Create Device Group' box is present")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group_name])

