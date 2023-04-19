from common.constant import Constant, Platform
from data_test.dataobjects.user import User
from common.helper import Helper, EmailDetailHelper
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from data_test.dataobjects.reservation import Reservation
from core.utilities.utilities import Calendar_Utilities, Utilities
from common.application_constants import ApplicationConst
from data_test.dataobjects.enum import WeekDays
from core.utilities.gmail_utility import GmailUtility
import re


class LogigearWebAutomationTestingBugs_FixedOn044_Test(TestBase):

    def test_c33882_verify_that_reservation_times_display_correctly_when_users_continue_creating_after_getting_conflict_error(self):
        """
        @author: Khoi Ngo
        @date: 10/4/2017
        @summary: Verify that reservation times display correctly when users continue creating after getting conflict error
        @precondition:
            Create org admin, normal user, device group has device and one reservation
        @description:
            First, users create a reservation with time is conflicted, they get conflict error.
            Then, users update time and click Create button again,
                they notice that the reservation displays with time sooner than updated time
                (number of hour deviation depends on time zone).
            For exam: if time zone is "Asia/Bangkok" UTC+7, number of hour deviation is 7.
        @steps:
            1) Login the staging site by organization account
                (khoi.ngo@logigear.com/L0gigear123!)
            2) Go to Beams tab
            3) Select device group A
            4) Select a device
            5) Open Create a Reservation dialog
            6) Create a Reservation have time conflict with other reservation
            7) Update time to not conflict.
            8) Click "Create" button again
        @expected:
            (8) A reservation displays with time like updated time
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()

            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name

            normal_user_2 = User()
            normal_user_2.generate_advanced_normal_user_data()
            normal_user_2.device_group = device_group_name

            reservation = Reservation()
            reservation.generate_start_time_and_end_time()
            reservation.beam_name = beam_name
            edited_reservation = reservation.generate_edit_start_time_and_end_time()

            TestCondition.create_device_group(device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user, normal_user_2])

            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_normal_user_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client_normal_user = Calendar_Utilities.add_calendar_account(calendar_reservations_normal_user_info)
            Calendar_Utilities.add_calendar_event(calendar_client_normal_user, reservation)

            # steps
            admin_beam_detail_page = LoginPage(self._driver).open()\
                                                            .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                                                            .goto_beams_tab()\
                                                            .select_device_group(device_group_name)\
                                                            .select_a_device(beam_name)\
                                                            .open_create_a_reservation_dialog()\
                                                            .reserve_a_beam(reservation.start_time, reservation.end_time, normal_user_2, False)\
                                                            .reserve_a_beam(edited_reservation['start_time'], edited_reservation['end_time'])

            reservation_page = admin_beam_detail_page.open_reservation_tab()
            actual_reservation_date_time = reservation_page.get_reservation_data(normal_user_2)
            expect_reservation_date_time = Helper.analyze_start_time_and_end_time(edited_reservation['start_time'], edited_reservation['end_time'], self._driver._driverSetting.language)
            self.assertEqual(actual_reservation_date_time, expect_reservation_date_time, 'Starting/Ending reservation times show incorrectly!')
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([normal_user, normal_user_2])
            TestCondition.delete_device_groups([device_group_name])


    def test_c33888_verify_that_amin_updates_a_access_time_once_creating_it_without_leaving_the_access_time_page(self):
        """
        @author: Khoi Ngo
        @date: 10/6/2017
        @summary: Verify that Amin updates a access time once creating it without leaving the access time page.
        @precondition:
            Create a device group A
            Create a user and add the user to device group A
        @steps:
            1. Login the staging site by organization account (khoi.ngo@logigear.com/L0gigear123!) 
            2. Go to Beams tab
            3. Select device group A
            4. Click Access Times tab
            5. Create a access time (any kind)
            6. Update the access time.
        @expected:
            (6) Admin can update access times successfully
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name

            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])

            origin_access_days = [WeekDays.Mon, WeekDays.Tue, WeekDays.Wed, WeekDays.Thu, WeekDays.Fri, WeekDays.Sat, WeekDays.Sun]
            allday_access_time_label = Utilities.generate_access_time_label(origin_access_days)
            new_access_days = [WeekDays.Tue, WeekDays.Thu]

            # steps
            admin_beam_detail_page = LoginPage(self._driver).open()\
                                                            .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                                                            .goto_beams_tab()\
                                                            .select_device_group(device_group_name)\
                                                            .goto_accesstimes_tab()\
                                                            .add_default_allday_access_times()\
                                                            .edit_default_access_times(allday_access_time_label, new_access_days)
            # verify point
            expected_item_label = "{} {}, {}".format(
                                    ApplicationConst.get_date_time_label("All day"),
                                    ApplicationConst.get_date_time_label("Tue"),
                                    ApplicationConst.get_date_time_label("Thu"))
            self.assertTrue(admin_beam_detail_page.is_default_access_time_label_displayed_on_sidebar(expected_item_label), \
                "Assertion Error: The default access times {} is not displayed in the sidebar".format(expected_item_label))
            
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                self.assertTrue(admin_beam_detail_page.is_default_allday_access_time_displayed_on_calendar(new_access_days), \
                    "Assertion Error: The default access times {} is not displayed in the calendar".format(expected_item_label))
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group_name])


    def test_c33891_verify_that_org_admin_can_add_remove_user_groups_for_user_on_edit_user_modal(self):
        """
        @author: Khoi Ngo
        @date: 10/9/2017
        @summary: Verify that Org admin can add/remove User Groups for user on Edit User modal
        @precondition:
            - Create a user group
            - Create a normal user
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as org admin
            2. Go to Users page
            3. Select the user
            4. Add User Groups on Edit User modal
            5. Enter the user group
            6. Repeat steps #2 and #3
            7. Remove the user from user group on Edit User modal
            8. Enter the user group and an check user
        @expected:
            (4)(7) Success message displays
            (5) User exists in user group
            (7) User is removed from user group
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.create_user_group(user_group_name)

            # steps
            admin_beam_detail_page = LoginPage(self._driver).open()\
                                                            .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                                                            .goto_users_tab()\
                                                            .goto_user_detail_page(normal_user)\
                                                            .edit_user(add_user_groups = [user_group_name], wait_for_completed = False)
            self.assertTrue(admin_beam_detail_page.is_success_msg_displayed(),"Success message doesn't display")

            admin_user_group_detail = admin_beam_detail_page.goto_user_group_detail(user_group_name)
            self.assertTrue(admin_user_group_detail.is_user_existed(normal_user.get_displayed_name()), "User doesn't exist in user group")

            admin_beam_detail_page = admin_user_group_detail.goto_users_tab()\
                                                            .goto_user_detail_page(normal_user)\
                                                            .edit_user(remove_user_groups = [user_group_name], wait_for_completed = False)
            self.assertTrue(admin_beam_detail_page.is_success_msg_displayed(),"Success message doesn't display")

            admin_user_group_detail = admin_beam_detail_page.goto_users_tab()\
                                                            .goto_user_group_detail_page(user_group_name)
            self.assertTrue(admin_user_group_detail.is_user_not_existed(normal_user.get_displayed_name()), "User still exists in user group")
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_user_groups([user_group_name])


    def test_c33892_verify_that_admin_can_change_timezone_of_reservation(self):
        """
        @author: Khoi Ngo
        @date: 10/11/2017
        @summary: Verify that admin can change timezone of reservation.
        @precondition:
            Create a device group A
            Create a user and add the user to device group A
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as org admin
            2. Go to Beams page and select a Device Group
            3. Open Reservations tab
            4. Create a reservation
            5. Click Edit button
            6. Select another Time Zone
            7. Click Update button
        @expected:
            (6) Times displays correctly as selected timezone
            (7) Success message displays 
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            
            beam = TestCondition.get_and_lock_beam(organization)
            beam_name = beam.beam_name
            
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.user_group = user_group_name
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
            TestCondition.create_user_group(user_group_name)
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            TestCondition.set_advanced_beam_reservation_permisson(beam, 'Allowed')\
            
            calendar_key = TestCondition.get_calendar_key_via_api(normal_user.email_address, normal_user.password)
            calendar_reservations_info = Helper.generate_calendar_reservation(normal_user.email_address, calendar_key)
            calendar_client = Calendar_Utilities.add_calendar_account(calendar_reservations_info)
            
            time_zone = 'America/Los_Angeles'
            
            #steps
            Calendar_Utilities.add_calendar_event(calendar_client, reservation_data)
            edit_reservation_dialog = LoginPage(self._driver).open().login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab().select_a_device(beam.beam_name).open_reservation_tab()\
                .open_edit_reservation_dialog(normal_user).custom_timezone(time_zone)
                
            # verify point:
            self.assertTrue(edit_reservation_dialog.does_start_time_display_correctly(reservation_data.start_time, time_zone),\
                            "Start time displays incorrectly")
            self.assertTrue(edit_reservation_dialog.does_end_time_display_correctly(reservation_data.end_time, time_zone),\
                            "End time displays incorrectly")
            
            beam_detail_page = edit_reservation_dialog.save_changes()
            self.assertEqual(beam_detail_page.get_msg_success(), ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL, 'Successful message does not display or it does not localize!')
            
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.set_advanced_beam_reservation_permisson(beam, "Not Allowed")
            TestCondition.delete_advanced_users([org_admin, normal_user], organization)
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group], organization)


    def test_c33893_verify_that_fuction_resend_invitation_for_user_in_advanced_org_works_correctly(self):
        """
        @author: Khoi Ngo
        @date: 10/11/2017
        @summary: Verify that fuction Re-Send Invitation for user in advanced org works correctly
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as org admin
            2. Invite a new user
            3. Go to Users tabs and select the new user
            4. Click "Re-Send Invitation" button on user details page
        @expected:
            (4) Success message displays
                Welcome email is resent correctly.
        """
        try:
            # pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            advance_org_admin = User()
            advance_org_admin.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver,[advance_org_admin])

            # steps
            admin_beam_detail_page = LoginPage(self._driver).open()\
                                                            .login(advance_org_admin.email_address, advance_org_admin.password)\
                                                            .invite_new_user(normal_user)
            welcome_mail = EmailDetailHelper.generate_welcome_email(normal_user, advance_org_admin.get_displayed_name())
            GmailUtility.delete_emails(mail_subject = welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = normal_user.email_address)                                                

            user_detail_page = admin_beam_detail_page.goto_users_tab()\
                                                      .goto_user_detail_page(normal_user)\
                                                      .resend_invitation()
            self.assertTrue(user_detail_page.is_success_msg_displayed(), "Success message doesn't display")

            resend_welcome_mail = EmailDetailHelper.generate_welcome_email(normal_user, advance_org_admin.get_displayed_name())
            lst_notification_emails = GmailUtility.get_messages(mail_subject = resend_welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = normal_user.email_address)
            GmailUtility.delete_emails(mail_subject = resend_welcome_mail.subject, reply_to = advance_org_admin.email_address, receiver = normal_user.email_address)                                                
            self.assertTrue(len(lst_notification_emails) == 1, "Assertion Error: Suitable Tech wasn't resend email")
            result = re.match(resend_welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(resend_welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
        finally:
            TestCondition.delete_advanced_users([normal_user,advance_org_admin])


    def test_c33894_verify_that_fuction_resend_invitation_for_user_in_simplified_org_works_correctly(self):
        """
        @author: Khoi Ngo
        @date: 10/11/2017
        @summary: Verify that fuction Re-Send Invitation for user in simplified org works correctly
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as simplified admin
            2. Invite a new user to device
            3. Select device
            4. Click new user in device to view user details page
            5. Click "Re-Send Invitation" button
        @expected:
            (5) Success message displays
                Welcome email is resent correctly.
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name

            normal_user = User()
            normal_user.generate_simplified_normal_user_data()

            simplified_org_admin = User()
            simplified_org_admin.generate_simplified_org_admin_data()
            TestCondition.create_simplified_organization_admin(self._driver,simplified_org_admin)

            # steps
            admin_beam_detail_page = LoginPage(self._driver).open()\
                                                            .login(simplified_org_admin.email_address, simplified_org_admin.password, simplifiedUser = True)\
                                                            .add_user(normal_user,beam_name)
            welcome_mail = EmailDetailHelper.generate_welcome_email(normal_user, simplified_org_admin.get_displayed_name(True), True, False)
            GmailUtility.delete_emails(mail_subject = welcome_mail.subject, reply_to = simplified_org_admin.email_address, receiver = normal_user.email_address)                                                

            user_detail_page = admin_beam_detail_page.goto_manage_beam_page(beam.beam_id)\
                                                      .goto_simplified_user_detail_page(normal_user)\
                                                      .resend_invitation()
            self.assertTrue(user_detail_page.is_success_msg_displayed(), "Success message doesn't display")

            resend_welcome_mail = EmailDetailHelper.generate_welcome_email(normal_user, simplified_org_admin.get_displayed_name(True), True, True)
            lst_notification_emails = GmailUtility.get_messages(mail_subject = resend_welcome_mail.subject, reply_to = simplified_org_admin.email_address, receiver = normal_user.email_address)
            GmailUtility.delete_emails(mail_subject = resend_welcome_mail.subject, reply_to = simplified_org_admin.email_address, receiver = normal_user.email_address)                                                
            self.assertTrue(len(lst_notification_emails) == 1, "Assertion Error: Suitable Tech wasn't resend email")
            result = re.match(resend_welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content, re.I | re.M)
            self.assertTrue(result, "Assertion Error: Email content does not display as expected. Expected email content is:\n'{}' but found:\n'{}'".format(resend_welcome_mail.trimmed_text_content, lst_notification_emails[0].trimmed_text_content))
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_simplified_users([normal_user])