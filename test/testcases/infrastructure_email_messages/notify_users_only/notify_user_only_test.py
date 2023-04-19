from datetime import datetime
import re
from common.constant import Constant
from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase


class NotifyUserOnly_Test(TestBase):
    
    def test_c11290_email_notification_notify_user_invite_new_user(self):
        """
        @author: Tham.Nguyen
        @date: 08/05/2016
        @summary: Email Notification: Notify user - Invite New User
        @precondition:           
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgsc
        @steps:
            1) Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2) From your organization dashboard or the Users tab, click on the "Invite a New User" button
            3) Enter an email address, name (optional), device and/or user groups (optional), and click "Invite user"
        
        @expected:          
            _The message "The invitation to <user's email> was successfully sent" appears.
            _The email notification sent
            From: "{Administrator's name} <notifications@suitabletech.com>"
            Subject: Welcome to Beam at {organization name}
            Reply-To: "{administrator's email address}"
            Body:
            Welcome to Beam at {Organization Name}
            {Administrator} invited you to Beam into {Organization name}
            To get started, click this link to activate your account and set your password:
            <activate account button/link>
            This link expires in 7 days.
            Your username is your email address: {invitee's email address}
            Etc.
        """
        try:            
            # precondition:
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            # steps
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()            
            
            LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_new_user(normal_user)
                        
            # verify points
            expected_message = EmailDetailHelper.generate_welcome_email(normal_user, admin_full_name=org_admin.get_displayed_name())
            lst_notification_emails = GmailUtility.get_messages(expected_message.subject, None, org_admin.email_address, normal_user.email_address, datetime.now())
            
            self.assertEqual(1, len(lst_notification_emails), "Assertion Error: The number email of '{}' returned to normal user '{}' is not correct".format(expected_message.subject, normal_user.email_address))
            does_email_match = re.match(expected_message.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)             
            self.assertTrue(does_email_match,
                "Assertion Error: Expected email content is '{}' but doesn't match '{}'".format(expected_message.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user, org_admin])
            
            
    def test_c11291_email_notification_notify_user_invite_existing_user(self):
        """
        @author: Tham.Nguyen
        @date: 08/05/2016
        @summary: Email Notification: Notify user - Invite Existing User
        @precondition:           
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgsc
            There is an org admin with 2 orgs
            Create a user (UserA) in an org (Org1)
        @steps:
            1) Login to Suitabletech.com as a multiple org admin with 2 orgs and select Manage Your Beams from the user dropdown menu
            2) Switch to Org2 on the top right of page
            3) Select "Invite a New User" button 
            4) Enter email, firstname, lastname of the existing user (UserA) in Org1 , select device group and user group
            5) Click "Invite User" button
        @expected:          
            Verify that the invited user receives the following email:
            From: "{Administrator's name} <notifications@suitabletech.com>"
            Subject: Welcome to Beam at {organization name}
            Reply-To: "{administrator's email address}"
            Body:
            Welcome to Beam at {Organization Name}
            {Administrator} invited you to Beam into {Organization name}
            You can use your existing account with the username: {invitee's email address}
            If you haven't installed the Beam software on your computer yet, click the following link to get started:
            {link to installers}
            You can see which devices are available by signing into the Beam software on your computer or mobile device.
            Etc.
        """
        try:
            # pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            
            multi_org_admin_user = User()
            multi_org_admin_user.generate_advanced_org_admin_data()
            #create device group
            device_group_name = Helper.generate_random_device_group_name()                           
            TestCondition.create_device_group(device_group_name, organization_name=Constant.AdvancedOrgName)
            TestCondition.create_device_group(device_group_name, organization_name=Constant.AdvancedOrgName_2)
            multi_org_admin_user.device_group = device_group_name
            normal_user.device_group = device_group_name
            
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.create_advanced_multi_organization_admin(self._driver, multi_org_admin_user, [Constant.AdvancedOrgName, Constant.AdvancedOrgName_2])
            
            # steps
            normal_user.organization = Constant.AdvancedOrgName_2
            
            LoginPage(self._driver).open()\
                .login(multi_org_admin_user.email_address, multi_org_admin_user.password)\
                .goto_another_org(Constant.AdvancedOrgName_2)\
                .invite_new_user(normal_user)
            
            expected_message = EmailDetailHelper.generate_welcome_existing_email(normal_user, multi_org_admin_user.get_displayed_name())

            #TODO: Test case failed due to bug https://jira.suitabletech.com/browse/INFR-2572
            # verify points            
            lst_notification_emails = GmailUtility.get_messages(expected_message.subject, None, multi_org_admin_user.email_address, normal_user.email_address, datetime.now())
            self.assertEqual(1, len(lst_notification_emails), "Assertion Error: '{}' was returned incorrect number email to normal user '{}'".format(expected_message.subject, normal_user.email_address))
            self.assertEqual(expected_message.trimmed_text_content, lst_notification_emails[0].trimmed_text_content,
                             "Assertion Error: Content email is incorrect. Expected email content is:\n'{}' but found:\n'{}'".format(expected_message.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user, multi_org_admin_user], Constant.AdvancedOrgName)
            TestCondition.delete_advanced_users([normal_user, multi_org_admin_user], Constant.AdvancedOrgName_2)
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_device_groups([device_group_name], Constant.AdvancedOrgName_2)
        
        
    def test_c11289_email_notification_notify_user_invite_temporary_user(self):
        """
        @author: Thanh Le
        @date: 08/08/2016
        @summary: Email Notification: Notify User - Invite Temporary User
        @precondition:    
            
        @steps:
            As an organization administrator or device group administrator:
                1. Go to "Manage my Beams" (/manage/)
                2. From the organization dashboard, click on "Invite a temporary user"
                3. Enter an email address, name (optional), device group, start time, and end time.
                4. Click "Invite"
                
        @expected:          
            Verify that the new temporary user receives the following email:
            
            From: "{Administrator name} <notifications@suitabletech.com>"
            Reply-To: "{administrator email}"
            Subject: You've been invited to Beam into {Organization name}
            Body:
            
            You've been invited to Beam into {Organization name}.
            
            {Administrator name} invited you to Beam into {Organization name}.
            
            To get started, click this link to activate your account and set a password.
            
            <button/link>
            
            This link expires in 7 days.
            
            Your username is your email address: {recipient's email address}
            
            You have access to the following {N} Beams:
            {List of Beams in device group(s), with time zones)
            
            You can Beam in during the following time period:
            Beginning: {start time}
            Ending: {end time}
            These times are in the time zone of the device to which you're connection.
            
            Etc.
        """
        try:
            # pre-condition:
            organization_name = Constant.AdvancedOrgName
            devices = []
            beams = []
            for _ in range(2):
                beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beams.append(beam)
                devices.append(beam.beam_name)
                
            device_group_name = Helper.generate_random_device_group_name(5)
            
            new_temp_user = User()
            new_temp_user.generate_advanced_normal_user_data()
            new_temp_user.device_group = device_group_name
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group_name
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)                            
            
            TestCondition.create_device_group(device_group_name, devices, organization_name)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])

            # steps
            LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_temporary_user(new_temp_user, start_date=starting_datetime, end_date=ending_datetime,
                                   link_to_beam_sofware=True, default_invitation=True, device_group=device_group_name)
            
            email_template = EmailDetailHelper.generate_welcome_temporary_user_email(
                    new_temp_user, starting_datetime, ending_datetime, devices, org_admin.get_displayed_name())
            actual_msgs = GmailUtility.get_messages(email_template.subject, receiver=new_temp_user.email_address)        
            
            self.assertEquals(len(actual_msgs), 1, 
                            "Assertion Error: The number of received emails is not correct")
            match_result = re.match(email_template.trimmed_text_content, actual_msgs[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(match_result, 
                            """Assertion Error: Email content is not correct. 
                            Expected:\n'{}' but found:\n'{}'""".format(
                                    email_template.trimmed_text_content, 
                                    actual_msgs[0].trimmed_text_content))
        finally:
            # post-condition:
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([new_temp_user, org_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)

