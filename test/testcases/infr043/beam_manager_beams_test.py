from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from common.constant import Constant
from common.helper import Helper

class BeamManagerBeams_Test(TestBase):
    
    def test_c33722_track_beam_link_date_and_person (self):
        """
        @author: Thanh Le
        @date: 5/3/2017
        @summary: Track Beam Link Date & Person
        @description: We will link a Beam and verify that the date of linking and user who linked it is available in the Beam Manager
        @precondition: Have an available Beam for linking
        @steps:
            1. Go to the Beam Link page https://stg1.suitabletech.com/setup/link/
            2. Fill out the linking form and click "Link your Beam"
            3. Visit the device the Beam Manager
            4. Click the Advanced button
        @expected:
            Verify that Linked By and Linked On are populated with the user and date.
        @note: Step #1 and #2 are done by manual
        """
        
        try: 
            #precondition:
            beam_name = Constant.BeamProNameUTF8
            expected_user = 'tjenkins@suitabletech.com'
            expected_link_date = Helper.get_data_of_beam_link_date(self._driver._driverSetting.language)     
                
            #steps
            device_advance_settings_dialog = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab()\
                .goto_beam_details_page_by_id(Constant.DeviceIDs[beam_name])\
                .goto_beam_advance_setting()\
            
            actual_user = device_advance_settings_dialog.get_linked_by_infomation()
            actual_link_date = device_advance_settings_dialog.get_link_date_infomation()
            device_advance_settings_dialog.cancel()

            #verify point
            self.assertEqual(actual_user, expected_user, "User displays incorrectly")
            self.assertEqual(actual_link_date, expected_link_date, "Linked By displays incorrectly")
        finally:
            pass
