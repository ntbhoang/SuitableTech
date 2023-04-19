from test.testbase import TestBase
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from common.constant import Constant
from common.helper import Helper, EmailDetailHelper
from common.application_constants import ApplicationConst
from core.utilities.utilities import Utilities, Image_Utilities
from pages.suitable_tech.admin.advanced.dashboard import admin_dashboard_page
from data_test.dataobjects.reservation import Reservation
from core.utilities.gmail_utility import GmailUtility
import re
from datetime import datetime
from core.utilities.utilities import Calendar_Utilities
from pages.suitable_tech.user.login_page import LoginPage
import pytest
        
class logigear_Bugs_Release_0_43_2_Test(TestBase):

    def test_c33705_verify_that_welcome_emails_contain_an_activate_link_whenever_inviting_a_normal_or_temporary_user_who_has_not_activated(self):
        """
        @author: Thanh.Le
        @date: 04/18/2017
        @summary: Verify that welcome emails contain an activate link whenever inviting a normal/temporary user who has not activated.
        @description: BUG_68 There is an inconsistency between welcome emails when inviting a normal/temporary user at first time and when inviting a normal/temporary user that has been already invited but not activated.
        @steps:
            1. Login to Suitabletech https://stg1.suitabletech.com with org admin user 
            2. Go to Manage Dashboard page
            3. Invite a new user 
            (e.g suitabletech3+userJan0112017LgvnTest123@gmail.com)
            4. Go to mail box and check content of Welcome email
            5. Invite the user again 
            6. Go to mail box and check content of Welcome email
        @expected:          
            (4)(6) The welcome emails contain an activate link
        """
        try:
            # pre-condition:
            organization_name = Constant.AdvancedOrgName
            device_group_name = Helper.generate_random_device_group_name(5)
            
            new_normal_user = User()
            new_normal_user.generate_advanced_normal_user_data()
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.device_group = device_group_name
            
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])

            #steps - temporary user
            dashboard_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_new_user(new_normal_user)
            
            email_template_1 = EmailDetailHelper.generate_welcome_email(new_normal_user, admin_full_name=org_admin.get_displayed_name())
            actual_msgs_1 = GmailUtility.get_messages(email_template_1.subject, None, org_admin.email_address, new_normal_user.email_address, datetime.now())
            GmailUtility.delete_emails(email_template_1.subject, receiver=new_normal_user.email_address)
            does_email_match_1 = re.match(email_template_1.trimmed_text_content, actual_msgs_1[0].trimmed_text_content, re.I | re.M)             
            self.assertTrue(does_email_match_1,
                "Assertion Error: Expected email content is '{}' but doesn't match '{}'".format(email_template_1.trimmed_text_content, actual_msgs_1[0].trimmed_text_content))
            
            dashboard_page.invite_new_user(new_normal_user)
            email_template_2 = EmailDetailHelper.generate_welcome_email(new_normal_user, admin_full_name=org_admin.get_displayed_name())
            actual_msgs_2 = GmailUtility.get_messages(email_template_2.subject, None, org_admin.email_address, new_normal_user.email_address, datetime.now())
            GmailUtility.delete_emails(email_template_2.subject, receiver=new_normal_user.email_address)
            does_email_match_2 = re.match(email_template_2.trimmed_text_content, actual_msgs_2 [0].trimmed_text_content, re.I | re.M)             
            self.assertTrue(does_email_match_2,
                "Assertion Error: Expected email content is '{}' but doesn't match '{}'".format(email_template_2.trimmed_text_content, actual_msgs_2[0].trimmed_text_content))
        finally:
            # post-condition:
            TestCondition.delete_advanced_users([new_normal_user, org_admin])
            TestCondition.delete_device_groups([device_group_name], organization_name)
    

    @pytest.mark.OnlyDesktop
    def test_c33706_verify_that_reservations_are_shown_correctly_when_user_selects_any_items_of_the_show_dropdown_at_reservation_page(self):
        """
        @author: Thanh.Le
        @date: 04/24/2017
        @summary: Verify that reservations are shown correctly when user selects any items of the "Show" dropdown at Reservation page.
        @precondition: Create Requested/Confirmed/Rejected reservations for a beam 
        @description: BUG_78 Reservations show incorrectly when user selects any item of the "Show" dropdown at Reservation page .
                      BUG_81 Missing checkbox shows "checked/unchecked" next to each item of the "Show" dropdown in the Reservation page
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com
            (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Manage Dashboard page
            3. Open Beams tab
            4. Create a device group and add QA BeamPlus Visitor1 beam to the group
            5. Go to Reservations tab of the device group
            6. Click Show button 
            7. Select all items of the "Show" dropdown
        @expected:          
            (7) The list of reservations should be shown correctly for selecting any item.
        """
        try:
            #pre-condition:
            device_group_name = Helper.generate_random_device_group_name()
            organization_name = Constant.AdvancedOrgName
     
            beam = TestCondition.get_and_lock_beam(organization_name)
            beam_name = beam.beam_name
                 
            reservation_1 = Reservation()
            reservation_1.generate_start_time_and_end_time()
            reservation_1.beam_name = beam_name

            reservation_2 = Reservation()
            reservation_2.generate_start_time_and_end_time()
            reservation_2.beam_name = beam_name

            reservation_3 = Reservation()
            reservation_3.generate_start_time_and_end_time()
            reservation_3.beam_name = beam_name
                 
            normal_user_1 = User()
            normal_user_1.generate_advanced_normal_user_data()
            normal_user_1.device_group = device_group_name

            normal_user_2 = User()
            normal_user_2.generate_advanced_normal_user_data()
            normal_user_2.device_group = device_group_name
                 
            TestCondition.create_device_group(device_group_name, [beam_name], organization_name)
                 
            #Invite a new user and add its account to CalDav client
            TestCondition.create_advanced_normal_users(self._driver, [normal_user_1, normal_user_2])

            calendar_key = TestCondition.get_calendar_key_via_api(normal_user_1.email_address, normal_user_1.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user_1.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)

            #Create confirmed reservations
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')            
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_1)

            #Create requested reservations
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'By Request')   
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_2)         

            #Create rejected reservations
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user_2.email_address, normal_user_2.password)
            calendar_reservations_info_1 = Helper.generate_calendar_reservation(normal_user_2.email_address, calendar_key)
            calendar_client_1 = Calendar_Utilities.add_calendar_account(calendar_reservations_info_1)
            Calendar_Utilities.add_calendar_event(calendar_client_1, reservation_3)
            
            #steps:
            reservations_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .reject_a_requested_reservation(normal_user_2)\
                .goto_beams_tab().select_device_group(device_group_name).goto_reservations_tab()
                  
            #Confirmed Reservations - Reservation Requests - Rejected Requests
            reservations_page = reservations_page.filter_reservation(True, True, True)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(True, True, True),\
                             "The Confirmed Reservations - Reservation Requests - Rejected Requests are filters incorrectly")
            
            #Confirmed Reservations - Reservation Requests
            reservations_page = reservations_page.filter_reservation(True, True, False)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(True, True, False),\
                            "The Confirmed Reservations - Reservation Requests are filters incorrectly")
        
            #Confirmed Reservations - Rejected Requests
            reservations_page = reservations_page.filter_reservation(True, False, True)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(True, False, True),\
                            "The Confirmed Reservations - Rejected Requests are filters incorrectly")
        
            #Reservation Requests - Rejected Requests
            reservations_page = reservations_page.filter_reservation(False, True, True)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(False, True, True),\
                            "Reservation Requests - Rejected Requests are filters incorrectly")
            
            #Confirmed Reservations
            reservations_page = reservations_page.filter_reservation(True, False, False)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(True, False, False),\
                            "The Confirmed Reservations are filters incorrectly")

            #Reservation Requests
            reservations_page = reservations_page.filter_reservation(False, True, False)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(False, True, False),\
                            "Reservation Requests are filters incorrectly")
        
            #Rejected Requests
            reservations_page = reservations_page.filter_reservation(False, False, True)
            self.assertTrue(reservations_page.are_reservations_filtered_correctly(False, False, True),\
                            "The Rejected Requests are filters incorrectly")
        finally:
            #post-condition:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([normal_user_1, normal_user_2])
            TestCondition.delete_device_groups([device_group_name], organization_name)
            
            
    def test_c33707_verify_that_the_starting_date_of_reservations_shows_correctly_on_reservation_page(self):
        """
        @author: Thanh.Le
        @date: 04/14/2017
        @summary: Verify that the starting date of reservations which are created on timezone -08:00 PST and Starting time from 4:00 PM to 11:00 PM shows correctly on Reservation page
        @description: BUG_79 The starting date value of reservations that are created on timezone -08:00 PST and Starting time from 4:00 PM to 11:00 PM shows the next date instead of the correct date on Reservation page
        @precondition: 
            1. Set timezone -08:00 PST for system  
            2. Create a device group with a beam having reservation permission
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com (thanh.viet.le@logigear.com/L0gigear123!)
            2. Go to Manage Dashboard > Beam page
            3. Select a device group and click "Reservations" tab
            4. Click "Reserve a Beam" button
            5. Enter all info on "Create a Reservation" button with Starting time from 4:00 PM to 11:00 PM 
            (e.g Starting February 25, 2017 at time 11:00 PM - Ending February 26, 2017 at time 3:00 PM)
            6. Click "Create" button
            7. Notice starting/ending date of the reservation shown on Reservation page
            
        @expected:          
            (7) The starting date should be shown correctly
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            user_group_name = Helper.generate_random_user_group_name()
            organization_name = Constant.AdvancedOrgName

            beam = TestCondition.get_and_lock_beam(organization_name)
            beam_name = beam.beam_name
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')
            
            period_of_time = Helper.get_period_of_time_base_on_timezone()
            
            reservation = Reservation()
            reservation.generate_start_time_and_end_time_in_period_of_time(period_of_time ['start'], period_of_time ['end'])
            reservation.beam_name = beam_name
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization_name
            org_admin.device_group = device_group_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            normal_user.user_group = user_group_name
            
            TestCondition.create_device_group(device_group_name, [beam_name], organization_name)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_user_group(user_group_name)
            
            #steps:
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .invite_new_user(normal_user)\
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
        finally:
            # post-condition       
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([org_admin, normal_user])
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_user_groups([user_group_name])
      
    
    def test_c33708_verify_that_search_function_of_Reservations_combobox_at_Edit_Device_dialog_works_correctly(self):
        """
        @author: Thanh.Le
        @date: 04/25/2017
        @summary: Verify that search function of Reservations combobox at Edit Device dialog works correctly
        @desciption: BUG_80 Search function of Reservations combobox at Edit Device dialog does not works 
        @precondition: Add a user to a Beam in Simplified Organization (LogiGear Mock Beam+ 2 in LogiGear Test 2)
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Manage Dashboard page
            3. Open Beams tab
            4. Select any beam
            5. Click Edit button to open Edit dialog 
            6. Click Reservations combobox.
            7. Enter any value in the combobox (e.g 'By Request')
        @expected:
            (7) Only 'By Request' is shown. The search function works correctly.
        """ 
        try:
            # pre-condition
            organization_name = Constant.AdvancedOrgName
            beam = TestCondition.get_a_beam(organization_name)
            import random
            permission = random.choice([ApplicationConst.LBL_ALLOWED, ApplicationConst.LBL_NOT_ALLOWED, ApplicationConst.LBL_BY_REQUEST, ApplicationConst.LBL_BY_ADMINISTRATORS_ONLY])
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization_name
            
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            #steps:
            beam_details_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                .goto_beam_details_page_by_id(beam.beam_id)
                
            edit_device_dialog = beam_details_page.open_edit_dialog().search_reservations_permission(permission)
            permission_name = edit_device_dialog.get_reservation_permission_name_at_the_first()
            
            # verify point
            self.assertEqual(permission_name, permission,'Search function of Reservation combobox works incorrectly')
        finally:
            TestCondition.delete_advanced_users([org_admin])
            
            
    def test_c33710_verify_that_image_for_Beam_at_Simplified_Organization_displays_correctly(self):
        """
        @author: Thanh.Le
        @date: 04/19/2017
        @summary: Verify that image for Beam+ at Simplified Organization displays correctly
        @desciption: BUG_90 The image for Beam+ at Simplified Organization displays incorrectly.        
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com(thanh.viet.le@logigear.com/Logigear123)
            2. Go to Dashboard page
            3. Move to Simplified Org (LogiGear Test 2)
            4. Notice the default image icon of Beam+
        @expected:
            The image for Beam+ at Simplified Organization should display correctly (the dark blue logo).
        @note: 
            [3/30/17] The LogiGear Mock Beam+ 3 was net setup to actually be a Beam+ device.  
            I've updated the configuration in the admin tool so the UI should know that its a Beam+.  
            Note, that the term "Beam+" is going away and will start to show up as simply "Beam".  
            So there is TWO products "Beam" and "BeamPro".   
        @note: Ready to automate
        """
        try:
            # pre-condition
            # using 'LogiGear Mock Beam+ 3'
            beam_id = Constant.DeviceIDs["LogiGear Mock Beam+ 3"]
            
            # steps:
            manage_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam_id)\
                .remove_image_icon()
            
            # verify point
            image_url = manage_page.get_icon_link()
            img_text_actual = Utilities.download_file(self._driver, image_url)
            img_text_expected = Utilities.get_test_image_file_path(self._driver, "beam_expected_image.svg", True)

            are_equal = Utilities.compare_text_from_file(self._driver, img_text_expected, img_text_actual)
            self.assertTrue(are_equal, "The image for Beam 3 + Simplified Organization image is not set the dark blue logo")
        finally:
            try:
                if img_text_actual:
                    Utilities.delete_file(img_text_actual)                
            except:
                pass
            
    
    def test_c33711_verify_that_the_open_file_dialog_displays_when_clicking_upload_content_button_at_manage_beam_content_dialog_on_firefox_and_ie_browsers(self):
        """
        @author: Thanh.Le
        @date: 04/21/2017
        @summary: Verify that the open file dialog displays when clicking "Upload Content" button at Manage Beam Content dialog on Firefox and IE browsers
        @desciption: BUG_92 Forbidden 403 error page displays when clicking "Upload Content" button at Manage Beam Content dialog on Firefox and IE browsers      
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com on Firefox/IE browsers
            (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Dashboard page 
            3. Select Orgnizations tab
            4. Click "Manage Beam Content" button at Settings of Orgnizations page
            5. Click "Upload Content"
        @expected:
            Open file dialog should display.
               
        @note: Ready to automate
        """
        try:
            # precondition
            img_file_name = "img2.jpg"     
                         
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
           
             
            #steps
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group_name)                
                
            #upload an image
            dialog_beam_content = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            dialog_beam_content.choose_file(img_file_copied)
            
            #verify point
            self.assertTrue(dialog_beam_content.is_image_displays(filecopied), "Image does not display after uploading")
            
            dialog_beam_content.delete_image_beam_content(filecopied)
            
            #verify point
            self.assertFalse(dialog_beam_content.is_image_displays(filecopied, 5), "Image still displays after deleting")                
            
            dialog_beam_content.click_continue_button()
        finally:
            TestCondition.delete_device_groups([device_group_name])
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)                
            except:
                pass
            
            
    def test_c33713_verify_that_user_is_able_to_remove_the_profile_image_of_All_users_user_group(self):
        """
        @author: Thanh.Le
        @date: 04/14/2017
        @summary: Verify that user is able to remove the profile image of "All users" user group
        @desciption: BUG_95 User is unable to remove the profile image of "All users" user group        
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com(thanh.viet.le@logigear.com/Logigear123)
            2. Go to Dashboard page 
            3. Select Users tab
            4. Select "All users" user group
            5. Edit new profile image of the group
            6. Remove the profile image
        @expected:
             The profile image should be removed and replaced by default image.
           
        @note: Ready to automate
        """
        try:
            img_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")            
               
            # steps
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .goto_user_group_detail_page(ApplicationConst.LBL_ALL_USERS_GROUP)\
                .change_image_icon(img_path)    
                   
            img_link = user_group_detail_page.get_icon_link()
            img_actual_upload = Utilities.download_file(self._driver, img_link) 
            img_expect = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual_upload, img_expect)
            self.assertTrue(are_equal, "The User icon is not set!")     
               
            user_group_detail_page.remove_image_icon()
                   
            img_actual_link = user_group_detail_page.get_icon_link()
            img_text_actual = Utilities.download_file(self._driver, img_actual_link)           
            img_text_expected = Utilities.get_test_image_file_path(self._driver, "tiles_contactGroupIcon_expected.svg", True)
                           
            #verify point:
            are_equal = Utilities.compare_text_from_file(self._driver, img_text_expected, img_text_actual)               
            self.assertTrue(are_equal, "The profile image does not removed and replaced by default image.")
        finally:
            try:
                if img_actual_upload:
                    Utilities.delete_file(img_actual_upload)
                if img_text_actual:
                    Utilities.delete_file(img_text_actual)
            except:
                pass      
            
    
    def test_c33714_verify_that_simplified_organization_admin_is_able_to_add_a_user_that_has_been_allowed_access_to_a_beam_to_other_beams(self):
        """
        @author: Thanh.Le
        @date: 04/18/2017
        @summary: Verify that Simplified Organization admin is able to add a user that has been allowed access to a Beam to other beams
        @desciption: BUG_101: Simplified Organization admin is unable to add a user that has been allowed access to a Beam to other beams. 
        @precondition: Add a user to a Beam in Simplified Organization (LogiGear Mock Beam+ 2 in LogiGear Test 2)
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as Simplified Organization Admin
                (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Simplified Organization (LogiGear Test 2)
            3. Select a beam (not LogiGear Mock Beam+ 2)
            4. Enter email and click "Add User" button
        @expected:
            Success message should display and the user should be added to the Beam.
        """ 
        try:
            # pre-condition:
            test_organization=Constant.SimplifiedOrgName
            beam_1 = TestCondition.get_and_lock_beam(test_organization)
            beam_name_1 = beam_1.beam_name
            
            beam_2 = TestCondition.get_and_lock_beam(test_organization)
            beam_name_2 = beam_2.beam_name
            
            user = User()
            user.generate_simplified_normal_user_data()            
            user.device_group = beam_name_1
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name_2
            
            TestCondition.create_simplified_normal_users(self._driver, user_array=[user], beam=beam_1)
            TestCondition.create_simplified_device_admin(
                                driver=self._driver, 
                                user_array=[simplified_dev_admin], 
                                beam=beam_2,
                                organization=simplified_dev_admin.organization)
            # step:
            simplied_detail_beam_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam_2.beam_id)
            
            simplied_detail_beam_page.add_user(user, False)
            
            # verify point
            success_message = simplied_detail_beam_page.get_msg_success()
            self.assertEqual(success_message, ApplicationConst.INFO_MSG_INVITE_USER_TO_SIMPL_BEAM_SUCCESSFUL.format(user.email_address, beam_name_2), 
                             'Successful message does not display or it does not localize')
            
            is_user_added = simplied_detail_beam_page.is_user_added(user)
            self.assertTrue(is_user_added, 'Cannot add user into Beam')
        finally:
            # post-condition:
            TestCondition.release_a_beam(beam_1)
            TestCondition.release_a_beam(beam_2)
            TestCondition.delete_simplified_users([simplified_dev_admin, user], test_organization)
            
    
    def test_c33715_verify_that_error_message_does_not_display_when_Advance_Organization_admin_invites_a_user_that_has_existed_in_the_organization_yet(self):
        """
        @author: Thanh.Le
        @date: 04/13/2017
        @summary: Verify that error message does not display when Advance Organization admin invites a user that has existed in the organization yet 
        @desciption: BUG_102 Error message does not display when Advance Organization admin invites a user that has existed in the organization yet
        @precondition: There is a normal user in Advance Organization (LogiGear Test)
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as Simplified Organization Admin (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Dashboard page
            3. Click "Invite a New User" button
            4. Invite the normal user that has existed in the organization yet
        @expected:
            The success message should display and a welcome email should be sent to the normal user's inbox.
            
        @note: Ready to automate
        """
        try:
            # pre-condition 
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()            
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
                            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .invite_new_user(normal_user, wait_for_completed = False)
                
            # verify point:
            self.assertEqual(admin_dashboard_page.get_msg_success(), ApplicationConst.INFO_INVITATION_MAIL_SENT_SUCCESSFUL.format(normal_user.email_address), 
                             "The invite to {} success message does not display.".format(normal_user.email_address))   
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user])
               

    def test_c33716_verify_that_Manager_Beam_Content_function_is_at_Device_group_settings_and_Organization_settings(self):
        """
        @author: Thanh.Le
        @date: 04/14/2017
        @summary: Verify that Manager Beam Content function is on Device group settings and Organization settings
        @desciption: BUG_107 Manager Beam Content function is removed after build 0.43.2 is released        
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com(thanh.viet.le@logigear.com/Logigear123)
            2. Go to Organization page
            3. Open Settings tab
        @expected:
            Manager Content Beam section should be displayed on Device group settings and Organization settings.
           
        @note: Ready to automate
        """
        try:
            # steps
            account_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_org_setting_page()
               
            #verify point:
            self.assertTrue(account_setting_page.is_beam_content_section_displayed(), 
                            "Manager Content Beam section doesn't display on the Settings page.")
        finally:
            pass
            
    