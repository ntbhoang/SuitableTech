from datetime import datetime
import re
from common.application_constants import ApplicationConst
from common.helper import Helper, EmailDetailHelper
from core.utilities.gmail_utility import GmailUtility
from core.utilities.test_condition import TestCondition
from core.utilities.utilities import Utilities
from data_test.dataobjects.enum import WeekDays
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from test.testbase import TestBase
from common.constant import Constant, Platform
from core.suitabletechapis.user_api import UserAPI
import pytest


class DeviceGroupAcess_Test(TestBase):
    
    def test_c11609_move_device_to_different_device_group_within_same_org_1_X(self):
        """
        @author: khoi.ngo
        @date: 8/19/2016
        @summary: Move device to different device group (within same org) [1.X]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs

            This test requires the Device Group Admin to be the admin for more than one Device Group.
        @steps:
            Steps To Complete Task: add newly paired Beam to a Device Group:
            1. Go to the "Beams" tab under the "Manage your Beams" dashboard 
            2. Select a Beam device
            3. Selects the "Edit" box above the device image icon
            4. hover your cursor over the "Group" drop down menu
        @expected:
            Verify that the user is warned about moving devices to other device groups.
        """
        try:
            # precondition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            
            device_group_1 = Helper.generate_random_device_group_name()
            device_group_1_device_list = [beam_name]
            
            device_group_2 = Helper.generate_random_device_group_name()
            device_group_2_device_list = []
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()            
            device_group_admin.device_group = device_group_1
            
            TestCondition.create_device_group(device_group_1, device_group_1_device_list, device_group_admin.organization)
            TestCondition.create_device_group(device_group_2, device_group_2_device_list, device_group_admin.organization)
            
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            TestCondition.set_advanced_device_group_admin(device_group_admin.email_address, device_group_2, device_group_admin.organization)
            
            # steps
            edit_beam_dialog = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_a_device(beam_name).open_edit_dialog().set_beam_group(device_group_2)
            
            # verify point
            self.assertEqual(edit_beam_dialog.get_warning_message(), ApplicationConst.WARN_MSG_CHANGE_DEVICE_GROUP_NAME, "No warning message displayed when modifying the Device Group of device {}".format(beam_name))
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([device_group_admin], device_group_admin.organization)
            TestCondition.delete_device_groups([device_group_1, device_group_2])
    
    
    def test_c11610_remove_device_from_group_1_X(self):
        """
        @author: khoi.ngo
        @date: 8/19/2016
        @summary: Remove device from group [1.X]
        @precondition: 
            Devices-Mod-Move_Group
            
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs

        @steps:
            1. go to the "Manage your Beams" dashboard, click on the "Beams" tab
            2. select a device group
            3. Select a device in the device group
            4. Click the "Edit" button above the device image icon
        @expected:
            Verify that as a Device Group Admin you are not permitted to remove device from group (i.e. no "Unlink this Device..." box 
        """
        try:
            # precondition
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            new_device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            admin_user.device_group = new_device_group_name
            
            TestCondition.create_device_group(new_device_group_name, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            edit_beam_dialog = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password).goto_beams_tab()\
                .select_device_group(new_device_group_name)\
                .select_a_device(beam_name).open_edit_dialog()
            
            # verify point
            self.assertFalse(edit_beam_dialog.is_button_unlink_displayed(), "Assertion Error: Unlink beam is display.")
            edit_beam_dialog.cancel()
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])


    def test_c11612_rename_device_group_1_x(self):
        """
        @author: khoi.ngo
        @date: 7/25/2016
        @summary: Rename Device group [ 1.X]
        @precondition: Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                    http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1) Go to the "Beams" tab under the "Manage your Beams" dashboard
            2) click on a device group
            3) Click on the "Settings" (will be directed to "Devices" tab first)
            4) Change the name of the device group in the "Name" string
            5) Click on the "Save Changes" box
            6) Logout and login as device group admin
            7) click on a device group
            8) Click on the "Settings" (will be directed to "Devices" tab first)
            9) Change the name of the device group in the "Name" string
            10) Click on the "Save Changes" box
        @expected:
            Verify that device group name has been changed by clicking back to the "Devices" tab
            and subsequently clicking back to the "Beams" tab
        """
        try:
            # precondition
            device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.device_group = device_group_name
            device_group_admin.generate_advanced_device_group_admin_data()

            new_device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            beams_settings_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_device_group(device_group_name)\
                .goto_setting_tab()
            
            # steps            
            devices_tab = beams_settings_page\
                .change_device_group_name(new_device_group_name)\
                .goto_devices_tab()
    
            # verify points
            self.assertEqual(devices_tab.get_device_group_name(), new_device_group_name,
                              "Assertion Error: Device group name is {} instead {} ".format(devices_tab.get_device_group_name(), new_device_group_name))
            
            all_devices_group = devices_tab.goto_beams_tab()
            self.assertTrue(all_devices_group.is_device_group_existed(new_device_group_name),
                            "Assertion Error: Cannot find device group: " + new_device_group_name)

            #login with device group admin
            beams_settings_page = devices_tab.logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_device_group(new_device_group_name)\
                .goto_setting_tab()\
                .change_device_group_name(device_group_name)\
                .goto_devices_tab()

            # verify points
            self.assertEqual(beams_settings_page.get_device_group_name(), device_group_name,
                              "Assertion Error: Device group name is {} instead {} ".format(devices_tab.get_device_group_name(), device_group_name))
            
            all_devices_group = beams_settings_page.goto_beams_tab()
            self.assertTrue(all_devices_group.is_device_group_existed(device_group_name),
                            "Assertion Error: Cannot find device group: " + device_group_name)
        finally:    
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([device_group_admin])


    def test_c11613_device_group_admin_delete_device_group_2_x(self):
        """
        @author: Quang.Tran
        @date: 7/25/2016
        @summary: Device Group Admin Delete Device group [ 2.X]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1) Click on the "Beams" tab under the "Manage your Beams" dashboard
            2) Go to the "Settings" tab
            3) go to the "Settings" tab
        @expected:
            Verify as a Device Group Admin you are not able to delete the Device-Group (i.e. the "Delete This Group" button is not visable in the "Settings" tab) 
        """
        try:
            # pre-condition
            new_device_group_name = Helper.generate_random_device_group_name()
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
            
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open().login(admin_user.email_address, admin_user.password)
            admin_beams_settings_page = admin_dashboard_page.goto_beams_tab()\
                .select_device_group(new_device_group_name)\
                .goto_setting_tab()
            
            # verify point
            self.assertFalse(admin_beams_settings_page.is_device_group_removable(),
                             "Assertion Error: Current Device Group admin user can delete the Device-Group.")
        finally:
            # clean up
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])
        
            
    def test_c11615_remove_user_from_device_group_2_x(self):
        """
        @author: tham.nguyen
        @date: 7/26/2016
        @summary: Remove a User from Device Group [2.X]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1) Under Beams, Select a Device Group, Select Members
            2) Next to each contact is a remove button
            3) Upon completion, a toast confirms the result
        @expected:
            1. Upon completion, a toast confirms the result
            2. Verify that removed user no longer has access to the device group
        """
        try:
            # pre-condition
            #create device group admin
            device_group_name = Helper.generate_random_device_group_name()                    
            device_group_admin = User()                            
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
                                                        
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            # steps
            
            members_in_beams_devices_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_device_group(device_group_name).goto_members_tab()\
                .search_user(normal_user.email_address)\
                .click_remove_user(UserAPI.get_displayed_name(normal_user))
            
            content_of_delete_alert = members_in_beams_devices_page.get_toast_msg(True)
            expected_content_of_delete_alert = str(ApplicationConst.DELETE_USER_FROM_DEVICE_GROUP).format(device_group_name)
            is_delete_arlert_content_correct = Utilities.are_strings_equal(content_of_delete_alert, expected_content_of_delete_alert)
            
            # expected
            self.assertEqual(True, is_delete_arlert_content_correct,
                             "Assertion Error: '{}' doesn't match '{}' when the device admin deleted a user".format(content_of_delete_alert, expected_content_of_delete_alert))
            
            self.assertTrue(members_in_beams_devices_page.is_user_disappeared(normal_user.email_address),
                            "Assertion Error: '{}' still exists in the device group '{}'".format(normal_user.email_address, device_group_name))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user, device_group_admin])
            TestCondition.delete_device_groups([device_group_name])
            
        
    def test_c11616_remove_a_usergroup_from_a_device_group_2_x(self):
        """
        @author: Quang.Tran
        @date: 08/03/2016
        @summary: Remove a UserGroup from a Device Group [2.x]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            
            A device group admin account
        @steps:
            
            1. Login to Suitabletech.com and navigate to the "Manage Your Beams" advanced UI.  
            2. Select "Beams"
            3. Select a Device Group
            4. Select Members
            5. Next to each User Group icon is a remove button, select the remove button.
            6. A pop-up asks you to confirm your action 
                "Staging.suitabletech.com says: Are you sure you want to remove this user group from the "XYZ-Random" Device Group? 
            7. Upon Completion the User Group is removed from the Beams > Members User group list. 
                 
        @expected:
            Verify that the user group no longer has access to the device group by visually inspecting that it has been removed. 
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            new_device_group_name = Helper.generate_random_device_group_name()
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
            
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_user_group(user_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            admin_beams_members_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_members_tab_of_a_device_group(new_device_group_name)\
                .add_user_group_to_device_group(user_group_name)\
                .remove_user_group(user_group_name)
            
            # verify point
            self.assertFalse(admin_beams_members_page.is_user_group_existed(user_group_name),
                        "Assertion Error: Current Device Group admin user cannot delete the user group from current device group.")
            
            user_group_page = admin_beams_members_page.goto_users_tab().goto_user_group_detail_page(user_group_name)
            device_group_name = user_group_page.get_property(ApplicationConst.LBL_DEVICE_GROUPS_PROPERTY)
            self.assertNotEqual(device_group_name, new_device_group_name,
                "Assertion Error: User Group {} still has access to the device group {}.".format(device_group_name, new_device_group_name))
        finally:
            # clean up
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])

    
    @pytest.mark.OnlyDesktop
    def test_c11618_view_device_group_in_list_and_icon_viewing_mode(self): 
        """
        @author: Tham Nguyen
        @date: 7/29/2016
        @summary: View DeviceGroup in List and Icon Viewing Mode 
        @steps:
            
            1. Go to the "Beams" tab under "Manage your Beams" dashboard
            2. Select a device Group
            3. select Icon view of devices (icon top right)
            4. Select List view of devices (icon top right)
        @expected:
          Verify Beam/Devices are all visible in a usable manner:
            1. Size of Icons are correct (i.e. when changing from icon/list view, the image does not get distorted or improperly zoomed in/out)
            2. Text sizes (make sure that the text sizes shrink to what looks appropriate)
        """
        try:
            #pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            TestCondition.create_device_group(device_group_name, [beam_name])

            # steps
            device_group_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_device_group(device_group_name)

            list_view_size = device_group_page.switch_to_list_view()\
                .get_item_size_in_list_view(beam_name)
            icon_view_size = device_group_page.switch_to_icon_view()\
                .get_item_size_in_icon_view(beam_name)
            
            # verify point
            self.assertTrue(icon_view_size > list_view_size,
                            "Assertion Error: Unable to switch from icon view to list view.")
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name])


    def test_c11620_add_device_group_default_access_time(self): 
        """
        @author: Quang.Tran
        @date: 7/25/2016
        @summary: Add Device Group Default Access Time  
        @precondition: 
            Login to Manage Your Beams as a device group admin
        @steps:
            
            1. Go to the "Beams" tab under the "Manage your Beams" dashboard 
            2. Select a device group
            3. Select the "Access Times" Tab
            
            4. To Create new Device Group Access times for all members:
                - Select the "Add Access Time" button to the right of "Access Times for All Members"
                - Select each day that all group members will have access to the devices in this device group.
                - Toggle "Time Range" to select the window of time all group members will have access to the devices 
                or Toggle the option for "All day"
                - If each session requires authorization, check the " Require session answer" check box (Optional)
            5. Click on the "Create" button to complete the form
                 
        @expected:
            Verify the restriction of user access updates accordingly to the rule you created. 
        """
        try:
            # pre-condition
            new_device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
            
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Thu, WeekDays.Wed, WeekDays.Fri]
            
            TestCondition.create_device_group(new_device_group_name, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)
            
            # steps
            admin_beam_access_times_page = admin_dashboard_page.goto_beams_tab()\
                .select_device_group(new_device_group_name).goto_accesstimes_tab()
            
            # Toggle 'All day' button
            admin_beam_access_times_page.add_default_allday_access_times(access_days)
            
            # verify points
            expected_item_label = "{} {}, {}, {}, {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Thu"),
                                    ApplicationConst.get_date_time_label("Fri"))
            
            self.assertTrue(admin_beam_access_times_page.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_access_times_page.is_default_allday_access_time_displayed_on_calendar(access_days), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
            
            # Toggle 'Time range' button
            admin_beam_access_times_page.add_default_timerange_access_times(access_days, starting_datetime, ending_datetime)
            
            # verify points
            expected_item_label = "{} {}, {}, {}, {}, {}".format(
                                    Helper.generate_time_range_label(starting_datetime, ending_datetime),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Thu"),
                                    ApplicationConst.get_date_time_label("Fri"))
            self.assertTrue(admin_beam_access_times_page.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_access_times_page.is_default_timerange_access_time_displayed_on_calendar(access_days, starting_datetime, ending_datetime), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([admin_user])
            TestCondition.delete_device_groups([new_device_group_name])
            
            
    def test_c11621_edit_device_group_default_access_time(self): 
        """
        @author: Thanh Le
        @date: 8/10/2016
        @summary: Edit Device Group Default Access Time  
        @precondition: 
            Login to Manage Your Beams as a device group admin
        @steps:            
            1. Go to the "Beams" tab under the "Manage your Beams" dashboard 
            2. Select a device group
            3. Select the "Access Times" Tab
            
            4. To edit Device Group Access times for all members:
                - Select a Access Time Rule for all members to edit
                - Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day".
                - If each session requires authorization, check the " Require session answer" check box (Optional) 
            5. Click on the "Update" button to complete the form
                 
        @expected:
            Verify that the access time rule changes are saved accordingly. 
        """
        try:
            # pre-condition            
            device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = device_group_name
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
                    
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Thu, WeekDays.Wed, WeekDays.Fri]
            access_time_label = "{} {}, {}, {}, {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Thu"),
                                    ApplicationConst.get_date_time_label("Fri"))
            expected_item_label = "{} {}, {}, {}, {}, {}".format(
                                    Helper.generate_time_range_label(starting_datetime, ending_datetime),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Thu"),
                                    ApplicationConst.get_date_time_label("Fri"))
            
            TestCondition.create_device_group(device_group_name, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            admin_beam_access_times_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab().select_device_group(device_group_name).goto_accesstimes_tab()\
                .add_default_allday_access_times(access_days)\
                .edit_default_access_times(access_time_label, new_access_days=access_days, new_starting_datetime=starting_datetime, new_ending_datetime=ending_datetime)  

            # verify points
            self.assertTrue(admin_beam_access_times_page.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:            
                self.assertTrue(admin_beam_access_times_page.is_default_timerange_access_time_displayed_on_calendar(access_days, starting_datetime, ending_datetime), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
        finally:            
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([admin_user])
            TestCondition.delete_device_groups([device_group_name])
        
        
    def test_c11622_add_device_group_member_access_time(self):
        """
        @author: Duy Nguyen
        @date: 8/8/2016
        @summary: Add Device Group Member Access Time 
        @Precondtions:
            Note: to give access time to a contact, they must be a member of the device group.
        @steps:
            To Create new Device Group Member Access Times:
            1. Click the "Add Access Time" button to the right of the "Members" text
            2. Complete the Access Time form: --Select a member from the "Choose a member..." drop down menu 
                Select each day that all group members will have access to the devices in this device group.
                Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day"
                If each session requires authorization, check the " Require session answer" check box (Optional)
            3. Click on the "Create" button to complete the form.
        @expected:
            Verify that the access time rule changes are saved according
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Thu, WeekDays.Wed, WeekDays.Fri]
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            
            device_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_device_group(device_group_name)
            
            # step
            access_time_page = device_page.goto_accesstimes_tab()\
                .add_member_allday_access_times(normal_user, access_days)
            
            # verify point
            expected_item_label = "{} {}, {}, {}, {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Thu"),
                                    ApplicationConst.get_date_time_label("Fri"))
            self.assertTrue(access_time_page.is_member_access_time_label_displayed_on_sidebar(normal_user, expected_item_label), \
                            "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))

            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:   
                self.assertTrue(access_time_page.is_member_allday_access_time_displayed_on_calendar(normal_user, access_days), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
            
            access_time_page.add_member_timerange_access_times(normal_user, access_days, starting_datetime, ending_datetime)
            
            # verify point:
            expected_item_label = "{} {}, {}, {}, {}, {}".format(
                                    Helper.generate_time_range_label(starting_datetime, ending_datetime),
                                    ApplicationConst.get_date_time_label("Mon"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Wed"),
                                    ApplicationConst.get_date_time_label("Thu"),
                                    ApplicationConst.get_date_time_label("Fri"))
            self.assertTrue(access_time_page.is_member_access_time_label_displayed_on_sidebar(normal_user, expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
           
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:    
                self.assertTrue(access_time_page.is_member_timerange_access_time_displayed_on_calendar(normal_user, access_days, starting_datetime, ending_datetime), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
        finally:
            # post-condition
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([normal_user])
        
    
    def test_c11623_edit_a_device_group_member_access_time(self):
        """
        @author: Khoi Ngo
        @date: 8/8/2016
        @summary: Edit a Device Group Member Access Time
        @Precondtions: None
        @steps:
            To Edit a Device Group Member Access Time:
            1. Login as a Device Admin and navigate to the "Beams" tab in the "Manage your Beams" dashboard.
            2. Edit the form as needed
                - Select each day that all group members will have access to the devices in this device group.
                - Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day"
                - If each session requires authorization, check the " Require session answer" check box (Optional)
            3. Click on the "Update" button to complete the form
        @expected:
            Verify that the access time rule changes are saved according;
            For example uncheck all access boxes for Hans, update
            Then see the reflected access time changes in the time-line diagram
        """
        try:
            # precondition
            device_group_name = Helper.generate_random_device_group_name()
            
            normal_user = User()                                            
            normal_user.generate_advanced_normal_user_data()                              
            normal_user.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name)                    
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
            
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Thu, WeekDays.Wed, WeekDays.Fri]
            
            # steps
            access_time = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_device_group(device_group_name)\
                .goto_accesstimes_tab().add_member_timerange_access_times(normal_user, access_days, starting_datetime, ending_datetime)
            
            new_access_days = [WeekDays.Mon]
            user_access_time_label = Utilities.generate_access_time_label(access_days, starting_datetime, ending_datetime)
            access_time.edit_member_access_times(normal_user, user_access_time_label, new_access_days)
             
            # verify points
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(access_time.is_default_allday_access_time_displayed_on_calendar(new_access_days), \
                                "Assertion Error: The access times does not change in the calendar")
            access_days_label = Utilities.generate_access_time_label(new_access_days)
            self.assertTrue(access_time.is_member_access_time_label_displayed_on_sidebar(normal_user, access_days_label), "The access times does not change in the sidebar")
        finally:
            # post-condition
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([normal_user])


    def test_c11624_invite_a_temporary_user_and_give_temporary_access_time(self):
        """
        @author: Khoi Ngo
        @date: 8/10/2016
        @summary: Invite a Temporary User and give temporary access time
        @Precondtions: None
        @steps:
            1. Login as a Device Admin and navigate to the "Beams" tab in the "Manage your Beams" dashboard.
            2. Select a device group and then go to the "Access Times" tab.
            3. Click the "Invite a Temporary User" box.
            4. Fill out the corresponding form
                - Select each day that all group members will have access to the devices in this device group.
                - Toggle "Time Range" to select the window of time all group members will have access to the devices or Toggle the option for "All day"
                - If each session requires authorization, check the " Require session answer" check box (Optional)
            5. Then click the "Invite" box
        @expected:
            1. Verify that the temporary access time rule changes are saved according
            2. If the user is a new user, verify that the user receives an email with instructions to create an account.
        """
        try:
            # precondition
            from core.i18n.i18n_support import I18NSupport  
            tomorrow =  Helper.generate_access_day()
            device_group_name = Helper.generate_random_device_group_name()
            device_list = []
            beam_list = []
            for _ in range(2):
                beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beam_list.append(beam)
                device_list.append(beam.beam_name)
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name           
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)   
            
            tomorrow =  Helper.generate_access_day()
            access_day = WeekDays( tomorrow.isoweekday() )
            
            TestCondition.create_device_group(device_group_name,device_list)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin]) 

            # steps            
            access_time = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_access_times_tab_of_a_device_group(device_group_name)\
                .invite_temporary_user(normal_user, starting_datetime, ending_datetime, True)

            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                is_access_time_rule_created = access_time.is_temporary_time_range_access_time_displayed_on_calendar(normal_user, [access_day], starting_datetime, ending_datetime)
                self.assertTrue(is_access_time_rule_created, "Assertion Error: The access temporary time rule is not displayed.")

            date_label = I18NSupport.localize_date_time_string( re.sub(' +',' ',tomorrow.strftime('%b %e, %Y')) )
            access_time_label = Utilities.generate_temporary_access_time_label(date_label, starting_datetime, ending_datetime)
            self.assertTrue(access_time.is_member_access_time_label_displayed_on_sidebar(normal_user, access_time_label), 
                            "Temporary user {} does not display on sidebar with access time: start time is {} and end time is {}".format(normal_user.email_address, starting_datetime, ending_datetime))

            email = EmailDetailHelper.generate_welcome_temporary_user_email(normal_user, starting_datetime, ending_datetime, device_list,admin_full_name=device_group_admin.get_displayed_name())
            email_invite_arrive = GmailUtility.get_messages(
                    mail_subject=email.subject,
                    reply_to=device_group_admin.email_address,
                    receiver=normal_user.email_address,
                    sent_day=datetime.now())
            self.assertEqual(1, len(email_invite_arrive), "Assertion Error: The number of email return is not correct.")

            result = re.match(email.trimmed_text_content.upper(), email_invite_arrive[0].trimmed_text_content.upper(), re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(email.trimmed_text_content, email_invite_arrive[0].trimmed_text_content))
        finally:
            # post-condition
            for beam in beam_list:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([device_group_admin, normal_user])
            TestCondition.delete_device_groups([device_group_name])
            
            
    def test_c11625_edit_device_group_temporary_access_time(self):
        """
        @author: khoi ngo
        @date: 8/10/2016
        @summary: Edit Device Group Temporary Access Time(s)
        @steps:
            1. Click on the temp member's name or the access time below his/her name
            2) Edit the form as needed
                    Set the start Date and Time
                    Set the End Date and Time
                    If each session requires authorization, check the " Require session answer" check box (Optional)
            3) Select the "Update" button to complete the form
        @expected:
            Verify that the access temp time rule changes are saved according
        """
        from core.i18n.i18n_support import I18NSupport
        try:
            # precondition
            
            device_group_name = Helper.generate_random_device_group_name()
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name           
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)  
            tomorrow =  Helper.generate_access_day()
            access_day = WeekDays( tomorrow.isoweekday() ) 
            
            new_starting_datetime = Helper.generate_date_time(hour_delta=7)
            new_ending_datetime = Helper.generate_date_time(hour_delta=16, minute_delta=30)  
            
            date_label = I18NSupport.localize_date_time_string( re.sub(' +',' ',tomorrow.strftime('%b %e, %Y')) )
            
            TestCondition.create_advanced_temporary_user(self._driver, normal_user, device_group_name, starting_datetime, ending_datetime, answer_required=False, activate_user = True)

            # steps
            access_time = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_access_times_tab_of_a_device_group(device_group_name)
            
            access_time_label = Utilities.generate_temporary_access_time_label(date_label, starting_datetime, ending_datetime)
            access_time.edit_temporary_access_times(normal_user, access_time_label, new_starting_datetime, new_ending_datetime, True)

            # verify points
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                is_access_time_rule_changed = access_time.is_temporary_time_range_access_time_displayed_on_calendar(normal_user, [access_day], new_starting_datetime, new_ending_datetime)
                self.assertTrue(is_access_time_rule_changed, "Assertion Error: The access temporary time rule is not changed")

            access_time_label = Utilities.generate_temporary_access_time_label(date_label, new_starting_datetime, new_ending_datetime)
            self.assertTrue(access_time.is_member_access_time_label_displayed_on_sidebar(normal_user, access_time_label), 
                            "Temporary user {} does not display on sidebar with access time: start time is {} and end time is {}".format(normal_user.email_address, new_starting_datetime, new_ending_datetime))
            
            email_invite_arrive = EmailDetailHelper.generate_access_time_has_changed_email(device_group_name, device_group_admin.get_displayed_name(), new_starting_datetime, new_ending_datetime)
            
            actual_email = GmailUtility.get_messages(email_invite_arrive.subject, receiver = normal_user.email_address)
            
            self.assertEqual(len(actual_email), 1, "Assertion Error: The number of email return is not correct")
            
            # TODO: This test case failed due to bug INFR-2436
            self.assertEqual(actual_email[0].trimmed_text_content, email_invite_arrive.trimmed_text_content, "Assertion Error: The content email is not correct. Expected:\n'{}' but found:\n'{}'".format(email_invite_arrive.trimmed_text_content, actual_email[0].trimmed_text_content))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([device_group_admin, normal_user])
            TestCondition.delete_device_groups([device_group_name])


    def test_c34084_hide_and_unhide_device_group_access_time_event_on_calendar(self):
        """
        @author: Quang Tran
        @date: 7/25/2018
        @summary: Hide and unhide Device Group Access Time event on calendar
        @precondition: Create a device group 
            Invite a normal user and temp user into the device group
            Set access time for the normal user
        @steps:
            1.Login as admin
            2.Go to Access Time tab of the device group
            3.Un-check default access
            4.Un-check access time of the normal user
            5.Un-check access time of temp user
            6.Check 3 access time above
        @expected:
            (3)(4)(5) Events disappear on the calendar
            (6) Events display on the calendar
        """
        try: 
            #pre-condition
            tomorrow =  Helper.generate_access_day()
            access_day_temp = WeekDays(tomorrow.isoweekday())
            
            access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Wed, WeekDays.Fri, WeekDays.Sat, WeekDays.Sun]

            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group)
    
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group 
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
    
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)
            temp_user = User()
            temp_user.generate_advanced_normal_user_data()
            temp_user.device_groups = device_group
            TestCondition.create_advanced_temporary_user(self._driver, temp_user, device_group, starting_datetime, ending_datetime)
    
            #steps
            access_time_page = LoginPage(self._driver).open()\
                    .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                    .goto_beams_tab()\
                    .select_device_group(device_group)\
                    .goto_accesstimes_tab()\
                    .add_member_allday_access_times(normal_user, access_days)\
                    .toggle_show_accesstime(False, False, False)
 
            #verify point
            self.assertFalse(access_time_page.is_default_allday_access_time_displayed_on_calendar(access_days),\
                             "Events All day every day still display on calendar")
            self.assertFalse(access_time_page.is_member_allday_access_time_displayed_on_calendar(normal_user, access_days),\
                             "Events of normal user still display on calendar")
            self.assertFalse(access_time_page.is_temporary_time_range_access_time_displayed_on_calendar(temp_user, [access_day_temp], starting_datetime, ending_datetime),\
                             "Events of temp user still display on calendar")
 
            access_time_page = access_time_page.toggle_show_accesstime()
 
            #verify point
            self.assertTrue(access_time_page.is_default_allday_access_time_displayed_on_calendar(access_days),\
                             "Events All day every day do not display on calendar")
            self.assertTrue(access_time_page.is_member_allday_access_time_displayed_on_calendar(normal_user, access_days),\
                             "Events of normal user do not still display on calendar")
            self.assertTrue(access_time_page.is_temporary_time_range_access_time_displayed_on_calendar(temp_user, [access_day_temp], starting_datetime, ending_datetime),\
                             "Events of temp user do not still display on calendar")

            access_time_page = access_time_page\
                    .toggle_accesstime_all_day(False)\
                    .toggle_accesstime_of_user(normal_user.get_displayed_name(), False)\
                    .toggle_accesstime_of_user(temp_user.email_address, False)

            #verify point
            self.assertFalse(access_time_page.is_default_allday_access_time_displayed_on_calendar(access_days),\
                             "Events All day every day still display on calendar")
            self.assertFalse(access_time_page.is_member_allday_access_time_displayed_on_calendar(normal_user, access_days),\
                             "Events of normal user still display on calendar")
            self.assertFalse(access_time_page.is_temporary_time_range_access_time_displayed_on_calendar(temp_user, [access_days], starting_datetime, ending_datetime),\
                             "Events of temp user still display on calendar")
        finally:
            TestCondition.delete_advanced_users([temp_user, normal_user])
            TestCondition.delete_device_groups([device_group])

