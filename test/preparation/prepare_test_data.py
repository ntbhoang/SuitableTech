from common.constant import Constant
from core.utilities.gmail_utility import GmailUtility
from test.testbase import TestBase
from common.helper import Helper
from core.utilities.test_condition import TestCondition


class PrepareTestData(TestBase):
    
    def test_prepare_test_data(self):
        beams_array = TestCondition.get_name_all_beams(Constant.AdvancedOrgName)
        device_group_name = Helper.generate_random_device_group_name()
        TestCondition.create_device_group(device_group_name, beams_array)
        TestCondition.delete_all_reservation_in_device_group(device_group_name)

        TestCondition.remove_all_device_groups(organization=Constant.AdvancedOrgName)
        TestCondition.remove_all_device_groups(organization=Constant.AdvancedOrgName_2)
        TestCondition.remove_all_user_groups(organization=Constant.AdvancedOrgName)
        TestCondition.remove_all_user_groups(organization=Constant.AdvancedOrgName_2)
        TestCondition.remove_test_advanced_users(keyword_array=["logigear1+user", "logigear2+user", "suitabletech3+user", "suitabletech4+user", "suitabletech5+user"], organization=Constant.AdvancedOrgName)
        TestCondition.remove_test_advanced_users(keyword_array=["logigear1+user", "logigear2+user", "suitabletech3+user", "suitabletech4+user", "suitabletech5+user"], organization=Constant.AdvancedOrgName_2)
        TestCondition.login_and_change_language_using_api(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, self._driver._driverSetting.language)
        TestCondition.login_and_change_language_using_api(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword, self._driver._driverSetting.language)
        TestCondition.change_authentication_to_OneLogin()
#         TestCondition.login_and_change_language_using_api(Constant.MixedMultiOrgAdminEmail, Constant.DefaultPassword, self._driver._driverSetting.language)
        TestCondition.reject_all_access_requests()
 
        for beam in Constant.SimplifiedBeams:
            TestCondition.delete_test_simplified_users(organization=Constant.SimplifiedOrgName, beam_id=beam["id"], keyword_array=["logigear1+user", "logigear2+user", "suitabletech3+user", "suitabletech4+user", "suitabletech5+user"])
         
        for i in range(5):
            GmailUtility.delete_all_emails(Constant.BaseEmails[i+1])
          
        TestCondition.prepare_beam_resources(self._driver)
        TestCondition.prepare_locales_resource(self._driver.driverSetting.platform)
        TestCondition.prepare_allowed_gsso_accounts(self._driver)        
        TestCondition.prepare_unallowed_gsso_accounts(self._driver)
        self.delete_temporary_files()

        list_email = TestCondition.get_email_from_file_json([TestCondition.GSSO_AND_NON_GSSO_RESOURCE, TestCondition.UNALLOWED_GSSO_RESOURCE])
        for email in list_email:
            if not TestCondition.check_account_exitst(email):
                TestCondition.invite_email_to_advance_org(self._driver, email)
