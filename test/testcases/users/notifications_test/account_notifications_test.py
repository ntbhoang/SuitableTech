from test.testbase import TestBase
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper


class AccountNotifications(TestBase):

    def test_c33875_enable_all_disable_all_and_restore_defaults_work_correctly(self):
        """
        @author: khoi.ngo
        @date: 9/29/2017
        @summary: Verify that Enable All, Disable All and Restore Defaults worrk correctly
        @precondition:
            - Create a normal user, device group admin and org admin
        @steps:
            1. Login as normal user
            2. Go to Account Settings -> Notifications
            3. Click Enable All button
            4. Click Disable All button
            5. Click Restore Defaults button
        @expected:
            (3). Success message displays and all checkboxes are checked
            (4). Success message displays and all checkboxes are unchecked
            (5). Success message displays and all checkboxes are restored
        """
        try:
            #pre-condition:
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])

            device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            TestCondition.create_device_group(device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            #steps:
            account_notification_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account()\
                .goto_notifications_tab()
            checklist_before = account_notification_page.get_notifications_checkboxes_status()    

            account_notification_page.enable_all_notifications()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertTrue(account_notification_page.are_all_notifications_enabled(), "Having some checkboxes are not checked")

            account_notification_page.disable_all_notifications()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertTrue(account_notification_page.are_all_notifications_disabled(), "Having some checkboxes are checked")

            account_notification_page.restore_to_default_notifications()
            checklist_after = account_notification_page.get_notifications_checkboxes_status()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertEqual(checklist_before, checklist_after, "Checkboxes are not restored")

            log_out_page = account_notification_page.logout()

            account_notification_page = log_out_page.goto_login_page()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_your_account()\
                .goto_notifications_tab()
            checklist_before = account_notification_page.get_notifications_checkboxes_status()    

            account_notification_page.enable_all_notifications()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertTrue(account_notification_page.are_all_notifications_enabled(), "Having some checkboxes are not checked")

            account_notification_page.disable_all_notifications()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertTrue(account_notification_page.are_all_notifications_disabled(), "Having some checkboxes are checked")

            account_notification_page.restore_to_default_notifications()
            checklist_after = account_notification_page.get_notifications_checkboxes_status()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertEqual(checklist_before, checklist_after, "Checkboxes are not restored")

            log_out_page = account_notification_page.logout()

            account_notification_page = log_out_page.goto_login_page()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_your_account()\
                .goto_notifications_tab()
            checklist_before = account_notification_page.get_notifications_checkboxes_status()    

            account_notification_page.enable_all_notifications()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertTrue(account_notification_page.are_all_notifications_enabled(), "Having some checkboxes are not checked")

            account_notification_page.disable_all_notifications()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertTrue(account_notification_page.are_all_notifications_disabled(), "Having some checkboxes are checked")

            account_notification_page.restore_to_default_notifications()
            checklist_after = account_notification_page.get_notifications_checkboxes_status()
            self.assertTrue(account_notification_page.is_success_msg_displayed(),"Success message doesn't display")
            self.assertEqual(checklist_before, checklist_after, "Checkboxes are not restored")
        finally:
            TestCondition.delete_advanced_users([normal_user,device_group_admin])
            TestCondition.delete_device_groups([device_group_name])

