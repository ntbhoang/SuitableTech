from common.application_constants import ApplicationConst
from common.constant import Constant
from common.helper import Helper
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.utilities import Utilities 
import pytest

class WelcomeToBeam_Block_Test(TestBase):

    def test_c33854_verify_that_content_on_welcome_to_beam_block_displays_correctly_for_each_users(self):
        """
        @author: Quang.Tran
        @date: 9/18/2017
        @summary: Verify welcome to beam block content
        @precondition:
            Create org admin, device group admin and normal user

        @steps:
            1) Login as org admin
            2) Login as device group admin
            3) Login as normal user
        @expected:
            (1)
            - Verify Welcome to Beam block includes (Beam image, Welcome to Beam section, Download and install section, and Link a new Beam section)
            - Verify Download and Link a new Beam links work
            (2)
            - Verify Welcome to Beam block includes (Beam image, Welcome to Beam section, Download and install section)
            - Verify Download link works
            (3)
            - Verify Welcome to Beam block includes (Beam image, Welcome to Beam section, Download and install section)
            - Verify Download link works
        """
        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = new_device_group_name

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            # pre-condition
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
            TestCondition.create_advanced_normal_users(self._driver,[normal_user])

            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)

            self.assertTrue(admin_dashboard_page.is_welcome_to_beam_block_image_display(),"Welcome to Beam block image for org admin doesn't display")
            self.assertEqual(Utilities.trimmed_text(admin_dashboard_page.get_welcome_to_beam_block_content())\
                ,Utilities.trimmed_text(ApplicationConst.SECT_WELCOME_TO_BEAM + '\n' + ApplicationConst.SECT_DOWNLOAD_AND_INSTALL + '\n' + ApplicationConst.SECT_LINK_A_NEW_BEAM)\
                , "Assertion Error: Expected Welcome to Beam block content is:\n'{}' but found:\n'{}'".format(ApplicationConst.SECT_WELCOME_TO_BEAM + '\n' + ApplicationConst.SECT_DOWNLOAD_AND_INSTALL + '\n' + ApplicationConst.SECT_LINK_A_NEW_BEAM,admin_dashboard_page.get_welcome_to_beam_block_content()))

            admin_dashboard_page.goto_download_page()

            self.assertEqual(self._driver.current_url, Constant.DownloadBeamAppURL, "Navigate to wrong download page")

            self._driver.back()
            admin_dashboard_page.goto_link_a_beam_page_by_link()

            self.assertEqual(self._driver.current_url, Constant.LinkABeamURL.format(Constant.OrgsInfo[Constant.AdvancedOrgName]), "Navigate to wrong link a beam page")

            logout_page = TestCondition.force_log_out(self._driver)

            admin_dashboard_page = logout_page.goto_login_page()\
                .login(device_group_admin.email_address, device_group_admin.password)

            self.assertTrue(admin_dashboard_page.is_welcome_to_beam_block_image_display(),"Welcome to Beam block image for org admin doesn't display")
            self.assertEqual(Utilities.trimmed_text(admin_dashboard_page.get_welcome_to_beam_block_content())\
                , Utilities.trimmed_text(ApplicationConst.SECT_WELCOME_TO_BEAM + '\n' + ApplicationConst.SECT_DOWNLOAD_AND_INSTALL)\
                , "Assertion Error: Expected Welcome to Beam block content is:\n'{}' but found:\n'{}'".format(ApplicationConst.SECT_WELCOME_TO_BEAM + '\n' + ApplicationConst.SECT_DOWNLOAD_AND_INSTALL,admin_dashboard_page.get_welcome_to_beam_block_content()))

            admin_dashboard_page.goto_download_page()

            self.assertEqual(self._driver.current_url, Constant.DownloadBeamAppURL, "Navigate to wrong download page")

            self._driver.back()
            logout_page = admin_dashboard_page.logout()

            simplified_normal_user_home_page = logout_page.goto_login_page()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser = True)

            self.assertTrue(simplified_normal_user_home_page.is_welcome_to_beam_block_image_display(),"Welcome to Beam block image for org admin doesn't display")
            self.assertEqual(Utilities.trimmed_text(simplified_normal_user_home_page.get_welcome_to_beam_block_content())\
                , Utilities.trimmed_text(ApplicationConst.SECT_WELCOME_TO_BEAM + '\n' + ApplicationConst.SECT_DOWNLOAD_AND_INSTALL)\
                , "Assertion Error: Expected Welcome to Beam block content is:\n'{}' but found:\n'{}'".format(ApplicationConst.SECT_WELCOME_TO_BEAM + '\n' + ApplicationConst.SECT_DOWNLOAD_AND_INSTALL,admin_dashboard_page.get_welcome_to_beam_block_content()))

            simplified_normal_user_home_page.goto_download_page()

            self.assertEqual(self._driver.current_url, Constant.DownloadBeamAppURL, "Navigate to wrong download page")
        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([device_group_admin,normal_user])


    def test_c33855_verify_that_show_all_help_messages_on_account_settings_page_works(self):
        """
        @author: Quang.Tran
        @date: 9/19/2017
        @summary: Verify that Show All Help Messages works
        @precondition:
            Create a normal user.

        @steps:
            1) Login as normal user
            2) Click dismiss and do not show again link
            3) Go to Account Settings page
            4) Click Show All Help Messages button
            5) Back to Dashboard page
        @expected:
            (2) Welcome to Beam block is dismissed
            (4) Success message displays
            (5) Welcome to Beam block displays
        """
        try:
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            # pre-condition
            TestCondition.create_advanced_normal_users(self._driver,[normal_user])

            # steps
            simplified_normal_user_home_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser = True)\
                .dismiss_welcome_to_beam_block()
            self.assertTrue(simplified_normal_user_home_page.is_welcome_to_beam_block_dismiss(), "Welcome to Beam block still displays")

            account_settings_page = simplified_normal_user_home_page.goto_your_account()\
                .show_all_help_messages()

            self.assertEqual(account_settings_page.get_msg_success(), ApplicationConst.LBL_SUCCESS_MESSAGE, "Assertion Error: Expected Success message is:\n'{}' but found:\n'{}'".format(ApplicationConst.LBL_SUCCESS_MESSAGE,account_settings_page.get_msg_success()))    

            simplified_normal_user_home_page = account_settings_page.goto_simplified_admin_home()
            self.assertTrue(simplified_normal_user_home_page.is_welcome_to_beam_block_display(), "Welcome to Beam block doesn't display")
        finally:
            TestCondition.delete_advanced_users([normal_user])


    @pytest.mark.OnlyDesktop
    def test_c33858_verify_that_help_button_displays_on_header_menu_for_device_group_admin_or_org_admin(self):
        """
        @author: Quang.Tran
        @date: 9/19/2017
        @summary: Verify that Help button display on header menu
        @precondition:
            Have device group admin and org admin.

        @steps:
            1) Login as org admin
            2) Click Help on header menu
            3) Logout and login again with device group admin
            4) Click Help on header menu
        @expected:
            (2)(4) Help page displays
        """
        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = new_device_group_name

            # pre-condition
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_beam_help_center()
            self.assertEqual(self._driver.current_url, Constant.HelpCenterURL, "Navigate to wrong help center page")
            self.assertEqual(200, admin_dashboard_page.get_status_code(Constant.HelpCenterURL), "Beam Help Center doesn't display.")

            self._driver.back()
            log_out_page = admin_dashboard_page.logout()

            admin_dashboard_page = log_out_page.goto_login_page()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beam_help_center()
            self.assertEqual(self._driver.current_url, Constant.HelpCenterURL, "Navigate to wrong help center page")
            self.assertEqual(200, admin_dashboard_page.get_status_code(Constant.HelpCenterURL), "Beam Help Center doesn't display.")
        finally:
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([new_device_group_name])


    def test_c33859_verify_that_milestones_match_up_with_FTUE(self):
        """
        @author: Quang.Tran
        @date: 9/20/2017
        @summary: Verify that Milestones match up with FTUE.
        @steps:
            1) Invite new user
            2) Go to mailbox and get Activation link
            3) Complete the FTUE flow
            4) Login as admin
            5) Go to Users tab
            6) Select the new user
        @expected:
            (6) Milestones match up with FTUE
            - Steps (Invited, Logged In, Agreement) are filled completed.
            - Steps (Connected and Called) are not filled completed.
        """
        try:
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            # steps
            LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .invite_new_user(normal_user).logout()

            TestCondition._activate_user(self._driver, normal_user, email_subject=ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE)

            admin_user_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .goto_user_detail_page(normal_user)

            self.assertTrue(admin_user_detail_page.is_milestones_filled_correctly(completed_milestones_number = 3),"Milestones are filled incorrectly")
        finally:
            TestCondition.delete_advanced_users([normal_user])

