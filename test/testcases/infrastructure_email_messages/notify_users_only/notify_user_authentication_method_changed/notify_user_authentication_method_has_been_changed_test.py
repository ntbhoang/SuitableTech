from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper, EmailDetailHelper
from core.utilities.gmail_utility import GmailUtility
import re
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from datetime import datetime


class NotifyUserAuthenticationMethodHasBeenChanged_Test(TestBase):
    
    def test_c11295_email_notification_password_changed(self):
        """
        @author: Thanh Le
        @date: 15/08/2016
        @summary: Email Notification: Password Changed 
        @precondition:    
            Create a Suitabletech account UserA (non-Google-authentication user)
        @steps:
            1. Navigate to the Suitable Tech Web login page URL:https://suitabletech.com/accounts/login/
            2. Login with the user in pre-condition (UserA)
            3. Select "Account Settings > Settings"
            4. Click "Change Your Password" under "Security" tab
            5. Complete form to change your password
            6. Go to mailbox of this user
                 
        @expected:          
            (6). Verify that your user receives the following email:
 
                From: support@suitabletech.com
                Subject: Your password has changed
                Body:
                 
                Your password has changed
                 
                Your password for Beam and suitabletech.com has been changed.
                 
                Your username: {recipient's email address}
                 
                If you believe this is in error, please contact support@suitabletech.com
        """
        try:
            # pre-condition
            user = User()
            user.generate_advanced_normal_user_data()
            new_password = Helper.generate_random_password()
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            user.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
             
            TestCondition.create_advanced_normal_users(self._driver, [user])
            expected_email = EmailDetailHelper.generate_password_changed_email(user.email_address)
            #delete the email change password that is generated after the first time login.
            GmailUtility.delete_emails(expected_email.subject, receiver=user.email_address)
             
            # steps
            LoginPage(self._driver).open()\
                .login(user.email_address, user.password, simplifiedUser=True)\
                .goto_your_account().goto_change_password_page()\
                .change_password(new_password, user.password)
                 
            # verify point                        
            actual_emails = GmailUtility.get_messages(expected_email.subject, receiver=user.email_address)             
            self.assertEqual(1, len(actual_emails), "Assertion Error: Number of received emails is not correct")
            self.assertEqual(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content, "Assertion Error: message content is not correct. Expected email content is '{}' but found '{}'".format(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content))
             
        finally:
            # post-condition
            TestCondition.delete_advanced_users([user])
            TestCondition.delete_device_groups([temp_device_group_name])
         
         
    def test_c11296_email_notification_password_reset(self):
        """
        @author: Thanh Le
        @date: 15/08/2016
        @summary: Email Notification: Password Reset 
        @precondition:    
            Create a Suitabletech account UserA (non-Google-authentication user)
        @steps:
            1. Navigate to the Suitable Tech Web login page URL:https://suitabletech.com/accounts/login/
            2. Click "Forgot password?" link
            3. Enter email address of your account (UserA's email)
            4. Click "Reset your password" button
            5. Go to mailbox of UserA
                 
        @expected:          
            (4). The "Password Reset Message Sent" message displays.
            (5) Verify that your user receives the following email:
            From: support@suitabletech.com
            Subject: Beam Password Reset
            Body:
             
            Beam password reset
             
            You're receiving this email because you requested a password reset for your Beam user account.
             
            Please go to the following page and choose a new password:
             
            <reset button/link>
             
            Your username, in case you've forgotten, is: {recipient's email address}
        """
        try:
            # pre-condition
            user = User()
            user.generate_advanced_normal_user_data()
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            user.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
             
            TestCondition.create_advanced_normal_users(self._driver, [user])
             
            # steps
            is_password_reset_message_sent_page_displayed = LoginPage(self._driver).open()\
                .goto_forgot_password_page()\
                .submit_reset_password_form(user.email_address).is_page_displayed()
             
            # verify point
            self.assertTrue(is_password_reset_message_sent_page_displayed, "Page contains message \"Password Reset Message Sent\" is not displayed")    
             
            expected_email = EmailDetailHelper.generate_password_reset_email(user.email_address)
            actual_emails = GmailUtility.get_messages(expected_email.subject, receiver=user.email_address)
             
            # verify point
            self.assertEqual(1, len(actual_emails), "Assertion Error: Number of received emails is not correct")
            result = re.match(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: message content is not correct. Expected email content is:\n'{}' but found:\n'{}'".format(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content))
             
        finally:
            # post-condition
            TestCondition.delete_advanced_users([user])
            TestCondition.delete_device_groups([temp_device_group_name])
             
    
    def test_c11294_email_notification_authentication_method_change_gsso_to_st_user(self):
        """
        @author: Thanh Le
        @date: 8/16/2016
        @summary: Email Notification: Authentication method change - GSSO to ST User
        @precondition:  There is a Google account
        @steps:
            1) Navigate to the Suitable Tech Web login page URL:https://suitabletech.com/accounts/login/
            2) Sign in with the Google account in pre-condition (UserA@gmail.com)
            3) Proceed to login to Suitabletech
            4) On "Welcome to Beam!" page, select "Account Setting > Settings > Security"
            5) Click "Disconnect from Google" button
        @expected:
            5)
            _Verify that the "Disconnect Successful" page displays.
            _Verify there is a notification email sent to user as
            from: Suitable Technologies Support <support@suitabletech.com>
            to: "<user name>" <user'email>
            subject: Your authentication method has been changed
            mailed-by: <mailer.suitabletech.com>
            signed-by: <mailer.suitabletech.com>
            
            User account: <user's email>
            
            This email acknowledges that you have disconnected your Beam account from Google.
            
            If you wish to sign in with a Suitable Technologies username and password, you must first reset your password: https://staging.suitabletech.com/accounts/password_reset/.
            
            If you believe this is in error, please contact <support@suitabletech.com>.
            @note:
            Simplified Google User Email (lgvnggac@gmail.com) has set auto fw email to logigear1@suitabletech.com for checking email content
        """
        try:
            # pre-condition:
            gsso_user = User()
            gsso_user.generate_un_allowed_gsso_user_data()
            TestCondition.create_advanced_gsso_user(self._driver, gsso_user)
            expected_gmail_message = EmailDetailHelper.generate_google_change_auth_email(gsso_user.email_address)

            # steps:
            account_setting_page = LoginPage(self._driver).open()\
                .login_with_google(gsso_user.email_address)\
                .goto_your_account()\
                .set_user_language(gsso_user)
            
            disassociation_completed_page = account_setting_page.disconect_from_google()
            
            # verify point
            self.assertTrue(disassociation_completed_page.is_page_displayed(),
                            "Assert Error: Disconnect Successful page is NOT displayed!")
            
            actual_gmail_message = GmailUtility.get_messages(mail_subject=expected_gmail_message.subject, receiver=gsso_user.email_address, sent_day=datetime.now())
            
            self.assertEqual(len(actual_gmail_message), 1, "Assertion Error: The number of notice email is not correct")
            
            result = re.match(expected_gmail_message.trimmed_text_content, actual_gmail_message[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(expected_gmail_message.trimmed_text_content, actual_gmail_message[0].trimmed_text_content))

        finally:
            TestCondition.release_an_unallow_st_email(gsso_user.email_address)
        