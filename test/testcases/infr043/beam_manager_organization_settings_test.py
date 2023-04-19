from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from common.constant import Constant
from core.utilities.test_condition import TestCondition

class Beam_Manager_Organization_Settings_0_43_Test(TestBase):

    def test_c33723_collect_primary_organization_contact_information(self):
        """
        @author: Thanh.Le
        @date: 05/4/2017
        @summary: Collect Primary Organization Contact information
        @precondition: 
            Must not have the required Primary Organization Contact information entered for the current organization. This can be achieved by removing required fields from the Organization Settings tab.
            Must have access to organization admin account           
        @steps:
            1. Log into the Beam Manager site as an organization admin.
            2. Notice a modal window titled Primary Organization Contact displays
            3. Enter required fields
            4. Click save
        @expected:
            The modal in step 2 should not display the next time an organization admin logs into the beam manager app.
            Verify the Primary Contact information has been saved and displays in the Organization Settings tab.
        """
        try:
            # pre-condition:
            contact_info =  {"last_name": "Tran",
                            "phone": "99999999999",
                            "postal_code": "1111111",
                            "city": "Ho Chi Minh",
                            "first_name": "Huy",
                            "country": "Viet Nam",
                            "state": "Ho Chi Minh",
                            "company_name": "LogiGear",
                            "job_title": "Manager",
                            "address_line_2": "2-9 street",
                            "email": "huy.quoc.tran@logigear.com",
                            "address_line_1": "Phan Xich Long street"}
            
            TestCondition.clear_all_info_in_primary_contact(Constant.AdvancedOrgName_2)
            
            # steps:    
            dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_another_org(Constant.AdvancedOrgName_2, False)

            #verify point:
            self.assertTrue(dashboard_page.is_primary_organization_contact_displayed(4), "Primary Organization Contact does not display")                        

            dashboard_page = dashboard_page.submit_primary_org_contact_info(contact_info)

            is_data_saved_at_settings_correctly = dashboard_page.goto_org_setting_page().is_data_of_primary_org_contact_correct(contact_info)
            
            #verify point:
            self.assertTrue(is_data_saved_at_settings_correctly,\
                            "The Primary Contact information has not been saved and displayed at the Organization Settings tab correclty")                        
        finally:
            TestCondition.setting_primary_contact_default(Constant.AdvancedOrgName_2)

