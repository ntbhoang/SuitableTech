from common.constant import Constant, Platform
from common.helper import Helper
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from common.application_constants import ApplicationConst
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.suitabletechapis.user_api import UserAPI
import pytest


class DeviceGroupAdmin_Test(TestBase):
    
    def test_c11227_grant_administrators_for_a_specific_device_group_2_X(self):
        """
        @author: Duy.Nguyen
        @date: 7/27/2016
        @summary: Grant Administrators for a specific device group [2.X]
        @precondition: 
        Use a Device Group admin account (cannot be an org admin account). Device group admins can be assigned by going to "manage your beams", beams, settings, administrators. 
        @steps:        
            1) Go to the "Manage your Beams" dashboard and click on the "Beams" tab
            2) select a device group
            3) Go to the "Settings" Tab
            4) Click the "add administrators" button to add users as administrators of the device group
            5) Click the save changes button at the top
            
        @expected:
            Login with the device group admin account and verify that the user account that was promoted is now able to adminster the new device group by checking the "adminstrates group" string in their user profile.         
            Verify that the newly added device group admin can invite other users to the device group they have been assigned to manage.
        """
        try:
            # precondition:
            device_group_name = Helper.generate_random_device_group_name()
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            
            sub_user = User()
            sub_user.generate_advanced_normal_user_data()
            sub_user.device_group = device_group_name
            sub_user.invitation_settings.include_the_default_invitation_message = None
            
            TestCondition.create_device_group(device_group_admin.device_group)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
             
            # steps:
            user_detail_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)\
                .add_administrator(normal_user)\
                .goto_users_tab().goto_user_detail_page(normal_user)
            
            # verify point:
            self.assertEqual(user_detail_page.get_user_administers_groups(), [device_group_name], "Assertion Error: The Administers Group information is not correct")
            
            user_detail_page = user_detail_page\
                .logout_and_login_again(normal_user.email_address, normal_user.password)\
                .invite_new_user(sub_user)\
                .goto_users_tab().goto_user_detail_page(sub_user)
            
            # verify point:
            self.assertEqual(user_detail_page.get_device_groups(), [device_group_name], "Assertion Error: The Device Groups information is not correct")
            
        finally:
            TestCondition.delete_advanced_users([device_group_admin, normal_user, sub_user])
            TestCondition.delete_device_groups([device_group_name])
        
    
    def test_c11591_device_group_admin_add_an_existing_user_as_another_device_group_admin_2_x(self):
        """
        @author: Duy.Nguyen
        @date: 8/3/2016
        @summary: Device Group Admin add an existing user as another Device Group Admin [2.X]
        @precondition: 
            Add UserA as device group admin of DeviceGroupA
            Add a Suitabletech User (UserB)
        @steps:    
            1) Login to Suitabletech.com as a device group admin (DeviceGroupAdminA) and select "Manage Your Beams" from the user dropdown menu
            2) Click on the "Beams" tab under the "Manage your Beams" dashboard
            3) Select a device group (DeviceGroupA) and select "Settings" tab
            4) Under the "Administrators" title in the "Settings" tab, click on the "Add Administrators" box and select one of the existing users in the organization (UserB) then click "Add Selected Users" button
            5) Click the blue button "Save Changes" towards the top-left side of the browser
            6) Go to the "Users" tab under the "Manage your Beams" dashboard
            7) Click on the desired user that you are checking device admin privileges (UserB)
        @expected:
            (5) Verify that a green popup occurs in the top right saying the "Changes were saved successfully". 
            (7). Verify that the selected usergroup (UserGroupB) is displayed in "Administrates Groups" field of UserB's detail page. 
        """        
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = device_group_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps:
            beam_setting_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)\
                .add_administrator(normal_user, False)
            
            # verify point:
            actual_msg_success = beam_setting_page.get_msg_success()
            
            self.assertEqual(ApplicationConst.INFO_MSG_SAVE_DEVICE_GROUP_SETTING_SUCCESSFUL, actual_msg_success,
                             "Assertion Error: There is no message with following content display")
            
            user_detail_page = beam_setting_page.goto_users_tab().goto_user_detail_page(normal_user)
            
            # verify point:
            self.assertEqual(user_detail_page.get_user_administers_groups(), [admin_user.device_group],
                              "Assertion Error: The Administers Group information is not correct")
            
        finally:
            TestCondition.delete_advanced_users([admin_user, normal_user])
            TestCondition.delete_device_groups([device_group_name])
            
    
    def test_c11593_device_group_admin_remove_self_from_admin_2_x(self):
        """
        @author: tham.nguyen
        @date: 7/25/2016
        @summary: Device Group Admin remove self from admin [2.X]
        @precondition: Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            A device group admin account.
        @steps:        
            1) Login to suitabletech.com and navigate to the "Manage your Beams" dashboard and go to the "Beams" Tab
            2) Then click on a "Device Group" and go to the "Settings" Tab
            3) Go to the "Administrators" box and try to remove yourself
             
        @expected:
            1) The "x" button (shown in pic above) is missing for your own user-ID in device group settings.
        """  
        try:
            # pre-conditions:
            organization_name = Constant.AdvancedOrgName
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name, [beam_name], organization_name)
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            
            TestCondition.create_advanced_device_group_admins(driver=self._driver, user_array=[device_group_admin])
            
            # steps
            admin_beams_settings_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
            
            # verify points
            self.assertFalse(admin_beams_settings_page.is_admin_removable(UserAPI.get_displayed_name(device_group_admin)), "Assertion Error: The device group admin '{}' can remove himself in admin beams setting page.".format(device_group_admin.get_displayed_name()))
        
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users(user_array=[device_group_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)


    def test_c11590_device_group_admin_for_multiple_orgs_sees_a_drop_down_list_to_select_site_1_x(self):
        """
        @author: Quang Tran
        @date: 7/29/2016
        @summary: Device Group Admin for multiple Orgs sees a drop-down list to select site [1.X]
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            
            1) You will need admin access to two or more device groups in two different orgs

        @steps:        
            1) Use a Device Group admin account (cannot be an org admin account)
            2) Go to the "Manage your Beams" dashboard
            3) In the upper right section of the admin page, you should see the organization name.
            4) Toggle the org name to a different organization 
             
        @expected:
            It turns into a drop down menu that allows you to change orgs;
            The web page should be directed to the new org when a different selection is made.
        """
        try:
            # precondition: create a new Device Group admin account
            device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()                            
            device_group_admin.generate_advanced_device_group_admin_data()
            TestCondition.create_advanced_device_group_admin_on_multi_organization(self._driver, device_group_admin,device_group_name)
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)
            
            # verify points
            does_dropdown_contain_multi_orgs = admin_dashboard_page.does_dropdown_contain_multi_orgs()
            self.assertTrue(does_dropdown_contain_multi_orgs,
                            "Assertion Error: Organization dropdown list is not displayed")
            
            page_title = admin_dashboard_page.goto_another_org(Constant.AdvancedOrgName)\
                .goto_another_org(Constant.AdvancedOrgName_2).get_page_title()
            
            # verify points
            is_page_displayed = Constant.AdvancedOrgName_2 in page_title
            self.assertTrue(is_page_displayed, "Assertion Error: Admin page is not switched to selected organization")
        finally:
            # postcondition
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_advanced_users([device_group_admin], Constant.AdvancedOrgName_2)
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_device_groups([device_group_name], Constant.AdvancedOrgName_2)
        
        
    def test_c11628_change_usergroup_icon_2_x(self):    
        """
        @author: Quang Tran
        @date: 8/18/2016
        @summary: Change UserGroup Icon [2.X] 
        @precondition:
            Login to Suitabletech.com and navigate to the Manage Your Beams dashboard with a Device Group Admin user account

        @steps:        
            1) Go to the "Users" tab under the "Manage your Beams" dashboard
            2) Select a user group
             
        @expected:
            Verify that the change image button is disabled for not allowing device group admin changing icon image.
        """
        
        try:
            # precondition
            user_group_name = Helper.generate_random_user_group_name()
            device_group_name = Helper.generate_random_device_group_name()                          
            device_group_admin = User()                                            
            device_group_admin.generate_advanced_device_group_admin_data()                                
            device_group_admin.device_group = device_group_name                        
                                                        
            TestCondition.create_device_group(device_group_name)                    
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            TestCondition.create_user_group(user_group_name)

            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)         
            
            # steps
            user_group_detail_page = admin_dashboard_page.goto_users_tab()\
                .goto_user_group_detail_page(user_group_name)
            
            # verify point: compare images by pixels
            is_change_icon_link_visible = user_group_detail_page.is_change_icon_link_displayed()
            self.assertFalse(is_change_icon_link_visible, "Assertion Error: The Device Group Admin can see the 'change icon' link.")
        finally:
            # clean up
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_user_groups([user_group_name])


    def test_c33874_device_group_admin_cannot_see_add_a_beam_or_add_devices_button(self):
        """
        @author: Khoi Ngo
        @date: 9/27/2017
        @summary: Verify that Device Group Admin cannot see Add a Beam or Add Devices button.
        @precondition:
            - Create device group hasn't device.
            - Add device group admin for device group
        @steps:
            1) Login as device group admin
            2) Go to Dashboard page
            3) Go to Beams page
            4) Select device group
        @expected:
            (2). Add a Beam button doesn't display
            (3). Add Devices button doesn't display
            (4). Add Devices button doesn't display
        """

        try:
            # precondition
            device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name

            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)
            self.assertFalse(admin_dashboard_page.is_add_a_beam_button_display(), "Add a Beam button still displays")

            admin_beam_page = admin_dashboard_page.goto_beams_tab()
            self.assertFalse(admin_beam_page.is_add_devices_button_display(), "Add Devices button still displays")

            admin_beam_device_page = admin_beam_page.select_device_group(device_group_name)
            self.assertFalse(admin_beam_device_page.is_add_devices_button_display(), "Add Devices button still displays")
        finally:
            # clean up
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group_name])


    @pytest.mark.OnlyDesktop
    def test_c33899_help_modal_displays_when_clicking_on_help_link_on_members_access_times_and_reservations_tab(self):
        """
        @author: Khoi Ngo
        @date: 10/13/2017
        @summary: Verify that Help modal displays when clicking on Help link on Members, Access Times, and Reservations tab
        @precondition:
            - Create device group admin
            - Create a device group
        @steps:
            1. Login as device group admin
            2. Select a device group
            3. Open Members tab, then click Help link
            4. Open Access Times tab, then click Help link
            5. Open Reservations tab, then click Help link
        @expected:
            (3), (4) and (5) Help modal displays.
        """

        try:
            # precondition
            device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name

            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            # steps
            member_tab = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab()\
                .select_device_group(device_group_name)\
                .goto_members_tab()\
                .open_help_dialog()
            
            self.assertTrue(member_tab.is_dialog_displayed(), "Help modal doesn't display")

            access_time_tab = member_tab.close_help_dialog()\
                .goto_accesstimes_tab()\
                .open_help_dialog()
            self.assertTrue(access_time_tab.is_dialog_displayed(), "Help modal doesn't display")

            reservations_tab = member_tab.close_help_dialog()\
                .goto_reservations_tab()\
                .open_help_dialog()
            self.assertTrue(reservations_tab.is_dialog_displayed(), "Help modal doesn't display")
        finally:
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group_name])


    def test_c33921_device_group_admin_can_see_beam_at_group_which_he_is_a_member(self):
        """
        @author: Khoi Ngo
        @date: 10/24/2017
        @summary: Verify that Device Group Admin can see Beam at group which he is a member
        @precondition:
            - Create two device groups (G1,G2) have one beam at each group
            - Create a device group admin is admin at G1 and belongs to G2
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as device group admin
            2. Go to Beams page
        @expected:
            (2) Admin can see Beam at both device groups
        """

        try:
            # precondition
            device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name

            device_group_name_2 = Helper.generate_random_device_group_name()
            beam_2 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name_2 = beam_2.beam_name

            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name

            TestCondition.create_device_group(device_group_name,[beam_name])
            TestCondition.create_device_group(device_group_name_2,[beam_name_2])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_device_group(device_group_name_2)\
                .goto_members_tab()\
                .add_user_to_device_group(device_group_admin)\
                .logout()

            # steps
            admin_devices_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab()
            self.assertTrue(admin_devices_page.is_device_displayed(beam_name), "Admin can't see Beam at group which he is a device group admin")
            # TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2530"
            self.assertTrue(admin_devices_page.is_device_displayed(beam_name_2), "Admin can't see Beam at group which he is a member")
        finally:
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group_name, device_group_name_2])
            TestCondition.release_a_beam(beam)
            TestCondition.release_a_beam(beam_2)


    def test_c33922_device_group_admin_add_user_into_session_answer_successfully_2_x(self):
        """
        @author: Khoi Ngo
        @date: 10/25/2017
        @summary: Verify that Device Group Admin can add user into Session answer successfully
        @precondition:
            Have a device group admin account.
            Have a normal user account.
            Have a device group.
        @steps:
            1. Login as Device Group Admin
            2. Navigate manage Beam page
            3. Select the device group
            4. Go to Setting tab
            5. Add user into Session Answer
        @expected:
            (5):
                Verify message success displayed
                The user displayed in Session Answer
        """
        from core.suitabletechapis.device_group_api import DeviceGroupAPI
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)

            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])

            # steps
            setting_tab_device_group = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab()\
                .select_device_group(device_group_name)\
                .goto_setting_tab()\
                .add_user_to_session_answer(normal_user, wait_for_completed=False)

            # verify point
            mgs_success = setting_tab_device_group.is_success_msg_displayed()
            self.assertTrue(mgs_success, "Message success is not displayed")

            self.assertTrue(setting_tab_device_group.is_user_displayed_in_session_answer(normal_user.get_displayed_name()), \
                            "User is added not displayed in Session Answer")

            list_anser_users = DeviceGroupAPI.get_list_answer_request_users(device_group_name)
            self.assertTrue(normal_user.email_address in list_anser_users, \
                            "User not added into Session Answer")

        finally:
            TestCondition.delete_advanced_users([normal_user, device_group_admin])
            TestCondition.delete_device_groups([device_group_name])


    def test_c33941_device_group_admin_is_able_to_sort_devices_2_x(self):
            """
            @author: Khoi Ngo
            @date: 11/02/2017
            @summary: Device group admin is able to sort devices
            @precondition:
                Have a device group admin account
                Device group has some beams
            @steps:
                1. Login as device group admin
                2. Go to Beams tab
                3. Click Name, Device Group, Location, Status, Last Used label on table of devices
            @expected:
                (3) Verify table of devices is sorted by Name, Device Group, Location, Status, Last Used
            """
            try:
                #pre-condition
                beam1 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beam_name1 = beam1.beam_name
                beam2 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beam_name2 = beam2.beam_name
                beam3 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beam_name3 = beam3.beam_name

                device_group_name = Helper.generate_random_device_group_name()
                TestCondition.create_device_group(device_group_name, [beam_name1, beam_name2, beam_name3])

                device_group_admin = User()
                device_group_admin.generate_advanced_device_group_admin_data()
                device_group_admin.device_group = device_group_name
                TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

                # steps sort with icon view
                beams_page = LoginPage(self._driver).open()\
                    .login(device_group_admin.email_address, device_group_admin.password)\
                    .goto_beams_tab()

                # verify point
                self.assertTrue(beams_page.check_sort_by_work_correctly(), "Device group admin cannot sort Beams icon in Beams tab")

                # steps sort with list view
                if self._driver.driverSetting.platform == Platform.WINDOWS or self._driver.driverSetting.platform == Platform.MAC:
                    beam_list_view = beams_page.switch_to_list_view()

                #verify point
                    self.assertTrue(beam_list_view.check_table_devices_can_sort(), "Device group admin can not sort devices in Beams tab")

            finally:
                TestCondition.release_a_beam(beam1)
                TestCondition.release_a_beam(beam2)
                TestCondition.release_a_beam(beam3)
                TestCondition.delete_device_groups([device_group_name])
                TestCondition.delete_advanced_users([device_group_admin])

