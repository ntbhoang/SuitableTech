from common.constant import Constant
from common.helper import Helper
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase


class DeviceGroupAccess_Test(TestBase):
        
    def test_c11079_setup_device_group_users_authentication_by(self):
        """
        @author: Thanh Le
        @date: 08/27/2016
        @summary: Setup Device Group Users Authentication by
        @precondition:           
            Create 2 groups have differences Auth method:
                "LGVN Device Group - Auth ST" (enable "Suitable Tech Auth" only and added a BeamA) 
                "LGVN Device Group - Auth Google" (enable "Google Auth" only and added a BeamB)
            Create 2 users has differences Auth logging 
                UserA = "lgvnsuitabletech1@gmail.com" (Only log by Suitable Tech method) 
                UserB = "lgvnsuitabletech@gmail.com" (Only log by GSSO method)
        @steps:
            1) Log in to Suitabletech with an org admin
            2) Add 2 users in pre-condition to both Device Groups
            3) Log in with each user and check the device they can see
        
        @expected:          
            3). UserA only sees the BeamA and does not see the BeamB.
            3). UserB only sees the BeamB and does not see the BeamA.
        """
        try:
            # precondition:
            beam1 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam1_name = beam1.beam_name
            beam2 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam2_name = beam2.beam_name
            auth = TestCondition.get_and_lock_org_authentication()
            TestCondition.change_authentication_to_BeamOrGoogleAccount()
            
            untest_device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=untest_device_group, device_array=[], organization_name=organization)
            
            device_group_auth_st = Helper.generate_random_device_group_name()
            device_group_auth_google = Helper.generate_random_device_group_name()
            
            gsso_user = User()  # Do NOT delete this GSSO user at clean up. Just release the email
            gsso_user.generate_un_allowed_gsso_user_data()
            TestCondition.create_advanced_gsso_user(self._driver, gsso_user)
            
            non_gsso_user = User()
            non_gsso_user.generate_advanced_normal_user_data()
            non_gsso_user.device_group = untest_device_group
            non_gsso_user.organization = organization
            
            TestCondition.create_device_group(device_group_auth_st, [beam1_name])
            TestCondition.create_device_group(device_group_auth_google, [beam2_name])
            TestCondition.create_advanced_normal_users(self._driver, [non_gsso_user])

            # steps:
            simplified_dashboad_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group_auth_st)\
                    .toggle_left_off_all_authentication_methods(False)\
                    .toggle_left_off_google_methods(False)\
                .goto_members_tab()\
                    .add_user_to_device_group(gsso_user)\
                    .add_user_to_device_group(non_gsso_user)\
                .goto_settings_tab_of_a_device_group(device_group_auth_google)\
                    .toggle_left_off_all_authentication_methods(False)\
                    .toggle_left_off_suitable_technologies_methods(False)\
                .goto_members_tab()\
                    .add_user_to_device_group(gsso_user)\
                    .add_user_to_device_group(non_gsso_user)\
                    .logout()\
                .goto_login_page()\
                    .login(non_gsso_user.email_address, non_gsso_user.password, simplifiedUser=True)
            
            # verify point:
            self.assertTrue(simplified_dashboad_page.is_device_title_displayed(beam1_name),
                            "Assertion Error: {} is NOT displayed!".format(beam1_name))
            self.assertFalse(simplified_dashboad_page.is_device_title_displayed(beam2_name),
                            "Assertion Error: {} is still displayed!".format(beam2_name))
            
            simplified_dashboad_page = simplified_dashboad_page.logout()\
                .goto_login_page()\
                .login_with_google(gsso_user.email_address)
            
            # verify point:
            self.assertTrue(simplified_dashboad_page.is_device_title_displayed(beam2_name),
                            "Assertion Error: {} is NOT displayed!".format(beam2_name))
            self.assertFalse(simplified_dashboad_page.is_device_title_displayed(beam1_name),
                            "Assertion Error: {} is still displayed!".format(beam1_name))
        finally:
            TestCondition.change_authentication_to_OneLogin()
            TestCondition.release_org_authentication(auth)
            TestCondition.release_a_beam(beam1)
            TestCondition.release_a_beam(beam2)
            TestCondition.release_an_unallow_st_email(gsso_user.email_address)
            TestCondition.delete_advanced_users([non_gsso_user])
            TestCondition.delete_device_groups([device_group_auth_st, device_group_auth_google, untest_device_group], organization)
