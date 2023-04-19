from common.constant import Constant
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
        
        
class NonAdminUserLoginManagementWebAppAccountHomePgView_Test(TestBase):
        
    def test_c11348_non_admin_user_beam_account_home_get_help(self):
        """
        @author: Thanh Le
        @date: 08/15/2016
        @summary: Non-Admin User Beam Account Home - Get Help
        @precondition:           
            1) Login to Suitabletech with the Simplified Org Admin account
            2) On Manage Your Beams page, enter user's email address which would like to invite and select "Add User" button
            3) Go to mailbox of this user and active it and login to Suitabletech site
            4) Complete see video.            
        @steps:
            1) Select on drop-down menu "Account Settings > Home"
            2) Click the "Get Help" button        
        @expected:          
            2) Verify that you get a new tab created with "Beam Help Center" page
        """
        try:
            # pre-condition
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()
            normal_user.device_group = beam_name
            
            # steps
            simplified_dashboard = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam.beam_id)\
                    .create_completed_simplified_normal_user(normal_user)\
                .goto_login_page()\
                    .login_as_unwatched_video_user(normal_user.email_address, normal_user.password)\
                .watch_video(normal_user, simplified=True)\
                
            # steps
            is_page_displayed = simplified_dashboard.open_beam_help_center_page().is_page_displayed()
            self._driver.switch_to_main_window()
        
            # verify points
            self.assertTrue(is_page_displayed, "Assert Error: Beam Help Center page is not displayed!")
            
        finally:
            # post-condition            
            TestCondition.delete_simplified_users([normal_user], normal_user.organization)
            

    def test_c11349_non_admin_user_simplified_dashboard_cannot_see_add_a_beam_button(self):
        """
        @author: Thanh Le
        @date: 08/15/2016
        @summary: Non-Admin User Beam Account Home - Add a Beam
        @precondition:           
            1) Login to Suitabletech with the Simplified Org Admin account
            2) On Manage Your Beams page, enter user's email address which would like to invite and select "Add User" button
            3) Go to mailbox of this user and active it and login to Suitabletech site
            4) Complete see video.            
        @steps:
            1) Select on drop-down menu "Account Settings > Home"
        @expected:
            1) Verify that Add a Beam button doesn't display            
        """
        try:
            # pre-condition
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()
            normal_user.device_group = beam_name
            
            simplified_dashboard = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam.beam_id)\
                    .create_completed_simplified_normal_user(normal_user)\
                .goto_login_page()\
                    .login_as_unwatched_video_user(normal_user.email_address, normal_user.password)\
                .watch_video(normal_user, simplified=True)
                
            # verify points   
            self.assertFalse(simplified_dashboard._lnkAddABeam.is_displayed(), 'Non-Admin User is able to see Add a Beam link')
            
        finally:
            # post-condition      
            TestCondition.delete_simplified_users([normal_user])
            
        
    def test_c11387_non_admin_user_beam_account_home_available_beams_view(self):
        """
        @author: Duy Nguyen
        @date: 08/18/2016
        @summary: Non-Admin User Beam Account Home - Available Beams View
        @precondition:           
            Use the following Test users and Organizations - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestUserAccounts
            
            FYI: Non Admin login account Home page will be moved to management App Page as follows:
            New redirected URL: https://staging.suitabletech.com/manage/#/home/
            Old redirected URL: https://staging.suitabletech.com/accounts/home/#
            
            Create a device group (DeviceGroupA) and add a device to this group (Beam1)
            Create a normal user (UserA)         
        @steps:
            1) Login to Suitable tech site with normal user credentials in pre-condition (UserA)
            2) Select "Account Settings > Home" from drop-down menu  
        @expected:
            (2) 
            _Verify the url is redirected to "https://staging.suitabletech.com/manage/#/home/"
            _Verify that all Beam(s) accessible to that non-Admin User within the Device Group they were added as a member are listed with the following properties:
            Name : <Beam Name>
            Location : <text string>
            Labels : <text string>
            Time Zone : <Country>/<Region>
            Connected Status: <Available/Configuring/Off-line/etc..>
            Battery Status : <xx%> <Charging>           
        """
        try:
            beam = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()
            normal_user.device_group = beam_name
            
            TestCondition.create_simplified_normal_users(
                self._driver, 
                user_array=[normal_user], 
                beam=beam)
            
            # steps:
            simplified_dashboard = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, True)\
            # verify point
            self.assertTrue(simplified_dashboard.is_beam_displayed(beam_name), "Assertion Error: Beam {} is not displayed".format(beam_name))

            #TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2441"
            self.assertEqual(self._driver.current_url, (Constant.SuitableTechHomeURL).format(Constant.OrgsInfo[Constant.SimplifiedOrgName]), "Assertion Error: The navigate url is not correct")
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_simplified_users([normal_user])
            
        
    def test_c11388_non_admin_user_beam_account_home_add_new_beams_to_available_beams_view(self):
        """
        @author: Duy Nguyen
        @date: 08/18/2016
        @summary: Non-Admin User Beam Account Home - Add New Beams to Available Beams View
        @precondition:           
            Use the following Test users and Organizations - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestUserAccounts
            
            FYI: Non Admin login account Home page will be moved to management App Page as follows:
            New redirected URL: https://staging.suitabletech.com/manage/#/home/
            Old redirected URL: https://staging.suitabletech.com/accounts/home/#
            
            As the Organization Admin add a non-Admin user as part of an Organization with valid devices linked within a Device Group (see Precondition test user account info above, i.e suitabletester2@gmail.com)
            1. Navigate to a Device Group with Active Beam devices i.e "dashboard->Beams->Device Group(i.e DeviceGroupTest-A)->Members"
            2. Select "Add Users" button then either "choose from Available Non-Users" or "Invite a new Non-Admin user" (i.e. suitabletester2@gmail.com)
        @steps:
            1) Using another Browser login with the non-Admin user (i.e. suitabletester2@gmail.com) credentials to their Beam Web Account
            2) Verify that the account web address is as follows: https://staging.suitabletech.com/manage/#/home/
            3) Verify that all Beam(s) accessible to that non-Admin User within the Device Group they were added as a member are listed with the following properties:
                Name : <Beam Name>
                Location : <text string>
                Labels : <text string>
                Time Zone : <Contry>/<Region>
                Connected Status: <Available/Configuring/Off-line/etc..>
                Battery Status : <xx%> <Charging>
            4) As the Organization Admin add the same non-Admin user (i.e. suitabletester2@gmail.com) as a member of another Device Group with additional Beam Devices
        @expected:
            Verify that all Beam(s) accessible to that non-Admin User within the Device Groups(i.e DeviceGroupTest-A & DeviceGroupTest-B) they have been added as a member are listed with the following properties: 
            Name : <Beam Name> Location : <text string> 
            Labels : <text string> 
            Time Zone : <Country>/<Region> 
            Connected Status: <Available/Configuring/Off-line/etc..> 
            Battery Status : <xx%> <Charging>              
        """
        try:
            beam1 = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            device1 = beam1.beam_name
            
            beam2 = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            device2 = beam2.beam_name
            
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()

            # steps:
            simplified_dashboard = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam1.beam_id)\
                    .create_completed_simplified_normal_user(normal_user)\
                .goto_login_page()\
                    .login_as_unwatched_video_user(normal_user.email_address, normal_user.password)\
                .watch_video(normal_user, True)

            # verify point
            self.assertTrue(simplified_dashboard.is_beam_displayed(device1), "Assertion Error: Beam {} is not displayed".format(device1))

            #TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2441"
            self.assertEqual(self._driver.current_url, (Constant.SuitableTechHomeURL).format(Constant.OrgsInfo[Constant.SimplifiedOrgName]), "Assertion Error: The navigate url is not correct")
            
            simplified_dashboard.logout_and_login_again(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam2.beam_id)\
                    .add_user(normal_user)\
                    .logout()\
                .goto_login_page()\
                    .login(normal_user.email_address, normal_user.password, True)\

            # verify point
            self.assertTrue(simplified_dashboard.is_beam_displayed(device1), "Assertion Error: Beam {} is not displayed".format(device1))
            self.assertTrue(simplified_dashboard.is_beam_displayed(device2), "Assertion Error: Beam {} is not displayed".format(device2))
            
        finally:
            TestCondition.release_a_beam(beam1)
            TestCondition.delete_simplified_users([normal_user])
            

    def test_c11389_non_admin_user_beam_account_home_remove_beams_from_available_beams_view(self):
        """
        @author: Duy Nguyen
        @date: 08/18/2016
        @summary: Non-Admin User Beam Account Home - Remove Beam from Available Beams View
        @precondition:           
            Use the following Test users and Organizations - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestUserAccounts
            
            FYI: Non Admin login account Home page will be moved to management App Page as follows:
            New redirected URL: https://staging.suitabletech.com/manage/#/home/
            Old redirected URL: https://staging.suitabletech.com/accounts/home/#
            
            As the Beam Organization Admin add a non-Admin user as part of an Organization with valid devices linked within a Device Group (see Precondition test user account info above, i.e suitabletester2@gmail.com)
            1. Navigate to a Device Group with Active Beam devices i.e "dashboard->Beams->Device Group(i.e DeviceGroupTest-A)->Members"
            2. Select "Add Users" button then either "choose from Available Non-Users" or "Invite a new Non-Admin user" (i.e. suitabletester2@gmail.com)
        @steps:
            1) Using another Browser login with the non-Admin user (i.e. suitabletester2@gmail.com) credentials to their Beam Web Account
            2) Verify that the account web address is as follows: https://staging.suitabletech.com/manage/#/home/
            3) Verify that all Beam(s) accessible to that non-Admin User within the Device Group they were added as a member are listed with the following properties:
                    Name : <Beam Name>
                    Location : <text string>
                    Labels : <text string>
                    Time Zone : <Contry>/<Region>
                    Connected Status: <Available/Configuring/Off-line/etc..>
                    Battery Status : <xx%> <Charging>
            4) As the Organization Admin add the same non-Admin user (i.e. suitabletester2@gmail.com) as a member of another Device Group with additional Beam Devices
            5) Verify that all Beam(s) accessible to that non-Admin User within the Device Groups(i.e DeviceGroupTest-A & DeviceGroupTest-B) they have been added as a member are listed with the following properties: 
                    Name : <Beam Name> Location : <text string> 
                    Labels : <text string> 
                    Time Zone : <Country>/<Region> 
                    Connected Status: <Available/Configuring/Off-line/etc..> 
                    Battery Status : <xx%> <Charging>       
            6) As the Organization Admin remove the same non-Admin user (i.e. suitabletester2@gmail.com) as a member of one of their Device Groups
        @expected:
            Verify that only the Beam(s) accessible to that non-Admin User within the Device Groups(i.e DeviceGroupTest-A) they have membership to are listed with the following properties:
             Name : <Beam Name> 
             Location : <text string> 
             Labels : <text string> 
             Time Zone : <Country>/<Region> 
             Connected Status: <Available/Configuring/Off-line/etc..> 
             Battery Status : <xx%> <Charging>            
        """
        try:
            beam1 = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            device1 = beam1.beam_name
            beam2 = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            device2 = beam2.beam_name
            
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()

            # steps:
            simplified_dashboard = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam1.beam_id)\
                .create_completed_simplified_normal_user(normal_user)\
                .goto_login_page()\
                .login_as_unwatched_video_user(normal_user.email_address, normal_user.password)\
                .watch_video(normal_user, True)
                
            # verify point
            self.assertTrue(simplified_dashboard.is_beam_displayed(device1), "Assertion Error: Beam {} is not displayed".format(device1))

            #TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2441"
            self.assertEqual(self._driver.current_url, (Constant.SuitableTechHomeURL).format(Constant.OrgsInfo[Constant.SimplifiedOrgName]), "Assertion Error: The navigate url is not correct")
            
            simplified_dashboard.logout_and_login_again(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam2.beam_id)\
                .add_user(normal_user)\
                .logout()\
                .goto_login_page()\
                .login(normal_user.email_address, normal_user.password, True)

            # verify point
            self.assertTrue(simplified_dashboard.is_beam_displayed(device1), "Assertion Error: Beam {} is not displayed".format(device1))
            self.assertTrue(simplified_dashboard.is_beam_displayed(device2), "Assertion Error: Beam {} is not displayed".format(device2))
            
            simplified_dashboard.logout_and_login_again(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam1.beam_id)\
                .remove_user(normal_user)\
                .logout()\
                .goto_login_page()\
                .login(normal_user.email_address, normal_user.password, True)\

            # verify point
            self.assertTrue(simplified_dashboard.is_beam_displayed(device2), "Assertion Error: Beam {} is not displayed".format(device2))
            self.assertFalse(simplified_dashboard.is_beam_displayed(device1), "Assertion Error: Beam {} is not displayed".format(device1))
        finally:
            TestCondition.release_a_beam(beam1)
            
