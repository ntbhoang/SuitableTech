from common.constant import Constant
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase


class DeviceGroupAdminTest(TestBase):
    
    def test_c11644_grant_administrators_for_a_specific_device_group_2_x(self):
        """
        @author: Thanh.Le
        @date: 8/02/2016
        @summary: Grant Administrators for a specific device group [2.X]
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Ref: NCA-5808 - Site Admin needs new, intermediate user roles implemented

            To get into Simplified Admin Mode: 
            1) Make sure that your organization only has Beam+'s
            2) Refresh the browser page, you may need to switch orgs and come back in order for the full "Manage your Beams" to fully refresh            
            Make sure to login as a Device Group Admin, not an Org Admin
            
            To make a "Device Admin" ~ "Device Group Admin" in simplified "Manage your Beams"
            1) Log onto the simplified "Manage your Beams" as an org admin            
            2) Click the "Manage" button below each of the Beam+'s you want another user to manage            
            3) If the user is not already invited (i.e. listed at bottom of page), fill out the "Invite a person to use this Beam" field            
            5) Verify that the new user gets added    
            --> inform message + new record        
            --> email confirmation            
            5) Then check the "Can Manage" box
            6) logout the org admin
        @steps
            1) Go to the simplified "Manage your Beams" dashboard and login as the recently added device admin
            2) Click the "Manage" button below each of the Beam+'s you want another user to manage
            3) If the user is not already invited (i.e. listed at bottom of page), fill out the "Invite a person to use this Beam" field
            4) Then check the "Can Manage" box
            
            --> These are the same instructions as above except now you are using a "device" admin. An Org admin can only invite you to "manage" new devices, but once you are managing a device you can invite other users to said device.

        @expected result:
            Precondition: 
            - verify that the device admin can manage all of the beam+'s that the org admin allowed privileges for; 
            - verify that the device admin can only see the beam+'s that the org admin gave priviledges for
            Test case: verify that the device admin can:
            1. invite new users to the beam+ device
            2. can add new device admins (i.e. can check the "Can Manage" box)
        """
        try:
            # preconditions:
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            beam_name = beam.beam_name
            
            test_device_admin = User()  
            test_device_admin.generate_simplified_normal_user_data()
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)
            
            # steps
            simplified_dashboard_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
            
            self.assertTrue(simplified_dashboard_page.can_manage_device(beam.beam_id),
                    "Assertion Error: The current device admin is not allowed to manage the beam '{}'".format(beam_name))
            
            self.assertEqual(simplified_dashboard_page.get_number_of_devices_displayed(), 1,
                    "Assertion Error: The current device admin can see the beam+'s that the org admin does not gave priviledges for.")
            
                
            simplified_beam_detail_page = simplified_dashboard_page.goto_manage_beam_page(beam.beam_id).add_user(test_device_admin)
            
            # verify point
            self.assertTrue(simplified_beam_detail_page.is_user_added(test_device_admin),
                    "Assertion Error: The current device admin cannot invite new user to the device {}".format(beam_name))                                

            simplified_beam_detail_page.set_user_can_manage(test_device_admin)
                    
            # verify point
            self.assertTrue(simplified_beam_detail_page.is_user_can_manage_checkbox_selected(test_device_admin),
                    "Assertion Error: The current device admin cannot grant administrator for other user.")
            
        finally:        
            # clean-up
            TestCondition.delete_simplified_users([test_device_admin, simplified_dev_admin])
                  
      
    def test_c11645_device_group_admin_for_multiple_orgs_sees_a_drop_down_list_to_select_site_1_x(self):
        """
        @author: Thanh.Le
        @date: 8/02/2016
        @summary: Device Group Admin for multiple Orgs sees a drop-down list to select site [1.X]
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs

            1) Need to have an account that has access to two different orgs
            2) one of the orgs the account needs to be a "device admin" in the simplified "Manage your Beams" dashboard (has a can manage checkbox next to user profile). 
            3) In the other org the account needs to be a "device group admin" in the full "Manage your Beams".
        @steps
            1) Login as a device admin in the simplified "Manage your Beams"
            2) In the upper right hand corner of the screen with the org name, if you have access to more than one org (see preconditions), a drop down menu will appear

        @expected Result
            1) Verify that if a "device admin" in the simplified "Manage your Beams" dashboard has access to more than one org, the dropdown menu appears.
        """
        try:
            # steps
            simplified_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_another_org(Constant.SimplifiedOrgName)
                  
            # verify point
            self.assertTrue(simplified_dashboard_page.is_organization_dropdown_displayed(),
                            "Assertion Error: Organization dropdown is NOT displayed")
        finally:
            pass        
    
      
    def test_c11647_device_group_admin_removes_an_existing_device_group_admin_2_x(self):
        """
        @author: khoi.ngo
        @date: 8/4/2016
        @summary: Device Group Admin Removes an existing Device Group Admin [2.X]
        @precondition:
            Follow the steps from the previous test case to set up 2 device group admins
        @steps:
            1. Login to the simplified "Manage your Beams" as a device admin 
            2. click the "manage" box under the device image icon
            3. UNCHECK the box next to the desired user under the "Can manage" field
            4. click "Remove Person" button.
            5. Verify removal toast
            
        @expected:
            the unchecked user is no longer a device admin (i.e. "can't manage")
        """
        try:
            # precondition
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_and_lock_beam(test_organization)
            beam_name = beam.beam_name
            
            removed_device_admin = User()  
            removed_device_admin.generate_simplified_normal_user_data()
            removed_device_admin.device_group = beam_name
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin, removed_device_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)

            # steps
            simplied_dashboard_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)\
                    .set_user_can_manage(removed_device_admin, False)\
                    .remove_user(removed_device_admin)
                
            # verify point
            self.assertFalse(simplied_dashboard_page.is_user_added(removed_device_admin),
                    "Assertion Error: User still exists in this device.")
            
            home_page = simplied_dashboard_page.logout().goto_login_page()\
                .login(removed_device_admin.email_address, removed_device_admin.password, True)
            
            self.assertFalse(home_page.can_manage_device(beam.beam_id),
                    "Assertion Error: The removed admin user still be able to manage the device.")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)      
            TestCondition.delete_simplified_users([simplified_dev_admin])
        
       
    def test_c11648_device_group_admin_cannot_remove_self_from_admin_2_x(self):
        """
        @author: Thanh.Le
        @date: 8/02/2016
        @summary: Device Group Admin cannot remove self from admin [2.X]
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1) Login as a device admin in simplified "Manage your Beams"
            2) Click the "Manage" button under the device image icon
        @expected:
            1) Verify that a grey "no-symbol" icon blocks you from the "Can't Manage" box
        """
        try:
            # preconditions
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            beam_name = beam.beam_name
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)
            
            # steps
            simplified_beam_detail_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)       
            
            # verify point
            self.assertTrue(simplified_beam_detail_page.is_user_can_manage_checkbox_disabled(simplified_dev_admin),
                            "Assertion Error: User checkbox is NOT disabled!")
            
        finally:
            TestCondition.delete_simplified_users([simplified_dev_admin])


    def test_c33910_device_group_admin_cannot_see_add_a_beam_button(self):
        """
        @author: Khoi Ngo
        @date: 10/19/2017
        @summary: Device Group Admin cannot see Add a Beam button
        @preconditions:
            Create a device group admin
        @steps:
            1. Login as device group admin
            2. Notice the Add a Beam button displays or not
        @expected:
            (2) Add a Beam button doesn't display
        """
        try:
            # preconditions
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name

            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name

            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)
            # steps
            simpplified_dashboard_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, simplifiedUser=True)

            # verify point
            self.assertFalse(simpplified_dashboard_page.is_add_a_beam_button_display(),
                            "Add a Beam button still displays")
        finally:
            TestCondition.delete_simplified_users([simplified_dev_admin])


    def test_c33911_delete_this_user_button_doesnt_display_for_device_group_admin(self):
        """
        @author: Khoi Ngo
        @date: 10/19/2017
        @summary: 'Delete This User' button doesn't display for device group admin
        @preconditions:
            Create a device group admin
        @steps:
            1. Login as device group admin
            2. Go to Beam manage of a Beam
            3. Add a new user
            4. Go to new user details page
        @expected:
            (4) 'Delete This User' button doesn't display.
        """
        try:
            # preconditions
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name

            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name

            normal_user = User()
            normal_user.generate_simplified_normal_user_data()
            normal_user.device_group = beam_name

            TestCondition.create_simplified_device_admin(self._driver, [simplified_dev_admin], beam)
            # steps
            simpplified_dashboard_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, simplifiedUser=True)\
                .goto_manage_beam_page(beam.beam_id)\
                .add_user(normal_user)\
                .goto_simplified_user_detail_page(normal_user)

            # verify point
            self.assertFalse(simpplified_dashboard_page.is_delete_user_button_display(),
                            "Delete This User button still displays")
        finally:
            TestCondition.delete_simplified_users([simplified_dev_admin, normal_user])


    def test_c33916_user_can_see_all_beams_which_he_is_a_member_and_device_admin(self):
        """
        @author: Khoi Ngo
        @date: 10/24/2017
        @summary: Device Group Admin can view beams on dashboard page that have manage permission one of them
        @preconditions:
            Have a normal user account.
            Have a org admin account.
        @steps:
            1. Login as org admin into Simplified org.
            2. Add a user in precondition into a beam.
            3. Set manage permission for a user.
            4. Continue to add a user in precondition into another beam.
            5. Logout device group admin.
            6. Login with a user account in precondition.
        @expected:
            (6) A User can view beams that is membership on the dashboard page.
        """
        try:
            # pre-condition
            beam1 = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            beam_name1 = beam1.beam_name
            beam2 = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            beam_name2 = beam2.beam_name

            normal_user = User()
            normal_user.generate_simplified_normal_user_data()

            # steps
            dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                .add_user(normal_user, beam_name1)\

            TestCondition._activate_user_temporary_password(self._driver, normal_user, localize=True)    

            dashboard_page = dashboard_page.add_user(normal_user, beam_name2, wait_user_display=True)\
                .goto_manage_beam_page(beam1.beam_id)\
                .set_user_can_manage(normal_user)\
                .logout().goto_login_page()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)

            # verify point
            #TODO: This test case faild due to bug "https://jira.suitabletech.com/browse/INFR-2530"
            self.assertTrue(dashboard_page.is_beam_displayed(beam_name1), "{} user have manage permission do not display on dashboard page".format(beam_name1))
            self.assertTrue(dashboard_page.is_beam_displayed(beam_name2), "{} do not display on dashboard page".format(beam_name2))

        finally:
            TestCondition.delete_simplified_users([normal_user])
            TestCondition.release_a_beam(beam1)
            TestCondition.release_a_beam(beam2)
