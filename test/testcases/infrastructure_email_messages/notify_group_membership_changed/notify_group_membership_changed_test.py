from data_test.dataobjects.user import User
from common.helper import Helper, EmailDetailHelper
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage


class NotifyGroupMemmbershipChanged_Test(TestBase):
    
    def test_c11286_email_notification_notify_group_membership_changed_user_added_to_group(self):
        """
        @author: Tham.Nguyen
        @date: 08/05/2016
        @summary: Email Notification: Notify Group Membership Changed - User Added to group
        @precondition:           
            Create a user (UserA)
            Login with UserA to Suitabletech.com UserA has the following notification enabled:
            Account Settings >Settings > Notifications > Notify me when... I am added to or removed from a device group
            This notification is enabled by default for new users.
            
        @steps:
            1) Login to Suitabletech.com with org admin select "Manage Your Beams" from the user dropdown menu
            2) Go to "Beams" tab and search for an existing device group (DeviceGroupA)
            3) Click on the "Members" sub-tab then select "Add Users" button
            4) Choose the target user (UserA) and select "Add Selected Users" button
        
        @expected:          
            (4) Verify that the added user receives the following email:
            From: "{Administrator name} <notifications@suitabletech.com>"
            Subject: "[Beam] You have been added to {device group name}"
            Reply-To: "{administrator's email address}"
            Body:
            You have been added to {device group name}
            {Administrator name} added you to {device group name}
            Etc.
        """
        try:
            # pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])

            org_admin = User()                                            
            org_admin.advanced_org_admin_data()

            device_group_name = Helper.generate_random_device_group_name()
            expected_added_device_group_msg = EmailDetailHelper.generate_added_to_device_group_email(
                                                    device_group_name=device_group_name, 
                                                    admin_full_name=org_admin.get_displayed_name())
            TestCondition.create_device_group(device_group_name)

            # steps
            LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account()\
                .goto_notifications_tab()\
                    .toggle_added_or_removed_from_device_group_notification(True)\
                    .logout()\
                .goto_login_page()\
                    .login(org_admin.email_address, org_admin.password)\
                .goto_members_tab_of_a_device_group(device_group_name)\
                    .add_user_to_device_group(normal_user)
            
            # verify points
            lst_emails = GmailUtility.get_messages(mail_subject=expected_added_device_group_msg.subject,
                                                   receiver=normal_user.email_address,
                                                   sent_day=datetime.now())
            self.assertTrue(len(lst_emails) == 1, 
                        """Assertion Error: '{}' was returned incorrect number email to normal user '{}'. 
                        The number email is '{}'"""\
                        .format(expected_added_device_group_msg.subject, normal_user.email_address, len(lst_emails)))
            self.assertEqual(expected_added_device_group_msg.trimmed_text_content, lst_emails[0].trimmed_text_content,
                        "Assertion Error: Expected email content is '{}' but doesn't match '{}'"\
                        .format(expected_added_device_group_msg.trimmed_text_content, lst_emails[0].trimmed_text_content))
            
        finally:
            # post-condition       
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group_name])


    def test_c11287_email_notification_notify_group_membership_changed_user_removed_from_group(self):
        """
        @author: Duy Nguyen
        @date: 08/15/2016
        @summary: Email Notification: Notify Group Membership Changed - User removed from group
        @precondition:           
            Ensure your "target" user has the following notification enabled:
            
            Manage my Beams > Your Account > Notifications > Notify me when... I am added to or removed from a device group
            
            This notification is enabled by default for new users.
            
        @steps:
        As an administrator:
            1) Go to the "Beams" tab and choose a device group from the dropdown
            2) Click on the "Members" sub-tab
            3) Find a user in the list and click the "remove" button
        
        @expected:          
            Verify that the removed user receives the following email:
            
            From: "{Administrator name} <notifications@suitabletech.com>"
            Subject: "[Beam] You have been removed from {device group name}"
            Reply-To: "{administrator's email address}"
            Body:
            
            You have been removed from {device group name}
            
            {Administrator name} removed you from {device group name}
            
            Etc.
        """        
        try:
            # precondition:
            new_device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(new_device_group_name)
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = new_device_group_name
            
            org_admin = User()                                            
            org_admin.advanced_org_admin_data()
            
            # create device group
            expected_remove_device_group_email = EmailDetailHelper.generate_removed_from_device_group_email(new_device_group_name, admin_full_name=org_admin.get_displayed_name())
            
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            
            dashboard_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser = True)\
                .goto_your_account()\
                .goto_notifications_tab().toggle_added_or_removed_from_device_group_notification(True)\
                .logout_and_login_again(email_address=org_admin.email_address, password=org_admin.password)
            
            # steps:
            dashboard_page.goto_members_tab_of_a_device_group(new_device_group_name)\
                .remove_user(normal_user.get_displayed_name())
            
            # verify point
            actual_email_remove_device_group = GmailUtility.get_messages(expected_remove_device_group_email.subject, 'notifications@suitabletech.com', None, normal_user.email_address, datetime.now())
            self.assertEqual(len(actual_email_remove_device_group), 1, "Assertion Error: The number of return email is not correct")
            self.assertEqual(expected_remove_device_group_email.trimmed_text_content, actual_email_remove_device_group[0].trimmed_text_content, \
            "Assertion Error: The content of return email is not correct. The expected email content is '{}' but the actual email content is '{}'".format(expected_remove_device_group_email.trimmed_text_content, actual_email_remove_device_group[0].trimmed_text_content))
            
        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([normal_user])  


    def test_c11288_email_notification_notify_group_membership_changed_user_added_admin_version(self):
        """
        @author: Duy Nguyen
        @date: 08/16/2016
        @summary: Email Notification: Notify Group Membership Changed - User Added (admin version)
        @precondition:           
            Ensure you have two administrator users.
            
            Ensure your "other" administrator user (Admin User B) has the following notification enabled:
            
            Manage my Beams > Your Account > Notifications > Notify me when... device group members are added or removed
            
            This notification is NOT enabled by default for new users.
            
        @steps:
        As an administrator (Admin User A):
            1) Go to "Manage my Beams" (/manage/)
            2) Go to the "Beams" tab and choose a device group from the dropdown
            3) Click on the "Members" sub-tab
            4) Click on "Add users"
            5) Find a target user(s) and click "Add selected users"
        
        @expected:          
            Verify that your "other" administrator (Admin User B) receives the following email:
            
            From: "{Administrator A name} <notifications@suitabletech.com>"
            Subject: "[Beam] A user was added to {device group name}"
            Reply-To: "{administrator A's email address}"
            Body:
            
            A user was added to {device group name}
            
            {Administrator A name} added {target user name} to {device group name}
            
            Etc.
        """
        try:
            # precondition:
            device_group = Helper.generate_random_device_group_name()
            
            admin_user_01 = User()
            admin_user_01.generate_advanced_device_group_admin_data()
            admin_user_01.device_group = device_group

            admin_user_02 = User()
            admin_user_02.generate_advanced_device_group_admin_data()
            admin_user_02.device_group = device_group
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            normal_user.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
            
            TestCondition.create_device_group(device_group)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user_01, admin_user_02])
            
            login_page = LoginPage(self._driver).open()\
                .login(admin_user_02.email_address, admin_user_02.password)\
                .goto_your_account()\
                .goto_notifications_tab()\
                .toggle_device_group_members_are_added_or_removed()\
                .logout().goto_login_page()
                                
            # steps:
            login_page.login(admin_user_01.email_address, admin_user_01.password)\
                .goto_members_tab_of_a_device_group(device_group)\
                .add_user_to_device_group(normal_user)
            
            # verify point:            
            expected_email = EmailDetailHelper.generate_notification_added_to_device_group_email(device_group_name=device_group, admin_full_name=admin_user_01.get_displayed_name(), user_full_name=normal_user.get_displayed_name())
            actual_msgs = GmailUtility.get_messages(expected_email.subject, receiver=admin_user_02.email_address)
            
            self.assertEqual(1, len(actual_msgs), "Assertion Error: The number of email return is not correct")
            self.assertEqual(expected_email.trimmed_text_content, actual_msgs[0].trimmed_text_content, "Assertion Error: Expected email content is '{}' but found '{}'".format(expected_email.trimmed_text_content, actual_msgs[0].trimmed_text_content))
                     
        finally:
            TestCondition.delete_advanced_users([admin_user_01, admin_user_02, normal_user])
            TestCondition.delete_device_groups([device_group, temp_device_group_name])
