from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.admin.advanced.dashboard import admin_dashboard_page
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from common.application_constants import ApplicationConst
from datetime import datetime
import re
from pages.suitable_tech.user.login_page import LoginPage


class NotifyUsersAdmins_Test(TestBase):

    def test_c11278_email_notification_admin_assigns_one_of_their_users_to_be_an_administrator(self):
        """
        @author: Thanh Le
        @date: 8/5/2016
        @summary: Email Notification: Admin assigns one of their users to be an administrator
        @precondition:           
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/displ11292 ay/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
             
            Create a user (UserA) and make sure user has the following notification enabled:
             
            Your Account > Notifications > Organizations > "Notify me when... I become an administrator"
             
            This notification is enabled by default for new users.
 
        @steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and search for created user in pre-condition (UserA), select this user
            3. Click "Edit" button and check on "Allow this user to administer this organization" checkbox then save change
 
        @expected:
            (3) A notification email is sent
            From: "{Name of administrator user} <notifications@suitabletech.com>"
            Subject: [Beam] You are now an administrator of {Org name}
            Body:
            You are now an administrator of {Org name}
             
            {Administrator name} made you an administrator of {Org name}
             
            etc.
 
        """
        try:
            #pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
             
            org_admin = User()
            org_admin.advanced_org_admin_data()            
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            normal_user.device_group = temp_device_group_name
            org_admin.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
             
            notification_email_template = EmailDetailHelper.generate_added_to_org_admin_email(org_admin.organization, org_admin.get_displayed_name())            
             
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
             
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account().goto_notifications_tab()\
                .toggle_become_admin_notification(True)\
                .logout_and_login_again(email_address=org_admin.email_address, password=org_admin.password)
              
            #steps
            admin_dashboard_page.goto_users_tab()\
                .goto_user_detail_page(normal_user).edit_user(allow_administer = True)\
                .goto_users_tab()
          
            actual_notification_email = GmailUtility.get_messages(notification_email_template.subject, receiver=normal_user.email_address)
               
            #verify points
            self.assertEqual(1, len(actual_notification_email), 
                             "Assertion Error: There should be one {} notification on new admin's inbox. Found {}".format(notification_email_template.subject, len(actual_notification_email)))
            self.assertEqual(notification_email_template.trimmed_text_content, actual_notification_email[0].trimmed_text_content, 
                             "Assertion Error: the actual notification content {} is not sent as expected {}".format(actual_notification_email[0].trimmed_text_content, notification_email_template.trimmed_text_content))
             
        finally:
            #post-condition
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([temp_device_group_name])
             
     
    def test_c11279_email_notification_admin_assigns_user_in_org_to_be_a_call_answer_authorizer(self):
        """
        @author: Thanh Le
        @date: 8/16/2016
        @summary: Email Notification: Admin assigns user in org to be a call answer authorizer
        @precondition:           
            Ensure that the new call authorizer user has the following notification enabled:
            Your Account > Notifications > My access to Beams > "Notify me when... I can change device settings or answer calls"
            This notification is enabled by default for new users.
 
        @steps:
            As an organization or device group administrator:
                1. Go to "Manage my Beams" (/manage/)
                2. Click on "Beams"
                3. Choose a device group from the device group dropdown menu
                4. Select the "Settings" tab
                5. Find the "Session answer" section and click the "Add Users" button
                6. Choose a user who you would like to be able to answer incoming session requests and click "Add selected users"
                7. Click "Save Changes" at the top of the page
 
        @expected:
            Verify the new session answer user receives the following email:
             
            From: "{Administrator name} <notifications@suitabletech.com>"
            Subject: [Beam] You can now accept sessions for {Device group name}
            Body:
             
            You can now accept sessions for {Device group name}
             
            {Administrator name} added you to the list of users who can answer session requests for {Device group name}
             
            etc.
        """
        try:
            #precondition:
            organization_name = Constant.AdvancedOrgName
            devices = []
            beams = []
            for _ in range(2):
                beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beams.append(beam)
                devices.append(beam.beam_name)
                 
            device_group_name = Helper.generate_random_device_group_name(5)
            TestCondition.create_device_group(device_group_name, devices, organization_name)
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
             
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()  
            org_admin.device_group = device_group_name          
             
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
             
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account().goto_notifications_tab()\
                .toggle_i_can_change_device_settings_or_answer_calls()\
                .logout_and_login_again(email_address=org_admin.email_address, password=org_admin.password)
             
            #steps
            admin_dashboard_page.goto_settings_tab_of_a_device_group(device_group_name).add_user_to_session_answer(normal_user)\
             
            notification_email_template = EmailDetailHelper.generate_can_now_accept_sessions_email(normal_user,admin_full_name=org_admin.get_displayed_name())
            actual_notification_email = GmailUtility.get_messages(notification_email_template.subject, receiver=normal_user.email_address)
              
            #verify points
            self.assertEqual(1, len(actual_notification_email), 
                             "Assertion Error: There should be one {} notification on new admin's inbox. Found {}".format(notification_email_template.subject, len(actual_notification_email)))
            self.assertEqual(notification_email_template.trimmed_text_content, actual_notification_email[0].trimmed_text_content, 
                             "Assertion Error: the actual notification content {} is not sent as expected {}".format(actual_notification_email[0].trimmed_text_content, notification_email_template.trimmed_text_content))
             
        finally:
            #post-condition
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user,org_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)
            
     
    def test_c11280_email_notification_admin_removes_existing_call_answer_authorizer(self):
        """
        @author: Thanh Le
        @date: 8/16/2016
        @summary: Email Notification: Admin removes existing call answer authorizer
        @precondition:           
            Ensure that the new call authorizer user has the following notification enabled:
            Your Account > Notifications > My access to Beams > "Notify me when... I can change device settings or answer calls"
            This notification is enabled by default for new users.
 
        @steps:
            As an organization or device group administrator:
                1. Go to "Manage my Beams" (/manage/)
                2. Click on "Beams"
                3. Choose a device group from the device group dropdown menu
                4. Select the "Settings" tab
                5. Find the "Session answer" section and click "X" button next to user to Remove this User
                6. Click "Save Changes" at the top of the page
 
        @expected: 
            Verify the below resulting Email notification Template:
             
            Subject: [Beam] <User_Full_Name> can no longer accept sessions for <Device_Group_name>
            From: notifications@suitabletech.com
            To: User_Email
            Date: Sent date
             
            <User_Full_Name> can no longer accept sessions for <Device_Group_name>
             
            <Admin Full Name> removed <User_Full_Name> from the list of users who can answer session requests for <Device_Group_name>.
             
            Have questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/
             
            You can change your email notification settings here: https://staging.suitabletech.com/manage/#/account/notifications/
             
            Thanks,
            Suitable Technologies
             
            Suitable Technologies, Inc.
            921 E Charleston Rd
            Palo Alto, CA 94303
            1-855-200-2326
        """
        try:
            #precondition:
            organization_name = Constant.AdvancedOrgName
            devices = []
            beams = []
            for _ in range(2):
                beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beams.append(beam)
                devices.append(beam.beam_name)
                 
            device_group_name = Helper.generate_random_device_group_name(5)
            TestCondition.create_device_group(device_group_name, devices, organization_name)
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
             
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()            
            org_admin.device_group = device_group_name
             
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
             
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account().goto_notifications_tab()\
                .toggle_i_can_change_device_settings_or_answer_calls(True)\
                .logout_and_login_again(email_address=org_admin.email_address, password=org_admin.password)
             
            #steps
            admin_dashboard_page.goto_settings_tab_of_a_device_group(device_group_name)\
                .add_user_to_session_answer(normal_user)\
                .remove_user_from_session_answer(normal_user)\
                .goto_beams_tab()
             
            notification_email_template = EmailDetailHelper.generate_can_no_longer_accept_sessions_email(normal_user,admin_full_name=org_admin.get_displayed_name())
            actual_notification_email = GmailUtility.get_messages(notification_email_template.subject, receiver=normal_user.email_address)
              
            #verify points
            self.assertEqual(1, len(actual_notification_email), 
                             "Assertion Error: There should be one {} notification on new admin's inbox. Found {}".format(notification_email_template.subject, len(actual_notification_email)))
            self.assertEqual(notification_email_template.trimmed_text_content, actual_notification_email[0].trimmed_text_content, 
                             "Assertion Error: the actual notification content {} is not sent as expected {}".format(actual_notification_email[0].trimmed_text_content, notification_email_template.trimmed_text_content))
             
        finally:
            #post-condition
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user,org_admin])      
            TestCondition.delete_device_groups([device_group_name], organization_name)

   
    def test_c11292_email_notification_notify_device_group_admin_cc_invite_email(self):
        """
        @author: Tham.Nguyen
        @date: 08/08/2016
        @summary: Email Notification: Notify Device Group Admin- CC invite email
        @precondition:           
            Create a device group admin
        @steps:
            1) Login to Suitabletech.com with the device Group Admin in pre-condition select "Manage Your Beams" from the user dropdown menu
            2) On dashboard page, click "Invite a New User" button
            3) Enter Email, First name, Last name, select device group, user group
            4) Check on "Email a copy to myself" checkbox
            5) Click "Invite User" button
        @expected:          
            (5)
            a. The pop-up message "The invitation to <user's email> was successfully sent." displays.
            b. Ensure that the invited user receives the following email:
            From: "{Admin name} <notifications@suitabletech.com>"
            Reply-To: "{Admin name} <{admin's email address}>"
            Subject: Welcome to Beam at {Organization name}
            Body:
            Welcome to Beam at {Organization name}
            {Admin name} invited you to Beam into {Organization name}.
            To get started, click this link to activate your account and set a password.
            <link/button>
            This link expires in 7 days.
            Your username is your email address: {recipient's email address}
            etc.
            c. Also verify that your administrator (the invitee) receives a copy of the above email:
            From: "{Admin name} <notifications@suitabletech.com>"
            Reply-To: "{Admin name} <{admin email address}>"
            Subject: Welcome to Beam at {Organization name} (copy)
            Body: 
            The following is your requested copy of the email sent to {recipient's email address}.
            {Copy of the original email, with <link removed> in place of the invitation link/button}
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()                          
            admin_user = User()                                            
            admin_user.generate_advanced_device_group_admin_data()                                
            admin_user.device_group = device_group_name                        
                                                        
            TestCondition.create_device_group(device_group_name)                    
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])            
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            normal_user.invitation_settings.email_a_copy_to_myself = True
            normal_user.invitation_settings.include_the_default_invitation_message = None
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .invite_new_user(normal_user, False)
                
            # verify points
            msg_success = admin_dashboard_page.get_msg_success()
            expected_pop_up_message = ApplicationConst.INFO_INVITATION_MAIL_SENT_SUCCESSFUL.format(normal_user.email_address)
            self.assertEqual(msg_success, expected_pop_up_message,
                             "Assertion Error: The pop-up expected message is '{}', but actual result is '{}'".format(expected_pop_up_message, msg_success))
            
            expected_message = EmailDetailHelper.generate_welcome_email(normal_user, admin_user.get_displayed_name())
            expected_copy_message = EmailDetailHelper.generate_welcome_admin_copy_email(normal_user, admin_user.get_displayed_name())
            
            lst_notification_emails = GmailUtility.get_messages(expected_message.subject, None, admin_user.email_address, normal_user.email_address, datetime.now())
            
            self.assertTrue(len(lst_notification_emails) == 1,
                             "Assertion Error: '{}' was returned incorrect number email to normal user '{}'".format(expected_message.subject, normal_user.email_address))
            does_email_match = re.match(expected_message.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(does_email_match,
                            "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_message.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
            
            lst_copy_emails = GmailUtility.get_messages(expected_copy_message.subject, None, admin_user.email_address, admin_user.email_address, datetime.now())
            does_email_exist = GmailUtility.does_copy_email_exist(lst_copy_emails, expected_copy_message)
                
            self.assertTrue(does_email_exist,
                            "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_copy_message.trimmed_text_content, lst_copy_emails[0].trimmed_text_content))
            
        finally:
            # post-condition
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([admin_user, normal_user])