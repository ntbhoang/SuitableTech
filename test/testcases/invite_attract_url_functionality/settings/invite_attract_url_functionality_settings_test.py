from data_test.dataobjects.user import User
from core.utilities.gmail_utility import GmailUtility
from common.helper import EmailDetailHelper, Helper
from common.constant import Constant
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage


class InviteAttractUrlFunctionalitySettings_Test(TestBase):
    
    def test_c11374_opt_out_of_attract_email_request_for_access_notification_admin_user_account_settings(self):
        """
        @author: Thanh Le
        @date: 8/4/2016
        @summary: Opt-Out of Attract Email Request for Access Notification: Admin User Account settings
        @precondition: 
            
        @steps:
            1) go to "Beams" in the "Manage your Beams" dashboard
            2) click on the desired device group
            3) Go to the "Settings" tab in the device group
            4) Deselect the "Notify administrators when someone requests access to this group"
            5) Copy the display URL if you cannot see the it displayed on the beam locally (e.g. https://staging.suitabletech.com/r/CTCPH2/)
            6) go to that link, and fill out the information with a standard user and hit "send"
            
        @expected:
            log onto the device group admin's email account, verify that no email was sent requesting access to the beam
        """
        try:
            # precondition:
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
            
            # steps
            beams_settings_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)\
                .toggle_request_access_notification(False)
                
            request_access_link = beams_settings_page.select_Dispplay_url_connect_invitation()\
                .get_link_access_request()
            
            user = User()
            user.generate_advanced_normal_user_data()
            user.device_group = device_group_name
            user.first_name = "User" 
            user.last_name = "Request Access " + Helper.generate_random_string(5)
            
            request_message = "test C11374"
            
            beams_settings_page.goto_request_access_page(request_access_link)\
                .send_request_beam_access(user, request_message)
            
            request_access_email_template = EmailDetailHelper.generate_request_access_email(device_group_name, user, request_message)
            
            messages = GmailUtility.get_messages(request_access_email_template.subject, reply_to=user.email_address, receiver=device_group_admin.email_address, timeout=30)
            
            # verify point
            self.assertEqual(0, len(messages), "Assertion Error: There should be no request access email sent to Admin")
        
        finally:
            # post-condition
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users(user_array=[device_group_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)

