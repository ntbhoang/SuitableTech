import re
from common.helper import Helper
from data_test.dataobjects.user import User
from core.utilities.gmail_utility import GmailUtility
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import EmailDetailHelper
from common.constant import Constant
from common.application_constants import ApplicationConst
from core.suitabletechapis.device_group_api import DeviceGroupAPI
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
import pytest


class SettingTest(TestBase):

    @pytest.mark.OnlyDesktop
    def test_c11080_create_api_keys(self):
        """
        @author: Khoi Ngo
        @date: 8/9/2016
        @summary: Create API Keys and Set Email Notifications Contacts
        @Precondtions: There is an org admin.
        @steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Select the "Settings" icon on far left of screen (looks like a cog)
            3. Enter a name for the new Key in the field provided
            4. Click on "Create New API key" button
        @expected:
            1. Your new API Key entry will be created with your Key name entered.
            2. The message "Your new API key is: '<API key>'. Please copy this key (without surrounding quotes)
                 and store it somewhere safe. Once you have this page, you will no longer have access to the secret portion of this key.\
                 For more information on how to use API keys, please check out the Web API Documentation Page" appears.
        """
        try:
            # steps
            key_name = Helper.generate_random_string()
            
            authentication_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()\
                .open_authentication_tab()\
                .create_api_key(key_name)
                
            text_msg_alert = authentication_page.get_text_msg()
            
            # verify points
            self.assertTrue(authentication_page.is_api_key_existed(key_name), "Assertion Error: API is not created.")
            
            # check text exists
            is_msg_corrected = re.match(ApplicationConst.INFO_MSG_NEW_API_NOTICE, text_msg_alert)
            self.assertTrue(is_msg_corrected, "Assertion Error: Message alert is not correct. Message: " + text_msg_alert)
        finally:
            # post-condition
            authentication_page.delete_api_key(key_name)
            

    def test_c11081_set_email_notifications_sender_information(self):
        """
        @author: Duy Nguyen
        @date: 8/29/2016
        @summary: Set Email Notifications Sender Information
        @Precondtions: 
            Create a Device group and add a Device Group Admin
        @steps:
            1) Login to Suitabletech.com and select "Manage Your Beams" from the user dropdown menu.
            2) In the upper right section of the admin page, you should see the Organization Settings (Gear icon). Click on the Gear icon
            3) Enter a "From" name for Email Notifications
            4) Using API to delete the Device Group created in Precondition
        @expected:
            Verify that Email notifications have the "From" field set to the Email address entered in the 
            "settings->Email Notifications Sender Information"
        """
        try:
            # precondition
            admin_device = User()
            admin_device.generate_advanced_device_group_admin_data()
            device_group_name = Helper.generate_random_device_group_name()
            admin_device.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_device])
            
            LoginPage(self._driver).open()\
                .login(admin_device.email_address, admin_device.password)\
                .goto_your_account()\
                .goto_notifications_tab()\
                    .toggle_device_groups_are_added_or_removed()\
                    .logout()
                
            # steps:
            org_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()
                
            origin_notification_sender = org_setting_page.get_email_notifications_name()
            
            test_notification_sender = Helper.generate_random_string()
            org_setting_page.submit_email_notifications_name(test_notification_sender).logout()
            DeviceGroupAPI.delete_device_group(device_group_name, Constant.AdvancedOrgName)

            # verify point:
            email_expected = EmailDetailHelper.generate_delete_device_group_email(admin_device, Constant.AdvancedOrgName)
            actual_email = GmailUtility.get_messages(mail_subject=email_expected.subject, receiver=admin_device.email_address)
            self.assertEqual(len(actual_email), 1, "Assertion Error: The number of return email is incorrect")
            self.assertIn(test_notification_sender, actual_email[0].sender,\
                        "Assertion Error: Email Notification is {} while expectation is {}".format(actual_email[0].sender, test_notification_sender))
        
        finally:
            # post-condition
            TestCondition.set_organization_setting("email notifications", origin_notification_sender)


    @pytest.mark.OnlyMobile
    def test_c34004_mobile_not_allow_to_create_API_keys(self):
        """
        @author: Khoi Ngo
        @date: 2/28/2018
        @summary: Mobile: Not allow to create API keys
        @Precondtions:
            Login as org admin on mobile site.
        @steps:
            1) Open the top navigation
            2) Select Organization
            3) Go to Authentication
            4) Scroll to API Keys section
        @expected:
            1) Verify that the message "API key generation not available on mobile site." displays.
            2) Verify that no Create New API Key button.
        """

        try:
            # steps:
            authentication_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()\
                .open_authentication_tab()

            # verify points:
            self.assertFalse(authentication_page.is_create_new_api_key_btn_displayed(), "Assertion Error: Create New API button is still displayed.")
            #TODO: Failed by bug #INFR-2711
            self.assertEqual(authentication_page.get_api_alert_msg(), ApplicationConst.INFO_MOBILE_MSG_CREATE_API, "Assertion Error: Content of API alert message is incorrect.")

        finally:
            pass
