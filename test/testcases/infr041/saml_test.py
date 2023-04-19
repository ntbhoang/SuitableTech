from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from common.constant import Constant
from core.utilities.test_condition import TestCondition

class SAML_Test(TestBase):
    
    def test_c33064_user_login_from_website_using_SAML(self):
        try:
            #pre-condition:
            auth = TestCondition.get_and_lock_org_authentication()
            TestCondition.change_authentication_to_OneLogin()

            # step
            #TODO: AD FS issue 
            dashboard_page = LoginPage(self._driver).open()\
                .login_as_sso_onelogin(Constant.OneLoginAccount, Constant.OneLoginPassword)
                
            self.assertTrue(dashboard_page.is_page_displayed, 'Admin Home Page does not display')
        finally:
            TestCondition.release_org_authentication(auth)
