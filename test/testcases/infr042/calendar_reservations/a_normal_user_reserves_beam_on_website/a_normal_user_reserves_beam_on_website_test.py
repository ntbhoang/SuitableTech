from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper, EmailDetailHelper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from data_test.dataobjects.reservation import Reservation
from common.application_constants import ApplicationConst
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime


class ANormalUserReservesBeamOnWebsite_Test(TestBase):
    
    def test_c33856_normal_users_will_see_reserve_this_Beam_button_if_the_beam_has_allowed_or_by_request_permission(self):
        """
        @author: tan.le
        @date: 09/18/2017
        @summary: Normal users will see Reserve this Beam button if the Beam has allowed or by request permission.
        @precondition:
            Invite a new user into device group has devices. Then activating new user.
        @steps:
            1. Login as org admin or device group admin
            2. Go to Beam details page and change reservation permission to Allowed.
            3. Login new user on another browser
            4. Notice the Reserve this Beam button displays or not
            5. Repeat step 2,3,4 with Not Allowed, By Request, and By Administrators Only permission.
            
        @expected:
            Normal users see Reserve this Beam button if permission is Allowed or By Request.
            Normal users cannot see Reserve this Beam button if permission is Not Allowed or By Administrators Only.
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName

            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            TestCondition.create_device_group(device_group_name, [beam_name], organization)
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=True)
            
            # Scenario 1: Allowed
            # steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Allowed")
            normal_user_dashboard_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)
                
            # verify
            self.assertTrue(normal_user_dashboard_page.is_btn_reserve_this_beam_displayed(beam_name),\
                            "Assertion Error: The normal user cannot see 'Reserve This Beam' button on Allowed beam")
            
            # Scenario 2: By Request
            #steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "By Request")
            normal_user_dashboard_page = normal_user_dashboard_page\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)
            
            # verify
            self.assertTrue(normal_user_dashboard_page.is_btn_reserve_this_beam_displayed(beam_name),\
                            "Assertion Error: The normal user cannot see 'Reserve This Beam' button on By Request beam")
 
            # Scenario 3: By Administrators Only
            #steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "By Administrator")
            normal_user_dashboard_page = normal_user_dashboard_page\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)
            
            # verify
            self.assertFalse(normal_user_dashboard_page.is_btn_reserve_this_beam_displayed(beam_name),\
                            "Assertion Error: The normal user can see 'Reserve This Beam' button on By Administrators Only beam")
        
            # Scenario 4: Not Allowed
            #steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
                
            normal_user_dashboard_page = normal_user_dashboard_page\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)
            
            # verify
            self.assertFalse(normal_user_dashboard_page.is_btn_reserve_this_beam_displayed(beam_name),\
                            "Assertion Error: The normal user can see 'Reserve This Beam' button on Not Allowed beam")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user], organization)
            TestCondition.delete_device_groups([device_group_name], organization)
            
            
    def test_c33857_normal_users_are_able_to_reserve_beam_that_has_allowed_or_by_request_permission(self):
        """
        @author: tan.le
        @date: 09/18/2017
        @summary: Normal users will see Reserve this Beam button if the Beam has allowed or by request permission.
        @precondition:
            Invite a new user into device group has devices. Then activating new user.
        @steps:
            1. Log as device group admin or org admin
            2. Change reservation permission to Allowed
            3. Login normal user on another browser
            4. Click Reserve this Beam button and create a new reservation.
            5. Back to org admin or device group admin
            6. Change reservation permission to By Request
            7. Back to normal user and create new reservation
        @expected:
            (4)
             - Success message displays
             - Reservation displays on reservation page
             - An email is sent to org admin and device group admin
            (7)
             - Success message displays
             - Reservation displays on reservation page
             - An email is sent to org admin and device group admin
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName

            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            TestCondition.create_device_group(device_group_name, [beam_name], organization)
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            device_group_admin.organization = organization
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=True)
            
            reservation_1 = Reservation()
            reservation_1.generate_start_time_and_end_time()
            reservation_1.beam_name = beam_name
             
            reservation_2 = Reservation()
            reservation_2.generate_start_time_and_end_time()
            reservation_2.beam_name = beam_name  
            
            # Scenario 1: Allowed
            # steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Allowed")
            normal_home_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .reserve_a_beam(reservation_1)
                
            #verify
            self.assertEqual(normal_home_page.get_msg_success(), ApplicationConst.INFO_MSG_CREATE_RESERVATION_SUCCESSFUL, 
                              "Assertion Error: Expected message is not displayed")
            
            #verify
            expected_reserve_beam_msg = EmailDetailHelper.generate_reservation_for_beam_was_create_email(
                                                    beam, normal_user, normal_user, reservation_1.start_time, reservation_1.end_time)
            actual_reserve_beam_msg = GmailUtility.get_messages(expected_reserve_beam_msg.subject,
                                       receiver=device_group_admin.email_address,
                                       sent_day=datetime.now())
            self.assertEqual(len(actual_reserve_beam_msg), 1, "Assertion Error: The number of return email is not correct")
            self.assertEqual(expected_reserve_beam_msg.trimmed_text_content, actual_reserve_beam_msg[0].trimmed_text_content,\
                            "Assertion Error: The content of return email is not correct. The expected email content is '{}' but the actual email content is '{}'".format(expected_reserve_beam_msg.trimmed_text_content, actual_reserve_beam_msg[0].trimmed_text_content))
           
            #verify
            reservation_tab = normal_home_page.logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                 .goto_beams_tab().select_a_device(beam_name).open_reservation_tab()
               
            actual_reservation_time_1 = reservation_tab.get_reservation_data(normal_user)
            expect_reservation_time_1 = Helper.format_start_time_and_end_time_on_website(reservation_1.start_time, reservation_1.end_time, self._driver._driverSetting.language)
              
            self.assertEqual(actual_reservation_time_1, expect_reservation_time_1,
                             "Assertion Error: Reservation data displays correctly on the Website")
            self.assertEqual(reservation_tab.get_reservation_status(normal_user), ApplicationConst.LBL_RESERVATION_CONFIRMED_STATUS, 
                 "Assertion Error: The reservation status is incorrect")
            
            reservation_tab = reservation_tab.delete_reservation(normal_user)
            
            # Scenario 2: By Request
            # steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "By Request")
            normal_home_page = reservation_tab\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)\
                .reserve_a_beam(reservation_2)
                
            #verify
            self.assertEqual(normal_home_page.get_msg_success(), ApplicationConst.INFO_MSG_REQUEST_RESERVATION_SUCCESSFUL, 
                              "Assertion Error: Expected message is not displayed")
              
            reservation_tab = normal_home_page.logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                 .goto_beams_tab().select_a_device(beam_name).open_reservation_tab()
               
            actual_reservation_time_2 = reservation_tab.get_reservation_data(normal_user)
            expect_reservation_time_2 = Helper.format_start_time_and_end_time_on_website(reservation_2.start_time, reservation_2.end_time, self._driver._driverSetting.language)
              
            #verify
            self.assertEqual(actual_reservation_time_2, expect_reservation_time_2,
                             "Assertion Error: Reservation data displays correctly on the Website")
            self.assertEqual(reservation_tab.get_reservation_status(normal_user), ApplicationConst.LBL_RESERVATION_REQUESTED_STATUS, 
                 "Assertion Error: The reservation status is incorrect")
            
            #verify
            #TODO: This testcase is failed by bug INFR-2390 
            self.assertTrue(False, "The notification is not sent to device group admin inbox when notification 'Users request reservations for Beams' is turned on.")
        
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([device_group_admin, normal_user], organization)
            TestCondition.delete_device_groups([device_group_name], organization)
        