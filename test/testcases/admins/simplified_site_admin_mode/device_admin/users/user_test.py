from datetime import datetime
from common.constant import Constant
from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.suitabletechapis.user_api import UserAPI


class User_Test(TestBase):
    
    def test_c11649_add_new_user_that_is_not_currently_in_the_org_1_X(self):
        """
        @author: khoi.ngo
        @date: 8/17/2016
        @summary: Add new user that is not currently in the org [1.X]
        @precondition:Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1. Log onto the simplified "Manage your Beams" as an org admin
            2. Click the "Manage" button below each of the Beam+'s you want another user to manage
            3. If the user is not already invited (i.e. listed at bottom of page),
                fill out the "Invite a person to use this Beam" field
            4. Verify that the new user gets added
            5. email confirmation
        @expected:
            New user receives invitation and has appropriate access to a device group.
        @review:
        """
        
        try:
            # precondition
            user_info = User()
            user_info.generate_simplified_normal_user_data()
            beam = TestCondition.get_a_beam(user_info.organization)
            
            simplified_org_admin = User()
            simplified_org_admin.generate_simplified_org_admin_data()
            simplified_org_admin_displayed_name = UserAPI.get_displayed_name(simplified_org_admin, simplified=True)

            # steps
            simplified_beam_detail_page = LoginPage(self._driver).open()\
                .login(simplified_org_admin.email_address, simplified_org_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)
            
            if not simplified_beam_detail_page.is_user_added(user_info):
                simplified_beam_detail_page.add_user(user_info)
                self.assertTrue(simplified_beam_detail_page.is_user_added(user_info), 
                                "Assertion Error: User does not exist in the device user list.")
                # verify point
                email_subject = EmailDetailHelper.generate_welcome_email(user_info, simplified_org_admin_displayed_name, simplified=True).subject
                actual_email_message = GmailUtility.get_messages(
                                            email_subject, None, 
                                            simplified_org_admin.email_address, user_info.email_address, datetime.now())
            
            self.assertEqual(len(actual_email_message), 1, "Assertion Error: The number of confirmation email is not correct")  
        finally:
            # clean up
            TestCondition.delete_simplified_users([user_info])
            
    
    def test_c11651_add_a_user_that_already_exists_in_another_organization_1_X(self):
        """
        @author: khoi.ngo
        @date: 8/17/2016
        @summary: Add a user that already exists in another organization [1.X]
        @precondition: Make sure admin account has Can Manage access to two org's 
        @steps:
            1. Log onto the simplified "Manage your Beams" as an org admin
            2. Click the "Manage" button below each of the Beam+'s you want another user to manage
            3. If the user is not already invited (i.e. listed at bottom of page), fill out the "Invite a person to use this Beam" field
            4. Verify that the new user gets added
            5. email confirmation
        @expected:
            The same user record should be added to the new organization as well. The user will now be in both.
            Verify that the user is now in two orgs.
            1. Login as a device admin in the simplified "Manage your Beams"
            2. In the upper right hand corner of the screen with the org name, 
                if you have access to more than one org (see preconditions), a drop down menu will appear
        @review:
        """
        try:
            # precondition
            device_group = Helper.generate_random_device_group_name()
            
            adv_organization = Constant.AdvancedOrgName
            smp_organization = Constant.SimplifiedOrgName
            
            new_user = User()
            new_user.generate_advanced_normal_user_data()
            new_user.device_group = device_group
            new_user.organization = adv_organization
            
            beam = TestCondition.get_a_beam(smp_organization)
            
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=adv_organization)
            TestCondition.create_advanced_normal_users(self._driver, [new_user], True)

            # steps          
            simplified_beam_detail = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_another_org(smp_organization)\
                .goto_manage_beam_page(beam.beam_id)
            
            simplified_beam_detail.add_user(new_user)
            new_user.organization = smp_organization
            
            # verify points
            # check user added in the second org
            self.assertTrue(simplified_beam_detail.is_user_added(new_user), 
                            "Assertion Error: User is not exists in the second organization")
            
            # check email arrive
            email_subject = EmailDetailHelper.generate_welcome_existing_email(new_user, 'Huy Tran', simplified=True).subject            
            actual_email_message = GmailUtility.get_messages(email_subject, None, Constant.AdvanceOrgAdminEmail, new_user.email_address, datetime.now())
            
            self.assertEqual(len(actual_email_message), 1, "Assertion Error: The number of confirmation email is not correct")

            # check user added in the first org
            new_user.organization = adv_organization
            is_user_exists_in_the_first_org = simplified_beam_detail.goto_another_org(new_user.organization, from_simplified_organization=True)\
                                                .goto_users_tab()\
                                                .is_user_existed(new_user.email_address, UserAPI.get_displayed_name(new_user))
            self.assertTrue(is_user_exists_in_the_first_org, 
                            "Assertion Error: User is not exists in the first organization")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([new_user])
            TestCondition.delete_simplified_users([new_user])
            TestCondition.delete_device_groups([device_group], adv_organization)
            

    def test_c11653_remove_user_from_device_2_x(self):
        """
        @author: khoi.ngo
        @date: 8/8/2016
        @summary: Remove User from Device [2.X]
        @precondition: Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1. Login as the Device Admin navigate to a Device you are authorized to "Manage"
            2. Select the red "Remove Person" button
            3. Click "Ok" on the toast
        @expected:
            Verify that the removed user no longer has access to that device
            verify that the removed user no longer has access to that device 
                (by login to the removed user and verify that the Beam+ is not displayed)
        """
        try:
            # precondition
            test_organization=Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            
            new_user = User()
            new_user.generate_simplified_normal_user_data()     
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            
            TestCondition.create_simplified_normal_users(
                self._driver, 
                user_array=[new_user], 
                beam=beam)
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver, 
                                user_array=[simplified_dev_admin], 
                                beam=beam,
                                organization=simplified_dev_admin.organization)
            # steps
            beam_detail_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)\
                    .remove_user(new_user)
            
            # verify points       
            self.assertFalse(beam_detail_page.is_user_added(new_user), "Assertion Error: User has access to this device")
            
            # verify points
            simplified_dashboard_page = beam_detail_page.logout()\
                .goto_login_page()\
                .login(new_user.email_address, new_user.password, True)\
            
            self.assertEqual(simplified_dashboard_page.get_number_of_devices_displayed(), 0,
                            "Assertion Error: The beam " + beam.beam_id + "is still displayed")
        finally:
            TestCondition.delete_simplified_users([simplified_dev_admin])

     
    def test_c33909_add_new_user_on_simplified_dashboard_page_2_x(self):
        """
        @author: khoi.ngo
        @date: 10/19/2017
        @summary: Add new user on Simplified Dashboard page [2.X]
        @precondition: 
        @steps: 
            1) Login as simplified org admin
            2) Enter email address into email text box
            3) Click Add User button
            4) Go to Beam Manage
        @expected:
            (3) Success message displays
            (4) New user displays in list users of device.
        """
        try:
            # pre-condition
            new_user = User()
            new_user.generate_advanced_normal_user_data()
            
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
            
            # steps
            beams_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                .add_user(new_user, beam_name)
            
            msg_success = beams_page.is_success_msg_displayed 
            beam_detail_page = beams_page.goto_manage_beam_page(beam.beam_id)
               
            # verify point           
            self.assertTrue(msg_success,  
                "No message displayed after add user {} into Simplified organization".format(new_user))
            
            self.assertTrue(beam_detail_page.is_user_added(new_user), 
                "New user {} not displayed in list of beam".format(new_user))
            
        finally:    
            TestCondition.delete_simplified_users([new_user])

