from selenium.webdriver.common.by import By
from common.constant import Constant
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from test.testbase import TestBase
from core.suitabletechapis.user_api import UserAPI


class DeleteUser_Test(TestBase):
    
    def test_c11236_can_not_delete_admin_1_x(self):
        """
        @author: khoi.ngo
        @date: 7/28/2016
        @summary: Can not delete admin [1.X] 
        @precondition: copy the url of a known organizational admin
        @steps:
            1.  log on to suitabletech.com with a standard user account
            2. paste the url of a known admin account
            3. make sure that the link doesn't connect when logged on with a standard user
        @expected:
            standard user cannot connect to admin user's URL
        """

        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.SimplifiedOrgName)
            
            normal_user = User()
            normal_user.generate_simplified_normal_user_data()
            TestCondition.create_simplified_normal_users(
                self._driver, 
                user_array=[normal_user], 
                beam=beam)
                      
            # steps
            LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, True)\
            
            self._driver.get('https://stg1.suitabletech.com/manage/130/#/users/logigear1+simpleadmin@suitabletech.com/')
            
            # verify point
            self.assertFalse(self._driver.find_element(By.XPATH, "//h2[.='Home › Simplified Org Admin']"), "Assertion Error: Normal user  user can connect to admin user's URL")
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_simplified_users([normal_user], Constant.SimplifiedOrgName)
        

    def test_c11242_grant_temporary_access(self):
        """
        @author: Thanh Le
        @date: 08/18/2016
        @summary: Grant Temporary Access (Dashboard) [2.X]  
        @precondition: There are a Simplified Org Admin account and an activated UserA
        @steps:
            Steps To Complete Task: Grant Temporary Access for a Simplified user
            1) Login to Suitabletech site with the Simplified Org Admin in pre-condition
            2) Go to "Manage Your Beams" page
            3) Enter email address to invite a person to use this Beam (UserA@suitabletech.com) and click "Add User" button
            4) Log out admin and log in with UserA then go to "Your Account" page
            5) Logout this User
            6) Login with Simplified Org Admin again
            7) Remove above invited user (UserA) from "People with access to this Beam" list then logout Simplified Admin
            8) Login with UserA again       
        @expected:
            4) Verify that invited user can see the added Beam (BeamA).
            8) Verify that user cannot see the Beam any more.    
        """
        try:
            # precondition:
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
            
            new_user = User()
            new_user.generate_simplified_normal_user_data()
            new_user.device_group = beam_name
            
            # steps
            simplified_dashboad_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam.beam_id)\
                    .create_completed_simplified_normal_user(new_user)\
                .goto_login_page()\
                    .login_as_unwatched_video_user(new_user.email_address, new_user.password)\
                    .watch_video(new_user, simplified = True)
            
            # verify points
            new_user_name = UserAPI.get_displayed_name(new_user, simplified=True)
            self.assertTrue(simplified_dashboad_page.is_beam_displayed(beam_name),
                            "Assert Error: {} can NOT see the Beam {}".format(new_user_name, beam_name))
            
            simplified_dashboad_page = simplified_dashboad_page.logout()\
                .goto_login_page()\
                    .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam.beam_id)\
                    .remove_user(new_user)\
                    .logout()\
                .goto_login_page()\
                    .login(new_user.email_address, new_user.password, True)\
            
            # verify points
            self.assertFalse(simplified_dashboad_page.is_beam_displayed(beam_name),
                            "Assert Error: {} can see the Beam {}".format(new_user_name, beam_name))
        finally:
            # post-condition            
            pass
