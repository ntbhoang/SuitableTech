from _datetime import datetime
import re
from common.application_constants import ApplicationConst
from common.constant import Constant, Platform
from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from test.testbase import TestBase
from core.utilities.utilities import Utilities, Image_Utilities
import pytest


class OrganizationAdmin_Test(TestBase):
     
    def test_c10930_remove_an_admin_1_x(self):
        """
        @author: khoi.ngo
        @date: 7/21/2016
        @summary: Remove an admin [1.X]
        @precondition: Verify that the user is an org admin
            1. Go to the "Users" tab under the "Manage your Beams" dashboard
            2. click on the desired user
            3. Verify that the "Administrator" field says "Yes" adjacent to the user image icon
        @steps:
            1. Go to the "User" tab under the "Manage your Beams" Admin dashboard
            2. Find a user that is an admin by clicking the show button and selecting "administrators only"
            3. Once an admin user is found, click on the edit box under the User name in the "Users" tab
            4. Unselect the "Allow this user to administer this organization"
        @expected:
            1. The admin will see a green "User was successfully saved" message
            2. The user that was removed as an admin will receive an email summarizing these changes
            3. The "Administrator" string should say "No" indicating that this user is no longer an admin of the organization being viewed.
        """
        try:
            # precondition
            org_admin1 = User()
            org_admin1.generate_org_admin_user_data()
            
            org_admin2 = User()
            org_admin2.generate_advanced_org_admin_data()
            
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin2])
            # steps
            user_detail_page = LoginPage(self._driver).open()\
                .login(org_admin1.email_address, org_admin1.password)\
                .goto_users_tab()\
                .goto_user_detail_page(org_admin2).edit_user(allow_administer = False, wait_for_completed = False)
            
            msg_success_text = user_detail_page.get_msg_success()   
            user_detail_page.wait_untill_success_msg_disappeared()
            
            # verify checkpoint 1
            self.assertEqual(msg_success_text, ApplicationConst.INFO_MSG_EDIT_USER_SUCCESS, "Assertion Error: The success message is not display")

            # verify checkpoint 2
            expected_email = EmailDetailHelper.generate_removed_from_org_admin_email(organization_name=Constant.AdvancedOrgName, admin_full_name=org_admin1.get_displayed_name())
            actual_emails = GmailUtility.get_messages(expected_email.subject, receiver=org_admin2.email_address)
            
            self.assertEqual(1, len(actual_emails), "Assertion Error: There should be only one email notification sent to User")
            self.assertEqual(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content, "Email content is not sent as expected. Expected email content is:\n'{}' but found:\n'{}'".format(expected_email.trimmed_text_content, actual_emails[0].trimmed_text_content))

            # verify checkpoint 3
            self.assertTrue(user_detail_page.is_administator_label_notice(ApplicationConst.LBL_NO), "Assertion Error: User is still Administrator of this organization")

        finally:
            # post-condition
            TestCondition.delete_advanced_users([org_admin2])
         
 
    def test_c10932_non_admin_user_does_not_have_access_to_manage_your_beams_functionality_detailed_steps_1_x(self):
        """
        @author: Quang.Tran
        @date: 7/21/2016
        @summary: Non Admin User does not have access to Manage Your Beams functionality (detailed steps) [1.X] 
        @preconditions:          
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            A user account that does not have admin privileges.
             
        @steps:
            Step 1. Ensure that test user: suitabletechqa2@gmail.com (pw: Baconisgood1) is not set as org admin or device group admin
            Step 2. Login to:https://staging.suitabletech.com/ as test user:suitabletechqa2@gmail.com
            Step 3. Verify Home page displays
             
        @expected:
            Verify Home page displays
        """
        try:
            organization = Constant.AdvancedOrgName
            non_admin_user = User()
            non_admin_user.generate_advanced_normal_user_data()
            non_admin_user.organization = organization
            TestCondition.create_advanced_normal_users(self._driver, [non_admin_user])
            
            # pre-condition              
            home_page = LoginPage(self._driver).open()\
                .login(non_admin_user.email_address, non_admin_user.password, simplifiedUser=True)
            
            # steps and verify 
            self.assertTrue(home_page.is_page_displayed(),
                            "Assertion Error: Manages Your Beams existed in Dropdownlist User Menu")
             
        finally:
            TestCondition.delete_advanced_users([non_admin_user])
            
 
    def test_c10933_site_admin_for_multiple_organizations_see_a_dropdown_list_to_select_site_1_x(self):
        """
        @author: khoi.ngo
        @date: 8/1/2016
        @summary: Manage Your Beams admin for multiple organizations sees a dropdown list to select site [1.X]
        @precondition: An admin account of at least two org's is required for this test.
        @steps:
            1) Login to Suitabletech.com and select "Manage Your Beams" from the user dropdown menu.
            2) In the upper right section of the admin page, you should see the organization name. 
                Click on the name and a dropdown list appears. Try to toggle to a different org.
        @expected:
            You are able to successfully toggle to different organizations.
        """
        try:
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)
             
            current_organization_name = admin_dashboard_page.get_organization_name()
            new_organization_name = admin_dashboard_page.goto_another_org(Constant.AdvancedOrgName_2)\
                .get_organization_name()

            # verify point               
            self.assertNotEqual(current_organization_name, new_organization_name,
                                "Assertion Error: Cannot change organization")
        finally:
            pass
        
      
    def test_c10937_add_a_new_user_no_group_no_email_copy_1_x(self):
        """
        @author: Duy.Nguyen
        @date: 7/21/2016
        @summary: Add a new user (no group, no email copy) [1.X]
        @preconditions:
            1. Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Login to Suitabletech.com and go to the manage your Beams advanced UI. 
        @steps:
            1. 1) Go to the "Users" tab under the "Manage your Beams" dashboard
            2. Click the box that says "Invite User"
            3. Fill out the required information in the next window but do not add the new user to a device group or user group and do not click the "Email a copy to myself" box
            DO NOT! do the following:
                - Add the user to a device group/user group
                - Check-box to send Email copy to site Admin
        @expected:
            The invited user receives an email confirming that he/she has been invited to a Beam organization (either email template is fine as the test does not specify if user is in database)
        """
        try: 
            # precondition
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.device_group = None
            user_info.user_group = None
            user_info.invitation_settings.include_a_link_to_the_beam_software = True
            
            org_admin = User()
            org_admin.advanced_org_admin_data()
            
            # steps
            LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_new_user(user = user_info)
                
            # verify point:
            welcome_mail = EmailDetailHelper.generate_welcome_email(user_info, org_admin.get_displayed_name())
            lst_notification_emails = GmailUtility.get_messages(mail_subject=welcome_mail.subject, reply_to=org_admin.email_address, receiver=user_info.email_address)
            self.assertTrue(len(lst_notification_emails) == 1, "Assertion Error: Suitable Tech was returned more than 1 email")
            result = re.match(welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
                        
        finally:
            # Clean up     
            TestCondition.delete_advanced_users([user_info])
            
            
    def test_c10938_add_new_user_not_in_db_1_x(self):
        """
        @author: Tham.Nguyen
        @date: 7/21/2016
        @summary: C10938: Add new user not in the database [1.X] 
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1. Go to the "Manage your Beams" dashboard on suitabletech.com 
            2. Click â€œInvite a new Userâ€�
            3. Fill out the Invite a new user form, enter the userâ€™s name that is not in the ST database, and has valid email address
        @expected:
            1. Make sure the user is successfully added to the organization by clicking on the users tab and locating their user profile.
            2. User receives a confirmation email
        """
        try:
            # pre-condition
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            
            org_admin = User()
            org_admin.advanced_org_admin_data()
            
            # steps
            admin_user_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_new_user(user=user_info)\
                .goto_users_tab()
                
            # verify point
            self.assertTrue(admin_user_page.is_user_existed(user_info.email_address, user_info.get_displayed_name()),
                            "Assertion Error: Email '" + user_info.get_displayed_name() + "' wasn't created successfully")
            
            expected_wc_email = EmailDetailHelper.generate_welcome_email(user_info, org_admin.get_displayed_name())
            lst_wc_emails = GmailUtility.get_messages(mail_subject=expected_wc_email.subject, reply_to=org_admin.email_address, receiver=user_info.email_address)
            
            self.assertTrue(len(lst_wc_emails) == 1,
                            "Assertion Error: '{}' was returned more than 1 email to normal user '{}'. The number of email return is '{}'".format(expected_wc_email.subject, user_info.email_address, len(lst_wc_emails)))
            does_email_match = re.match(expected_wc_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(does_email_match,
                            "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_wc_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content))
            
        finally:
            # post-condition
            TestCondition.delete_advanced_users([user_info])
         
         
    def test_c10939_add_a_user_already_exists_in_another_organization_1_x(self):
        """
        @author: khuongduy.nguyen
        @date: 7/21/2016
        @summary: Add a user that already exists in another organization [1.X]
        @precondition: Admin account of 2 organizations that the desired user account is not already a member of.
        Login to Suitabletech.com and go to the advanced management UI.
        @steps:
            1) Go to the "Users" tab under the "Manage your Beams" dashboard and invite the desired user to the new organization.
            2) Switch orgs by selecting the org name in the top right corner. 
            3) Confirm that the desired user is not listed under the "Users" tab in the "Manage your beams" dashboard
            4) Invite the desired user to the new organization
        @expected:
            The same user record should be added to the new organization as well. The user will now be in both. This can be confirmed by checking under the "Users" tab in both of the organizations
        """            
        try:
            # Pre-condition:
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.invitation_settings.include_the_default_invitation_message = None
            
            multi_org_admin= User()                                            
            multi_org_admin.generate_advanced_org_admin_data()
            TestCondition.create_advanced_multi_organization_admin(self._driver, multi_org_admin)
             
            # steps:
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(multi_org_admin.email_address, multi_org_admin.password)

            admin_user_page = admin_dashboard_page.invite_new_user(user_info)\
                .goto_another_org(Constant.AdvancedOrgName_2)\
                .goto_users_tab()
             
            # verify point
            user_display_name = user_info.get_displayed_name()
            self.assertTrue(admin_user_page.is_user_not_existed(user_info.email_address, user_display_name),
                             "Assertion Error: The desired user appears in this organization")
            # handle for edge
            admin_user_page = admin_user_page.goto_dashboard_tab().goto_users_tab().invite_new_user(user_info)\
                .goto_users_tab()
             
            # verify point
            self.assertTrue(admin_user_page.is_user_existed(user_info.email_address, user_display_name),
                             "Assertion Error: The desired user does not appear in this organization")
             
            admin_user_page.goto_another_org(Constant.AdvancedOrgName).goto_users_tab()
             
            # verify point
            self.assertTrue(admin_user_page.is_user_existed(user_info.email_address, user_display_name),
                             "Assertion Error: The desired user does not appear in this organization")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([user_info, multi_org_admin], organization=Constant.AdvancedOrgName)
            TestCondition.delete_advanced_users([user_info, multi_org_admin], organization=Constant.AdvancedOrgName_2)
 
 
    def test_c10940_add_a_new_user_with_an_initial_group_chosen_1_x(self):
        """
        @author: thanh.viet.le
        @date: 7/28/2016
        @summary: Add a new user with an initial group chosen [1.X] 
        @precondition: Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1) Go to the "Users" tab under the "Manage your Beams" dashboard
            2) Click the box that says "Invite User"
            3) Fill out the required information in the next window and make sure to add the user to a Device group
        @expected:
            Make sure the user is successfully added to the device group by clicking the "Beams" tab, selecting the device group icon that the user account was invited to, and selecting "members". The user desired user account should be listed under users.
            User account should also receive a confirmation email *(either template is fine depending on if user account already exists in database)
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
            TestCondition.create_device_group(device_group_name, devices, organization_name)
            
            user = User()
            user.generate_advanced_normal_user_data()
            user.device_group = device_group_name
            
            
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            # steps
            admin_beams_members_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()\
                .invite_new_user(user)\
                .goto_members_tab_of_a_device_group(device_group_name)
                
            is_user_exist_in_device_group = admin_beams_members_page.is_user_existed(user.email_address, user.get_displayed_name())
            self.assertTrue(is_user_exist_in_device_group, "Assertion Error: The invited User is not displayed in Device Group's Users list")
            
            expected_wc_email = EmailDetailHelper.generate_welcome_email(user, org_admin.get_displayed_name())
            lst_wc_emails = GmailUtility.get_messages(mail_subject=expected_wc_email.subject, reply_to=org_admin.email_address, receiver=user.email_address)
            
            self.assertTrue(len(lst_wc_emails) == 1,
                            "Assertion Error: '{}' was returned more than 1 email to normal user '{}'. The number of email return is '{}'".format(expected_wc_email.subject, user.email_address, len(lst_wc_emails)))
            does_email_match = re.match(expected_wc_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(does_email_match,
                            "Assertion Error: Expected email content is:\n'{}' but found:\n'{}'".format(expected_wc_email.trimmed_text_content, lst_wc_emails[0].trimmed_text_content))
            
        finally:
            # post-condition
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([user, org_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)
            
        
    def test_c10941_add_new_user_and_send_copy_email_to_site_admin_1_x(self):
        """
        @author: Tham.Nguyen
        @date: 7/21/2016
        @summary: Add a new user and send a copy of the email to the site admin [1.X] 
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1. Log into the Suitabletech.com and navigate to the advanced "Manage your Beams" page.
            2. Click â€œInvite a new Userâ€� button from the dashboard. 
            3. Enter the userâ€™s name and email address (they will receive an email),
                DO the following:
                Add the user to a device group
                Check-box to send Email copy to site Admin
        @expected:
            1. Verify a copy of the email is received by the admin, with a header banner and the link removed.
        """
        try:
            # pre-conditions
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.invitation_settings.email_a_copy_to_myself = True
            
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            # steps
            LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_new_user(user=user_info)
                
            expected_email = EmailDetailHelper.generate_welcome_admin_copy_email(user_info, org_admin.get_displayed_name())
            lst_messages = GmailUtility.get_messages(mail_subject=expected_email.subject, receiver=org_admin.email_address, sent_day=datetime.now())
            
            flag = False
            if lst_messages:
                for g_message in lst_messages:
                    if(g_message.html_content.find(user_info.email_address) >= 0 and g_message.html_content.find("Removed") >= 0 
                       and g_message.html_content.find("https://dm92u2vspm71b.cloudfront.net/static/site/img/beam_logo.png") >= 0):
                        flag = True
                        break
            # verify points
            self.assertTrue(flag, "Assertion Error: Org admin '{}' doesn't receive a copy of the email inviting a new user '{}'".format(org_admin.get_displayed_name(), user_info.email_address))
        finally:    
            # post-condition
            TestCondition.delete_advanced_users([user_info, org_admin])
         
     
    def test_c10929_add_an_existing_user_as_an_admin(self):
        """
        @author: Duy.Nguyen
        @date: 7/20/2016
        @summary: C10929: Add an existing user as an admin [1.X]
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
             
            Existing User added to an Org
            1) Click on the "Users" tab in the "Manage your Beams" Dashboard (need to be an admin of the org)
            2) Click on "Invite User" (adding them to org of your choosing)
            3) Go to the choosen user's email account; follow the instructions
            --> Expected Result
            The choosen user is now listed under the "Users" Tab in the "Manage your Beams" Advanced admin dashboard
     
        @steps:
            1) Go to the "Users" tab
            2) click the icon for the existing user of choice
            3) Click the "Edit" box directly below the user's name
            4) check the box that states "Allow this user to administer this organization"; save changes
        @expected:
            -->Green box appears saying that the "The user was successfully saved"
            -->The "Administrator" string says "Yes"
            --> the choosen user given admin priviledges receives an email confirming that they are now an admin
        """   
        try:
            # Pre-Condition:
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
            
            new_user = User()
            new_user.generate_advanced_normal_user_data()
            new_user.device_group = device_group
            new_user.organization = organization
            
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            TestCondition.create_advanced_organization_admins(driver=self._driver, user_array=[org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [new_user])
            
            # Test Case Steps:    
            user_detail_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()\
                .goto_user_detail_page(new_user)\
                .edit_user(allow_administer = True, wait_for_completed = False)
            
            self.assertEqual(user_detail_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_USER_SUCCESS, "Assertion Error: The success message is not display")
            self.assertEqual(user_detail_page.get_user_info(ApplicationConst.LBL_ADMINISTRATOR), ApplicationConst.LBL_YES, "Assertion Error: Administrator label does not display as Yes")
            
            expected_email = EmailDetailHelper.generate_added_to_org_admin_email(new_user.organization, org_admin.get_displayed_name())
            actual_email = GmailUtility.get_messages(mail_subject=expected_email.subject, receiver=new_user.email_address, sent_day=datetime.now())
            self.assertEqual(len(actual_email), 1, "Assertion Error: The number of return email is not correct")
            self.assertEqual(expected_email.trimmed_text_content, actual_email[0].trimmed_text_content, \
            "Assertion Error: The content of return email is not correct. The expected content is '{}' but the actual content is '{}'".format(expected_email.trimmed_text_content, actual_email[0].trimmed_text_content))
        
        finally:               
            # Cleanup
            TestCondition.delete_advanced_users([new_user, org_admin])
            TestCondition.delete_device_groups([device_group], organization)
     
      
    def test_c11082_users_search(self):
        """
        @author: tham.nguyen
        @date: 7/21/2016
        @summary: "Users" Search - Icon View 
        @precondition: Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                    http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:        
            1) Go to the "Manage your Beams" dashboard
            2) Go to the "Users" tab
            3) Search for the userâ€™s ID or email address for the following users:
                Search for email : KhKorean@suitabletech.com
                Search for User Name: KhKorean ê¸°í˜�ê¶Œ
                Search for email : IrishFada@suitabletech.com
                Search for User Name: IrishFada SinÃ©ad_Ã¡Ã©Ã­Ã³Ãº
            4) Click â€œUsersâ€� button link after each search result, verify that you get the default â€œUsersâ€� page
        @expected:
            Verify that you are able to search for a user
        """
        try:
            # steps
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
            
            user_info = User()
            user_info.generate_advanced_normal_user_data()
            user_info.first_name = "Advanced Normal User " + Helper.generate_random_string(length=4)
            user_info.last_name = "LN " + Helper.generate_random_string()
            user_info.device_group = device_group
            user_info.organization = organization
            TestCondition.create_advanced_normal_users(self._driver, [user_info])
            
            admin_user = User()                                            
            admin_user.generate_advanced_org_admin_data()
            admin_user.device_group = device_group
            admin_user.organization = organization
            TestCondition.create_advanced_organization_admins(self._driver, [admin_user])
            
            account_settings_page = LoginPage(self._driver).open()\
                .login(user_info.email_address, user_info.password, simplifiedUser=True)\
                .goto_your_account().set_first_last_name(user_info).save_change()
            # verify points
            admin_users_page = account_settings_page\
                .logout_and_login_again(admin_user.email_address, admin_user.password)\
                .goto_users_tab()

            is_user_existed = admin_users_page.is_user_existed(user_info.first_name, user_info.get_displayed_name())
            self.assertTrue(is_user_existed, "Assertion Error: Cannot find the user with this first name '{}'".format(user_info.first_name))
            
            user_detail_page = admin_users_page.select_user(user_info.get_displayed_name())
            self.assertTrue(user_detail_page.is_user_page_displayed(user_info.get_displayed_name()), "Assertion Error: User details page is not displayed after clicking on User button")
            admin_users_page = user_detail_page.goto_users_tab()
            
            is_user_existed = admin_users_page.is_user_existed(user_info.last_name, user_info.get_displayed_name())
            self.assertTrue(is_user_existed, "Assertion Error: Cannot find the user with this last name '{}'".format(user_info.last_name))
            
            user_detail_page = admin_users_page.select_user(user_info.get_displayed_name())
            self.assertTrue(user_detail_page.is_user_page_displayed(user_info.get_displayed_name()), "Assertion Error: User details page is not displayed after clicking on User button")
            admin_users_page = user_detail_page.goto_users_tab()
            
            is_user_existed = admin_users_page.is_user_existed(user_info.email_address, user_info.get_displayed_name())
            self.assertTrue(is_user_existed, "Assertion Error: Cannot find the user with this email address '{}'".format(user_info.email_address))
            
            user_detail_page = admin_users_page.select_user(user_info.get_displayed_name())
            self.assertTrue(user_detail_page.is_user_page_displayed(user_info.get_displayed_name()), "Assertion Error: User details page is not displayed after clicking on User button")
            admin_users_page = user_detail_page.goto_users_tab()
            
            self.assertTrue(admin_users_page.is_user_existed(user_info.get_displayed_name()),
                            "Assertion Error: Cannot find the user with displayed name " + user_info.get_displayed_name())
             
            user_detail_page = admin_users_page.select_user(user_info.get_displayed_name())
            self.assertTrue(user_detail_page.is_user_page_displayed(user_info.get_displayed_name()), "Assertion Error: User details page is not displayed after clicking on User button")
        finally:    
            # post-condition
            TestCondition.delete_advanced_users([admin_user, user_info])
            TestCondition.delete_device_groups([device_group], organization)
            
         
    def test_c10931_remove_self_from_admin_1_x(self):
        """
        @author: tham.nguyen
        @date: 7/27/2016
        @summary: C10931 Remove self from admin [1.X] 
        @precondition: Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
   
            Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu. 
        @steps:
            1) Go to the "Users" tab under the "Manage your beams" Dashboard
            2) Click the user admin account that is currently being used (i.e. the account you logged onto the suitable tech site with)
            3) Click the "Edit" box, and try to remove self as an admin by unchecking the box and saving changes
   
        @expected:
          You should not be able to remove self as an admin
        --> a "no-symbol" will appear over the checkbox when the mouse hovers over the check box. You should not be able to change this setting. 
        """
        try:
            # pre-condition
            admin_user = User()
            admin_user.generate_advanced_org_admin_data()
            
            TestCondition.create_advanced_organization_admins(self._driver, [admin_user])
            # steps
            user_detail_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_users_tab()\
                .goto_user_detail_page(admin_user)
            
            is_allow_user_to_administrater_org_enabled = user_detail_page.is_allow_user_to_administrater_org_enabled()
               
            self.assertFalse(is_allow_user_to_administrater_org_enabled,
                             "Assertion Error: Admin can still removed itself from administrator the org.")
        finally:
            TestCondition.delete_advanced_users([admin_user])
        
        
    @pytest.mark.OnlyDesktop
    def test_c11722_users_search_detailed_view(self):
        """
        @author: Thanh Le
        @date: 8/16/2016
        @summary: C11722: "Users" Search - Detailed View 
        @precondition:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs            
            Invite 2 users (UserA and UserB)  
        @steps:
            1) Login to Suitabletech as an org admin select "Manage Your Beams" from the user dropdown menu
            2) Go to "Users" tab and select list view button (next to icon view button) on the right hand side of page
            3) Enter UserA's email address to "Search Users" textbox   
        @expected:
            4) Verify the user displays in icon shrink down as in list view mode.
        """
        try:
            # preconditions:
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
            
            userA = User()
            userA.generate_advanced_normal_user_data()
            userA.device_group = device_group
            userA.organization = organization
            
            userB = User()
            userB.generate_advanced_normal_user_data()
            userB.device_group = device_group
            userB.organization = organization
            
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            TestCondition.create_advanced_normal_users(self._driver, [userA, userB], activate_user=False)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            # steps
            admin_users_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()
            
            admin_users_page.search_for_user(userA.email_address)

            list_view_size = admin_users_page.switch_to_list_view()\
                .get_item_size_in_list_view(userA.get_displayed_name())
            icon_view_size = admin_users_page.switch_to_icon_view()\
                .get_item_size_in_icon_view(userA.get_displayed_name())
                
            # verify points
            self.assertTrue(icon_view_size > list_view_size,
                            "Assertion Error: Unable to switch from icon view to list view.")
        finally:
            TestCondition.delete_advanced_users([userA, userB, org_admin])
            TestCondition.delete_device_groups([device_group], organization)
            
            
    def test_c33889_change_user_icon(self):
        """
        @author: Tan Le
        @date: 10/06/2017
        @summary: C33889: Change user icon
        @precondition:
            Invite a new user and a temporary user
        @steps:
            1. Login admin site as Org admin
            2. Go to Dashboard and select Users tab
            3. Select a normal user
            4. Change profile image
            5. Back Users page
            6. Select a temporary user
            7. Change profile image
        @expected:
            (4)(7) Org admin can change profile image successfully.
        """
        try:
            # preconditions:
            organization = Constant.AdvancedOrgName
            new_device_group = Helper.generate_random_device_group_name()
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.organization = organization
            
            temp_user = User()
            temp_user.generate_advanced_normal_user_data()
            temp_user.device_group = new_device_group
             
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)  
             
            TestCondition.create_device_group(new_device_group)
            TestCondition.create_advanced_temporary_user(self._driver, temp_user, new_device_group, starting_datetime, ending_datetime)
            
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=False)
            
            file_path = Utilities.get_test_image_file_path(self._driver, "img_med.jpg")
            file_path_2 = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
            
            # steps for normal user
            normal_users_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_users_tab().goto_user_detail_page(normal_user)\
                .set_image_icon(file_path).change_image_icon(file_path_2)
            
            image_url = normal_users_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)

            # verify points
            self.assertTrue(are_equal, "Assertion Error: The normal user profile image is not set!")

            # steps for temporary user
            temporary_user_page = normal_users_page.goto_users_tab()\
                .goto_user_detail_page(temp_user).set_image_icon(file_path).change_image_icon(file_path_2)
                
            image_url = temporary_user_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            
            # verify points
            self.assertTrue(are_equal, "Assertion Error: The temporary user profile image is not set!")

        finally:
            TestCondition.delete_advanced_users([normal_user, temp_user])
            TestCondition.delete_device_groups([new_device_group], organization)


    def test_c33914_invite_a_temporary_user_become_guess_user(self):
        """
        @author: Khoi Ngo
        @date: 10/20/2017
        @summary: invite a Temporary User become Guess User
        @precondition:
            Invite a temporary user
        @steps:
            1. Login admin site as Org admin
            2. Go to Dashboard and select Users tab
            3. Select the Temporary User
            4. Invite the Temporary User to Guess User
            5. Select Users tab
            6. Search for the above Guess User
        @expected:
            (4)
            - Success mesage is displayed
            - '(Temporary User)' at the end of display name is disappeared
            - Invite This User button is appeared
            - User receives a confirmation email

            (6)
            - Temporary User icon is disappeared
        """
        try:
            # preconditions:
            new_device_group = Helper.generate_random_device_group_name()

            temp_user = User()
            temp_user.generate_advanced_normal_user_data()
            temp_user.device_group = new_device_group

            starting_datetime = Helper.generate_date_time(hour_delta=16)
            ending_datetime = Helper.generate_date_time(hour_delta=22, minute_delta=30)

            advance_org_admin = User()
            advance_org_admin.generate_advanced_org_admin_data()

            TestCondition.create_device_group(new_device_group)
            TestCondition.create_advanced_temporary_user(self._driver, temp_user, new_device_group, starting_datetime, ending_datetime)
            TestCondition.create_advanced_organization_admins(self._driver,[advance_org_admin])

            # steps
            temp_user_detail_page = LoginPage(self._driver).open()\
                .login(advance_org_admin.email_address, advance_org_admin.password)\
                .goto_users_tab()\
                .goto_user_detail_page(temp_user)\
                .invite_user(temp_user)
            self.assertTrue(temp_user_detail_page.is_success_msg_displayed(),"Success mesage isn't displayed")
            self.assertFalse(temp_user_detail_page.is_temporary_user_label_displayed(),"'(Temporary User)' at the end of display name still displays")

            #TODO: Test case failed due to bug https://jira.suitabletech.com/browse/INFR-2572
            welcome_mail = EmailDetailHelper.generate_welcome_email(temp_user, advance_org_admin.get_displayed_name())
            lst_notification_emails = GmailUtility.get_messages(mail_subject = welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = temp_user.email_address)
            GmailUtility.delete_emails(mail_subject = welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = temp_user.email_address)                                                
            self.assertTrue(len(lst_notification_emails) == 1, "Assertion Error: Suitable Tech wasn't resend email")
            result = re.match(welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))

            admin_users_page = temp_user_detail_page.goto_users_tab()\
                .search_for_user(temp_user.email_address)
            self.assertFalse(admin_users_page.is_temporary_user_icon_display(temp_user.get_displayed_name()), "Temporary User icon still displays")
        finally:
            TestCondition.delete_advanced_users([temp_user, advance_org_admin])
            TestCondition.delete_device_groups([new_device_group])


    def test_c33931_org_admin_can_sort_beams_2_x(self):
        """
        @author: Khoi Ngo
        @date: 10/30/2017
        @summary: Org admin can sort Beams
        @precondition:
            Have an org admin account.
            Have some beams.
        @steps:
            1. Login as org admin
            2. Go to Beams tab
            3. Click Name, Device Group, Location, Status, Last Used label on table of devices
        @expected:
            (3) Verify table of devices is sorted by Name, Device Group, Location, Status, Last Used
        """
        try:
            # steps sort with icon view
            beams_all_devices_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()

            # verify point
            self.assertTrue(beams_all_devices_page.check_sort_by_work_correctly(), "Beams icon is not sorted")

            # steps sort with list view
            if self._driver.driverSetting.platform == Platform.WINDOWS or self._driver.driverSetting.platform == Platform.MAC:
                beam_list_view = beams_all_devices_page.switch_to_list_view()

            # verify point
                self.assertTrue(beam_list_view.check_table_devices_can_sort(), "Table is not sorted")
        finally:
            pass


    @pytest.mark.OnlyDesktop
    def test_c33932_filter_users_and_user_groups_on_list_view_of_users_page(self):
        """
        @author: Khoi Ngo
        @date: 10/31/2017
        @summary: Check if filter on list view of User page works correctly or not
        @precondition:
            Invite a temporary user
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as advanced org admin
            2. Go to Users page
            3. Change to list view
            4. Choose Show -> Guest Only
            5. Choose Show -> Administrators Only
            6. Check on Temporary Users
            7. Uncheck on Temporary Users
            8. Check on User Groups
            9. Uncheck on User Groups
        @expected:
            (4) Verify that all accounts have Guest User icon at Privileges column
            (5) Verify that all accounts have Organization Admin icon at Privileges column
            (6) Verify that Temporary User icon displays on Users table
            (7) Verify that Temporary User icon doesn't display on Users table
            (8) Verify that User Groups table displays
            (8) Verify that User Groups table disappears
        """
        try:
            # preconditions:
            auth = TestCondition.get_and_lock_org_authentication()
            TestCondition.change_authentication_to_OneLogin()
            new_device_group = Helper.generate_random_device_group_name()

            temp_user = User()
            temp_user.generate_advanced_normal_user_data()
            temp_user.device_group = new_device_group

            starting_datetime = Helper.generate_date_time(hour_delta=16)
            ending_datetime = Helper.generate_date_time(hour_delta=22, minute_delta=30)

            TestCondition.create_device_group(new_device_group)
            TestCondition.create_advanced_temporary_user(self._driver, temp_user, new_device_group, starting_datetime, ending_datetime)
            list_temp_users = TestCondition.get_all_email_users(temp_only=True)
            # steps

            admin_users_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_users_tab()\
                .switch_to_list_view()\
                .click_show_button_and_select(ApplicationConst.LBL_MENU_GUEST_ONLY)

            #verify point list mode
            self.assertTrue(admin_users_page.is_icon_displayed_at_each_users_on_table(Constant.IconName["guest_user"]), "Having an account misses Guest User icon at Privileges column")
  
            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_ADMINISTRATOR_ONLY)
            self.assertTrue(admin_users_page.is_icon_displayed_at_each_users_on_table(Constant.IconName["org_admin"]), "Having an account misses Organization Admin icon at Privileges column")
  
            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_TEMPORARY_USERS)
            self.assertTrue(admin_users_page.check_users_display_with_icon(list_temp_users, Constant.IconName["temp_user"]),"Temporary User icon doesn't display on Users table")
  
            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_TEMPORARY_USERS)
            self.assertFalse(admin_users_page.check_users_display_with_icon(list_temp_users, Constant.IconName["temp_user"], False),"Temporary User icon still displays on Users table")
  
            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_USER_GROUPS)
            self.assertTrue(admin_users_page.is_user_group_table_displayed(), "User Groups table doesn't display")
  
            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_USER_GROUPS)
            self.assertFalse(admin_users_page.is_user_group_table_displayed(), "User Groups table still displays")

            #verify point icon mode
            admin_users_page = admin_users_page.switch_to_icon_view().click_show_button_and_select(ApplicationConst.LBL_MENU_GUEST_ONLY)
            self.assertTrue(admin_users_page.is_icon_displayed_at_each_users_on_icon_mode(Constant.IconName["guest_user"]), "Having an account misses Guest User icon at page")

            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_ADMINISTRATOR_ONLY)
            self.assertTrue(admin_users_page.is_icon_displayed_at_each_users_on_icon_mode(Constant.IconName["org_admin"]), "Having an account misses Organization Admin icon at page")

            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_TEMPORARY_USERS)
            self.assertTrue(admin_users_page.check_users_display_with_icon(list_temp_users, Constant.IconName["temp_user"]),"Temporary User icon doesn't display on page")

            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_TEMPORARY_USERS)
            self.assertFalse(admin_users_page.check_users_display_with_icon(list_temp_users, Constant.IconName["temp_user"], False),"Temporary User icon still displays on page")

            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_USER_GROUPS)
            self.assertTrue(admin_users_page.is_user_group_table_displayed(), "User Groups table doesn't display")

            admin_users_page = admin_users_page.click_show_button_and_select(ApplicationConst.LBL_MENU_USER_GROUPS)
            self.assertFalse(admin_users_page.is_user_group_table_displayed(), "User Groups table still displays")

        finally:
            TestCondition.release_org_authentication(auth)
            TestCondition.delete_advanced_users([temp_user])
            TestCondition.delete_device_groups([new_device_group])


    def c33942_org_admin_can_sort_devices_in_device_support_tab(self):
        """
        @author: Quang Tran
        @date: 11/02/2017
        @summary: Org admin can sort table of device in Device Support tab
        @precondition:
            Have an org admin account.
        @steps:
            1. Login as org admin
            2. Go to Organization  tab
            3. Select Device Support tab
            4. Click Device, Serial Number, Service Expiration, Warranty Expiration on table
        @expected:
            (4) Verify table of devices is sorted by Device, Serial Number, Service Expiration, Warranty Expiration
        """
        try:
            # pre-condition
            org_admin = User()
            org_admin.advanced_org_admin_data()

            # steps
            organization_device_support_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_org_setting_page()\
                .open_device_support_tab()

            #verify point
            self.assertTrue(organization_device_support_page.check_table_devices_can_sort(), \
                            "Table can not sort when click each label header")
        finally:
            pass


    def test_c33943_org_admin_can_edit_first_name_and_last_name_of_account_that_have_domain_is_verified(self):
        """
        @author: Quang Tran
        @date: 11/02/2017
        @summary: Org admin can edit first name and last name of account that have domain is verified
        @precondition:
            - Invite an user who has domain is verified
            Ex: domain is logigear.com
        @steps:
            1. Login as org admin
            2. Go to Users page
            3. Select the user has domain is verified
            4. Click on Edit button
            5. Edit first name, last name of the user
            6. Select another user have not domain logigear.com
            7. Click on Edit button
        @expected:
            (5) Change is successfully
            (7) Last name and first name do not display
        """
        try:
            # pre-condition
            normal_user1 = User()
            normal_user1.generate_advanced_normal_user_data("logigear.com")

            normal_user2 = User()
            normal_user2.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user1, normal_user2], activate_user=False)

            last_name_str = Helper.generate_random_last_name()
            first_name_str = Helper.generate_random_first_name()

            # steps
            user_detail_page = LoginPage(self._driver).open()\
                    .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                    .goto_users_tab()\
                    .select_user(normal_user1.get_displayed_name())\
                    .edit_user(verified_domain_user = True, first_name = first_name_str, last_name = last_name_str, wait_for_completed = False)

            #verify point
            self.assertTrue(user_detail_page.is_success_msg_displayed(), "Message success is not displayed ")
            name_display = user_detail_page.get_user_info(ApplicationConst.LBL_LOCATION_NAME)
            self.assertEqual(name_display, first_name_str + " " + last_name_str, "Can not edit first name and last name of user")

            edit_user_dialog =  user_detail_page.goto_users_tab()\
                    .select_user(normal_user2.get_displayed_name())\
                    .open_edit_user_dialog()

            # verify point
            self.assertFalse(edit_user_dialog.is_firstname_lastname_field_display(), "First Name and Last Name field still display in edit user dialog")

        finally:
            #post-condition
            TestCondition.delete_advanced_users([normal_user1, normal_user2])

