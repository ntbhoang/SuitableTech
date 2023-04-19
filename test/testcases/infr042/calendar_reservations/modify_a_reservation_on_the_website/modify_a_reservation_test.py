from data_test.dataobjects.user import User
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.utilities.utilities import Calendar_Utilities
from data_test.dataobjects.reservation import Reservation
from common.application_constants import ApplicationConst
 
 
class ModifyingReservation_Test(TestBase):
    
    def test_c33302_modify_an_admin_only_reservation(self):
        """
        @author: thanh.le
        @date: 03/15/2017
        @summary: Modifying an 'Admin Only' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you admin privileges (either org admin or device group admin).
            3. The device should be set to accept reservations 'By Administrators' only.
            4. Reserve this device in the future.
        @steps:
            1. On the Website, find the event corresponding to your reservation.
            2. Modify the start and end times of this event.
        @expected:
            1. Successful message should be displayed.
            2. The start and end times of your reservation should change to match those which you selected.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
             
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
             
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group
            device_group_admin.organization = organization
            
            reservation_data_1 = Reservation()
            reservation_data_1.generate_start_time_and_end_time()
            reservation_data_1.beam_name = beam_name
            
            reservation_data_2 = Reservation()
            reservation_data_2.generate_start_time_and_end_time()
            reservation_data_2.beam_name = beam_name
           
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Administrator')
            
            calendar_key = TestCondition.get_calendar_key_via_api(device_group_admin.email_address, device_group_admin.password)
            calendar_reservations_info_1 = Helper.generate_calendar_reservation(device_group_admin.email_address, calendar_key)
            
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info_1)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data_1)
            edit_time_1 = reservation_data_1.generate_edit_start_time_and_end_time()
            reservation_data_1.start_time = edit_time_1['start_time']
            reservation_data_1.end_time = edit_time_1['end_time']
            expected_time_1 = Helper.analyze_start_time_and_end_time(reservation_data_1.start_time, reservation_data_1.end_time, self._driver._driverSetting.language)
            
            # steps
            beam_details_page = LoginPage(self._driver).open()\
                    .login(device_group_admin.email_address, device_group_admin.password)\
                    .goto_beams_tab()\
                    .select_a_device(beam_name)\
                    .open_reservation_tab()\
                    .update_reservation(device_group_admin, reservation_data_1.start_time, reservation_data_1.end_time)
            
            # verify point
            # 1. Successful message displays
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL, 'Successful message does not display or it does not localize!')
            
            # 2. Start time and end time show correctly on website
            actual_time_1 = beam_details_page.get_reservation_data(device_group_admin)
            self.assertEqual(actual_time_1, expected_time_1, 'Starting/Ending reservation times show incorrectly!')
            
            # 3. Start time and end time are saved into DB correct
            does_reservation_existed = Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data_1)
            self.assertTrue(does_reservation_existed, 'Starting/Ending reservation times does not match between website and calendar app!')
            
            TestCondition.delete_advanced_users([device_group_admin], organization)
            calendar_key = TestCondition.get_calendar_key_via_api(org_admin.email_address, org_admin.password)
            calendar_reservations_info_2 = Helper.generate_calendar_reservation(org_admin.email_address, calendar_key)
            
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info_2)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data_2)
            edit_time_2 = reservation_data_2.generate_edit_start_time_and_end_time()
            reservation_data_2.start_time = edit_time_2['start_time']
            reservation_data_2.end_time = edit_time_2['end_time']
            expected_time_2 = Helper.analyze_start_time_and_end_time(reservation_data_2.start_time, reservation_data_2.end_time, self._driver._driverSetting.language)
            
            # steps
            beam_details_page = beam_details_page.logout_and_login_again(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                .select_a_device(beam_name)\
                .open_reservation_tab()\
                .update_reservation(org_admin, reservation_data_2.start_time, reservation_data_2.end_time)
            
            # verify point
            # 1. Successful message displays
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL, 'Successful message does not display or it does not localize!')
            
            # 2. Start time and end time show correctly on website
            actual_time_2 = beam_details_page.get_reservation_data(org_admin)
            self.assertEqual(actual_time_2, expected_time_2, 'Starting/Ending reservation times show incorrectly!')
            
            # 3. Start time and end time are saved into DB correct
            does_reservation_existed = Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data_2)
            self.assertTrue(does_reservation_existed, 'Starting/Ending reservation times does not match between website and calendar app!')
            
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group], organization)
            TestCondition.delete_advanced_users([org_admin], organization)
             
    
    def test_c33303_modifying_a_always_allowed_reservation(self):
        """
        @author: thanh.le
        @date: 03/20/2017
        @summary: Modifying an 'Always Allowed' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Belong to an organization that contains at least one device that is set to accept reservations from all users.
            3. Reserve this device in the future.
        @steps:
            1. On the Website, find the event corresponding to your reservation.
            2. Modify the start and end times of this event.
        @expected:
            1. Successful message should be displayed.
            2. The start and end times of your reservation should change to match those which you selected.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
             
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
             
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
             
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')
            
            calendar_key = TestCondition.get_calendar_key_via_api(org_admin.email_address, org_admin.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(org_admin.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            edit_time = reservation_data.generate_edit_start_time_and_end_time()
            reservation_data.start_time = edit_time['start_time']
            reservation_data.end_time = edit_time['end_time']
            expected_time = Helper.analyze_start_time_and_end_time(reservation_data.start_time, reservation_data.end_time, self._driver._driverSetting.language)
            
            # steps
            beam_details_page = LoginPage(self._driver).open()\
                    .login(org_admin.email_address, org_admin.password)\
                    .goto_beams_tab()\
                    .select_a_device(beam_name)\
                    .open_reservation_tab()\
                    .update_reservation(org_admin, reservation_data.start_time, reservation_data.end_time)
            
            # verify point
            # 1. Successful message displays
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL, 'Successful message does not display or it does not localize!')
            
            # 2. Start time and end time show correctly on website
            actual_time = beam_details_page.get_reservation_data(org_admin)
            self.assertEqual(actual_time, expected_time, 'Starting/Ending reservation times show incorrectly!')
            
            # 3. Start time and end time are saved into DB correct
            does_reservation_existed = Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data)
            self.assertTrue(does_reservation_existed, 'Starting/Ending reservation times does not match between website and calendar app!')
            
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group], organization)
            TestCondition.delete_advanced_users([org_admin], organization)
             
    
    def test_c33304_modify_a_by_request_reservation(self):
        """
        @author: thanh.le
        @date: 03/20/2017
        @summary: Modifying a 'By Request' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
            4. Reserve this device in the future, and leave the status of this reservation as' requested'.
        @steps:
            1. On the Website, find the event corresponding to your reservation.
            2. Modify the start and end times of this event.
        @expected:
            1. Successful message should be displayed.
            2. The start and end times of your reservation should change to match those which you selected.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
             
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
             
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            normal_user.organization = organization
        
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
                     
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            edit_time = reservation_data.generate_edit_start_time_and_end_time()
            reservation_data.start_time = edit_time['start_time']
            reservation_data.end_time = edit_time['end_time']
            expected_time = Helper.format_start_time_and_end_time_on_website(reservation_data.start_time, reservation_data.end_time, self._driver._driverSetting.language)
            
            # steps
            beam_details_page = LoginPage(self._driver).open()\
                    .login(org_admin.email_address, org_admin.password)\
                    .goto_beams_tab().select_a_device(beam_name)\
                    .open_reservation_tab()\
                    .update_reservation(normal_user, reservation_data.start_time, reservation_data.end_time)
            
            # verify point
            # 1. Successful message displays
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL, 'Successful message does not display or it does not localize!')
            
            # 2. Start time and end time show correctly on website
            actual_time = beam_details_page.get_reservation_data(normal_user)
            self.assertEqual(actual_time, expected_time, 'Starting/Ending reservation times show incorrectly!')
            
            # 3. Start time and end time are saved into DB correct
            does_reservation_existed = Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data)
            self.assertTrue(does_reservation_existed, 'Starting/Ending reservation times does not match between website and calendar app!')
            
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group], organization)
            TestCondition.delete_advanced_users([org_admin, normal_user], organization)
             

    def test_c33305_modify_a_confirmed_reservation(self):
        """
        @author: thanh.le
        @date: 03/20/2017
        @summary: Modifying a 'Confirmed' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
            4. Reserve this device in the future, and leave the status of this reservation as' requested'.
        @steps:
            1. On the Website, find the event corresponding to your confirmed reservation.
            2. Modify the start and end times of this event.
        @expected:
            1. Successful message should be displayed.
            2. The start and end times of your reservation should change to match those which you selected.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
             
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
             
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group
            normal_user.organization = organization
        
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            TestCondition.approve_reservation(calendar_client, reservation_data)
            edit_time = reservation_data.generate_edit_start_time_and_end_time()
            reservation_data.start_time = edit_time['start_time']
            reservation_data.end_time = edit_time['end_time']
            expected_time = Helper.format_start_time_and_end_time_on_website(reservation_data.start_time, reservation_data.end_time, self._driver._driverSetting.language)
            
            # steps
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab().select_a_device(beam_name)\
                .open_reservation_tab()\
                .update_reservation(normal_user, reservation_data.start_time, reservation_data.end_time)
            
            # verify point
            # 1. Successful message displays
            self.assertEqual(beam_details_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL, 'Successful message does not display or it does not localize!')
            
            # 2. Start time and end time show correctly on website
            actual_time = beam_details_page.get_reservation_data(normal_user)
            self.assertEqual(actual_time, expected_time, 'Starting/Ending reservation times show incorrectly!')
            
            # 3. Start time and end time are saved into DB correct
            does_reservation_existed = Calendar_Utilities.does_reservation_existed(calendar_client, reservation_data)
            self.assertTrue(does_reservation_existed, 'Starting/Ending reservation times does not match between website and calendar app!')
            
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group], organization)
            TestCondition.delete_advanced_users([org_admin, normal_user], organization)