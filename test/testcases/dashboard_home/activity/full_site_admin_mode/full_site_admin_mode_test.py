from test.testbase import TestBase
from common.constant import Constant
from pages.suitable_tech.user.login_page import LoginPage
    
class FullSiteAdminModeTest(TestBase):
        
    def test_c11251_can_see_device_activity_1x(self):
        """
        @author: Quang Tran
        @date: 09/28/2017
        @summary: Can see device activity [1.X]
        @precondition: 
        @steps:
            1. Go to "Beams" in the "Manage your beams" dashboard
            2. Click on a device

        @expected:
            Admin can see device activities
        """
        try:            
            # steps            
            import random
            beam_name = random.choice([Constant.BeamProNameUTF8, Constant.BeamPlusName])
            
            beam_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .goto_beam_details_page_by_id(Constant.DeviceIDs[beam_name])
            
            # verify points
            self.assertTrue(beam_detail_page.are_activities_shown_in_recent_activity_tab(),\
                            "Assertion Error: There is no acitivity shown in Recent Activity tab.")
            self.assertTrue(beam_detail_page.is_show_more_button_displayed_in_recent_activity_tab(),\
                            "Assertion Error: Show More button is not displayed in Recent Activity tab.")

        finally:
            pass