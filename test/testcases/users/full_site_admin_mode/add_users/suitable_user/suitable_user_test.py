from common.constant import Constant, Platform
from common.helper import EmailDetailHelper, Helper
from core.utilities.gmail_utility import GmailUtility
from core.utilities.utilities import Utilities
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
import re
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from data_test.dataobjects.enum import WeekDays
from common.application_constants import ApplicationConst


class SuitableUser_Test(TestBase):

    def test_c10952_grant_temporary_access_dashboard_2_x(self):
        """
        @author: Thanh.Le
        @date: 8/08/2016
        @summary: Grant Temporary Access (Dashboard) [2.X]
        @precondition: 
            Login as org admin
        @steps:
            1) Navigate to full "Manage your Beams" dashboard
            2) Click on the blue "Invite a Temporary User" box
            3) Fill out the corresponding toast            
        @expected:
            1) Target Users will be notified via email of
            a. Who Invited them (Organization)
            b. What device group(s) they have been added to
            c. Their Access Times to above device groups
            d. UserName
            e. Link to create a password / get client
            2) Once The Invitation has been created, the system will add the user(s) to your organization, and record of the access times to the target device groups affected
        """
        try:
            from core.i18n.i18n_support import I18NSupport  
            # pre-condition:
            tomorrow =  Helper.generate_access_day()
            organization_name = Constant.AdvancedOrgName
            devices = []
            beams = []
            for _ in range(2):
                beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
                beams.append(beam)
                devices.append(beam.beam_name)
                
            device_group_name = Helper.generate_random_device_group_name(5)
            TestCondition.create_device_group(device_group_name, devices, organization_name)
            
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            org_admin.device_group = device_group_name
            
            new_temp_user = User()
            new_temp_user.generate_advanced_normal_user_data()
            new_temp_user.device_group = device_group_name
            
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)
                                    
            # steps
            dashboard_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_temporary_user(new_temp_user, start_date=starting_datetime, end_date=ending_datetime,
                                   link_to_beam_sofware=True, default_invitation=True, device_group=device_group_name)
            
            email_template = EmailDetailHelper.generate_welcome_temporary_user_email(new_temp_user, starting_datetime, ending_datetime, devices, org_admin.get_displayed_name())
            actual_msgs = GmailUtility.get_messages(email_template.subject, receiver=new_temp_user.email_address)        
            
            self.assertEquals(len(actual_msgs), 1, "Assertion Error: The number of received emails is not correct")
            match_result = re.match(email_template.trimmed_text_content, actual_msgs[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(match_result, "Assertion Error: Email content is not correct. Expected:\n'{}' but found:\n'{}'".format(email_template.trimmed_text_content, actual_msgs[0].trimmed_text_content))

            #verify point
            admin_users_page = dashboard_page.goto_users_tab()
            self.assertTrue(admin_users_page.is_user_existed(new_temp_user.get_displayed_name()), "Temporary does not display on Users tab")
            
            access_time_page = admin_users_page.goto_beams_tab()\
                .select_device_group(device_group_name)\
                .goto_accesstimes_tab()

            #verify point
            date_label = I18NSupport.localize_date_time_string( re.sub(' +',' ',tomorrow.strftime('%b %e, %Y')) )
            access_time_label = Utilities.generate_temporary_access_time_label(date_label, starting_datetime, ending_datetime)
            self.assertTrue(access_time_page.is_member_access_time_label_displayed_on_sidebar(new_temp_user, access_time_label), 
                            "Temporary user {} does not display on sidebar with access time: start time is {} and end time is {}".format(new_temp_user.email_address, starting_datetime, ending_datetime))
            tomorrow =  Helper.generate_access_day()
            access_day = WeekDays(tomorrow.isoweekday())
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(access_time_page.is_member_timerange_access_time_displayed_on_calendar(new_temp_user, [access_day],starting_datetime, ending_datetime), 
                                "Temporary user {} does not display on calendar with access time: start time is {} and end time is {}".format(new_temp_user.email_address, starting_datetime, ending_datetime))
                    
        finally:
            # post-condition:
            for beam in beams:
                TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name], organization_name)


    def test_c34003_an_error_message_displays_when_inputting_an_invalid_email(self):
        '''
        @author: Khoi.Ngo
        @date: 02/28/2018
        @summary: An error message displays when inputting an invalid email.
        @precondition:
            1. Login as org admin or device group admin.
            2. Have an invalid email.
        @steps:
            1) Go to Dashboard
            2) Select Invite a New User
            3) Input an invalid email address
            4) Hit Invite User button
        @expected:
            1) Verify that an error message "Enter a valid email address." displays on the top right of screen.
        '''

        try:
            # pre-condition:
            invalid_user = User()
            invalid_user.generate_advanced_normal_user_data()
            invalid_user.email_address = 'abcdef@abcdef'

            # steps:
            dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .invite_new_user(invalid_user, wait_for_completed=False)

            # verify points:
            self.assertTrue(dashboard_page.is_error_msg_displayed(close = False), "Assertion Error: Error message doesn't display.")
            self.assertEqual(dashboard_page.get_error_message(), ApplicationConst.INFO_MSG_INVITE_INVALID_EMAIL, "Assertion Error: Content of error message is incorrect.")

        finally:
            pass

