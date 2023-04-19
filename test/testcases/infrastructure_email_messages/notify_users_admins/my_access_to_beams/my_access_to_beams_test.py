from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper, EmailDetailHelper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from data_test.dataobjects.reservation import Reservation
from core.utilities.gmail_utility import GmailUtility
from datetime import datetime


class MyAccessToBeams_Test(TestBase):
    
    def test_c33873_email_notification_admin_rejects_approves_removes_reservation(self):
        """
        @author: tan.le
        @date: 09/21/2017
        @summary: Email Notification: Admin approves or rejects reservation
        @precondition:
            Create a device group and add a device group admin
            Add device to device group
            Invite a user to the device group 
        @steps:
            1. Normal user turns on "I reserve Beams" notification
            2. Device group admin sets the device's permission to By Request
            3. Normal user requests a reservation
            4. Device group admin rejects the request
            5. Normal user requests another reservation
            6. Device group admin approves the request
            7. Device group admin es the request
        @expected:
            (4)(6) Email notifications are sent to normal user's inbox 
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
            
            reservation = Reservation()
            reservation.generate_start_time_and_end_time()
            reservation.beam_name = beam_name
            
            # Scenario 1: Reject reservation
            # steps
            TestCondition.set_advanced_beam_reservation_permisson(beam, "By Request")
            reservation_tab = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account().goto_notifications_tab()\
                .toggle_i_reserve_beams(True)\
                .goto_simplify_normal_user_home().reserve_a_beam(reservation)\
                .logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_a_device(beam_name).open_reservation_tab()\
                .reject_a_requested_reservation(normal_user)
                
            #verify
            expected_reject_reservation_msg = EmailDetailHelper.generate_reject_reservation_email(
                                                    beam, device_group_admin, reservation.start_time, reservation.end_time)
            actual_reject_reservation_msg = GmailUtility.get_messages(expected_reject_reservation_msg.subject,
                                        receiver=normal_user.email_address,
                                        sent_day=datetime.now())
            self.assertEqual(len(actual_reject_reservation_msg), 1, "Assertion Error: The number of return email is not correct")
            
            self.assertEqual(expected_reject_reservation_msg.trimmed_text_content, actual_reject_reservation_msg[0].trimmed_text_content,\
                            "Assertion Error: The content of return email is not correct. The expected email content is '{}' but the actual email content is '{}'"\
                            .format(expected_reject_reservation_msg.trimmed_text_content, actual_reject_reservation_msg[0].trimmed_text_content))
            
            #Scenario 2: Approve reservation
            #steps            
            reservation_tab = reservation_tab\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)\
                .reserve_a_beam(reservation)\
                .logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_a_device(beam_name).open_reservation_tab()\
                .approve_a_requested_reservation(normal_user)

            #verify
            expected_approve_reservation_msg = EmailDetailHelper.generate_approve_reservation_email(
                                                    beam, device_group_admin, reservation.start_time, reservation.end_time)
            actual_approve_reservation_msg = GmailUtility.get_messages(expected_approve_reservation_msg.subject,
                                        receiver=normal_user.email_address,
                                        sent_day=datetime.now())

            self.assertEqual(len(actual_approve_reservation_msg), 1, "Assertion Error: The number of return email is not correct")

            self.assertEqual(expected_approve_reservation_msg.trimmed_text_content, actual_approve_reservation_msg[0].trimmed_text_content,\
                            "Assertion Error: The content of return email is not correct. The expected email content is '{}' but the actual email content is '{}'"\
                            .format(expected_approve_reservation_msg.trimmed_text_content, actual_approve_reservation_msg[0].trimmed_text_content))

            # Scenario 3: Remove reservation
            # steps            
            reservation_tab = reservation_tab.delete_reservation(normal_user)

            #verify
            expected_remove_reservation_msg = EmailDetailHelper.generate_remove_reservation_email(
                                                    beam, device_group_admin, reservation.start_time, reservation.end_time)
            actual_remove_reservation_msg = GmailUtility.get_messages(expected_remove_reservation_msg.subject,
                                       receiver=normal_user.email_address,
                                       sent_day=datetime.now())

            self.assertEqual(len(actual_remove_reservation_msg), 1, "Assertion Error: The number of return email is not correct")
            self.assertEqual(expected_remove_reservation_msg.trimmed_text_content, actual_remove_reservation_msg[0].trimmed_text_content,\
                            "Assertion Error: The content of return email is not correct. The expected email content is '{}' but the actual email content is '{}'"\
                            .format(expected_remove_reservation_msg.trimmed_text_content, actual_remove_reservation_msg[0].trimmed_text_content))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([device_group_admin, normal_user], organization)
            TestCondition.delete_device_groups([device_group_name], organization)

