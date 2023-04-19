from data_test.dataobjects.user import User
from data_test.dataobjects.reservation import Reservation
from common.constant import Constant, Platform
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.utilities.utilities import Calendar_Utilities
from common.application_constants import ApplicationConst


class CalendarAccount_Test(TestBase):

    def test_c33087_add_calendar_account(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Adding Calendar Account
        @precondition:
            1. Have a CalDav compatible client (https://en.wikipedia.org/wiki/CalDAV#Client).
        @steps:
            1. Obtain your User Name, Password, and Server Address from the 'Calendar Reservation Settings' section of your account settings page. Please note that this password is not the same as the password you use to log into your Suitable account.
            2. Use these three values to add the calendar account to your calendar client. Each client will have slightly different workflows for adding a new account.
            
        @expected:
            1. The calendar account should be successfully added.
            2. New calendars should be created, each corresponding to a Beam in your organization(s) for which you can create reservations for.
            3. Any existing reservations which are not more than 2 weeks in the past should be populated in the new calendar.
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
            normal_user.organization = organization
                        
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            
            # steps
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            # verify points                       
            self.assertTrue(Calendar_Utilities.does_calendar_account_added(calendar_client),
                    "Could not add calendar account for user: {}".format(normal_user.email_address))
            
            self.assertTrue(Calendar_Utilities.is_calendar_existed(calendar_client, beam_name),
                    "Calendar does not display on the client app")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group], organization)
   
            
    def test_c33090_delete_a_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Deleting a Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. This account should be populated with at least one reservation event.
            3. This reservation event can be either 'confirmed' or 'requested'.
        @steps:
            1. Delete the event corresponding to the reservation which you wish to delete.
            
        @expected:
            1. The reservation should no longer exist.
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
            normal_user.organization = organization
            
            reservation_data_1 = Reservation()
            reservation_data_1.generate_start_time_and_end_time()
            reservation_data_1.beam_name = beam_name
            
            reservation_data_2 = Reservation()
            reservation_data_2.generate_start_time_and_end_time()
            reservation_data_2.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data_1)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data_2)
            TestCondition.approve_reservation(calendar_client, reservation_data_1)
            
            # steps
            Calendar_Utilities.delete_reservation(calendar_client, reservation_data_1)
            Calendar_Utilities.delete_reservation(calendar_client, reservation_data_2)
            
            # verify points
            self.assertFalse(Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data_1),
                "Reservation is still exist!")
            self.assertFalse(Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data_2),
                "Reservation is still exist!")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group], organization)
                

    def test_c33350_deleting_a_reservation_on_website(self):
        """
        @author: thanh.le
        @date: 03/20/2017
        @summary: Deleting a Reservation on Website
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. This account should be populated with at least one reservation event.
            3. This reservation event is confirmed.
        @steps:
            1. Login as Device group admin/ Org Admin
            2. Delete the event corresponding to the reservation on website.
            
        @expected:
            1. 'The reservation was deleted.' message displays.
            2. The reservation should no longer exist on both Website and CalDav client.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            
            #Step
            beam_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_a_device(beam.beam_name)\
                .open_reservation_tab().delete_reservation(normal_user)
                
            # verify
            self.assertEqual(beam_detail_page.get_msg_success(), ApplicationConst.INFO_MSG_DELETE_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            self.assertTrue(beam_detail_page.is_reservation_deleted(normal_user), "Assertion Error: The reservation is not delete on website")
            self.assertFalse(Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data),
                "Reservation still exists in Calendar client!")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group],organization)
            
            
    def test_c33351_rejecting_a_reservation_on_website(self):
        """
        @author: thanh.le
        @date: 03/22/2017
        @summary: Rejecting a Reservation on Website
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. This account should be populated with at least one reservation event.
            3. This reservation event is requested
        @steps:
            1. Login as Device group admin/ Org Admin
            2. Reject the event corresponding to the reservation at Dashboard page, Reservation tab in device detail page
            
        @expected:
            1. 'The reservation was rejected.' message displays.
            2. The reservation should have rejected status on Website and no longer exist CalDav client.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            reservation_data_1 = Reservation()
            reservation_data_1.generate_start_time_and_end_time()
            reservation_data_1.beam_name = beam_name
            
            reservation_data_2 = Reservation()
            reservation_data_2.generate_start_time_and_end_time()
            reservation_data_2.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
             
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data_1)
            
            #Step - at Dashboard page
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .reject_a_requested_reservation(normal_user)
            
            # verify
            self.assertEqual(admin_dashboard_page.get_msg_success(), ApplicationConst.INFO_MSG_REJECT_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")   
            self.assertFalse(Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data_1),
                "Reservation still exists in Calendar client!")
            
            #Step - at Reservation tab in device detail page 
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data_2)
            beam_detail_page = admin_dashboard_page.goto_beams_tab().select_a_device(beam.beam_name)\
                .open_reservation_tab().reject_a_requested_reservation(normal_user)
                
            # verify
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertEqual(beam_detail_page.get_msg_success(), ApplicationConst.INFO_MSG_REJECT_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            else:
                self.assertEqual(beam_detail_page.get_msg_success(), ApplicationConst.INFO_MOBILE_MSG_REJECT_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            self.assertEqual(beam_detail_page.get_reservation_status(normal_user), ApplicationConst.LBL_RESERVATION_REJECTED_STATUS, 
                             "Assertion Error: The reservation status is incorrect")
            self.assertFalse(Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data_2),
                "Reservation still exists in Calendar client!")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group],organization)
            
            