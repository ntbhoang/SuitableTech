from common.constant import Constant, Platform
from common.helper import Helper, EmailDetailHelper
from core.utilities.gmail_utility import GmailUtility
from core.utilities.utilities import Utilities
from data_test.dataobjects.enum import WeekDays
from data_test.dataobjects.user import User
from pages.suitable_tech.admin.advanced.dashboard import admin_dashboard_page
from common.application_constants import ApplicationConst
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from data_test.dataobjects import beam
import re, pytest


class DeviceGroup_Test(TestBase):

    def test_c10924_add_device_to_a_new_created_device_group_1_x(self):
        """
        @author: Thanh.Le
        @date: 8/4/2016 
        @summary: Add device to a new created device group [1.X]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgsc
            
            There are existing Beams
            Beam1
            Beam2
        @steps:
            Steps To Complete Task: Add New Device Group then adding device to it
            1) Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2) Go to "Beams" tab and select "Create Device Group" button
            3) Enter device name to "Name" field
            4) Select the "Choose device to add to this group" button then Select device under device list (Beam1)
            5) Click "Create Device Group" button
            6) Go to "Beams" tab and search for above device group
            7) Click on "Add Devices" button on the right top of page
            8) Select a device and click on "Add Selected Devices"
           
        @expected:
            (5) 
            _The message "The device group was successfully created" appears.
            _The device group with added devices (Beam1) is created.

            (8) Newly added device is listed in device group.
        """
        try:
            # pre-condition
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()

            beam1 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam2 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam1_name = beam1.beam_name
            beam2_name = beam2.beam_name
            # steps
            new_device_group_name = Helper.generate_random_device_group_name()

            admin_beams_devices_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab()\
                .create_new_device_group(new_device_group_name, [beam1_name], False)
                
            success_message = admin_beams_devices_page.get_msg_success()
            
            # verify point
            self.assertEqual(success_message, ApplicationConst.INFO_MSG_CREATE_DEVICE_GROUP_SUCCESSFUL,
                              "Assertion Error: The message is invalid!")
            self.assertTrue(admin_beams_devices_page.is_device_existed(beam1_name),
                             "Assertion Error: The device is NOT existed!")
                     
            admin_beams_devices_page = admin_beams_devices_page.goto_beams_tab().select_device_group(new_device_group_name)\
                .add_devices([beam2_name])

            # verify point
            self.assertTrue(admin_beams_devices_page.is_device_existed(beam2_name),
                             "Assertion Error: The device is NOT existed!")
        finally:
            # post-conditions
            TestCondition.release_a_beam(beam1)
            TestCondition.release_a_beam(beam2)
            TestCondition.delete_device_groups([new_device_group_name])

                
    def test_c10925_move_device_to_different_group_1_x(self):
        """
        @author: Thanh.Le
        @date: 8/10/2016 
        @summary: Move device to different group [1.X]
        @precondition:
        @steps:
            Steps To Complete Task: add newly paired Beam to a Device Group:
                1) Select the "Beams" drop down menu
                2) Select the â€œAll Beamsâ€� link
                3) Click on any Beam
                4) Selects the "Edit" above target Beam device
                5) Select the drop down menu under "Group" to select the destination Device Group
                6) Click the save changes to complete the move
            
        @expected:
                6) Beam has been moved to new group
        """
        try:
            # pre-condition
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()
             
            new_device_group_name_a = Helper.generate_random_device_group_name()
            new_device_group_name_b = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
             
            # create 2 device group
            TestCondition.create_device_group(new_device_group_name_a)
            TestCondition.create_device_group(new_device_group_name_b, [beam_name])
             
            # steps
            admin_beams_devices_page = LoginPage(self._driver).open().goto_login_page()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab().select_a_device(beam_name).set_beam_group(new_device_group_name_a)\
                .goto_beams_tab().select_device_group(new_device_group_name_a)
                 
            # verify point
            self.assertTrue(admin_beams_devices_page.is_device_existed(beam_name),
                            "Assertion Error: The device is NOT existed!")            
        finally:
            # post-conditions
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name_a, new_device_group_name_b])
     
     
    def test_c10926_remove_device_from_group_by_org_admin_1_X(self):
        """
        @author: Duy Nguyen
        @date: 08/10/2016
        @summary: Remove device from group by org admin[1.X]
        @precondition: 
            Devices-Mod-Move_Group
             
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            1. Added a newly paired beam (Beam1)
            2. Create a device group (DeviceGroupA)
            3. Add Beam1 to DeviceGroupA
 
        @steps:
            1. Login to Suitabletech.com as an org admin and then select "Manage Your Beams"
            2. Go to "Beams" tab and select the device group (DeviceGroupA) which contains the device (Beam1)
            3. Select this device group and click "Delete this Group" button
            4. Select "Ok" on "Are you sure you want to delete this device group?" warning pop-up
            5. Go to "Beams" tab and select "Create Device Group" button 
            6. Enter device group name into "Name" field and select "Choose devices to add to this group" button then select the Beam1 device
            7. Click "Create Device Group" button
 
        @expected:
            (4) Verify that the device (Beam1) is not in a group.
             
            (7). 
            _The device group is created.
            _The device (Beam1) is belongs to the created device group.
        """       
        try:
            # pre-condition:
            # create device group
            device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
             
            TestCondition.create_device_group(device_group_name, [beam_name])
             
            # create org admin
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()
            admin_user.device_group = device_group_name
             
            # steps:
            admin_beam = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab()
 
            beam_detail_page = admin_beam.goto_settings_tab_of_a_device_group(device_group_name)\
                .delete_device_group().select_a_device(beam_name)\
             
            # verify point
            beam_group = beam_detail_page.get_beam_group()
            is_no_group = (beam_group == ApplicationConst.LBL_NONE_PROPERTY or beam_group == "")
            self.assertTrue( is_no_group, "Assertion Error: Group property is not correct")
             
            group_page = beam_detail_page.goto_beams_tab().create_new_device_group(device_group_name, [beam_name])\
                .goto_beams_tab()
            # verify point:
            self.assertTrue(group_page.is_device_group_existed(device_group_name), "Assertion Error: Device Group is not exist")
             
            detail_device_page = group_page.select_a_device(beam_name)
            # verify point:
            self.assertEqual(detail_device_page.get_beam_group(), device_group_name, "Assertion Error: Group property is not correct")
             
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name])
 
 
    def test_c10950_adding_newly_paired_beams_to_a_device_group_2_x(self):  
        """
        @author: Quang Tran
        @date: 8/10/2016
        @summary: Adding newly paired Beams to a device Group [2.X]
        @precondition: 
            Add new Beam already paired.
            There is an existing device group (DeviceGroupA)
        @steps:
            1. Go to Dashboard page by selecting Manage Your Beams from the user dropdown menu
            2. Go to "Beams" tab and select a device (Beam1) under "Devices" section
            3. Click "Edit" button
            4. Select a device group (DeviceGroupA) in "Group" list
            5. Select "Save Changes" button to save changes
            6. Go to "Beam" tab and select "Create Device Group" button
            7. Enter the device group name to "Name" field (DeviceGroupB)
            8. Click the "Choose devices to add to this group" button and select the existing device (Beam1) in pre-condition
            9. Select "Create Device Group" button
 
        @expected:
            (5)
            _The "The device was saved successfully." message appear.
            _Device (Beam1) is added to selected device group (DeviceGroupA).
            (9)
            _The "The device group was successfully created." message appear.
            _Device (Beam1) is added to selected device group (DeviceGroupB)
            _Device (Beam1) is removed from selected device group (DeviceGroupA).
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            new_device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            TestCondition.create_device_group(device_group_name)
             
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
 
            admin_beams_detail_page = admin_dashboard_page.goto_beams_tab()\
                .select_a_device(beam_name).set_beam_group(device_group_name, False)
             
            # verify point (5)
            success_msg = admin_beams_detail_page.get_msg_success()
            self.assertEqual(success_msg, ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL, \
                "Assertion Error: No message displayed after modifying the Device Group of device {}.".format(beam_name)) 
             
            beam_group_detail_page = admin_beams_detail_page.goto_beams_tab().select_device_group(device_group_name)
            is_added = beam_group_detail_page.is_device_existed(beam_name)
            self.assertTrue(is_added,
                "Assertion Error: Device '{}' is not added to selected device group '{}'.".format(beam_name, device_group_name))
             
            admin_beams_device_page = beam_group_detail_page.goto_beams_tab()\
                .create_new_device_group(new_device_group_name, [beam_name], False)
            success_msg = admin_beams_device_page.get_msg_success()
             
            # verify point (9) 
            self.assertEqual(success_msg, ApplicationConst.INFO_MSG_CREATE_DEVICE_GROUP_SUCCESSFUL, \
                "Assertion Error:No message displayed after modifying the Device Group of device {}.".format(beam_name)) 
 
            beam_group_detail_page = admin_beams_device_page.goto_beams_tab().select_device_group(new_device_group_name)
                         
            is_device_added = beam_group_detail_page.is_device_existed(beam_name)
            self.assertTrue(is_device_added,
                "Assertion Error: Device '{}' is not added to selected device group '{}'.".format(beam_name, new_device_group_name))
             
            is_device_removed = beam_group_detail_page.goto_beams_tab().select_device_group(device_group_name)\
                .is_device_existed(beam_name)
            self.assertFalse(is_device_removed,
                "Assertion Error:Device '{}' is not removed from old device group '{}'.".format(beam_name, device_group_name))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name, new_device_group_name])
     
     
    def test_c10961_delete_device_group_1_x(self):
        """
        @author: Quang Tran
        @date: 7/21/2016
        @summary: Delete Device group [ 1.X] 
        @precondition: Use the Admin Test Organization
        @steps:
            1) Go to the "Beams" tab under the "Manage your Beams" dashboard
            2) Click on the "Settings" Tab
            3) click on the box that says "Delete this Group" and then "save changes"
        @expected:
            device group should be deleted
        """
        try: 
            # pre-condition : create a new device group#   
            beam =   TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)       
            beam_name = beam.beam_name
            new_device_group_name = Helper.generate_random_device_group_name()
            org_admin = User()
            org_admin.generate_org_admin_user_data()                                
           
            TestCondition.create_device_group(new_device_group_name, [beam_name])           
                             
            # steps
            admin_beams_all_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)\
                .delete_device_group()
             
            # verify point
            is_deleted = admin_beams_all_page.is_device_group_not_existed(new_device_group_name)            
            self.assertTrue(is_deleted, "Assertion Error: The Device-Group {} cannot be deleted.".format(new_device_group_name))
             
        finally:
            TestCondition.release_a_beam(beam)
     
     
    def test_c10962_add_a_user_to_a_device_group_1_x(self):
        """
        @author: tham.nguyen
        @date: 8/4/2016
        @summary: Add a User to a Device Group [2.X] 
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Create a Device Group (DeviceGroupA)
            Invite a new User (UserA)
        @steps:
            Steps To Complete Task: Add user to a Device Group
            1) Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2) Go to "Beams" tab and select existing device group (DeviceGroupA)
            3) Select "Members" tab and click on "Add Users" button
            4) Select a user (UserA) and click "Add Selected Users" button
             
        @expected: 
            1) Newly added user (UserA) is added under user list of this device group.
            2) The device group name displays in "Device Groups" field of newly added user detail page.
        """   
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            normal_user.organization = organization
             
            org_admin = User()
            org_admin.generate_org_admin_user_data()                                
            org_admin.device_group = device_group
            org_admin.organization = organization
             
            test_device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(test_device_group)           
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
             
            # steps
            admin_member_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_members_tab_of_a_device_group(test_device_group)\
                .add_user_to_device_group(normal_user)
                 
            # verify points
            is_user_displayed = admin_member_page.is_user_existed(normal_user.email_address, normal_user.get_displayed_name())
            self.assertTrue(is_user_displayed,
                        "Assertion Error: The newly added user {} isn't added under user list of this device group {}.".format(normal_user.email_address, test_device_group))
            detail_user_page = admin_member_page.goto_users_tab().goto_user_detail_page(normal_user)
             
            lst_devices = detail_user_page.get_device_groups()
            self.assertIn(test_device_group, lst_devices, "Assertion Error: The device group name displaying in 'Device Groups' field of newly added user detail page doesn't match a device group '{}' that added the user.".format(test_device_group))
             
        finally:
            # post-codition
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group, test_device_group], organization)
 
     
    def test_c10963_remove_a_user_from_a_device_group_1_x(self):
        """
        @author: tham.nguyen
        @date: 8/5/2016
        @summary: Remove a User from Device Group [2.X]
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Add a device group (DeviceGroupA) 
            Create user (UserA) added to this group.
        @steps:
            1) Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2) Go to "Beams" tab and select existing device group (DeviceGroupA)
            3) Select "Members" tab
            4) Click "Remove" red button on the user icon would like to remove (UserA)
            5) Click "OK" button on pop-up message
             
        @expected: 
            1) The pop-up message appears as "Are you sure you want to remove this member from <DeviceGroup name> device group?"
            2) The removed user (UserA) disappears under "Users" list.
            3) The device group name is not displayed in "Device Groups" field of removed user detail page.
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            normal_user.organization = organization
              
            org_admin = User()
            org_admin.generate_org_admin_user_data()                                
            org_admin.device_group = device_group_name
            org_admin.organization = organization
             
            TestCondition.create_device_group(device_group_name)           
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            expected_alert = str(ApplicationConst.DELETE_USER_FROM_DEVICE_GROUP).format(device_group_name)
             
            # steps
            admin_beam_member_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_members_tab_of_a_device_group(device_group_name)\
                .click_remove_user(normal_user.get_displayed_name())            
             
            # verify points
            alert_dialog = admin_beam_member_page.get_toast_msg()
            is_alert_content_correct = Utilities.are_strings_equal(alert_dialog, expected_alert)
            self.assertEqual(True, is_alert_content_correct,
                "Assertion Error: Content of deleting alert '{}' doesn't match expected content alert '{}'".format(alert_dialog, expected_alert))
             
            self.assertTrue(admin_beam_member_page.is_user_disappeared(normal_user.email_address, normal_user.get_displayed_name),
                "Assertion Error: " + normal_user.email_address + " still exists in device group " + device_group_name)
             
            detail_user_page = admin_beam_member_page.goto_users_tab().goto_user_detail_page(normal_user)
             
            lst_devices = detail_user_page.get_device_groups()
            self.assertNotIn(device_group_name, lst_devices, "Assertion Error: The device group name displaying in 'Device Groups' field of newly added user detail page matchs a device group '{}' that added the user, but the user was removed from the device group".format(device_group_name))
             
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group_name])
     
 
    def test_c10964_remove_a_usergroup_to_a_device_group_2_x(self):
        """
        @author: khoi.ngo
        @date: 8/5/2016
        @summary: Remove a UserGroup to a Device Group [2.X]
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
             
            Add a user group (UserGroupA)
            Add a device group (DeviceGroupA)
 
        @steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Beams" tab and select existing device group (DeviceGroupA)
            3. Select "Members"
            4. Click "Remove" red button on the user group icon would like to remove (UserGroupA)
            5. Click "Ok" button
        @expected:
            1. The pop-up message appears as "Are you sure you want to remove this user group from <DeviceGroup name> device group?"
            2. The removed user group (UserGroupA) disappears under "User Group" list .
            3. The device group name is not displayed in "Device Groups" field of removed user group (UserGroupA's) detail page.
        """
        try:
            # precondition
            device_group_name = Helper.generate_random_device_group_name()
            user_group_name = Helper.generate_random_user_group_name()
                    
            org_admin = User()
            org_admin.generate_org_admin_user_data()                                
           
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_user_group(user_group_name)
            TestCondition.add_user_group_to_device_group(device_group_name, [user_group_name])
             
            # steps            
            device_member = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_members_tab_of_a_device_group(device_group_name)
             
            toast_msg = device_member.click_remove_user(user_group_name).get_toast_msg()
            if toast_msg:
                toast_msg = Utilities.normalize_text(toast_msg)
            dialog_msg = str(ApplicationConst.WARN_MSG_REMOVE_USER_GROUP).format(device_group_name)
             
            # verify points
            self.assertEqual(toast_msg, dialog_msg,
                             "Assertion Error: Confirm message is not correct '{}'".format(toast_msg))
            self.assertTrue(device_member.is_user_group_disappeared(device_group_name),
                            "Assertion Error: User group still display under 'User Group' list.")            
            device_group_property = device_member.goto_users_tab()\
                .goto_user_group_detail_page(user_group_name).get_property(ApplicationConst.LBL_DEVICE_GROUPS_PROPERTY)
            self.assertNotEqual(device_group_property, device_group_name,
                                "Assertion Error: The device group name still display in 'Device Groups' field")
        finally:
            # post-condition
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_user_groups([user_group_name])
                    
 
    def test_c10965_add_a_new_device_group_a_then_add_existing_device_already_in_group_b_2_x(self):
        """
        @author: Thanh.Le
        @date: 8/9/2016
        @summary: Add a new Device Group A then add existing Device already in Group B [2.X]
        @precondition:
            1) Create a device group (DeviceGroupA) with Device Group Admin (DeviceGroupAdminA)
            2) Add devices (Beam1, Beam2) to the above DeviceGroupA
        @steps:
            1) Login to Suitabletech.com as an org admin and select "Manage Your Beams" from the user dropdown menu
            2) Go to "Beams" tab and select "Create Device Group" button
            3) Enter Device Group name and click "Choose devices to add to this group" button
            4) Select the devices which already added to the DeviceGroupA (Beam1, Beam2)
            5) Select "Create Device Group" button            
        @expected:
            5)    
            _There is message "The device group was successfully created." appears.
            _There is an email sent to admin to alert removal. 
             
        """
        try:
            # pre-condition
            new_device_group_name_a = Helper.generate_random_device_group_name()
            new_device_group_name_b = Helper.generate_random_device_group_name()
             
            new_device_group_admin_user = User()
            new_device_group_admin_user.generate_advanced_device_group_admin_data()
            new_device_group_admin_user.device_group =  new_device_group_name_a
             
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            TestCondition.create_device_group(new_device_group_name_a, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver,[new_device_group_admin_user])
            # steps
            LoginPage(self._driver).open()\
                .login(new_device_group_admin_user.email_address, new_device_group_admin_user.password)\
                .goto_your_account()\
                    .goto_notifications_tab()\
                    .toggle_device_groups_settings_are_changed()\
                    .logout().goto_login_page()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                    .create_new_device_group(new_device_group_name_b)\
                    .add_devices([beam_name])
                 
            # verify points
            notification_email_template = EmailDetailHelper.generate_beam_removed_from_device_group_email(new_device_group_name_a, org_admin.get_displayed_name(), beam_name)
            actual_notification_email = GmailUtility.get_messages(notification_email_template.subject, receiver=new_device_group_admin_user.email_address)
            self.assertEqual(1, len(actual_notification_email),
                             "Assertion Error: There should be one {} notification on new admin's inbox. Found {}".format(notification_email_template.subject, len(actual_notification_email)))
            self.assertEqual(notification_email_template.trimmed_text_content, actual_notification_email[0].trimmed_text_content,
                          "Assertion Error: the actual notification content {} is not sent as expected {}".format(actual_notification_email[0].trimmed_text_content, notification_email_template.trimmed_text_content))
                 
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([new_device_group_admin_user])
            TestCondition.delete_device_groups([new_device_group_name_a, new_device_group_name_b])            
 
 
    def test_c10966_move_a_existing_beam_device_from_device_group_a_to_another_device_group_b_2_x(self):
        """
        @author: Thanh.Le
        @date: 8/9/2016
        @summary: Move a existing (Beam) Device from Device Group A to another Device Group B [2.X]
        @precondition:
            1) Create a device group (DeviceGroupA) with Device Group Admin (DeviceGroupAdminA)
            2) Add devices (Beam1, Beam2) to the above DeviceGroupA
            3) Create another device group (DeviceGroupB)
        @steps:
            1) Login to Suitabletech.com as an org admin and select "Manage Your Beams" from the user dropdown menu
            2) Go to "Beams" tab and select the created device group (DeviceGroupB)
            3) Click "Add Devices" button and select device which already added in DeviceGroupA in pre-condition (Beam1, Beam2)
            4) Select "Add Selected Devices" button  
        @expected:
            4)
            _Selected devices are added to DeviceGroupB
            _Admin of DeviceGroupA recieves an email notifies the removal.
             
        """
        try:
            # pre-condition
            new_device_group_name_a = Helper.generate_random_device_group_name()
            new_device_group_name_b = Helper.generate_random_device_group_name()
             
            new_device_group_admin_user = User()
            new_device_group_admin_user.generate_advanced_device_group_admin_data()
            new_device_group_admin_user.device_group = new_device_group_name_a
             
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
             
            TestCondition.create_device_group(new_device_group_name_a, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [new_device_group_admin_user])
            # steps
            admin_beams_page = LoginPage(self._driver).open()\
                .login(new_device_group_admin_user.email_address, new_device_group_admin_user.password)\
                .goto_your_account()\
                    .goto_notifications_tab()\
                    .toggle_device_groups_settings_are_changed()\
                    .logout().goto_login_page()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                    .create_new_device_group(new_device_group_name_b, [beam_name], False)
                 
            # verify points
            msg = admin_beams_page.get_msg_success()
            self.assertEqual(ApplicationConst.INFO_MSG_CREATE_DEVICE_GROUP_SUCCESSFUL, msg, "Assertion Error: Create devide group success message is not displayed")
             
            # verify points
            notification_email_template = EmailDetailHelper.generate_beam_removed_from_device_group_email(new_device_group_name_a, org_admin.get_displayed_name(), beam_name)
            actual_notification_email = GmailUtility.get_messages(notification_email_template.subject, receiver=new_device_group_admin_user.email_address)
            self.assertEqual(1, len(actual_notification_email),
                             "Assertion Error: There should be one {} notification on new admin's inbox. Found {}".format(notification_email_template.subject, len(actual_notification_email)))
            self.assertEqual(notification_email_template.trimmed_text_content, actual_notification_email[0].trimmed_text_content,
                          "Assertion Error: the actual notification content {} is not sent as expected {}".format(actual_notification_email[0].trimmed_text_content, notification_email_template.trimmed_text_content))
                 
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([new_device_group_admin_user])
            TestCondition.delete_device_groups([new_device_group_name_a, new_device_group_name_b])            
 
 
    def test_c11073_add_device_group_default_access_time(self):
        """
        @author: Quang.Tran
        @date: 08/05/2016
        @summary: Add Device Group Default Access Time  
        @precondition: 
            Add a device group (DeviceGroupA)
        @steps:
            Steps to add Device Group Default Access Time:
             
                1.Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
                2.Go to "Beams" tab
                3.Select an existing device group (DeviceGroupA)
                4.Select "Access Time" tab and click "Add Access Time" button on the right of "Access Times for All Members"
                5.On "Create Access Time for All Members" pop-up, 
                    _Select each day that all group members will have access to the devices in this device group 
                    _Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day" 
                    _If each session requires authorization, check the " Require session answer" check box (Optional)
                6.Click on the "Create" button to complete the form
 
        @expected:
            (6) A Device Group Default Access Time ("All day every day") record is added under "Access Times for All Members" section and on the table.
        """
         
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
             
            new_device_group_name = Helper.generate_random_device_group_name()
             
            org_admin = User()
            org_admin.generate_org_admin_user_data()
             
            TestCondition.create_device_group(device_group_name=new_device_group_name, device_array=[beam_name])
             
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Thu, WeekDays.Wed, WeekDays.Fri, WeekDays.Sat, WeekDays.Sun]
                 
            # steps
            admin_beam_access_times_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_access_times_tab_of_a_device_group(new_device_group_name)
             
            # Toggle 'All day' button
            admin_beam_access_times_page.add_default_allday_access_times(access_days)
             
            # verify points
            expected_item_label = "{} {}".format(
                                        ApplicationConst.get_date_time_label("All day"),
                                        ApplicationConst.get_date_time_label("every day")) 
             
            self.assertTrue(admin_beam_access_times_page.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_access_times_page.is_default_allday_access_time_displayed_on_calendar(access_days), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
             
            # Toggle 'Time range' button
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30) 
            admin_beam_access_times_page.add_default_timerange_access_times(access_days, starting_datetime, ending_datetime)
             
            # verify points
            expected_item_label = "{} {}".format(
                                        Helper.generate_time_range_label(starting_datetime, ending_datetime),
                                        ApplicationConst.get_date_time_label("every day"))
             
            self.assertTrue(admin_beam_access_times_page.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_access_times_page.is_default_timerange_access_time_displayed_on_calendar(access_days, starting_datetime, ending_datetime), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups(device_group_array=[new_device_group_name])
        
     
    def test_c11074_add_device_group_member_access_time(self):
        """
        @author: Quang.Tran
        @date: 08/08/2016
        @summary: Add Device Group Member Access Time  
        @precondition: 
            Add a device group (DeviceGroupA) with a user (UserA) added
        @steps:
        Steps to add device group member access time:
         
            1.Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Beams" tab
            3. Select an existing device group (DeviceGroupA)
            4. Select "Access Time" tab and click "Add Access Time" button under "Members" section
            5. On "Create Member-Specific Access Time" pop-up, 
                _Select a user in "Choose a member" access on these days 
                _Select each day that the specific member will have access to the devices in this device group 
                _Toggle "Time Range" to select the window of time which the specific member will have access to the devices or Toggle the option for "All day" 
                _If each session requires authorization, check the " Require session answer" check box (Optional)
            6. Click on the "Create" button to complete the form
         
        @expected:
            (6) A default access time for specific member (UserA) is created under "Members" section and on the table.
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            new_device_group_name = Helper.generate_random_device_group_name()
          
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()                                
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = new_device_group_name
         
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Wed, WeekDays.Fri]
             
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)
             
            TestCondition.create_device_group(new_device_group_name, [beam_name])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)            
                 
            # steps
            admin_beam_access_times_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_access_times_tab_of_a_device_group(new_device_group_name)
             
            # Toggle 'All day' button
            admin_beam_access_times_page.add_member_allday_access_times(normal_user, access_days)
             
            # verify points
            expected_item_label = "{} {}, {}, {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Fri"))
              
            self.assertTrue(admin_beam_access_times_page.is_member_access_time_label_displayed_on_sidebar(normal_user, expected_item_label), \
                "Assertion Error: The access time role '{}' for user '{}' is not displayed in the sidebar".format(expected_item_label, normal_user.get_displayed_name()))
              
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_access_times_page.is_member_allday_access_time_displayed_on_calendar(normal_user, access_days), \
                    "Assertion Error: The access time role '{}' for user '{}' is not displayed in the calendar".format(expected_item_label, normal_user.get_displayed_name()))
                  
            # Toggle 'Time range' button
            admin_beam_access_times_page.add_member_timerange_access_times(normal_user, access_days, starting_datetime, ending_datetime)
              
            # verify points
            expected_item_label = "{} {}, {}, {}, {}".format(
                                    Helper.generate_time_range_label(starting_datetime, ending_datetime),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Fri"))
              
            self.assertTrue(admin_beam_access_times_page.is_member_access_time_label_displayed_on_sidebar(normal_user, expected_item_label), \
                "Assertion Error: The access time role '{}' for user '{}' is not displayed in the sidebar".format(expected_item_label, normal_user.get_displayed_name()))
              
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_access_times_page.is_member_timerange_access_time_displayed_on_calendar(normal_user, access_days, starting_datetime, ending_datetime), \
                    "Assertion Error: The access time role '{}' for user '{}' is not displayed in the calendar".format(expected_item_label, normal_user.get_displayed_name()))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([normal_user])
             
     
    def test_c11075_edit_a_device_group_member_access_time(self):
        """
        @author: Quang.Tran
        @date: 08/08/2016
        @summary: Edit A Device Group Member Access Time  
        @precondition: 
            Add a device group (DeviceGroupA) with a user (UserA) added
             
            Steps to create a access time for a specific member:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Beams" tab
            3. Select an existing device group (DeviceGroupA)
            4. Select "Access Time" tab and click "Add Access Time" button under "Members" section
            5. On "Create Member-Specific Access Time" pop-up,
            _Select a user in "Choose a member" access on these days
            _Select each day that the specific member will have access to the devices in this device group
            _Toggle "Time Range" to select the window of time which the specific member will have access to the devices or Toggle the option for "All day"
            _If each session requires authorization, check the " Require session answer" check box (Optional)
            6. Click on the "Create" button to complete the form
 
        @steps:
            Steps to edit a Device Group Member Access Time:
         
            1. Select the access time record created in pre-condition by clicking the record under "Members" section
            2. Change some info _Uncheck to deselect some days _Toggle "Time range" and change Beginning/ Ending time
            3. Select "Update" button to save changes
            4. Select the access time record created in pre-condition by clicking the record on the access time table
            5. Change some info _Uncheck to deselect some days _Toggle "Time range" and change Beginning/ Ending time
            6. Select "Update" button to save changes
         
        @expected:
            (3) (6) All changes are updated to the selected access time record.
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            new_device_group_name = Helper.generate_random_device_group_name()
             
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()                                
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = new_device_group_name
         
            origin_access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Wed, WeekDays.Thu, WeekDays.Fri, WeekDays.Sat]
            new_access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Wed, WeekDays.Fri]
             
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
             
            new_starting_datetime = Helper.generate_date_time(hour_delta=8)
            new_ending_datetime = Helper.generate_date_time(hour_delta=16, minute_delta=30)
             
            TestCondition.create_device_group(new_device_group_name, [beam_name])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
             
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_access_times_tab_of_a_device_group(new_device_group_name)\
                .add_member_allday_access_times(normal_user, origin_access_days)\
                .add_member_timerange_access_times(normal_user, origin_access_days, starting_datetime, ending_datetime)\
                .goto_dashboard_tab()
                 
            # steps
            admin_beam_access_times_page = admin_dashboard_page.goto_access_times_tab_of_a_device_group(new_device_group_name)
             
            # Toggle 'All day' button
            access_time_label = Utilities.generate_access_time_label(origin_access_days)
            admin_beam_access_times_page.edit_member_access_times(normal_user, access_time_label, new_access_days)
             
            # verify points
            expected_item_label = "{} {}, {}, {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Fri"))
             
            is_displayed_on_sidebar = admin_beam_access_times_page.is_member_access_time_label_displayed_on_sidebar(normal_user, expected_item_label)   
            self.assertTrue(is_displayed_on_sidebar, \
                "Assertion Error: The access time role '{}' for user '{}' is not displayed in the sidebar".format(expected_item_label, normal_user.get_displayed_name()))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                is_displayed_on_calendar = admin_beam_access_times_page.is_member_allday_access_time_displayed_on_calendar(normal_user, new_access_days)  
                self.assertTrue(is_displayed_on_calendar, \
                    "Assertion Error: The access time role '{}' for user '{}' is not displayed in the calendar".format(expected_item_label, normal_user.get_displayed_name()))
               
            # Toggle 'Time range' button
            access_time_label = Utilities.generate_access_time_label(origin_access_days, starting_datetime, ending_datetime)
            admin_beam_access_times_page.edit_member_access_times(normal_user, access_time_label, new_access_days, new_starting_datetime, new_ending_datetime)
               
            # verify points
            expected_item_label = "{} {}, {}, {}, {}".format(
                                    Helper.generate_time_range_label(new_starting_datetime, new_ending_datetime),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Fri"))
             
            is_displayed_on_sidebar = admin_beam_access_times_page.is_member_access_time_label_displayed_on_sidebar(normal_user, expected_item_label)  
            self.assertTrue(is_displayed_on_sidebar, \
                "Assertion Error: The access time role '{}' for user '{}' is not displayed in the sidebar".format(expected_item_label, normal_user.get_displayed_name()))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                is_displayed_on_calendar = admin_beam_access_times_page.is_member_timerange_access_time_displayed_on_calendar(normal_user, new_access_days, new_starting_datetime, new_ending_datetime)  
                self.assertTrue(is_displayed_on_calendar, \
                    "Assertion Error: The access time role '{}' for user '{}' is not displayed in the calendar".format(expected_item_label, normal_user.get_displayed_name()))
             
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([normal_user])
             
 
    def test_c11076_edit_device_group_default_access_time(self):
        """
        @author: Quang.Tran
        @date: 08/05/2016
        @summary: Edit Device Group Default Access Time  
        @precondition: 
        Add a device group (DeviceGroupA)
         
        Steps to create a access time for a device group:
         
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Beams" tab
            3. Select an existing device group (DeviceGroupA)
            4. Select "Access Time" tab and click "Add Access Time" button on the right of "Access Times for All Members"
            5. On "Create Access Time for All Members" pop-up, 
                _Select each day that all group members will have access to the devices in this device group 
                _Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day" 
                _If each session requires authorization, check the " Require session answer" check box (Optional)
            6. Click on the "Create" button to complete the form
 
        @steps:
        Steps To Complete Task: Edit Access Times for a Device Group
         
            1. Select the access time record created in pre-condition by clicking the record under "Access Times for All Members" section
            2. Change some info 
                _Uncheck to deselect some days 
                _Toggle "Time range" and change Beginning/ Ending time
            3. Select "Update" button to save changes
            4. Select the access time record created in pre-condition by clicking the record on the access time table
            5. Change some info 
                _Uncheck to deselect some days 
                _Toggle "Time range" and change Beginning/ Ending time
            6. Select "Update" button to save changes
 
        @expected:
            (3) (6) All changes are updated to the selected access time record.
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            new_device_group_name = Helper.generate_random_device_group_name()
             
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()                                
             
            origin_access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Thu, WeekDays.Wed, WeekDays.Fri, WeekDays.Sat, WeekDays.Sun]
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
             
            new_access_days = [WeekDays.Mon, WeekDays.Tue]
             
            new_starting_datetime = Helper.generate_date_time(hour_delta=8)
            new_ending_datetime = Helper.generate_date_time(hour_delta=16, minute_delta=30)
            new_expected_item_label = "{} {}, {}".format(
                                    Helper.generate_time_range_label(new_starting_datetime, new_ending_datetime),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"))
             
            TestCondition.create_device_group(new_device_group_name, [beam_name])
             
            admin_beams_access_time_pg = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_access_times_tab_of_a_device_group(new_device_group_name)\
                .add_default_allday_access_times(origin_access_days)\
                .add_default_timerange_access_times(origin_access_days, starting_datetime, ending_datetime)
                 
            # steps            
            # Case 1: Toggle 'All day' button
            allday_access_time_label = Utilities.generate_access_time_label(origin_access_days)
            admin_beams_access_time_pg.edit_default_access_times(allday_access_time_label, new_access_days)
            # verify points
            expected_item_label = "{} {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"))
            
            self.assertTrue(admin_beams_access_time_pg.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beams_access_time_pg.is_default_allday_access_time_displayed_on_calendar(new_access_days), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
             
            # Case 2: Toggle 'Time range' button
            timerange_access_time_label = Utilities.generate_access_time_label(origin_access_days, starting_datetime, ending_datetime)
            admin_beams_access_time_pg.edit_default_access_times(timerange_access_time_label, new_access_days, new_starting_datetime, new_ending_datetime)
            # verify points
             
            self.assertTrue(admin_beams_access_time_pg.is_default_access_time_label_displayed_on_sidebar(new_expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(new_expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beams_access_time_pg.is_default_allday_access_time_displayed_on_calendar(new_access_days), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(new_expected_item_label))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
 
 
    def test_c11077_add_device_group_temporary_access_time(self):
        """
        @author: Thanh Le
        @date: 08/19/2016
        @summary: Add Device Group Temporary Access Time(s):  
        @precondition: Steps To Complete Task: Add Access Times for a Device Group
            From your organization's Site Admin 2.0 Dashboard.
            Select the "Beam" drop down menu, then select an existing Device Group listed
            Select the "Access" Tab
            To Create new Device Group Access times for all members:
            Select the "Add Access Time" button to the right of "Access Times for All Members"
            Select each day that all group members will have access to the devices in this device group.
            Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day"
            If each session requires authorization, check the " Require session answer" check box (Optional)
            Click on the "Create" button to complete the form.
        @steps:
            To Create new Device Group Temporary Access Time(s):
            1. Select the "Add Access Time" button to the right of "Temporary Contacts" text
            2. Complete the form:
            - Enter the email of the target Contact or new Contact you wish to grant access to.
            - Select the start date and time.
            - Select the end date and time.
            - If the Contacts require session authorization, toggle the "Require session answer" option
            - Sending an email is also optional
            3. Click the "Invite" button to complete the form    
        @expected:
            The temporary access time has been added successfully    
        """
        try:
            from core.i18n.i18n_support import I18NSupport  
            # pre-condition:
            tomorrow = Helper.generate_access_day()
            access_day = WeekDays(tomorrow.isoweekday()) 
            new_device_group = Helper.generate_random_device_group_name()
             
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()
 
            new_temp_user = User()
            new_temp_user.generate_advanced_normal_user_data()            
             
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)                         
         
            TestCondition.create_device_group(new_device_group)
 
            # steps
            admin_beams_access_times_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_access_times_tab_of_a_device_group(new_device_group)\
                .invite_temporary_user(new_temp_user, start_date=starting_datetime, end_date=ending_datetime, link_to_beam_sofware=True, default_invitation=True)
                                    
            # verify point
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beams_access_times_page.is_temporary_time_range_access_time_displayed_on_calendar(new_temp_user, [access_day], starting_datetime, ending_datetime),
                             "Assertion Error: The access temporary time rule is not displayed!")            
            date_label = I18NSupport.localize_date_time_string( re.sub(' +',' ',tomorrow.strftime('%b %e, %Y')) )
            access_time_label = Utilities.generate_temporary_access_time_label(date_label, starting_datetime, ending_datetime)
            self.assertTrue(admin_beams_access_times_page.is_member_access_time_label_displayed_on_sidebar(new_temp_user, access_time_label), 
                            "Temporary user {} does not display on sidebar with access time: start time is {} and end time is {}".format(new_temp_user.email_address, starting_datetime, ending_datetime))
        finally:
            # post-condition:
            TestCondition.delete_device_groups([new_device_group])
             
             
    def test_c11078_edit_device_group_temporary_access_time(self):
        """
        @author: Thanh Le
        @date: 08/19/2016
        @summary: Edit Device Group Temporary Access Time(s):  
        @precondition: Steps To Complete Task: Add Access Times for a Device Group
            From your organization's Site Admin 2.0 Dashboard.
            Select the "Beam" drop down menu, then select an existing Device Group listed
            Select the "Access" Tab
            To Create new Device Group Access times for all members:
            Select the "Add Access Time" button to the right of "Access Times for All Members"
            Select each day that all group members will have access to the devices in this device group.
            Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day"
            If each session requires authorization, check the " Require session answer" check box (Optional)
            Click on the "Create" button to complete the form.
        @steps:
            Note: To Edit a Temporary Contact Access Time:
            1. Click the Pencil Icon next to the target entry in the "Temporary Contacts" list or click on the representative time block on the calendar itself.
            2. Edit the form as needed
            - Set the start Date and Time
            - Set the End Date and Time
            - If each session requires authorization, check the " Require session answer" check box (Optional)
            3. Select the "Update" button to complete the form 
        @expected:
            The temporary access time has been edited successfully
        """
        try:
            # pre-condition:
            from core.i18n.i18n_support import I18NSupport  
            tomorrow = Helper.generate_access_day()
            access_day = WeekDays(tomorrow.isoweekday()) 
            new_device_group = Helper.generate_random_device_group_name()
             
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()                                
            admin_user.device_group = new_device_group
             
            new_temp_user = User()
            new_temp_user.generate_advanced_normal_user_data()
            new_temp_user.device_group = new_device_group
             
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)  
             
            updated_start_time = Helper.generate_date_time(hour_delta=8)
            updated_end_time = Helper.generate_date_time(hour_delta=16, minute_delta=30)  
             
            TestCondition.create_device_group(new_device_group)
            TestCondition.create_advanced_temporary_user(self._driver, new_temp_user, new_device_group, starting_datetime, ending_datetime)
             
            # steps
            admin_beams_access_times_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_access_times_tab_of_a_device_group(new_device_group)
                 
            temporary_user_access_time_label = admin_beams_access_times_page.get_temporary_user_access_time_label(starting_datetime, ending_datetime)            
            admin_beams_access_times_page = admin_beams_access_times_page.edit_temporary_access_times(new_temp_user, access_time_label=temporary_user_access_time_label, start_date=updated_start_time, end_date=updated_end_time)
             
            # verify point
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beams_access_times_page.is_temporary_time_range_access_time_displayed_on_calendar(new_temp_user, [access_day], updated_start_time, updated_end_time),
                             "Assertion Error: The access temporary time is NOT edited successfully!")
            date_label = I18NSupport.localize_date_time_string( re.sub(' +',' ',tomorrow.strftime('%b %e, %Y')) )
            access_time_label = Utilities.generate_temporary_access_time_label(date_label, updated_start_time, updated_end_time)
            self.assertTrue(admin_beams_access_times_page.is_member_access_time_label_displayed_on_sidebar(new_temp_user, access_time_label), 
                            "Temporary user {} does not display on sidebar with access time: start time is {} and end time is {}".format(new_temp_user.email_address, updated_start_time, updated_end_time))
        finally:
            # post-condition:
            TestCondition.delete_advanced_users([new_temp_user])
            TestCondition.delete_device_groups([new_device_group])
         
     
    @pytest.mark.OnlyDesktop
    def test_c11581_view_devicegroup_in_list_and_icon_viewing_mode(self):
        """
        @author: Thanh Le
        @date: 08/17/2016
        @summary: View DeviceGroup in List and Icon Viewing Mode
        @precondition: 
            View DeviceGroup in List and Icon Viewing Mode
        @steps:
            1) Navigate to Admin 2.0 "Beams' tab
            2) Select a device Group
            3) select List view of devices
            4) Select Icon view of devices
 
        @expected:
            Verify Beam/Devices are all visible in a usable manner:
                1. Size of Icons are correct
                2. Text sizes
        """       
        try:
             
            # pre-condition
            new_device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            org_admin.device_group = new_device_group
            org_admin.organization = organization
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            TestCondition.create_device_group(new_device_group, [beam_name], organization)
                         
            # steps:
            admin_beams_devices_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                .select_device_group(new_device_group)

            list_view_size = admin_beams_devices_page.switch_to_list_view()\
                .get_item_size_in_list_view(beam_name)
            icon_view_size = admin_beams_devices_page.switch_to_icon_view()\
                .get_item_size_in_icon_view(beam_name)
             
            # verify point
            self.assertTrue(icon_view_size > list_view_size,
                            "Assertion Error: Unable to switch from icon view to list view.")
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group], organization)


    @pytest.mark.OnlyDesktop
    def test_c33949_show_function_works_correctly_in_members_tab_of_device_group(self):
        """
        @author: Quang Tran
        @date: 12/1/2017
        @summary: Show function works correctly in Members tab of device group
        @precondition: 
            Create a device group 
            Add some admins and users to the device group
        @steps:
            1) Login as admin
            2) Select the device group
            3) Go to Members tab
            4) Select any item in Show dropdown
 
        @expected:
            Users are shown correctly with any item is selected in Show dropdown
        """ 
        try:
            #pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
     
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
     
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            TestCondition.create_advanced_normal_users(self._driver, [device_group_admin])
      
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group_name
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
     
            TestCondition.set_advanced_device_group_admin(device_group_admin.email_address, device_group_name, Constant.AdvancedOrgName)

            #steps
            members_page = LoginPage(self._driver).open()\
                    .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                    .goto_beams_tab()\
                    .select_device_group(device_group_name)\
                    .goto_members_tab()\
                    .switch_to_list_view()\
                    .click_show_button_and_select(ApplicationConst.LBL_MENU_GUEST_ONLY)

            #verify point 
            #TODO: Test case failed due to bug https://jira.suitabletech.com/browse/INFR-2574
            self.assertTrue(members_page.is_icon_displayed_at_each_users_on_table(Constant.IconName["guest_user"]), 
                        "Having an account misses Guest User icon at Privileges column")
            members_page = members_page.click_show_button_and_select(ApplicationConst.LBL_MENU_ADMINISTRATOR_ONLY)
            self.assertTrue(members_page.is_icon_displayed_at_each_users_on_table(Constant.IconName["org_admin"]), 
                        "Having an account misses Org admin icon at Privileges column")
            members_page = members_page.click_show_button_and_select(ApplicationConst.LBL_MENU_USER_GROUPS)
            self.assertTrue(members_page.is_user_group_table_displayed, "User group does not display")

            members_page = members_page.switch_to_icon_view()\
                    .click_show_button_and_select(ApplicationConst.LBL_MENU_GUEST_ONLY)
            #verify point
            self.assertTrue(members_page.is_icon_displayed_at_each_users_on_icon_mode(Constant.IconName["guest_user"]), 
                        "Having an account misses Guest User icon at Privileges column")
            members_page = members_page.click_show_button_and_select(ApplicationConst.LBL_MENU_ADMINISTRATOR_ONLY)
            self.assertTrue(members_page.is_icon_displayed_at_each_users_on_icon_mode(Constant.IconName["org_admin"]), 
                        "Having an account misses Org admin icon at Privileges column")
            members_page = members_page.click_show_button_and_select(ApplicationConst.LBL_MENU_USER_GROUPS)
            self.assertTrue(members_page.is_user_group_table_displayed, "User group does not display")

        finally:
            TestCondition.delete_advanced_users([normal_user, device_group_admin, org_admin])
            TestCondition.delete_device_groups([device_group_name])


    def test_c34006_search_and_sort_work_correctly_in_members_tab_of_device_group(self):
        """
        @author: Khoi Ngo
        @date: 03/05/2018
        @summary: Search and sort functions work correctly in Members tab of DeviceGroup.
        @precondition:
            Login as org admin or device group admin
            Have a Device Group with several user members
        @steps:
            1) Login as admin
            2) Go to Beams tab
            3) Select the Device Group in preconditions
            4) Go to Members tab
            5) Sort by First Name, Last Name, Username
            6) Search for an user in the Device Group

        @expected:
            1) Verify that Sort by First Name, Last Name, Username work correctly
            2) Verify that Search works correctly
        """
        try:
            # pre-condition:
            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group)

            user_member_1 = User()
            user_member_1.generate_advanced_normal_user_data()
            user_member_1.device_group = device_group

            user_member_2 = User()
            user_member_2.generate_advanced_normal_user_data()
            user_member_2.device_group = device_group

            user_member_3 = User()
            user_member_3.generate_advanced_normal_user_data()
            user_member_3.device_group = device_group

            TestCondition.create_advanced_normal_users(self._driver, [user_member_1, user_member_2, user_member_3])

            # steps for icon view
            beam_member_page = LoginPage(self._driver).open()\
                    .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                    .goto_beams_tab()\
                    .select_device_group(device_group)\
                    .goto_members_tab()

            # verify search works correctly
            self.assertTrue(beam_member_page.check_search_user_work_correctly(user_member_1), "Assert Error: Search function works incorrectly")

            if self._driver.driverSetting.platform == Platform.WINDOWS or self._driver.driverSetting.platform == Platform.MAC:
                #TO DO: This is failed by INFR-2721
                # verify points Sort by
                    self.assertTrue(beam_member_page.check_sort_by_work_correctly(), "Assertion Error: Sort function with icon view works incorrectly.")

                # steps for list view
                    beam_member_list_view = beam_member_page.switch_to_list_view()
                # verify points Sort table
                    self.assertTrue(beam_member_list_view.check_table_users_can_sort(), "Assertion Error: Table is not sorted correctly.")

        finally:
                TestCondition.delete_advanced_users([user_member_1, user_member_2, user_member_3])
                TestCondition.delete_device_groups([device_group])

