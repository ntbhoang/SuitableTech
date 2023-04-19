from test.testbase import TestBase
from core.utilities.test_condition import TestCondition
from common.constant import Constant
from data_test.dataobjects.user import User
from common.helper import Helper
from pages.suitable_tech.user.login_page import LoginPage


class AdHoc_Test(TestBase):
    
    def test_c33923_user_can_see_beams_in_device_group_that_he_is_a_member_2_x(self):
        """
        @author: Thanh Le
        @date: 10/27/2017
        @summary: User can see Beams in Device Group that he is a member. 
        @precondition: 
            Have org admin account
            Have 2 device group (A, B) contain a beam for each
            Have a user group contain a normal user
        @steps:
            1) Login as org admin 
            2) Go to Beams tab
            3) Select device group A 
            4) Add the user group into device group A
            5) Go to Beams tab
            6) Select device group B
            7) Add the user into device group B
            8) Login with normal user in precondition on another browser
            9) Remove the user from the user group
            10) Remove the user from device group B
        @expected:
            Verify point:
                (8) The user can see 2 beam of 2 device groups (A, B) on dashboard page
                (9) Beam of device group A not displayed on dashboard page of the user
                (10) Beam of device group B not displayed on dashboard page of the user 
        """
        try:
            # pre-condition
            beam1 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name1 = beam1.beam_name
            beam2 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name2 = beam2.beam_name

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])

            device_group_name1 = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name1, [beam_name1])
            device_group_name2 = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name2, [beam_name2])

            user_group_name = Helper.generate_random_user_group_name()
            TestCondition.create_user_group(user_group_name, [normal_user])

            # steps
            dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_device_group(device_group_name1)\
                .goto_members_tab()\
                .add_user_group_to_device_group(user_group_name)\
                .goto_beams_tab()\
                .select_device_group(device_group_name2)\
                .goto_members_tab()\
                .add_user_to_device_group(normal_user)\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)

            # verify point
            self.assertTrue(dashboard_page.is_beam_displayed(beam_name1), \
                            "Beam {} not displayed on dashboard page".format(beam_name1))
            self.assertTrue(dashboard_page.is_beam_displayed(beam_name2), \
                            "Beam {} not displayed on dashboard page".format(beam_name2))

            dashboard_page = dashboard_page.logout_and_login_again(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_device_group(device_group_name2)\
                .goto_members_tab()\
                .remove_user(normal_user.get_displayed_name())\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)
            # verify point
            self.assertFalse(dashboard_page.is_beam_displayed(beam_name2), \
                             "Beam {} still displayed on dashboard page".format(beam_name2))

            dashboard_page = dashboard_page.logout_and_login_again(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_device_group(device_group_name1)\
                .goto_members_tab()\
                .goto_user_group_detail_page(user_group_name)\
                .remove_user(normal_user.get_displayed_name())\
                .logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)
            #TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2551"
            # verify point
            self.assertFalse(dashboard_page.is_beam_displayed(beam_name1), \
                             "Beam {} still displayed on dashboard page".format(beam_name1))

        finally:
            # post-condition
            TestCondition.release_a_beam(beam1)
            TestCondition.release_a_beam(beam2)
            TestCondition.delete_device_groups([device_group_name1, device_group_name2])
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_user_groups([user_group_name])

