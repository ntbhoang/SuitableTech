from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.utilities.utilities import Calendar_Utilities
from data_test.dataobjects.reservation import Reservation
from common.application_constants import ApplicationConst


class CreatingAReservation_Test(TestBase):

    def test_c33091_creating_an_admin_only_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating an 'Admin Only' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you admin privileges (either org admin or device group admin).
            3. The device should be set to accept reservations 'By Administrators' only.
        @steps:
            1. Add a new event in the calendar corresponding to the device over which you have admin privileges.
            
        @expected:
            1. A new reservation for the device should be created, with the start and end times which you selected via your calendar client.
            2. In your calendar client, the name of the event you have just created should change, after a few seconds, to "<device_name> Reservation"
        """
            
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName

            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            TestCondition.set_advanced_beam_reservation_permisson(beam, "By Administrator")
            
            reservation_data_1 = Reservation()
            reservation_data_1.generate_start_time_and_end_time()
            reservation_data_1.beam_name = beam_name
                
            reservation_data_2 = Reservation()
            reservation_data_2.generate_start_time_and_end_time()
            reservation_data_2.beam_name = beam_name           
             
            org_admin = User()                                            
            org_admin.advanced_org_admin_data()
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            device_group_admin.organization = organization
             
            TestCondition.create_device_group(device_group_name, [beam_name], organization)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            calendar_key = TestCondition.get_calendar_key_via_api(org_admin.email_address, org_admin.password)
            calendar_reservations_org_admin_info = Helper.generate_calendar_reservation(org_admin.email_address, calendar_key)
            calendar_client_org_admin = Calendar_Utilities.add_calendar_account(calendar_reservations_org_admin_info)
            
            calendar_key = TestCondition.get_calendar_key_via_api(device_group_admin.email_address, device_group_admin.password)
            calendar_reservations_device_group_admin_info = Helper.generate_calendar_reservation(device_group_admin.email_address, calendar_key)
            calendar_client_device_group_admin = Calendar_Utilities.add_calendar_account(calendar_reservations_device_group_admin_info)
             
            # steps
            Calendar_Utilities.add_calendar_event(calendar_client_org_admin, reservation_data_1)
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab().select_a_device(beam.beam_name).open_reservation_tab()
            
            actual_reservation_date_time = beam_details_page.get_reservation_data(org_admin)
            expect_reservation_date_time = Helper.analyze_start_time_and_end_time(reservation_data_1.start_time, reservation_data_1.end_time, self._driver._driverSetting.language)
            actual_reservation_name_1 = Calendar_Utilities.get_event_name(calendar_client_org_admin, reservation_data_1)
            expected_reservation_name = Helper.analyze_reservation_name(beam_name, self._driver._driverSetting.language, False)
            
            # verify point:
            self.assertEqual(actual_reservation_date_time, expect_reservation_date_time, 'Reservation shows incorrectly!')
            self.assertEqual(actual_reservation_name_1, expected_reservation_name,
                            "Assertion Error: Reservation name displays as {} instead of {}.".format(actual_reservation_name_1, expected_reservation_name))
            # steps
            Calendar_Utilities.add_calendar_event(calendar_client_device_group_admin, reservation_data_2)
             
            beam_details_page.logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_a_device(beam.beam_name).open_reservation_tab()
            actual_reservation_date_time = beam_details_page.get_reservation_data(device_group_admin)
            expect_reservation_date_time = Helper.analyze_start_time_and_end_time(reservation_data_2.start_time, reservation_data_2.end_time, self._driver._driverSetting.language)
            actual_reservation_name_2 = Calendar_Utilities.get_event_name(calendar_client_device_group_admin, reservation_data_2)
             
            # verify point:
            self.assertEqual(actual_reservation_date_time, expect_reservation_date_time, 'Starting/Ending reservation times show incorrectly!')
            self.assertEqual(actual_reservation_name_2, expected_reservation_name,
                            "Assertion Error: Reservation name displays as {} instead of {}.".format(actual_reservation_name_2, expected_reservation_name))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([device_group_admin], organization)
            TestCondition.delete_device_groups([device_group_name], organization)
            
    
    def test_c33092_creating_an_always_allowed_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating an 'Always Allowed' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Belong to an organization that contains at least one device that is set to accept reservations from all users.
        @steps:
            1. Add a new event in the calendar corresponding to the device over which you have admin privileges.
            
        @expected:
            1. A new reservation for the device should be created, with the start and end times which you selected via your calendar client.
            2. In your calendar client, the name of the event you have just created should change, after a few seconds, to "<device_name> Reservation"
        """
        
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')

            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            #steps
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            actual_reservation_name = Calendar_Utilities.get_event_name(calendar_client, reservation_data)
            expected_reservation_name = Helper.analyze_reservation_name(beam_name, self._driver._driverSetting.language, False)
            
            # verify point:
            self.assertEqual(actual_reservation_name, expected_reservation_name,
                            "Assertion Error: Reservation name displays as {} instead of {}.".format(actual_reservation_name, expected_reservation_name))
            
            beam_details_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_a_device(beam.beam_name).open_reservation_tab()
                
            actual_reservation_date_time = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_date_time = Helper.analyze_start_time_and_end_time(reservation_data.start_time, reservation_data.end_time, self._driver._driverSetting.language)
            
            # verify point:
            self.assertEqual(actual_reservation_date_time, expect_reservation_date_time, 'Starting/Ending reservation times show incorrectly!')
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user], organization)
            TestCondition.delete_device_groups([device_group])
            
            
    def test_c33093_creating_a_by_request_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating an 'Always Allowed' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
        @steps:
            1. Add a new event in the calendar corresponding to the device over which you have admin privileges.
            
        @expected:
            1. A new reservation for the device should be created, with the start and end times which you selected via your calendar client.
            2. In your calendar client, the name of the event you have just created should change, after a few seconds, to "<device_name> Reservation (Pending Approval)"
        """
        
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
                
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
                
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            #steps
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            actual_reservation_name = Calendar_Utilities.get_event_name(calendar_client, reservation_data)
            expected_reservation_name = Helper.analyze_reservation_name(beam_name, self._driver._driverSetting.language, True)
            
            # verify point:
            self.assertEqual(actual_reservation_name, expected_reservation_name,
                            "Assertion Error: Reservation name displays as {} instead of {}.".format(actual_reservation_name, expected_reservation_name))
            
            beam_details_page = LoginPage(self._driver).open().login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_a_device(beam.beam_name).open_reservation_tab()
            
            actual_reservation_date_time = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_date_time = Helper.analyze_start_time_and_end_time(reservation_data.start_time, reservation_data.end_time, self._driver._driverSetting.language)
            
            # verify point:
            self.assertEqual(actual_reservation_date_time, expect_reservation_date_time, 'Starting/Ending reservation times show incorrectly!')
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user], organization)
            TestCondition.delete_device_groups([device_group])
            
    
    def test_c33306_creating_a_reservation_which_has_the_same_time_with_the_rejected_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating a Reservation which has the same time with the rejected reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
        @steps:
            1. Add a new event in the calendar corresponding to the device over which you have admin privileges.
            2. Reject the event on the website
            3. Add another event which has the same time with the rejected event
            
        @expected:
            1. A new reservation for the device should be created, with the start and end times which you selected via your calendar client.
            2. In your calendar client, the name of the event you have just created should change, after a few seconds, to "<device_name> Reservation (Pending Approval)"
        """
        
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group

            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
                
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
                
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            #steps
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            TestCondition.reject_reservation(calendar_client, reservation_data)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            
            actual_reservation_name = Calendar_Utilities.get_event_name(calendar_client, reservation_data)
            expected_reservation_name = Helper.analyze_reservation_name(beam_name, self._driver._driverSetting.language, True)
            
            beam_details_page = LoginPage(self._driver).open().login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_a_device(beam.beam_name).open_reservation_tab()
            
            actual_reservation_date_time = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_date_time = Helper.analyze_start_time_and_end_time(reservation_data.start_time, reservation_data.end_time, self._driver._driverSetting.language)
            
            # verify point:
            self.assertEqual(actual_reservation_date_time, expect_reservation_date_time, 'Starting/Ending reservation times show incorrectly!')
            self.assertEqual(actual_reservation_name, expected_reservation_name,
                            "Assertion Error: Reservation name displays as {} instead of {}.".format(actual_reservation_name, expected_reservation_name))
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user], organization)
            TestCondition.delete_device_groups([device_group])
            
            
    def test_c33307_create_a_reservation_in_the_past_test(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating a Reservation that has start time and end time in the past
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you admin privileges (either org admin or device group admin).
            3. The device should be set to accept reservations.
        @steps:
            1. Add a new event with the start time in the past in the calendar corresponding to the device over which you have admin privileges.            
        @expected:
            1. An error message should show up in your calendar client saying the operation was not successful.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time_in_the_past()
            reservation_data.beam_name = beam_name
                
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
                
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            #steps
            event = Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            self.assertNotEqual(event.__class__.__name__, 'Event', 'User can create a reservation with date time in the past!')
        
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user], organization)
            TestCondition.delete_device_groups([device_group])


    def test_c34000_create_a_reservation_for_user_does_not_have_access(self):
        """
        @author: khoi.ngo
        @date: 02/09/2018
        @summary: Creating a reservation for user who does not have access to the requested device.
        @precondition:
            1. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            2. Set accept reservations of the device to 'Allowed'.
            3. Have a user account which does not have access to your device (or does not have membership to your device group).
        @steps:
            1. Login with admin account (an org or device group admin).
            2. Select the device.
            3. Create a reservation for user who does not have access to the requested device.
        @expected:
            1. An alert message displays
            2. Verify content of message is "This user does not have access to the requested device..."
        """

        try:
            #pre-condition:
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName

            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')

            # steps
            beam_reservation_dialog = LoginPage(self._driver).open()\
                                        .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                                        .goto_beams_tab().select_device_group(device_group).select_a_device(beam.beam_name)\
                                        .open_create_a_reservation_dialog().reserve_a_beam(False, False, normal_user, False)

            # verify points
            self.assertTrue(beam_reservation_dialog.is_alert_dialog_msg_display(), "Assertion Error: An alert message is not displayed.")

            self.assertEqual(beam_reservation_dialog.get_alert_dialog_msg(), ApplicationConst.WARN_MSG_USER_DOES_NOT_HAVE_ACCESS_DEVICE, "Message is not mentioned that the user does not have access to the requested device.")

        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user], organization)
            TestCondition.delete_device_groups([device_group])
