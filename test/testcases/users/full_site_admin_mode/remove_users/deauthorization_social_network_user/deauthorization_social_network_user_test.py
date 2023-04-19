from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from core.webdriver.drivers.driver import Driver
from core.webdriver.drivers.driversetting import DriverSetting
from pages.suitable_tech.user.login_page import LoginPage

class DeAuthorizationSocialNetworkUser_Test(TestBase):
    
    def test_c11673_sign_on_account_google_only_and_de_authorization_user_by_removing_web_beam_cookies(self):
        """
        @author: khoi.ngo
        @date: 8/17/2016
        @summary: Sign-On Account (Google only) and DE AUTHORIZATION User by Removing web (Beam cookies)
        @precondition:
            Add new Google Contact Account
                1. Create a google account as follows: https://accounts.google.com/SignUpWithoutGmail?hl=en (i.e. suitabletester2@gmail.com )
            
            Add and login to a new Suitable Tech Web Contact Account
                1. On Site Admin Dashboard, select the “Invite a New Contact” button
                2. Complete the invite Contact form:
                    • Using the same Google contact email address (i.e. suitabletester1@gmail.com, *required field)
                    • select any target contact group(s) (optional) (populated by any detected contact groups) (multiple selections allowed)
                    • select any target device group(s) (optional) (populated by any detected device groups)(multiple selections allowed)
                    • Review and personalize Invite email
                3. Click “send invite” button. (result notification will appear confirming action)
                4. Target contact will be notified via email of
                    • Who Invited them (Organization)
                    • What device group(s) they have been added to (derived from direct association and group association)
                    • Login ID [email address]
                    • Link to create a password / get client
                5. Once an invite has been sent, the system will create a new profile for each new contact invited (regardless if they have activated their account)
                6. Login as the new test user, into your mail service and retrieve your account welcome email for your newly created SuitableTech Account
                7. Follow the instructions within the email (i.e. To get started, click the account initialization link)
                8. Logout out of the contact user account
        @steps:
            1. Within your Browser go to settings and clear browser cookies
            2. Google Chrome Browser: • Clear Content settings->Cookies->"All Cookies and Site data" for all time
            3. Navigate to the Suitable Tech Web login page URL:https://staging.suitabletech.com/accounts/login/
            4. Select the Google(or Social Network) Single Sign On button
            5. Select the same google account that you created in the Preconditions steps:(i.e. Add new Google Contact Account, suitabletester2@gmail.com)
        @expected:
            Verify that you will have re-enter your Google(or Social Network) password before you are forwarded to the test account Suitable Tech Web home page
        
        @note: We using the account lgvn1usertest@gmail.com which activated to skip pre-conditon.
        """
        try:
            # pre-condition:
            non_gsso_user = User()
            non_gsso_user.generate_non_gsso_user_data()
            TestCondition.create_advanced_non_gsso_user(driver=self._driver, user=non_gsso_user)            
            # steps:            
            self._driver.quit()
            self._driver = Driver.get_driver(DriverSetting.load())
            self._driver.maximize_window()  
            

            is_re_enter_password = LoginPage(self._driver).open().goto_google_signin_page().is_reenter_password(non_gsso_user.email_address)
            self.assertTrue(is_re_enter_password, "Assertion Error: User doesn't need re-enter password")
        finally:
            TestCondition.release_an_allow_st_email(non_gsso_user.email_address)
            
            