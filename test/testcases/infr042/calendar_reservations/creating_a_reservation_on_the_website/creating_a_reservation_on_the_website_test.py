from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.utilities.utilities import Calendar_Utilities
from data_test.dataobjects.reservation import Reservation
from common.application_constants import ApplicationConst


class CreatingAReservationOnTheWebsite_Test(TestBase):

    def test_c33299_creating_an_admin_only_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating an 'Admin Only' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you admin privileges (either org admin or device group admin).
            3. The device should be set to accept reservations 'By Administrators' only.
        @steps:
            1. Add a new reservation on the Website corresponding to the device over which you have admin privileges.
            
        @expected:
            1. 'The reservation was created' message displays.
            2. Reservation data displays correctly on the Website and Calendar client app.
        """
           
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName

            beam_1 = TestCondition.get_and_lock_beam(organization)
            beam_name_1 = beam_1.beam_name
            beam_2 = TestCondition.get_and_lock_beam(organization)
            beam_name_2 = beam_2.beam_name
            
            TestCondition.set_advanced_beam_reservation_permisson(beam_1, "By Administrator")
            TestCondition.set_advanced_beam_reservation_permisson(beam_2, "By Administrator")
            
            reservation_1 = Reservation()
            reservation_1.generate_start_time_and_end_time()
            reservation_1.beam_name = beam_name_1
             
            reservation_2 = Reservation()
            reservation_2.generate_start_time_and_end_time()
            reservation_2.beam_name = beam_name_2          
              
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization
             
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            device_group_admin.organization = organization
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name, [beam_name_1, beam_name_2], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            
            org_calendar_key = TestCondition.get_calendar_key_via_api(org_admin.email_address, org_admin.password)
            calendar_reservations_org_admin_info = Helper.generate_calendar_reservation(org_admin.email_address, org_calendar_key)
            
            dv_admin_calendar_key = TestCondition.get_calendar_key_via_api(device_group_admin.email_address, device_group_admin.password)
            calendar_reservations_dev_admin_info = Helper.generate_calendar_reservation(device_group_admin.email_address, dv_admin_calendar_key)
            
            calendar_client_org_admin = Calendar_Utilities.add_calendar_account(calendar_reservations_org_admin_info)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=False, pass_safety_video=False)
            
            # steps - org admin
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab().select_a_device(beam_1.beam_name)\
                .reserve_a_beam(reservation_1.start_time, reservation_1.end_time, normal_user)
            
            # verify
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_CREATE_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            
            beam_details_page.open_reservation_tab()
            actual_reservation_time_1 = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_time_1 = Helper.format_start_time_and_end_time_on_website(reservation_1.start_time, reservation_1.end_time, self._driver._driverSetting.language)
            
            self.assertEqual(actual_reservation_time_1, expect_reservation_time_1,
                            "Assertion Error: Reservation data displays correctly on the Website")
            
            is_calendar_added_to_calendar_client = Calendar_Utilities.is_calendar_existed(calendar_client_org_admin, beam_name_1)
            
            self.assertTrue(is_calendar_added_to_calendar_client, "Assertion Error: Reservation is not added to Calendar client")
            
            #step - device group admin
            calendar_client_device_group_admin = Calendar_Utilities.add_calendar_account(calendar_reservations_dev_admin_info)
        
            beam_details_page.logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab().select_a_device(beam_2.beam_name)\
                .reserve_a_beam(reservation_2.start_time, reservation_2.end_time, normal_user)
                
            # verify
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_CREATE_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            
            beam_details_page.open_reservation_tab()
            actual_reservation_time_2 = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_time_2 = Helper.format_start_time_and_end_time_on_website(reservation_2.start_time, reservation_2.end_time, self._driver._driverSetting.language)
            
            self.assertEqual(actual_reservation_time_2, expect_reservation_time_2,
                            "Assertion Error: Reservation data displays correctly on the Website")
            
            is_calendar_added_to_calendar_client = Calendar_Utilities.is_calendar_existed(calendar_client_device_group_admin, beam_name_2)
            
            self.assertTrue(is_calendar_added_to_calendar_client, "Assertion Error: Reservation is not added to Calendar client")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam_1)
            TestCondition.release_a_beam(beam_2)
            TestCondition.set_advanced_beam_reservation_permisson(beam_1, "Not Allowed")
            TestCondition.set_advanced_beam_reservation_permisson(beam_2, "Not Allowed")
            TestCondition.delete_advanced_users([org_admin, normal_user], organization)
            TestCondition.delete_device_groups([device_group_name], organization)
            
            
    def test_c33300_creating_an_always_allowed_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating an 'Always Allowed' Reservation 
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Belong to an organization that contains at least one device that is set to accept reservations from all users.
        @steps:
            1. Add a new reservation on Website corresponding to the device that accepts reservations from all users.
        @expected:
            1. 'The reservation was created' message displays.
            2. Reservation data displays correctly on the Website and Calendar client app.
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
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            reservation = Reservation()
            reservation.generate_start_time_and_end_time()
            reservation.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')
             
            #step
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab().select_a_device(beam.beam_name)\
                .reserve_a_beam(reservation.start_time, reservation.end_time, normal_user)
            
            # verify
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_CREATE_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            
            beam_details_page = beam_details_page.open_reservation_tab()
            actual_reservation_time = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_time = Helper.format_start_time_and_end_time_on_website(reservation.start_time, reservation.end_time, self._driver._driverSetting.language)
            
            self.assertEqual(actual_reservation_time, expect_reservation_time,
                            "Assertion Error: Reservation data displays correctly on the Website")

            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)            

            is_calendar_added_to_calendar_client = Calendar_Utilities.does_reservation_existed(calendar_client, reservation)
            self.assertTrue(is_calendar_added_to_calendar_client, "Assertion Error: Reservation is not added to Calendar client")       
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([org_admin, normal_user], organization)
            TestCondition.delete_device_groups([device_group], organization)
            
            
    def test_c33301_creating_a_by_request_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Creating an 'By Request' Reservation 
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
        @steps:
            1. Add a new reservation on the Website corresponding to the device over which you have admin privileges.
        @expected:
            1. 'The reservation was created' message displays.
            2. Reservation data displays correctly on the Website and Calendar client app.
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
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            reservation = Reservation()
            reservation.generate_start_time_and_end_time()
            reservation.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
             
            #step
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab().select_a_device(beam.beam_name)\
                .reserve_a_beam(reservation.start_time, reservation.end_time, normal_user)
            
            # verify
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_CREATE_RESERVATION_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            
            beam_details_page = beam_details_page.open_reservation_tab()
            actual_reservation_time = beam_details_page.get_reservation_data(normal_user)
            expect_reservation_time = Helper.format_start_time_and_end_time_on_website(reservation.start_time, reservation.end_time, self._driver._driverSetting.language)
            
            self.assertEqual(actual_reservation_time, expect_reservation_time,
                            "Assertion Error: Reservation data displays correctly on the Website")
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            is_calendar_added_to_calendar_client = Calendar_Utilities.is_calendar_existed(calendar_client, beam_name)
            self.assertTrue(is_calendar_added_to_calendar_client, "Assertion Error: Reservation is not added to Calendar client")       
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([org_admin, normal_user], organization)
            TestCondition.delete_device_groups([device_group], organization)