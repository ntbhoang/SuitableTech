import re
from common.application_constants import ApplicationConst
from common.constant import Constant
from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from data_test.dataobjects.user import User
from pages.suitable_tech.others_page import OthersPage
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase


class Email_Admin_Request_Notifications_Test(TestBase):
    
    def test_c11383_click_attract_request_link_from_email_for_an_out_of_date_accepted_request(self):
        """
        @author: Khoi Ngo
        @date: 8/25/2016
        @summary: Click Attract Request link from email, for an out of date accepted request.
        @precondition: 
            Login to Suitabletech with an org admin and create a DeviceGroup (DeviceGroupA)
            Create 2 device group admins (DeviceGroupAdmin1@suitabletech.com and DeviceGroupAdmin2@suitabletech.com) are the admin of DeviceGroupA
        @steps:
            1. Login to Suitabletech site as an org admin and select "Manage Your Beams" go to dashboard page
            2. On "Beams"->"DeviceGroup-A"->"Settings"->"Notifications"
            3. Select "Notify admins when someone requests access to this group"
            4. Copy URL in "Access Requests" section and browse to the "Request Beam Access" page
            5. Enter Email Address of a user (UserA@suitabletech.com), Lastname, Firstname, and Message then click 'Send' button
            6. Go to mail box of the first device group admin (DeviceGroupAdmin1@suitabletech.com)
            7. Click "Accept Request" button
            8. Go to mailbox of the second device group admin (DeviceGroupAdmin2@suitabletech.com)
            9. Click "Accept Request" button   
        @expected:
            (8) The 'Approved" page displays.
            (9) The error page displays.
        """
        beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
        beam_name = beam.beam_name
        device_list = [beam_name]
        device_group_name = Helper.generate_random_device_group_name()
        
        org_admin = User()
        org_admin.advanced_org_admin_data()
        # create device group
        temp_device_group_name = Helper.generate_random_device_group_name()
        org_admin.device_group = temp_device_group_name
        TestCondition.create_device_group(temp_device_group_name)
        
        device_admin_1 = User()
        device_admin_1.generate_advanced_device_group_admin_data()
        device_admin_1.device_group = device_group_name
        
        device_admin_2 = User()
        device_admin_2.generate_advanced_device_group_admin_data()
        device_admin_2.device_group = device_group_name
        
        normal_user = User()
        normal_user.generate_advanced_normal_user_data()
        normal_user.device_group = device_group_name
        
        try:
            # precondition
            TestCondition.create_device_group(device_group_name, device_list, org_admin.organization)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_admin_1, device_admin_2])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            
            setting_page = LoginPage(self._driver).open()\
                .login(device_admin_1.email_address, device_admin_1.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
            
            # steps
            link_request = setting_page.toggle_request_access_notification().get_link_access_request()
            setting_page.select_Dispplay_url_connect_invitation()
            request_access_page = setting_page.goto_request_access_page(link_request)
            request_access_page.send_request_beam_access(normal_user)
            
            # verify points
            account_1_approve_link = GmailUtility.get_approve_request_link(reply_to=normal_user.email_address, receiver=device_admin_1.email_address)
            approve_access_page = OthersPage(self._driver).open(account_1_approve_link)
            header_page = approve_access_page.get_header()
            self.assertEqual(header_page, ApplicationConst.LBL_APPROVED_REQUEST_ACCESS_BEAM_HEADER, "Assertion Error: Approved page is not display")
            
            account_2_approve_link = GmailUtility.get_approve_request_link(reply_to=normal_user.email_address, receiver=device_admin_2.email_address)
            error_page = OthersPage(self._driver).open(account_2_approve_link)
            header_page = error_page.get_header()
            self.assertEqual(header_page, ApplicationConst.LBL_ERROR_REQUEST_ACCESS_BEAM_HEADER, "Assertion Error: Request can be approved more than once.")
                      
        finally:
            #TestCondition.reject_all_access_requests(org_admin.organization)
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user, device_admin_1, device_admin_2])
            TestCondition.delete_device_groups([device_group_name, temp_device_group_name])


    def test_c11386_click_attract_request_link_from_email_for_an_out_of_date_rejected_request(self):
        """
        @author: Khoi Ngo
        @date: 8/25/2016
        @summary: Click Attract Request link from email, for an out of date rejected request.
        @precondition: 
            Login to Suitabletech with an org admin and create a DeviceGroup (DeviceGroupA)
            Create 2 device group admins (DeviceGroupAdmin1@suitabletech.com and DeviceGroupAdmin2@suitabletech.com) are the admin of DeviceGroupA
        @steps:
            1. Login to Suitabletech site as an org admin and select "Manage Your Beams" go to dashboard page
            2. On "Beams"->"DeviceGroup-A"->"Settings"->"Notifications"
            3. Select "Notify admins when someone requests access to this group"
            4. Copy URL in "Access Requests" section and browse to the "Request Beam Access" page
            5. Enter Email Address of a user (UserA@suitabletech.com), Lastname, Firstname, and Message then click 'Send' button
            6. Go to mail box of the first device group admin (DeviceGroupAdmin1@suitabletech.com)
            7. Click "Reject Request" button
            8. Go to mailbox of the second device group admin (DeviceGroupAdmin2@suitabletech.com)
            9. Click "Accept Request" button   
        @expected:
            (8) The 'Rejected" page displays.
            (9) The error page displays.
        """
        try:
            # precondition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            device_group_name = Helper.generate_random_device_group_name()
            
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(temp_device_group_name)
            
            device_admin_1 = User()
            device_admin_1.generate_advanced_device_group_admin_data()
            device_admin_1.device_group = device_group_name
            
            device_admin_2 = User()
            device_admin_2.generate_advanced_device_group_admin_data()
            device_admin_2.device_group = device_group_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name, [beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_admin_1, device_admin_2])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], False)
            
            # steps
            setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group_name)
            
            link_request = setting_page.toggle_request_access_notification()\
                .select_Dispplay_url_connect_invitation()\
                .get_link_access_request()
            request_access_page = setting_page.goto_request_access_page(link_request)
            request_access_page.send_request_beam_access(normal_user)
            
            # verify points
            account_1_reject_link = GmailUtility.get_reject_request_link(reply_to=normal_user.email_address, receiver=device_admin_1.email_address)
            
            reject_access_page = OthersPage(self._driver).open(account_1_reject_link)
            header_page = reject_access_page.get_header()
            
            self.assertEqual(header_page, ApplicationConst.LBL_REJECTED_REQUEST_ACCESS_BEAM_HEADER, "Assertion Error: Rejected page is not display")
            
            account_2_approve_link = GmailUtility.get_approve_request_link(reply_to=normal_user.email_address, receiver=device_admin_2.email_address)
            
            error_page = OthersPage(self._driver).open(account_2_approve_link)
            header_page = error_page.get_header()
            
            self.assertEqual(header_page, ApplicationConst.LBL_ERROR_REQUEST_ACCESS_BEAM_HEADER, "Assertion Error: User can approve again.")
                      
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user, device_admin_1, device_admin_2])
            TestCondition.delete_device_groups([device_group_name, temp_device_group_name])


    def test_c11362_new_user_attract_email_notification_request_for_access_verify_format(self):
        """
        @author: Thanh Le
        @date: 8/26/2016
        @summary: New User Attract Email Notification Request for Access - Verify Format
        @precondition: 
            1) Login to Suitabletech with an org admin and create a DeviceGroup (DeviceGroupA)
            2) Create an device group admin (DeviceGroupAdmin@suitabletech.com) is the admin of DeviceGroupA
        @steps:
            1) Login to Suitabletech site as an org admin and select "Manage Your Beams" go to dashboard page
            2) On "Beams"->"DeviceGroup-A"->"Settings"->"Notifications"
            3) Select "Notify admins when someone requests access to this group"
            4) Copy URL in "Access Requests" section and browse to the "Request Beam Access" page
            5) Enter Emai Address (new user), Lastname, Firstname, and Message then click 'Send' button
            6) Go to mail box of device group admin (DeviceGroupAdmin@suitabletech.com)           
        @expected:
            6) Verify that the device group admin received the mail requesting access to your Beam group as below:
            From: support=suitabletech.com@mailer.suitabletech.com [mailto:support=suitabletech.com@mailer.suitabletech.com] On Behalf Of Suitable Technologies Support
            Sent: <Week Day>, <Month> <Day>, <Year> <hh:mm AM/PM>
            To: < Admin’s Email-ID>@<Domain>
            Subject: Someone is requesting access to your Beam group
            
            Someone has requested access to the Beam group "<Device Group Name>".
            
            Email: < Requester’s Email-ID>@<Domain>
            First name: <Requester’s First Name>
            Last name: < Requester’s Last Name>
            Message: < Requester’s Message>
            
            To approve this request, click on the link below:
            https://staging.suitabletech.com/r/exxkIrC34CJ38oXTp9uu5xh7w4O9nPFeRtKSIW3sH8lpR28sy36ooiszoK75sOI0206/a/
            
            Otherwise, reject this request by clicking the link below:
            https://staging.suitabletech.com/r/exxkIrC34CJ38oXTp9uu5xh7w4O9nPFeRtKSIW3sH8lpR28sy36ooiszoK75sOI0206/r/
        """
        try:
            # Precondition:
            device_group_name = Helper.generate_random_device_group_name()            
            admin_user = User()
            admin_user.generate_advanced_org_admin_data()
            admin_user.device_group = device_group_name
            user = User()
            user.generate_advanced_normal_user_data()
            user.first_name = "User" 
            user.last_name = "Request Access " + Helper.generate_random_string(5)
            request_message = "test c11362 - New User Attract Email Notification Request for Access - Verify Format"            
            TestCondition.create_device_group(device_group_name)            
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            
            # steps
            beams_settings_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
                        
            request_access_link = beams_settings_page\
                .select_Dispplay_url_connect_invitation()\
                .get_link_access_request()
            
            beams_settings_page.toggle_request_access_notification().logout()\
                .goto_request_access_page(request_access_link)\
                    .send_request_beam_access(user, request_message)\
                
            request_access_email_template = EmailDetailHelper.generate_request_access_email(device_group_name, user, request_message)            
            messages = GmailUtility.get_messages(request_access_email_template.subject, reply_to=user.email_address, receiver=admin_user.email_address)
            self.assertEquals(len(messages), 1, "Assertion Error: The number of received emails is not correct")
            
            actual_message = messages[0].trimmed_text_content
            expected_message = request_access_email_template.trimmed_text_content
            result = re.match(expected_message, actual_message, re.I | re.M)
            
            # verify point
            self.assertTrue(result, "Assertion Error: Email content is not correct. Expected:\n'{}' but found:\n'{}'".format(expected_message, actual_message))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([user])
            TestCondition.delete_device_groups([device_group_name])
            
            
    def test_c11373_existing_user_attract_email_notification_request_for_access_verify_format(self):
        """
        @author: Thanh Le
        @date: 8/26/2016
        @summary: Existing User Attract Email Notification Request for Access - Verify Format
        @precondition: 
            1) Login to Suitabletech with an org admin and create a DeviceGroup (DeviceGroupA)
            2) Create an device group admin (DeviceGroupAdmin@suitabletech.com) is the admin of DeviceGroupA
        @steps:
            1) Login to Suitabletech site as an org admin and select "Manage Your Beams" go to dashboard page
            2) On "Beams"->"DeviceGroup-A"->"Settings"->"Notifications"
            3) Select "Notify admins when someone requests access to this group"
            4) Copy URL in "Access Requests" section and browse to the "Request Beam Access" page
            5) Enter Email Address of the existing user (UserA@suitabletech.com), Lastname, Firstname, and Message then click 'Send' button
            6) Go to mail box of device group admin (DeviceGroupAdmin@suitabletech.com)           
        @expected:
            6) Verify that the device group admin received the mail requesting access to your Beam group as below:
            From: support=suitabletech.com@mailer.suitabletech.com [mailto:support=suitabletech.com@mailer.suitabletech.com] On Behalf Of Suitable Technologies Support
            Sent: <Week Day>, <Month> <Day>, <Year> <hh:mm AM/PM>
            To: <Admin’s Email-ID>@<Domain>
            Subject: Someone is requesting access to your Beam group
            
            Someone has requested access to the Beam group "DeviceGroupTest-A".
            
            Email: < Requester’s Email-ID>@<Domain>
            First name: <Requester’s First Name>
            Last name: < Requester’s Last Name>
            Message: < Requester’s Message>
            
            To approve this request, click on the link below:
            https://staging.suitabletech.com/r/HALXgiVAXczI2RFbMB3wZWouIGiidxN32GPo7o16SHsL1SLVCcdkftxHmKsWQ25L206/a/
            
            Otherwise, reject this request by clicking the link below:
            https://staging.suitabletech.com/r/HALXgiVAXczI2RFbMB3wZWouIGiidxN32GPo7o16SHsL1SLVCcdkftxHmKsWQ25L206/r/
        """
        try:
            # Precondition
            device_group_name = Helper.generate_random_device_group_name()
            admin_user = User()
            admin_user.generate_advanced_org_admin_data()
            admin_user.device_group = device_group_name
            
            user = User()
            user.generate_advanced_normal_user_data()
            user.device_group = device_group_name
            user.first_name = "User" 
            user.last_name = "Request Access " + Helper.generate_random_string(5)
            request_message = "test c11373 - Existing User Attract Email Notification Request for Access - Verify Format"
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
            TestCondition.create_advanced_normal_users(self._driver, [user])
            
            # steps
            beams_settings_page = LoginPage(self._driver).open().login(admin_user.email_address, admin_user.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
                        
            request_access_link = beams_settings_page.select_Dispplay_url_connect_invitation()\
            .get_link_access_request()
            beams_settings_page.toggle_request_access_notification()
                     
            beams_settings_page.goto_request_access_page(request_access_link)\
                .send_request_beam_access(user, request_message)\
                
            request_access_email_template = EmailDetailHelper.generate_request_access_email(device_group_name, user, request_message)            
            messages = GmailUtility.get_messages(request_access_email_template.subject, reply_to=user.email_address, receiver=admin_user.email_address)
            
            self.assertEqual(len(messages), 1, "Assertion Error: The number of email return is incorrect. The actual number email is {}".format(len(messages)))
            
            actual_message = messages[0].trimmed_text_content
            expected_message = request_access_email_template.trimmed_text_content
            result = re.match(expected_message, actual_message, re.I | re.M)
            
            # verify point
            self.assertTrue(result, "Assertion Error: The email's content is invalid! The expected email content is {} but the actual email content is {}".format(expected_message, actual_message))
            
        finally:
            # post-condition
            TestCondition.delete_advanced_users([user])
            TestCondition.delete_device_groups([device_group_name])
            
    
    def test_c11363_attract_device_group_email_request_access_notification_request_accepted(self):
        """
        @author: Thanh Le
        @date: 8/25/2016
        @summary: Attract Device Group Email Request Access Notification Request-Accepted
        @precondition: 
            1) Login to Suitabletech with an org admin and create a DeviceGroup (DeviceGroupA)
            2) Create an device group admin (DeviceGroupAdmin@suitabletech.com) is the admin of DeviceGroupA
        @steps:
            1) Login to Suitabletech site as an org admin and select "Manage Your Beams" go to dashboard page
            2) On "Beams"->"DeviceGroup-A"->"Settings"->"Notifications"
            3) Select "Notify admins when someone requests access to this group"
            4) Copy URL in "Access Requests" section and browse to the "Request Beam Access" page
            5) Enter Email Address of the existing user (UserA@suitabletech.com), Lastname, Firstname, and Message then click 'Send' button
            6) Log in as org admin and go to Dashboard > Notificaton tab
            7) Go to mail box of device group admin (DeviceGroupAdmin@suitabletech.com)
            8) Click "Approve Request" button            
        @expected:
            6) Verify that there is a notification about the user request to access Beam
            7) Verify that as the device group admin you will receive the "Someone is requesting access to your Beams" email.
            8) Verify that the "Approved" page displays with message "The access request has already been approved"
        """
        try:
            # Precondition
            device_group_name = Helper.generate_random_device_group_name()
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name            
            
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            
            user = User()
            user.generate_advanced_normal_user_data()
            user.first_name = "User" 
            user.last_name = "Request Access " + Helper.generate_random_string(5)
            user.device_group = device_group_name
            request_message = "test c11363 - Attract Device Group Email Request Access Notification Request-Accepted"

            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            # steps
            beams_settings_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
                        
            request_access_link = beams_settings_page.select_Dispplay_url_connect_invitation()\
            .get_link_access_request()
            home_page = beams_settings_page.toggle_request_access_notification().logout()
                     
            request_beam_access_page = home_page.goto_request_access_page(request_access_link)\
                .send_request_beam_access(user, request_message)\
            
            admin_dashboard_page = request_beam_access_page.goto_login_page()\
                .login(org_admin.email_address, org_admin.password)\
            
            is_access_request_displayed = admin_dashboard_page.is_access_request_displayed(user)
            self.assertTrue(is_access_request_displayed, "Assertion Error: Request Access record does not display or it does not localize")
            
            request_access_email_template = EmailDetailHelper.generate_request_access_email(device_group_name, user, request_message)            
            messages = GmailUtility.get_messages(request_access_email_template.subject, reply_to=user.email_address, receiver=device_group_admin.email_address)
            # verify point
            self.assertEqual(1, len(messages), "Assertion Error: The number of email return is not correct")                
                
            actual_message = messages[0].trimmed_text_content
            expected_message = request_access_email_template.trimmed_text_content
            result = re.match(expected_message, actual_message, re.I | re.M)
            
            # verify point
            self.assertTrue(result, "Assertion Error: The email's content is invalid! The expected email content is {} but the actual email content is {}".format(expected_message, actual_message))
                
            notification_message = admin_dashboard_page.logout().approve_request_beam_access(user_email_address=user.email_address, admin_email_address=device_group_admin.email_address)\
                .get_notification_message()           
            # verify point
            self.assertEqual(notification_message, ApplicationConst.LBL_APPROVED_NOTIFICATION_MESSAGE,
                             "Assertion Error: The Approved page is NOT displayed!")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([device_group_admin, user])
            TestCondition.delete_device_groups([device_group_name])


    def test_c11364_attract_device_group_email_request_access_notification_request_rejected(self):
        """
        @author: Thanh Le
        @date: 8/25/2016
        @summary: Attract Device Group Email Request Access Notification Request-Rejected
        @precondition: 
            1) Login to Suitabletech with an org admin and create a DeviceGroup (DeviceGroupA)
            2) Create an device group admin (DeviceGroupAdmin@suitabletech.com) is the admin of DeviceGroupA
        @steps:
            1) Login to Suitabletech site as an org admin and select "Manage Your Beams" go to dashboard page
            2) On "Beams"->"DeviceGroup-A"->"Settings"->"Notifications"
            3) Select "Notify admins when someone requests access to this group"
            4) Copy URL in "Access Requests" section and browse to the "Request Beam Access" page
            5) Enter Email Address of the existing user (UserA@suitabletech.com), Lastname, Firstname, and Message then click 'Send' button
            6) Log in as org admin and go to Dashboard > Notificaton tab
            7) Go to mail box of device group admin (DeviceGroupAdmin@suitabletech.com)
            8) Click "Reject Request" button            
        @expected:
            6) Verify that there is a notification about the user request to access Beam
            7) Verify that as the device group admin you will receive the "Someone is requesting access to your Beams" email.
            8) Verify that the "Rejected" page displays with message: "The access request has already been rejected.".
        """
        try:
            # Precondition
            device_group_name = Helper.generate_random_device_group_name()
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name            
            
            org_admin = User()
            org_admin.advanced_org_admin_data()
            
            user = User()
            user.generate_advanced_normal_user_data()
            user.device_group = device_group_name
            user.first_name = "User" 
            user.last_name = "Request Access " + Helper.generate_random_string(5)
            request_message = "test c11364 - Attract Device Group Email Request Access Notification Request-Rejected"

            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            # steps
            beams_settings_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
                        
            request_access_link = beams_settings_page.select_Dispplay_url_connect_invitation()\
            .get_link_access_request()
            home_page = beams_settings_page.toggle_request_access_notification().logout()
                     
            request_beam_access_page = home_page.goto_request_access_page(request_access_link)\
                .send_request_beam_access(user, request_message)\
            
            admin_dashboard_page = request_beam_access_page.goto_login_page()\
                .login(org_admin.email_address, org_admin.password)\
            
            is_access_request_displayed = admin_dashboard_page.is_access_request_displayed(user)
            self.assertTrue(is_access_request_displayed, "Assertion Error: Request Access record does not display or it does not localize")
            
            request_access_email_template = EmailDetailHelper.generate_request_access_email(device_group_name, user, request_message)            
            messages = GmailUtility.get_messages(request_access_email_template.subject, reply_to=user.email_address, receiver=device_group_admin.email_address)
            # verify point
            self.assertEqual(1, len(messages), "Assertion Error: The number of email return is not correct")                
                
            actual_message = messages[0].trimmed_text_content
            expected_message = request_access_email_template.trimmed_text_content
            result = re.match(expected_message, actual_message, re.I | re.M)
            
            # verify point
            self.assertTrue(result,
                            "Assertion Error: The email's content is invalid! The expected email content is {} but the actual email content is {}"\
                            .format(expected_message, actual_message))
            
            notification_message = admin_dashboard_page.logout().reject_request_beam_access(user_email_address=user.email_address, admin_email_address=device_group_admin.email_address)\
                .get_notification_message()
            
            # verify point
            self.assertEqual(notification_message, ApplicationConst.LBL_REJECTED_NOTIFICATION_MESSAGE,
                             "Assertion Error: The Rejected page is NOT displayed!")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([device_group_admin, user])
            TestCondition.delete_device_groups([device_group_name])


    def test_c11365_admin_dashboard_notifications_beam_device_access_request_accept_ignore_logs(self):
        """
        @author: Quang Tran
        @date: 01/15/2018
        @summary: Admin Dashboard Notifications- Beam Device Access Request Accept/Ignore: logs
        @steps:
            1) Log onto the admin in charge of the device group
            2) on the dashboard page
            3) Click accept or reject       
        @expected:
            1) if accept, verify that the user requesting access is able to get that access (e.g. WP Test User)
            2) if reject, verify that the user requesting access is NOT able to connect (e.g. WP Test User)
        """
        try:
            # Precondition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name

            device_group_name = Helper.generate_random_device_group_name()

            user = User()
            user.generate_advanced_normal_user_data()

            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name            

            user = User()
            user.generate_advanced_normal_user_data()
            user.device_group = device_group_name

            TestCondition.create_device_group(device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            #steps
            beams_settings_page = LoginPage(self._driver).open()\
                    .login(device_group_admin.email_address, device_group_admin.password)\
                    .goto_settings_tab_of_a_device_group(device_group_name)
            request_access_link = beams_settings_page.select_Dispplay_url_connect_invitation()\
                    .get_link_access_request()
            home_page = beams_settings_page.toggle_request_access_notification().logout()
                     
            request_beam_access_page = home_page.goto_request_access_page(request_access_link)\
                .send_request_beam_access(user)\

            dashboard_page = request_beam_access_page.goto_login_page()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .approve_request_access_device_group(user.email_address)

            TestCondition._activate_user(self._driver, user, pass_safety_video=True, email_subject=ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE)

            dashboard_page = dashboard_page.logout_and_login_again(user.email_address, user.password, loginAgainAsNormalUser=True)

            self.assertTrue(dashboard_page.is_beam_displayed(beam_name), "User cannot access to device group")
        finally:
            TestCondition.delete_advanced_users([device_group_admin, user])
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.release_a_beam(beam)

