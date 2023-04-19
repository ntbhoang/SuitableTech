from test.testbase import TestBase
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from common.application_constants import ApplicationConst
import pytest

class Suitable_User_0_41_Test(TestBase):

    @pytest.mark.OnlyDesktop
    def test_c11720_org_admin_user_can_remove_another_org_admin_user (self):
        """
        @author: Thanh.Le
        @date: 04/26/2017
        @summary: Verify that the user has a "no" next to the Administrator text box
        @desciption: Org admin User can remove another org admin user 
        @precondition: Org needs to have two org admins
        @steps:
            1) Go to the "Users" Tab under the "Manage your Beams" dashboard
            2) click the "Show" drop-down menu next to the "Search Users" text box > select the "Administrators Only" selection
            3) Select one of the org admins
            4) Select the "Edit" box above the user image icon
            5) uncheck the box that allows the user to administer the org > save changes
        @expected:
            1) Verify that the user has a "no" next to the Administrator text box
        """ 
        try:
            #pre-condtion:
            org_admin1 = User()                                            
            org_admin1.generate_advanced_org_admin_data()
            org_admin2 = User()                                            
            org_admin2.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin1, org_admin2])            
            
            #steps:
            user_detail_page = LoginPage(self._driver).open()\
                .login(org_admin1.email_address, org_admin1.password)\
                .goto_users_tab().click_show_button_and_select(ApplicationConst.LBL_MENU_ADMINISTRATOR_ONLY)\
                .goto_user_detail_page(org_admin2).edit_user(allow_administer=False, wait_for_completed=False)
            
            # verify point
            self.assertTrue(user_detail_page.is_administator_label_notice(ApplicationConst.LBL_NO), "User is still Administrator of this organization")

        finally:
            TestCondition.delete_advanced_users([org_admin1, org_admin2])
            
            