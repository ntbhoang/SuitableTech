from common.constant import Constant
from common.helper import Helper
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.utilities import Calendar_Utilities
from data_test.dataobjects.reservation import Reservation
from common.helper import EmailDetailHelper
from core.utilities.gmail_utility import GmailUtility
import datetime

class Reservation_Test(TestBase):


    def test_c33944_verify_that_user_still_sees_beam_in_reservation_after_beam_is_changed_to_another_device_group(self):
        """
        @author: Khoi.Ngo
        @date: 11/16/2017
        @summary: Verify that user still sees beam in reservation after beam is changed to another device group
        @precondition:
            - Create two device groups
            - Add device beam to the first device group
            - Create one normal user in the first device group
            - Create one reservation for the above user with the above beam

        @steps:
            1. Login to Suitabletech staging site as org admin
            (khoi.ngo@logigear.com/L0gigear123!)
            2. Go to Beams page and select the second device group
            3. Move beam to the second device group
            4. Go to reservation tab of the second device group
            5. At the reservation time, login to Suitabletech staging site as the normal user in first group
        @expected:
            (4) Reservation of the normal user in the first group is displayed
            (5) Reserved Beam is displayed
        """
        try:
            device_group_1 = Helper.generate_random_device_group_name()
            device_group_2 = Helper.generate_random_device_group_name()

            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name

            reservation_1 = Reservation()
            reservation_1.start_time = datetime.datetime.now()
            reservation_1.end_time = datetime.datetime.now() + datetime.timedelta(hours= 1)
            reservation_1.beam_name = beam_name

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_1

            # pre-condition
            TestCondition.create_device_group(device_group_1,[beam_name])
            TestCondition.create_device_group(device_group_2)
            TestCondition.create_advanced_normal_users(self._driver,[normal_user])

            #Invite a new user and add its account to CalDav client
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])

            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)

            #Create confirmed reservations
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_1)

            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_device_group(device_group_1)\
                .goto_reservations_tab()
            self.assertTrue(admin_dashboard_page.is_reservation_displayed(normal_user.get_displayed_name()), "Reservation of the normal user isn't displayed")

            simplified_dashboard_page = admin_dashboard_page.goto_beams_tab()\
                .select_device_group(device_group_2)\
                .add_devices([beam_name])\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser = True)
            #TODO: Test case failed due to bug https://jira.suitabletech.com/browse/INFR-2558
            self.assertTrue(simplified_dashboard_page.is_beam_displayed(beam_name), "Reserved Beam isn't displayed")
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_1, device_group_2])
            TestCondition.delete_advanced_users([normal_user])


    def test_c34039_verify_an_email_sends_to_user_when_their_reservation_is_changed(self):
        """
        @author: Tan Le
        @date: 05/24/2018
        @summary: Verify an email sends to user when their reservation is changed
        @precondition:
            - Invite new user and active
            - Create device group that has a device and add the user
            - Change reservation permission of device to 'Allowed'

        @steps:
            1. Open login site (https://stg1.suitabletech.com/accounts/login/?next=/manage/)
            2. Login new user
            3. Create new reservation
            4. Logout and Login with org admin
            5. Go to Reservation of the device group above
            6. Change time for the reservation that is created at step 3
        @expected:
            - An email sends to a new user
            - The time that is changed shows correctly in the email.
        """
        try:
            device_group_name = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name=beam.beam_name

            reservation = Reservation()
            reservation.beam_name=beam_name
            reservation.generate_start_time_and_end_time()
            start_time_new=reservation.start_time
            end_time_new=reservation.end_time

            user =User()
            user.generate_advanced_normal_user_data()
            user.device_group=device_group_name
            admin_user=User()
            admin_user.advanced_org_admin_data()

            TestCondition.create_device_group(device_group_name, device_array=[beam.beam_name])
            TestCondition.create_advanced_normal_users(self._driver, [user])
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Allowed")

            # Steps
            device_details_page = LoginPage(self._driver).open()\
                                    .login(user.email_address, user.password,True)\
                                    .reserve_a_beam(reservation)
            logout_page=device_details_page.logout()

            edit_time = reservation.generate_edit_start_time_and_end_time()
            reservation.start_time = edit_time['start_time']
            reservation.end_time = edit_time['end_time']

            device_details_page = logout_page.goto_login_page()\
                                    .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                                    .goto_beams_tab()\
                                    .select_a_device(beam_name)\
                                    .open_reservation_tab()\
                                    .update_reservation(user, reservation.start_time, reservation.end_time)

            #verify point
            expected_reserve_beam_msg = EmailDetailHelper.generate_reservation_for_beam_has_change(beam, admin_user.get_displayed_name(), start_time_new, end_time_new, reservation.start_time, reservation.end_time)
            actual_reserve_beam_msg = GmailUtility.get_messages(expected_reserve_beam_msg.subject, receiver=user.email_address,sent_day=datetime.datetime.now())
            self.assertEqual(expected_reserve_beam_msg.trimmed_text_content, actual_reserve_beam_msg[0].trimmed_text_content, "Content email is incorrect")

        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([user])
