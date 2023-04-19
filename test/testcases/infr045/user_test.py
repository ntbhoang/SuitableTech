from common.constant import Constant
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage

class User_Test(TestBase):


    def test_c33946_the_safety_video_is_displayed_for_user_of_organization_has_temporary_passwords(self):
        """
        @author: Khoi.Ngo
        @date: 11/20/2017
        @summary: The safety video is displayed for user of organization has temporary passwords
        @precondition:
            - Have organization using temporary passwords
            (Simplified organization 'Logigear Test 2')

        @steps:
            1. Login and Invite a new user to the org
            2. Logout and login with the new user
            3. Set up pasword successfully

        @expected:
            - The safety video is displayed when clicking Continue button.
            - Home page is displayed when finishing watching the video.
        """
        try:
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()
            beam = TestCondition.get_a_beam(normal_user.organization)

            # steps
            simplified_dashboard_page = LoginPage(self._driver)\
                .open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                .add_user(normal_user, beam.beam_name)

            temporary_password = TestCondition._get_user_temporary_password(normal_user, localize = True)
            password_change_complete_page = simplified_dashboard_page.logout().goto_login_page().login_as_unactivated_user(normal_user.email_address, temporary_password).change_password(normal_user.password, temporary_password)

            welcome_to_beam_page = password_change_complete_page.continue_login(temp_pass=False)
            self.assertTrue(welcome_to_beam_page.is_welcome_user_page_displayed(), "The safety video is not displayed")

            watch_completely_safety_video = welcome_to_beam_page.watch_video(normal_user, simplified=True, had_name=False)
            self.assertTrue(watch_completely_safety_video.is_page_displayed(), "Home page is not displayed")

        finally:
            TestCondition.delete_simplified_users([normal_user])

