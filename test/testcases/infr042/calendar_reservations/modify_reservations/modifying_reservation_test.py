from data_test.dataobjects.user import User
from common.constant import Constant
from common.application_constants import ApplicationConst
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.utilities.utilities import Calendar_Utilities
from data_test.dataobjects.reservation import Reservation
 
 
class ModifyingReservation_Test(TestBase):
    
    def test_c33094_attempting_modify_confirmed_reservation(self):
        """
        @author: thanh.le
        @date: 02/16/2017
        @summary: Attempting to Modify a Confirmed Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
            4. Reserve this device in the future, and set the status of this reservation to 'confirmed'.
        @steps:
            1. In your calendar client, find the event corresponding to your confirmed reservation.
            2. Attempt to modify the start and end times of this event via your calendar client.
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
            normal_user.organization = organization
               
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
           
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user], activate_user=True, pass_safety_video=False)
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
             
            # normal user reverse a beam
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
                     
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            TestCondition.approve_reservation(calendar_client, reservation_data)
             
            # steps
            edit_time = reservation_data.generate_edit_start_time_and_end_time()
            response = Calendar_Utilities.modify_reservation_time(calendar_client, reservation_data, edit_time)

            # verify points   
            self.assertEqual(response,"400 Bad Request", "The start and end times of your reservation change via your calendar client.")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([org_admin, normal_user])
            TestCondition.delete_device_groups([device_group], organization)
             
     
    def test_c33095_modifying_admin_only_reservation(self):
        """
        @author: thanh.le
        @date: 02/21/2017
        @summary: Modifying an 'Admin Only' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you admin privileges (either org admin or device group admin).
            3. The device should be set to accept reservations 'By Administrators' only.
            4. Reserve this device in the future.
        @steps:
            1. In your calendar client, find the event corresponding to your reservation.
            2. Modify the start and end times of this event via your calendar client..
        @expected:
            1. The start and end times of your reservation should change to match those which you selected via your calendar client.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Administrator')
             
            org_admin_reservation_data = Reservation()
            org_admin_reservation_data.generate_start_time_and_end_time()
            org_admin_reservation_data.beam_name = beam_name
                     
            device_group_reservation_data = Reservation()
            device_group_reservation_data.generate_start_time_and_end_time()
            device_group_reservation_data.beam_name = beam_name   
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
            
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group
            device_group_admin.organization = organization
            
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            calendar_key = TestCondition.get_calendar_key_via_api(org_admin.email_address, org_admin.password)
            org_admin_calendar_reservations_info = Helper.generate_calendar_reservation(org_admin.email_address, calendar_key)
            org_admin_calendar_client = Calendar_Utilities.add_calendar_account(org_admin_calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(org_admin_calendar_client, org_admin_reservation_data)
            
            # steps
            org_admin_edit_time = org_admin_reservation_data.generate_edit_start_time_and_end_time()
            org_admin_expected_time = Helper.analyze_start_time_and_end_time(org_admin_edit_time['start_time'], org_admin_edit_time['end_time'], self._driver._driverSetting.language)
            Calendar_Utilities.modify_reservation_time(org_admin_calendar_client, org_admin_reservation_data, org_admin_edit_time)

            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                .select_a_device(beam_name)\
                
            org_admin_observe_time = beam_details_page.open_reservation_tab()\
                .get_reservation_data(org_admin)     
                       
            # verify points   
            self.assertEqual(org_admin_observe_time, org_admin_expected_time, "The start and end times of your reservation doesn't change via your calendar client.")
            TestCondition.delete_advanced_users([org_admin], organization)
            
            # device group admin reverse a beam
            calendar_key = TestCondition.get_calendar_key_via_api(device_group_admin.email_address, device_group_admin.password)
            device_group_calendar_reservations_info = Helper.generate_calendar_reservation(device_group_admin.email_address, calendar_key)
            device_group_calendar_client = Calendar_Utilities.add_calendar_account(device_group_calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(device_group_calendar_client, device_group_reservation_data)
             
            dvg_admin_edit_time = device_group_reservation_data.generate_edit_start_time_and_end_time()
            dvg_admin_expected_time = Helper.analyze_start_time_and_end_time(dvg_admin_edit_time['start_time'], dvg_admin_edit_time['end_time'], self._driver._driverSetting.language)
            Calendar_Utilities.modify_reservation_time(device_group_calendar_client, device_group_reservation_data, dvg_admin_edit_time)
            
            device_group_observe_time = beam_details_page.logout_and_login_again(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab()\
                .select_a_device(beam_name)\
                .open_reservation_tab()\
                .get_reservation_data(device_group_admin)
             
            # verify points   
            self.assertEqual(device_group_observe_time, dvg_admin_expected_time, "The start and end times of your reservation doesn't change via your calendar client.")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group], organization)
            TestCondition.delete_advanced_users([device_group_admin], organization)


    def test_c33096_modifying_always_allowed_reservation(self):
        """
        @author: thanh.le
        @date: 02/22/2017
        @summary: Modifying an 'Always Allowed' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Belong to an organization that contains at least one device that is set to accept reservations from all users.
            3. Reserve this device in the future.
        @steps:
            1. In your calendar client, find the event corresponding to your reservation.
            2. Modify the start and end times of this event via your calendar client.
        @expected:
            1. The start and end times of your reservation should change to match those which you selected via your calendar client.
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
             
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.user_group = user_group_name
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
             
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_user_group(user_group_name)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')
             
            # normal user reverse a beam
            dashboard_page = LoginPage(self._driver).open()\
                    .login(org_admin.email_address, org_admin.password)\
                    .invite_new_user(normal_user)\
            
            TestCondition._activate_user(self._driver, normal_user, email_subject=ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE)
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
                     
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            
            edit_time = reservation_data.generate_edit_start_time_and_end_time()
            expected_time = Helper.analyze_start_time_and_end_time(edit_time['start_time'], edit_time['end_time'], self._driver._driverSetting.language)
                  
            # steps
            Calendar_Utilities.modify_reservation_time(calendar_client, reservation_data, edit_time)
            observe_time = dashboard_page.goto_beams_tab()\
                    .select_a_device(beam_name)\
                    .open_reservation_tab()\
                    .get_reservation_data(normal_user)
            
            # verify points   
            self.assertEqual(observe_time, expected_time, "The start and end times of your reservation doesn't change via your calendar client.")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([org_admin, normal_user])
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group], organization)
            
            
    def test_c33097_modifying_by_request_reservation(self):
        """
        @author: thanh.le
        @date: 02/22/2017
        @summary: Modifying a 'By Request' Reservation
        @precondition:
            1. Have a CalDav client with your Suitable account added to it.
            2. Have at least one device over which you do not have admin privileges (meaning you are neither an org or device group admin).
            3. The device should be set to accept reservations 'By Request' only.
            4. Reserve this device in the future, and leave the status of this reservation as' requested'.
        @steps:
            1. In your calendar client, find the event corresponding to your reservation.
            2. Modify the start and end times of this event via your calendar client.
        @expected:
            1. The start and end times of your reservation should change to match those which you selected via your calendar client.
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
             
            reservation_data = Reservation()
            reservation_data.generate_start_time_and_end_time()
            reservation_data.beam_name = beam_name
                      
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            #normal_user.user_group = user_group_name
            normal_user.device_group = device_group
            normal_user.organization = organization
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group
            org_admin.organization = organization
             
            TestCondition.create_device_group(device_group, [beam_name], organization)
            TestCondition.create_user_group(user_group_name)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')
             
            # normal user reverse a beam
            dashboard_page = LoginPage(self._driver).open()\
                    .login(org_admin.email_address, org_admin.password)\
                    .invite_new_user(normal_user)\
            
            TestCondition._activate_user(self._driver, normal_user, email_subject=ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE.format(normal_user.organization))
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
                   
            edit_time = reservation_data.generate_edit_start_time_and_end_time()
            expected_time = Helper.analyze_start_time_and_end_time(edit_time['start_time'], edit_time['end_time'], self._driver._driverSetting.language)
   
            # steps
            Calendar_Utilities.modify_reservation_time(calendar_client, reservation_data, edit_time)
            observe_time = dashboard_page.goto_beams_tab()\
                    .select_a_device(beam_name)\
                    .open_reservation_tab()\
                    .get_reservation_data(normal_user)
            
            # verify points   
            self.assertEqual(observe_time, expected_time, "The start and end times of your reservation doesn't change via your calendar client.")
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([org_admin, normal_user])
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group], organization)            
            
