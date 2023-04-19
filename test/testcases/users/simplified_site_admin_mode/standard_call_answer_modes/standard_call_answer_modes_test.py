from common.constant import Constant
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from test.testbase import TestBase


class StandardCallAnswerModes(TestBase):
    
    def test_c11273_login_as_guest_user_verify_menu_options(self):
        """
        @author: khoi.ngo
        @date: 7/28/2016
        @summary: Login as guest user verify menu options
        @steps:
            1. log on as a user that is not an admin in any org to suitabletech.com
        @expected:
            All non admins should only see the following button options:
            - Download
            - Get help
        """
        try:
            #pre-condition:
            beam = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            new_user = User()
            new_user.generate_simplified_normal_user_data()
            TestCondition.create_simplified_normal_users(
                self._driver, 
                user_array=[new_user], 
                beam=beam)
            
            #steps:
            simplified_dashboard = LoginPage(self._driver).open()\
                .login(new_user.email_address, new_user.password, True)\
                        
            self.assertTrue(simplified_dashboard._lnkDownloadtheBeamDesktopSoftware.is_displayed(), "Assertion Error: Download beam software is not displayed")
            self.assertTrue(simplified_dashboard._lnkGetHelp.is_displayed(), "Assertion Error: Get help is not displayed")
        finally:
            #post-condition:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_simplified_users([new_user])
            
