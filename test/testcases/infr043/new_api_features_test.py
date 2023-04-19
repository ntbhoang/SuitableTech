from test.testbase import TestBase
from common.constant import Constant, Platform
from pages.okta_page.okta_sign_in_page import OktaSignInPage
from common.application_constants import ApplicationConst
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
from core.suitabletechapis.user_api import UserAPI
from core.utilities.test_condition import TestCondition
from common.helper import Helper

class NewAPIFeature_Test(TestBase):
    
    def test_c33693_system_user_groups_migration(self):
        """
        @author: Thanh Le
        @date: 6/02/2017
        @summary: System User Groups migration
        @steps:
            1. visit an Org whose auth method is SAML. Verify that all admins and purchasing admins are also users.
            2. visit an Org whose auth method is NOT SAML.
        @expected:
            #1. a.Verify that all users are in the All_Users user group. 
                b.Verify that all users that have verified domains (essentially, email domains associated with the Org) are in the Saml Users user group.
            #2. a.Verify that all admins and purchasing admins are also users. 
                b.Verify that all users are in the All_Users user group. 
                c.Verify that there is NO Saml Users user group.
        """
        try:
            #steps
            auth = TestCondition.get_and_lock_org_authentication()
            TestCondition.change_authentication_to_Okta()
            TestCondition.change_authentication_to_BeamOrGoogleAccount(organization=Constant.AdvancedOrgName_2)
            
            admin = User()
            admin.advanced_org_admin_data()
            
            user_group_page = LoginPage(self._driver).open()\
                .login(admin.email_address, admin.password)\
                .goto_users_tab()
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                user_group_page = user_group_page.click_items_button_and_select(ApplicationConst.LBL_100_ITEMS)\
                .select_user_group(ApplicationConst.LBL_ALL_USERS_GROUP)
            else:
                user_group_page = user_group_page.select_user_group(ApplicationConst.LBL_ALL_USERS_GROUP)
            
            expected_number_users = len(UserAPI.get_list_users(Constant.AdvancedOrgName))
            number_users_on_site = user_group_page.get_all_users_in_group()
            
            self.assertTrue(expected_number_users == number_users_on_site, 'Number users list on All Users group are not correct.')
            
            user_group_page = user_group_page.goto_users_tab().select_user_group(ApplicationConst.LBL_SAML_USERS_GROUP)
            
            expected_number_users = len(UserAPI.get_list_users_base_domain('logigear.com', Constant.AdvancedOrgName))
            number_users_on_site = user_group_page.get_all_users_in_group()
            
            self.assertTrue(expected_number_users == number_users_on_site, 'Number users list on SAML group are not correct.')
            
            user_page = user_group_page.goto_another_org(Constant.AdvancedOrgName_2)\
                .goto_users_tab()
             
            self.assertFalse(user_page.is_user_group_existed(ApplicationConst.LBL_SAML_USERS_GROUP), "SAML user group displays ")
            self.assertTrue(user_page.is_user_existed(admin.get_displayed_name()),"admins doesn't exist in users tab")
            self._driver.refresh()
            user_page.select_user_group(ApplicationConst.LBL_ALL_USERS_GROUP)
     
            expected_number_users = len(UserAPI.get_list_users(Constant.AdvancedOrgName_2))
            number_users_on_site = user_group_page.get_all_users_in_group()
             
            self.assertTrue(expected_number_users == number_users_on_site, 'Number users list on All Users group are not correct.')
        finally:
            TestCondition.release_org_authentication(auth)
            
        
    def test_c33717_user_login_from_website_using_Okta(self):
        """
        @author: Thanh Le
        @date: 6/05/2017
        @summary: user login from website using Okta
        @precondition: a working okta connector
            the ability to add test organizations and set up required okta connector details
            the ability to add and delete test users to okta
        @steps:
            Starting from the Suitable Home page:
            1. click the login button in the upper right hand corner
            2. on the new page, click the sign in with SSO button
            3. on the new page, type the user's name, i.e., email address; and click the sign in button
            4. the Okta page will load; the user's name/email address should be preloaded; enter the user's password and click login button
            5. user should be shown their account home page
        @expected:
            Using each supported browser on each supported OS, the test user should be able to login from the Suitable home page. 
            After having logged in, the user should be able to manager their beams, etc.
        """
        try:
            #pre-condition:
                auth = TestCondition.get_and_lock_org_authentication()
                TestCondition.change_authentication_to_Okta()

                device_group_name = Helper.generate_random_device_group_name()
                TestCondition.create_device_group(device_group_name, organization_name = Constant.OktaOrgName)

            #steps
                dashboard_page = LoginPage(self._driver).open()\
                    .login_as_sso_okta(Constant.OktaAccount, Constant.OktaPassword)
                self.assertTrue(dashboard_page.is_page_displayed(), "the user cannot be able to manage their beams")

                org_auth_page = dashboard_page.goto_settings_tab_of_a_device_group(device_group_name)
                self.assertTrue(org_auth_page.is_UI_auth_methods_disabled(), "UI auth methods for device groups still enable")
        finally:
            TestCondition.delete_device_groups([device_group_name],Constant.OktaOrgName)
            TestCondition.change_authentication_to_OneLogin()
            TestCondition.release_org_authentication(auth)


    def test_c33720_change_Okta_account_properties(self):
        """
        @author: Thanh Le
        @date: 6/05/2017
        @summary: user login from website using Okta
        @precondition: a working Okta connector
            the ability to add test organizations and set up required Okta connector details
            the ability to add and delete test users to Okta
        @steps:
            Okta provides fname/lname/email/username and Suitable provides the user's photo. Any changes to these properties should be observable the next time the user authenticates.
        @expected:
            Okta provides fname/lname/email/username and Suitable provides the user's photo. Any changes to these properties should be observable the next time the user authenticates.
  
        """
        #pre-condition
        okta_user = User()
        okta_user.generate_okta_user_data()    
         
        #steps
        OktaSignInPage(self._driver).open()\
            .signin_to_homepage(okta_user.email_address, okta_user.password)\
            .goto_setting_page()\
            .update_personal_information(okta_user)
             
        LoginPage(self._driver).open()\
            .login_sso(Constant.OktaAccount)
        account_setting_page = AdminDashboardPage(self._driver).goto_your_account()
          
        self.assertTrue(account_setting_page.is_contact_info_correct(okta_user), "Okta account displays incorrect")
        
        