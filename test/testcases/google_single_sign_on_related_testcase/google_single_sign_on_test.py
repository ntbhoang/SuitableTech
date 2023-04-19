from datetime import datetime
import re
from common.constant import Constant
from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from data_test.dataobjects.user import User
from data_test.dataobjects.google_account import GoogleAccount
from pages.suitable_tech.user.login_page import LoginPage
from pages.gmail_page.gmail_sign_in_page import GmailSignInPage
from common.application_constants import ApplicationConst
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.webdriver.drivers.driver import Driver
from core.webdriver.drivers.driversetting import DriverSetting
from core.utilities.utilities import Utilities


class GoogleSingleSignOn_Test(TestBase):

    def c11662_invitees_to_suitable_no_account_previously_with_no_gsso(self):
        """
        @author: khoi.ngo
        @date: 8/16/2016
        @summary: Single Sign-On Account (Google only) and account state (already logged into Google at time of sign-on)
        @Note: Please follow below manual steps for setting up Google Account for testing:
                1. Go to Suitable Tech page "https://staging.suitabletech.com/accounts/login/"
                2. Click Sign-in with Google
                3. Click Create Account for creating Google Account
                4. Fill all Google Account information and keep sign-in to Suitable Tech page (email id = lgvnsuitabletech<number>@gmail.com, password = Logigear123)
                5. Logout Suitable Tech page.
                6. Update the newly Google Account to variable "GGAccCreatedBySTEmail" in "SuitableTech/common/constant.py" file
                7. Run automation.
        @precondition:
            C11662 is probably for the case where the user gets invited, clicks "Sign in with Google", but doesn't have a Google account,
            so they have to go through the process of setting up a google account before getting redirected back to our site
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            Using an existing Google account to login due to automation limitation:
            1. Login to Suitabletech.com
            2. Click "Sign in with Google" red button
            3. Enter the existing Google account
            4. Proceed to login
        @expected:
            Google account can log in to Suitabletech site.
        """
        try:
            # precondition
            google_account = GoogleAccount()
            google_account.generate_google_account_data()
            gmail = TestCondition.create_new_google_account(self._driver, google_account)

            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.email_address = gmail

            # steps
            welcome_page = LoginPage(self._driver).open().login_as_unwatched_google_user(user_info.email_address)

            # verify point
            self.assertTrue(welcome_page.is_logged_in(), "Assertion Error: The account login failed.")

        finally:
            # post-condition:
            TestCondition.delete_advanced_users([user_info])


    def test_c11293_email_notification_authentication_method_change_st_to_gsso_user(self):
        """
        @author: Thanh Le
        @date: 8/16/2016
        @summary: Email Notification: Authentication method change - ST to GSSO
        @precondition:  Create a Suitabletech account which not set up for GSSO (UserA@gmail.com)
        @steps:
            1) Navigate to the Suitable Tech Web login page URL:https://suitabletech.com/accounts/login/
            2) Select the "Sign in with Google" red button
            3) Sign in with the Suitabletech account in pre-condition (UserA@gmail.com) and proceed to "Confirm New Authentication Method" page
            4) Select "Yes" button
            5) Go to mailbox of this account and check for email notification
        @expected:
            3) Verify that you are presented with the following warning message before you can proceed:
            _Confirm New Authentication Method
            _WARNING: Only one authentication method is allowed per account
            _Do you really want to change your authentication method to Google? [Yes/No]
   
            4) User logs in to Suitabletech site successfully.
   
            5) The notification email sent as
            from: Suitable Technologies Support <support@suitabletech.com>
            to: "<user name>" <user'email>
            subject: Your authentication method has been changed
            mailed-by: <mailer.suitabletech.com>
            signed-by: <mailer.suitabletech.com>
   
            This email acknowledges that your authentication method has been changed to Google. You must use Google to login to the website and Beam client from now on.
   
            If you believe this is in error, please contact support@suitabletech.com.
        """
        try:
            # pre-condition:
            un_allowed_gsso_user = User() #DO NOT DELETE this user
            un_allowed_gsso_user.generate_un_allowed_gsso_user_data()
            TestCondition.create_advanced_unallowed_gsso_user(self._driver, un_allowed_gsso_user)
    
            self._driver = Driver.get_driver(DriverSetting.load())
            self._driver.maximize_window()
            GmailUtility.delete_all_emails(receiver=un_allowed_gsso_user.email_address)
   
            # steps:
            confirm_association_page = LoginPage(self._driver).open()\
                .goto_confirm_association_page(un_allowed_gsso_user.email_address, un_allowed_gsso_user.password)
   
            # verify point
            confirm_association_page.wait_page_ready(60)
            self.assertTrue(confirm_association_page.is_page_displayed(),
                            "Assert Error: Confirm New Authentication Method is NOT displayed!")
            self.assertTrue(
                Utilities.compare_HTML_texts(
                    confirm_association_page.get_warning_message(),
                    ApplicationConst.TXTF_CONFIRM_ASSOCIATION_WARNING_MESSAGE),
                "Assert Error: The Confirmation New Authentication Method message is NOT correct!")
   
            dashboard_page = confirm_association_page.change_auth()
   
            # verify point
            self.assertTrue(dashboard_page.is_page_displayed(),
                            "Assert Error: User logs in to Suitabletech site NOT successfully!")
            expected_gmail_message = EmailDetailHelper.generate_connect_google_change_auth_email(un_allowed_gsso_user.email_address)
            actual_gmail_message = GmailUtility.get_messages(expected_gmail_message.subject, sender=None, reply_to=None,
                                                              receiver=un_allowed_gsso_user.email_address, sent_day=datetime.now(), timeout=10)
            result = re.match(expected_gmail_message.trimmed_text_content, actual_gmail_message[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(expected_gmail_message.trimmed_text_content, actual_gmail_message[0].trimmed_text_content))
        finally:
            TestCondition.release_an_unallow_st_email(un_allowed_gsso_user.email_address)
   
   
    def c11675_sign_on_account_google_only_and_de_authorization_user_by_remove_google_account(self):
        """
        @author: duy.nguyen
        @date: 8/16/2016
        @summary: Sign-On Account (Google only) and DE AUTHORIZATION User by Remove Google Account
        @Note: Please follow below manual steps to set up Google email for testing:
                1. Create a Google Account "https://accounts.google.com/SignUp"
                2. Fill necessary account information (email id = lgvnsuitabletech<number>@gmail.com, password = Logigear123)
                3. Set auto-forward to "logigear1@suitabletech.com"
                4. Update the newly google account to variable "DeletedGoogleEmail" in "SuitableTech/common/constant.py" file
                5. Run automation
        @precondition:  Create a google account
            1. On Site Admin Dashboard, select the “Invite a New User” button
            2. Complete the invite form:
                • Using the same Google contact email address (i.e. suitabletester1@gmail.com)
                • select any target contact group(s)
                • select any target device group(s)
                • Review and personalize Invite email
            3. Click “Invite User” button
            4. Target contact will be notified via email of
                • Who Invited them (Organization)
                • What device group(s) they have been added to (derived from direct association and group association)
                • Login ID [email address]
                • Link to create a password / get client
            5. Go to mailbox and activate this user
            6. Logout out of the newly created user
    
        @steps:
            1. Delete the test Google Contact Account:(i.e. suitabletester2@gmail.com ) you created in the Precondition step.
            2. Navigate to the Suitable Tech Web login page URL:https://staging.suitabletech.com/accounts/login/
            3. Select the Google(or Social Network) Single Sign On button
        @expected:
            Verify that the previous Google Contact Account: can not be seen.
        """
        try:
            # pre-condition:
            google_account = GoogleAccount()
            google_account.generate_google_account_data()
            gmail = TestCondition.create_new_google_account(self._driver, google_account)
   
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
    
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.email_address = gmail
            user_info.password = Constant.DefaultPassword
            user_info.device_group = device_group
            user_info.organization = organization
            #Create new account without active
            TestCondition.create_advanced_normal_users(driver = self._driver, user_array = [user_info],activate_user=False)
    
            #active account
            TestCondition.active_user_with_new_gmail(driver = self._driver,user = user_info)
    
            # steps:
            GmailSignInPage(self._driver).open().log_in_gmail(user_info.email_address, user_info.password)\
                .remove_google_account()
                    
            self._driver.get(Constant.SuitableTechURL)    
                
            google_signin_page = LoginPage(self._driver).open()\
                .login_with_google_account_expecting_error(user_info.email_address)          
            # verify point:
            self.assertTrue(google_signin_page.is_google_error_message_displayed(),
                            "Assertion Error: The deleted google account still use GSSO Authentication")
                   
        finally:
            TestCondition.delete_advanced_users([user_info])
            TestCondition.delete_device_groups([device_group], organization)
 
 
    def c11674_sign_on_account_google_only_and_de_authorization_user_by_remove_authorization_gsso_auth_page(self):
        """
        @author: duy.nguyen
        @date: 8/19/2016
        @summary: Sign-On Account (Google only) and DE AUTHORIZATION User by Remove Google Account
        @note:  Please follow below manual steps to set up Google email for testing:
                1. Create a Google Account "https://accounts.google.com/SignUp"
                2. Fill necessary account information (email id = lgvnsuitabletech<number>@gmail.com, password = Logigear123)
                3. Set auto-forward to "logigear1@suitabletech.com"
                4. Update the newly google account to variable "NewGmailNonGSSOAuthenForwarded_01" in "SuitableTech/common/constant.py" file
                5. Run automation
        @precondition: Create a Google account (UserA@gmail.com)
            Create a Suitabletech user which has the same email with the above Google account as below steps:
                  
            Login to Suitabletech.com as an org admin and then select "Manage Your Beams"
            On dashboard page,select "Invite a New User" button
            Enter email address which is the same Google account above (UserA@gmail.com), firstname, lastname, select device group, and usergroup
            Click Invite button
            Go to this invited user's mailbox
            Click "Activate account" button on the "Welcome to Beam at <org name>" email
            Enter "New password" and "Confirm password"
            Log out this user
        @steps:
            1.Navigate to https://staging.suitabletech.com/accounts/login/
            2.Select "Sign in with Google" red button and sign in with the Google account in pre-condition (UserA@gmail.com)
            3.Proceed to login to Suitabletech site
            4.Select "Account Settings > Settings"
            5.Click on "Disconnect from Google" button
            6.Click "reset your password" link
            7.Enter email address and click "Reset my password" button
            8.Open mailbox of this user and set new password
            9.Log out this user
            10.Clear Browser history
            11.Navigate to https://staging.suitabletech.com/accounts/login/ again
            12.Select "Sign in with Google" red button
            13.Sign in with the same Google account above and proceed
            14.Click "Yes" button to accept
        @expected:
            (6). The "Disconnect Successful" page displays.
            (8). User logs in to Suitabletech site successfully.
            (13). The "Confirm New Authentication Method" page displays. 
            (14)
            _Verify that user logs in to Suitalbetech site successfully.
            _Verify that the "Your authentication method has been changed" email sent.
        """
        try:
            # pre-condition:
            google_account = GoogleAccount()
            google_account.generate_google_account_data()
            gmail = TestCondition.create_new_google_account(self._driver, google_account)
 
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.email_address = gmail
            user_info.device_group = Helper.generate_random_device_group_name()
            user_info.user_group = Helper.generate_random_user_group_name()
            user_info.password = Constant.DefaultPassword
                  
            expected_generate_email = EmailDetailHelper.generate_connect_google_change_auth_email(gmail)
            GmailUtility.delete_emails(expected_generate_email.subject, None, None, user_info.email_address, datetime.now())
                  
            TestCondition.create_user_group(user_info.user_group)
            TestCondition.create_device_group(user_info.device_group)
            TestCondition.create_advanced_normal_users(driver=self._driver, user_array=[user_info])
                  
            # steps:
            disassociate_page = LoginPage(self._driver).open().login_with_google_as_new_auth(gmail).change_auth(True)\
                .goto_account_settings_page_by_menu_item().disconect_from_google()
                  
            # verify point:
            self.assertTrue(disassociate_page.is_page_displayed(), "Assertion Error: There is no message Disconnect Successful display")
                  
            welcome_page = disassociate_page.reset_password(user_info)
                  
            # verify point:
            self.assertTrue(welcome_page.is_welcome_user_page_displayed(), "Assertion Error: User not login successfully")
                  
            welcome_page.logout().goto_login_page()
                  
            confirm_associate_page = LoginPage(self._driver).open().login_with_google_as_new_auth(gmail, Constant.DefaultPassword, True)
                  
            # verify point:
            self.assertTrue(confirm_associate_page.is_page_displayed(), "Assertion Error: The Confirm New Authentication Method page is not displays")
                  
            confirm_associate_page.change_auth(True)
                  
            # verify point:
            lst_notification_emails = GmailUtility.get_messages(expected_generate_email.subject, None, None, user_info.email_address, datetime.now())
            self.assertTrue(len(lst_notification_emails) == 3, "Assertion Error: The number of notification mail is not correct")
            result = re.match(expected_generate_email.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is '{}' but found '{}'".format(expected_generate_email.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
                   
        finally:
            TestCondition.delete_advanced_users([user_info])
            TestCondition.delete_user_groups([user_info.user_group])
            TestCondition.delete_device_groups([user_info.device_group])

