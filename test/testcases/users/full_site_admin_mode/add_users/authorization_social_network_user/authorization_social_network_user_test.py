from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from pages.suitable_tech.user.welcome_to_beam_page import WelcomeToBeamPage
from test.testbase import TestBase
from core.webdriver.drivers.driver import Driver
from common.application_constants import ApplicationConst
from core.webdriver.drivers.driversetting import DriverSetting
from core.utilities.utilities import Utilities
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime
from pages.suitable_tech.user.password_setup_page import PasswordSetupPage


class AuthorizationSocialNetworkUser_Test(TestBase):

    def test_c11664_suitabletech_account_existed_previously_non_first_time_user_authorized(self):
        """
        @author: tham.nguyen
        @date: 08/17/2016
        @summary: SuitableTech Account existed previously Non-First time user authorized
        @precondition:
            To add new user:
            1. Login to Suitabletech.com as an org admin and then select "Manage Your Beams"
            2. On dashboard page,select "Invite a New User" button
            3. Enter email address , firstname, lastname, select device group, and usergroup
            4. Click Invite button
            5. Log out of Suitabletech
        @steps:
            1) Go to new invited user in pre-condition mailbox
            2) Click "Activate account" button on the "Welcome to Beam at <org name>" email
            3) Enter "New password" and "Confirm password" then select "Set password" button
            4) Logout this user
            5) Go to Suitabletech and login again
            
        @expected:
            (5) . Verify that the "Welcome to Beam!" page displays that means user logins successfully.
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.user_group = user_group_name
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            TestCondition.create_device_group(device_group, [], organization)
            TestCondition.create_user_group(user_group_name)

            # steps
            LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .invite_new_user(normal_user)\
                .logout()
                
            activation_link = GmailUtility.get_email_activation_link(receiver=normal_user.email_address, sent_day=datetime.now())   
            welcome_page = PasswordSetupPage(self._driver, activation_link).set_password(normal_user.password)
                
            welcome_page = TestCondition.force_log_out(self._driver).goto_login_page()\
                .login_as_unwatched_video_user(normal_user.email_address, normal_user.password)
            
            # verify points
            self.assertTrue(welcome_page.is_welcome_user_page_displayed(),
                    "Assertion Failed: New user '{}' couldn't log in successfully after resetting his password".format(normal_user.email_address))
            
        finally:
            # post-condition
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group], organization)
            
        
    def test_c11665_suitabletech_account_not_existed_previously_first_time_user_authorized(self):
        """
        @author: tham.nguyen
        @date: 08/17/2016
        @summary: SuitableTech Account not existed previously First time user authorized
        @precondition:
            To add new user:
            1. Login to Suitabletech.com as an org admin and then select "Manage Your Beams"
            2. On dashboard page,select "Invite a New User" button
            3. Enter email address , firstname, lastname, select device group, and usergroup
            4. Click Invite button
            5. Log out of Suitabletech
        @steps:
            1. Go to new invited user in pre-condition mailbox
            2. Click "Activate account" button on the "Welcome to Beam at <org name>" email
            3. Enter "New password" and "Confirm password" then select "Set password" button
            
        @expected:
            (3). Verify that the "Welcome to Beam!" page displays that means user logins successfully.
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.user_group = user_group_name
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            TestCondition.create_device_group(device_group, [], organization)
            TestCondition.create_user_group(user_group_name)
            
            # steps
            LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .invite_new_user(normal_user)\
                .logout()
                
            activation_link = GmailUtility.get_email_activation_link(receiver=normal_user.email_address, sent_day=datetime.now())   
            welcome_page = PasswordSetupPage(self._driver, activation_link).set_password(normal_user.password)
               
            # verify points                       
            self.assertTrue(welcome_page.is_welcome_user_page_displayed(),
                    "Assertion Failed: New user '{}' couldn't log in successfully after resetting his password".format(normal_user.email_address))
            
        finally:
            # post-condition
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group], organization)
            
            
    def test_c11667_single_sign_on_account_suitabletech_only_and_account_state_already_logged_into_suitabletech_at_time_of_sign_on(self):
        """
        @author: khoi.ngo
        @date: 8/15/2016
        @summary: Single Sign-On Account (SuitableTech only) and account state (already logged into SuitableTech at time of sign-on)
        @precondition: 
            To add new user (Suitabletech account):
                1. Login to Suitabletech.com as an org admin and then select "Manage Your Beams"
                2. On dashboard page,select "Invite a New User" button
                3. Enter email address (UserA), firstname, lastname, select device group, and usergroup
                4. Click Invite button
                5. Go to this invited user's mailbox
                6. Click "Activate account" button on the "Welcome to Beam at <org name>" email
                7. Enter "New password" and "Confirm password"
                8. User log in to Suitabletech site and do not logout
        @steps:
            1. On the same browser which the account in pre-condition are logging in, open a new tab
            2. Navigate to https://staging.suitabletech.com/accounts/login/
        @expected:
            The Welcome page of current logged user (UserA) displays.
        """
        try:
            # precondition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            temp_device_group_name = Helper.generate_random_device_group_name()
            normal_user.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            
            # steps
            LoginPage(self._driver).open().login_as_unwatched_video_user(normal_user.email_address, normal_user.password)
            self._driver.open_new_tab(Constant.SuitableTechLoginURL)
            welcome_to_beam_page = WelcomeToBeamPage(self._driver)
            
            # verify point
            self.assertTrue(welcome_to_beam_page.is_welcome_user_page_displayed(), "Assertion Error: User cannot login.")
            
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([temp_device_group_name])
            
            
    def test_c11663_a_suitable_user_who_does_not_want_to_migrate_to_a_gsso_user(self):
        """
        @author: khoi.ngo
        @date: 8/16/2016
        @summary: A suitable user who does not want to migrate to a GSSO user
        @precondition: 
            Create a Google account (UserA@gmail.com)
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
            1. Navigate to https://staging.suitabletech.com/accounts/login/
            2. Select "Sign in with Google" red button and sign in with the Google account in pre-condition (UserA@gmail.com)
            3. Proceed to login to Suitabletech site
            4. Select "Account Settings > Settings"
            5. Click on "Disconnect from Google" button
            6. Click "reset your password" link
            7. Enter email address and click "Reset my password" button
            8. Open mailbox of this user and set new password
            9. Log out this user
            10. Clear Browser history
            11. Navigate to https://staging.suitabletech.com/accounts/login/ again
            12. Select "Sign in with Google" red button
            13. Sign in with the same Google account above and proceed
            14. Click "No" button to decline
        @expected:
            (6). The "Disconnect Successful" page displays.
            (8). User logs in to Suitabletech site successfully.
            (13). The "Confirm New Authentication Method" page displays.
            (14) Login page displays.
        """
        try:
            # precondition
            non_gsso_user = User()
            non_gsso_user.generate_un_allowed_gsso_user_data()
            TestCondition.create_advanced_non_gsso_user(driver=self._driver, user=non_gsso_user)
            
            # steps
            simplied_dashboard = LoginPage(self._driver).open()\
                .login_with_google_as_new_auth(non_gsso_user.email_address, non_gsso_user.password, logged_in_before=True)\
                .change_auth(True)
            
            # step
            disconect_page = simplied_dashboard.goto_your_account().disconect_from_google()
            
            # verify point
            self.assertTrue(disconect_page.is_page_displayed(), "Assertion Error: Disconnect Successful page is not display")

            # steps
            simplified_dashboard_page = disconect_page.reset_password(non_gsso_user)
            
            # verify point
            self.assertTrue(simplified_dashboard_page.is_page_displayed(), "Assertion Error: User log in to Suitabletech site failed.")
            
            # steps
            login_page = simplified_dashboard_page.logout().goto_login_page()
            
            # verify point
            confirm_association_page = login_page.login_with_google_as_new_auth(non_gsso_user.email_address, non_gsso_user.password, logged_in_before=True)
            confirm_msg_displayed = confirm_association_page.is_page_displayed()
            self.assertTrue(confirm_msg_displayed, "Assertion Error: The Confirm New Authentication page is not displays.")
            login_page = confirm_association_page.change_auth(False)
            
            self.assertTrue(login_page.is_page_displayed(), "Assertion Error: Login pages is not display.")
            
        finally:
            # post-condition:
            TestCondition.release_an_unallow_st_email(non_gsso_user.email_address)
            try:
                GmailUtility.delete_all_emails(non_gsso_user.email_address)
            except:
                pass
        
        
    def test_c11666_single_sign_on_account_google_only_and_account_state_already_logged_into_google_at_time_of_sign_on(self):
        """
        @author: khoi.ngo
        @date: 8/15/2016
        @summary: Single Sign-On Account (Google only) and account state (already logged into Google at time of sign-on)
        @precondition: Create an GSSO account (UserA@gmail.com)
        @steps:
            1. Navigate to the Suitable Tech Web login page URL:https://suitabletech.com/accounts/login/
            2. Select the "Sign in with Google" red button
            3. Sign in with the account in pre-condition
            4. Open a new browser tab and navigate to https://staging.suitabletech.com/accounts/login/
            5. Select the Sign in with Google" red button
            6. Proceed to login
        @expected:
            Verify that the account is successfully logged into the Suitabletech. 
        """
        try:
            # precondition
            gsso_user = User()
            gsso_user.generate_un_allowed_gsso_user_data()
            TestCondition.create_advanced_gsso_user(self._driver, gsso_user)
        
            # steps
            LoginPage(self._driver).open()\
                .login_with_google_as_new_auth(gsso_user.email_address, gsso_user.password, logged_in_before=True)
            
            self._driver.open_new_tab(Constant.SuitableTechURL)
            is_user_logged_in = LoginPage(self._driver).open().is_logged_in()

            # verify point
            self.assertTrue(is_user_logged_in, "Assertion Error: The account login failed.")
        finally:
            TestCondition.release_an_unallow_st_email(gsso_user.email_address)
        
        
    def test_c11668_single_sign_on_account_suitabletech_accept_conditions_for_moving_to_GSSO(self):
        """
        @author: duy.nguyen
        @date: 8/4/2016
        @summary: Single Sign-On Account (SuitableTech) Accept Conditions for moving to GSSO (yes)
        @precondition: Pre-existing suitable account that is authenticated with their suitable tech user/pass (i.e. not set up for GSSO)
        @note: This test case need a Google Account which have ST Authentication. So we can automate this testcase without create anything.
        @steps:
            1. Navigate to the Suitable Tech Web login page URL:https://suitabletech.com/accounts/login/
            2. Select the Google(or Social Network) Single Sign On button
            3. Sign on by using the red "sign on with Google button" that is the same google account that you created in the Preconditions steps:(i.e. Add new Google Contact Account, suitabletester2@gmail.com)
            4. Verify that you are presented with the following warning message before you can proceed:
                • Confirm New Authentication Method
                • WARNING: Only one authentication method is allowed per account
                • Do you really want to change your authentication method to Google? [Yes/No]
            5. Select "Yes" to conform you want to change your SuitableTech Account authentication method to Google
            6. Verify that we are successfully logged into the Suitable Tech Web Account 
        @expected:
            New user account is able to successfully sign on with their Google Account. 
        """  
        try:
            # precondition
            non_gsso_user = User()
            non_gsso_user.generate_non_gsso_user_data()
            TestCondition.create_advanced_non_gsso_user(driver=self._driver, user=non_gsso_user)
            
            # steps
            confirm_page = LoginPage(self._driver).open()\
                .login_with_google_as_new_auth(non_gsso_user.email_address, non_gsso_user.password, True)
               
            # verify point
            self.assertTrue(Utilities.compare_HTML_texts(confirm_page.get_warning_message(), ApplicationConst.TXTF_CONFIRM_ASSOCIATION_WARNING_MESSAGE), "Assertion Error: Warning message's content is not correct")
            #self.assertEqual(confirm_page.get_warning_message(), ApplicationConst.TXTF_CONFIRM_ASSOCIATION_WARNING_MESSAGE, "Assertion Error: Warning message's content is not correct")
            
            welcome_page = confirm_page.change_auth(True)
            # verify point
            self.assertTrue(welcome_page.is_page_displayed(), "Assertion Error: The account login failed.")
            
        finally:
            # post-condition
            TestCondition.release_an_allow_st_email(non_gsso_user.email_address)

            
    def test_c11669_google_single_sign_on_account_accept_conditions_for_moving_to_suitabletech_account(self):
        """
        @author: duy.nguyen
        @date: 8/4/2016
        @summary: Single Sign-On Account (Google) Accept Conditions for moving to SuitableTech Account (yes)
        @precondition: Login using an existing suitable account that has GSSO authentication
        @note: This test case need a Google Account which have GSSO Authentication. So we can automate it without create anything.
        @steps:
            1. Login to the account: https://suitabletech.com/accounts/login/ with the user in pre-condition
            2. Select "Account Settings" in drop-down menu under username on top-right page
            3. Select the "Settings" tab on the left-hand side
            4. Under the "Security" field, select "Disconnect from Google" button
        @expected:
            Verify that the "Disconnect Successful" page displays.
            Verify that the your account is unable to login using your the Suitabletech.com credentials.
        """  
        try:
            # pre-condition:
            gsso_user = User()
            gsso_user.generate_non_gsso_user_data()
            TestCondition.create_advanced_gsso_user(self._driver, gsso_user)
            
            # step:
            disassociate_page = LoginPage(self._driver).open()\
                    .login_with_google(gsso_user.email_address, gsso_user.password)\
                    .goto_your_account()\
                    .disconect_from_google()
            
            # verify point
            self.assertTrue(disassociate_page.is_page_displayed(), "Assertion Error: Disassociate page is not displayed")
            self.assertFalse(disassociate_page.is_logged_in(), "Assertion Error: Use is still logged in")
            
            login_page = disassociate_page.goto_login_page()\
                .login_expecting_error(gsso_user.email_address, gsso_user.password)

            self.assertTrue(login_page.is_page_displayed(), "Assertion Error: User still can access to Suitable Page")
        finally:
            TestCondition.release_an_allow_st_email(gsso_user.email_address)


    def test_c11670_suitableTech_account_decline_conditions_for_moving_to_GSSO(self):
        """
        @author: duy.nguyen
        @date: 8/5/2016
        @summary: Single Sign-On: (SuitableTech Account) Decline Conditions for moving to GSSO (No)
        @precondition:  Clear browser cookie making sure there is no Google account signed in beforehand
                        Create a Google account (UserA@gmail.com)
        @note: This test case require a Google Account which never access to ST page. So we can automate without create anything.
        @steps:
            1. Login to the account: https://suitabletech.com/accounts/login/
            2. Select "Sign in with Google" red button
            3. Enter email/ password and do proceed
            4. Select "Deny" button to decline
        @expected:
           (3) The "Beam world like to: View your email address/ View your basic info" page displays.
            (4) Login page displays for re-login.
        """  
        try:
            # pre-condition:
            non_gsso_user = User() # DO NOT DELETE this user
            non_gsso_user.generate_un_allowed_gsso_user_data()
            TestCondition.create_advanced_unallowed_gsso_user(self._driver, non_gsso_user)
            
            self._driver = Driver.get_driver(DriverSetting.load())
            self._driver.maximize_window()
            
            # steps:
            confirm_association_page = LoginPage(self._driver).open()\
                .goto_confirm_association_page(non_gsso_user.email_address, non_gsso_user.password)
            
            # verify point:
            self.assertTrue(confirm_association_page.is_page_displayed(),\
                            "Assertion Error: There is no confirm association page display")
            
            login_page = confirm_association_page.decline_change_authentication()
            
            # verify point
            self.assertTrue(login_page.is_page_displayed(), "Assertion Error: Login page is not display")
                        
        finally:
            TestCondition.release_an_unallow_st_email(non_gsso_user.email_address)
        
        