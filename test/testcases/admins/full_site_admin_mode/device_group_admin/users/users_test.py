from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper, EmailDetailHelper
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime
from data_test.dataobjects.user import User
import re
from pages.suitable_tech.admin.advanced.dashboard import admin_dashboard_page
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.suitabletechapis.user_api import UserAPI


class Users_Test(TestBase):
    
    def test_c11589_invite_new_user_not_currently_in_the_org_1_x(self):
        """
        @author: Quang Tran
        @date: 7/29/2016
        @summary: Invite new user not currently in the Org [1.X]
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Device Group Admin account
        @steps:
            1) Login to Suitabletech.com and navigate to the "Manage Your Beams" dashboard as the Device Group Admin. 
            2) Click “Invite a new User” button
            3) Enter the user’s name that is not currently in the Org and has a valid email address, 
            select a device group in the "Invite New User" form and select "invite user" in the bottom right corner of the form. 
            
        @expected:
            1. Invited user receives a new user not in database email
            2. Check the accounts users profile for access to the device group in which they were invited to. (i.e. Device Group String)
        
        @note: Ready to automate
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            new_device_group_name = Helper.generate_random_device_group_name()
            
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = new_device_group_name
            normal_user.invitation_settings.include_the_default_invitation_message = None
            
            TestCondition.create_device_group(new_device_group_name, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                
            # testcase's steps 
            admin_dashboard_page = admin_dashboard_page.invite_new_user(normal_user)
            
            # verify
            expected_email = EmailDetailHelper.generate_welcome_email(normal_user, admin_user.get_displayed_name())
            actual_emails = GmailUtility.get_messages(expected_email.subject, receiver=normal_user.email_address)
            
            self.assertEqual(len(actual_emails), 1, "Assertion Error: The number of email return is not correct")
            does_email_match = re.match(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(does_email_match,
                "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content))
                    
            # verify
            user_detail_page = admin_dashboard_page.goto_users_tab().goto_user_detail_page(normal_user)
            device_groups = user_detail_page.get_device_groups()
            
            self.assertEqual(device_groups, [new_device_group_name], "User is not assigned to the device groups {}.".format(new_device_group_name))
        finally:
            # restore the previous value and clean up
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user, admin_user])
            TestCondition.delete_device_groups([new_device_group_name])

    
    def test_c11594_invite_a_new_user_no_group_no_email_copy_1_x(self):
        """
        @author: tham.nguyen
        @date: 7/22/2016
        @summary: Invite a new user and test "Email a copy to myself" email that the admin would receive [1.X] 
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            A device group admin account and a user account that is not in the ST database. Removing a QA test account would take place in staff Admin --> Site --> Users to remove the user from the Beam dbase
        @steps:
            1) Login to Suitabletech.com and navigate to the "Manage Your Beams" advanced UI as the Device Group Admin 
            2) Click “Invite a new User” button
            3) Enter the user’s name and email address (he/she will receive an email)
            4) Check the "email a copy to myself" box
        @expected:
            1. Invitation email is successfully sent to the admin and new user. 
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group, [], organization)
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group
            TestCondition.create_advanced_device_group_admins(driver=self._driver, user_array=[device_group_admin])
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.invitation_settings.email_a_copy_to_myself = True
            normal_user.invitation_settings.include_the_default_invitation_message = None
            
            # steps            
            LoginPage(self._driver).open().login(device_group_admin.email_address, device_group_admin.password)\
                .invite_new_user(normal_user)
            
            # verify points
            expected_wc_email = EmailDetailHelper.generate_welcome_email(normal_user, device_group_admin.get_displayed_name())
            lst_wc_emails = GmailUtility.get_messages(expected_wc_email.subject, None, device_group_admin.email_address, normal_user.email_address, datetime.now())
            
            self.assertEqual(len(lst_wc_emails), 1, "Assertion Error: The number of email return is not correct")
            does_email_match = re.match(expected_wc_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(does_email_match,
                "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_wc_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content))
            
            expected_copy_email = EmailDetailHelper.generate_welcome_admin_copy_email(normal_user, UserAPI.get_displayed_name(device_group_admin))
            lst_copy_emails = GmailUtility.get_messages(expected_copy_email.subject, None, device_group_admin.email_address, device_group_admin.email_address, datetime.now())
            does_email_exist = GmailUtility.does_copy_email_exist(lst_copy_emails, expected_copy_email) 
                
            self.assertTrue(does_email_exist,
                "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_copy_email.trimmed_text_content, lst_copy_emails[0].trimmed_text_content))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user, device_group_admin])
            TestCondition.delete_device_groups([device_group], organization)
            
        
    def test_c11596_add_a_new_user_with_no_initial_device_group_chosen_2_x(self):
        """
        @author: tham.nguyen
        @date: 7/27/2016
        @summary: Add a new user with no initial Device group chosen [2.X]
        @precondition:
            Pertains to http://jira.suitabletech.com/browse/NCA-8776 "Admins should not be able to invite new users without assigning to a device group. "
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs

        @steps:
            1) Login to Suitabletech.com and navigate to the "Manage Your Beams" advanced UI as the Device Group Admin 
            2) Click the box that says "Invite User"
            3) Fill out the required information in the next window and make sure to NOT add the user to a Device group. 
        @expected:
           ***Pending http://jira.suitabletech.com/browse/NCA-8776 the device group field will be mandatory and the expected result
           will be that the user is not able to submit form without specifying device group. 
        
        """
        try:
            # pre-condition
            organization = Constant.AdvancedOrgName
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = None
            normal_user.invitation_settings.include_the_default_invitation_message = None
            
            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group, [], organization)
            admin_user = User()                                            
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = device_group
            admin_user.organization = organization
            
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .open_invite_a_new_user_dialog().enter_invite_user_info(normal_user)
                
            is_invite_user_button_disabled = admin_dashboard_page.is_invite_user_button_disabled()
            
            # TODO: This test case failed due to bug "http://jira.suitabletech.com/browse/INFR-1174"
            self.assertTrue(is_invite_user_button_disabled, "Assertion Failed: The Invite User button is still enabled although the device group is not entered")
            admin_dashboard_page.cancel_invite_user_dialog()
        finally:
            TestCondition.delete_advanced_users([admin_user, normal_user], organization)
            TestCondition.delete_device_groups([device_group], organization)

    
    def test_c11597_invite_a_new_user_and_add_to_device_group_and_email_copy_to_admin_1_x(self):
        """
        @author: tham.nguyen
        @date: 7/22/2016
        @summary: Invite a New User + add to device group + email copy to admin[1.X] 
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            A device group admin account and a separate pre existing user account.
        @steps:
            1) Login to Suitabletech.com and navigate to the "Manage Your Beams" advanced UI using a device group admin account.
            2) Select the "Invite New User" button
            3) Fill out the required information in the form, check the box to "email a copy to myself" and select invite user in the bottom right
        @expected:
            1. Verify a copy of the email is received by the admin.
            2. Verify that the invited user receives email and has access to the beams in selected device group. 
            This can be done by navigating to the user account under the users tab and verifying that 
            the "device group" string is populated with the device group the user was assigned access too.
        """
        try: 
            # pre-condition
            organization_name = Constant.AdvancedOrgName
            devices = []
            beams = []
            for _ in range(2):
                beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beams.append(beam)
                devices.append(beam.beam_name)
                
            device_group_name = Helper.generate_random_device_group_name(5)
            TestCondition.create_device_group(device_group_name, devices, organization_name)
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            TestCondition.create_advanced_device_group_admins(driver=self._driver, user_array=[device_group_admin])
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            normal_user.invitation_settings.email_a_copy_to_myself = True
            normal_user.invitation_settings.include_the_default_invitation_message = None
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .invite_new_user(normal_user)
                
            displayed_name = device_group_admin.get_displayed_name()
            expected_welcome_email = EmailDetailHelper.generate_welcome_email(normal_user, displayed_name)
            expected_copy_email = EmailDetailHelper.generate_welcome_admin_copy_email(normal_user, displayed_name)
            
            admin_detail_user_page = admin_dashboard_page.goto_users_tab().goto_user_detail_page(normal_user)
            lst_devices = admin_detail_user_page.get_device_groups()
            
            # verify points
            self.assertEqual(lst_devices[0], normal_user.device_group,
                             "Assertion Error: Normal user was assigned to device group name '{}', but the user's device group in the user detail page is {}".format(normal_user.device_group, lst_devices[0]))
            
            lst_wc_emails = GmailUtility.get_messages(expected_welcome_email.subject, None, device_group_admin.email_address, normal_user.email_address, datetime.now())
            
            self.assertTrue(len(lst_wc_emails) == 1,
                            "Assertion Error: '{}' was returned incorrect email to normal user '{}'. The number email return is {}".format(expected_welcome_email.subject, normal_user.email_address, len(lst_wc_emails)))
            does_email_match = re.match(expected_welcome_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(does_email_match,
                            "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_welcome_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content))
            
            lst_copy_emails = GmailUtility.get_messages(expected_copy_email.subject, None, device_group_admin.email_address, device_group_admin.email_address, datetime.now())
            does_email_exist = GmailUtility.does_copy_email_exist(lst_copy_emails, expected_copy_email) 
                
            self.assertTrue(does_email_exist,
                "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_copy_email.trimmed_text_content, lst_copy_emails[0].trimmed_text_content))
        finally:
            # post-condition
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user, device_group_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)
            
        
    def test_c11595_add_a_user_that_already_exists_in_another_organization_1_x(self):
        """
        @author: Tham.Nguyen
        @date: 08/02/2016
        @summary: Add a user that already exists in another organization [1.X]
        @precondition:           
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Device group admin privileges in two different orgs.
        @steps:
            1) Login to Suitabletech.com and navigate to the "Manage Your Beams" advanced UI as the Device Group Admin
            2) Select the "Invite a new user" button. Invite a new user that exists in another org in which your account has device group admin access to.
            Select a device group you manage to assign them access. 
            VP: Confirm the invited user account has access under the users profile located under the users tab. 
            This can be confirmed by viewing the "Device Groups" String in their user profile.
            4) Switch orgs and confirm that the desired user is still listed under the "Users" tab in the "Manage your beams" section
        @expected:          
            The same user record should be added to the new organization as well. The user will now be in both.
        """
        try:
        # pre-condition
            # create device group
            devices = []
            device_group_name = Helper.generate_random_device_group_name(5)
            organizations = [Constant.AdvancedOrgName, Constant.AdvancedOrgName_2]
            
            device_group_admin = User()                            
            device_group_admin.generate_advanced_device_group_admin_data()
            
            TestCondition.create_advanced_device_group_admin_on_multi_organization(self._driver, device_group_admin, device_group_name, devices, organizations)                           
        # steps
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            normal_user.invitation_settings.include_the_default_invitation_message = None
            
            user_detail_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .invite_new_user(normal_user)\
                .goto_users_tab().goto_user_detail_page(normal_user)
                
            users_page = user_detail_page.goto_another_org(organizations[1])\
                .invite_new_user(normal_user).goto_users_tab()
            
        # verify points
            is_user_existed_in_org = users_page.is_user_existed(normal_user.email_address, UserAPI.get_displayed_name(normal_user))
                
            self.assertTrue(is_user_existed_in_org, "Assertion Error: Normal user '{}' is not existed in the second Organization '{}'".format(normal_user.email_address, Constant.AdvancedOrgName_2))
            
            users_page.goto_another_org(organizations[0])\
                .goto_users_tab()
            
            is_user_existed_in_org = users_page.is_user_existed(normal_user.email_address, UserAPI.get_displayed_name(normal_user))
            self.assertTrue(is_user_existed_in_org, "Assertion Error: Normal user '{}' is not existed in the first Organization '{}'".format(normal_user.email_address, Constant.AdvancedOrgName))
        
        finally:
        # post-condition
            TestCondition.delete_advanced_users([device_group_admin, normal_user], Constant.AdvancedOrgName)
            TestCondition.delete_advanced_users([device_group_admin, normal_user], Constant.AdvancedOrgName_2)
            TestCondition.delete_device_groups([device_group_name], organizations[0])
            TestCondition.delete_device_groups([device_group_name], organizations[1])
            
            
    def test_c11634_remove_user_from_organization_2_x(self):
        """
        @author: Thanh Le
        @date: 08/17/2016
        @summary: Remove User from Organization[2.X]
        @precondition:           
            Device Group Admin Account and a user account that already has access.
        @steps:
            Delete A User from the Organization:
            1) Login to Suitabletech.com and navigate to the Manage Your Beams advanced UI as a device group admin.
            2) Select the Users tab at the top            
            3) Select a user from the list of users by clicking on their name.
            4) A red "Remove from Organization" button on the right side of the users profile should be missing. Please note the picture below is should exclude the red "Remove From Organization" button pictured below.
        @expected:          
            As a Device Group Admin you are not allowed to remove a user from the organization
            --> Verify that there is no red "Remove from Organization" button on the right side
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group
            device_group_admin.organization = organization
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
              
            # steps  
            user_detail_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_users_tab().goto_user_detail_page(normal_user)
            
            # verify points
            self.assertFalse(user_detail_page.is_user_removable(),
                             "Assertion Error: User can be removable!")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user, device_group_admin], organization)
            TestCondition.delete_device_groups([device_group], organization)
    
    
    def test_c11635_remove_user_from_device_group_2_x(self):
        """
        @author: tham.nguyen
        @date: 7/26/2016
        @summary: Remove User from Device Group[2.X]
        @precondition: Use the Admin Test Organization
        @steps:
            1) Login to SuitableTech.com, navigate to the Manage Your Beams advanced UI as a Device Group Admin (not an org admin).
            2) click on the "Beams" tab, select a device group
            3) Go to the "Members" Tab
            4) In the "Users" section, click on the red "Remove" box to remove desired User
        @expected:
            1. Verify that the User has been removed by viewing the users account under the users tab. The user should no longer have this device group listed in the 'Device Group" string. 
        """
        try:
            # pre-condition
            organization_name = Constant.AdvancedOrgName
                
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name, [], organization_name)
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            # steps
            admin_beam_member_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_members_tab_of_a_device_group(device_group_name)\
                .remove_user(UserAPI.get_displayed_name(normal_user))
             
            # verify points
            self.assertFalse(admin_beam_member_page.is_user_existed(normal_user.email_address, UserAPI.get_displayed_name(normal_user)),
                            "Assertion Error: User '{}' was not removed in the device group '{}'".format(UserAPI.get_displayed_name(normal_user), device_group_name))
        finally:
            TestCondition.delete_advanced_users([normal_user, device_group_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)


    def test_c33903_invite_a_new_user_on_users_page(self):
        """
        @author: Khoi Ngo
        @date: 10/17/2017
        @summary: Invite a New User on Users page
        @precondition:
            - Create UserGroup, Device Group
        @steps:
            1. Login as org admin
            2. Go to Users page
            3. Click Invite User button
            4. Enter mail address and choose UserGroup, Device Group at precondition
            5. Click Invite User button
        @expected:
            (5)
             - Success message displays
             - An email send to user
             - New user displays on Users page
        """
        try:
            device_group_name = Helper.generate_random_device_group_name()
            user_group_name = Helper.generate_random_user_group_name()

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            normal_user.user_group = user_group_name

            advance_org_admin = User()
            advance_org_admin.advanced_org_admin_data()

            # pre-condition
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_user_group(user_group_name)

            # steps
            admin_user_page = LoginPage(self._driver).open()\
                .login(advance_org_admin.email_address,advance_org_admin.password)\
                .goto_users_tab()\
                .invite_new_user(normal_user, False)
            self.assertTrue(admin_user_page.is_success_msg_displayed(), "Success message doesn't display")

            welcome_mail = EmailDetailHelper.generate_welcome_email(normal_user, advance_org_admin.get_displayed_name())
            lst_notification_emails = GmailUtility.get_messages(mail_subject = welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = normal_user.email_address)
            self.assertTrue(len(lst_notification_emails) == 1, "Assertion Error: Suitable Tech wasn't send email")
            result = re.match(welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
            GmailUtility.delete_emails(mail_subject = welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = normal_user.email_address)                                                

            self.assertTrue(admin_user_page.is_user_existed(normal_user.email_address), "New user doesn't display on Users page")
        finally:
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_advanced_users([normal_user])

