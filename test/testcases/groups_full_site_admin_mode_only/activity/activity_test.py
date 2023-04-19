from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from common.constant import Constant

class Activity_Test(TestBase):

    def test_c10936_can_select_or_deselect_status_1x(self):
        """
        @author: Khoi Ngo
        @date: 01/18/2018
        @summary: Can select/deselect: In a call, Offline, Configuring, Upgrading [1.X]
        @precondition:
            Have an Org admin account
            Select a time range that have all these status appearing in time line (from 04/26/2017 to 11/28/2017 )
        @steps:
            1) Login Advance site with Org admin account
            2) Go to "Activity" tab
            3) Click on the "Status" drop-down menu
            4) Select and/or deselect from these options: In a call, Miss calls, Offline, Configuring, Upgrading

        @expected:
            1) The activity bars change accordingly.
            2) The activity bars should not have bars that are not selected.
        """
        try:
            #pre-condition:
            date_range = { 'from_date': {'dd':'26','mm':'04','yyyy':'2017'}, 'to_date': {'dd':'28','mm':'11','yyyy':'2017'}}

            #steps
            activity_page = LoginPage(self._driver).open()\
                    .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                    .goto_activity_tab()

            self.assertTrue(activity_page.check_activity_status_work_correctly(date_range), "Assertion Error: Activity status appear incorrectly in time line.")
 
        finally:
            pass

