from test.testbase import TestBase
from common.constant import Constant
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.gmail_utility import GmailUtility
from core.utilities.utilities import Utilities, CSV_Utilities
from common.application_constants import ApplicationConst
from common.email_detail_constants import EmailDetailConstants
import pytest

class ActivityExports_Test(TestBase):
    
    @pytest.mark.OnlyDesktop
    def test_c33700_export_activity_with_key_work_search(self):
        """
        @author: Thanh Le
        @date: 4/28/2017
        @summary: Export activity with keyword search
        @steps:
            1. Click on the "Activity" tab in the Beam manager.
            2. Do a keyword search to narrow down the activity results displayed (e.g. the name of a Beam pilot). If no results are shown try expanding your date range or choosing a different keyword.
            3. Click on the "Export CSV" button.
        @expected:
            1. An email should be received with a button to download your requested activity export.
            2. The downloaded file should be a CSV file which includes all the records that were shown in the results screen of the "Activity" tab in the Beam manager.
        """
        try:
            # pre-condition
            organization_name = Constant.AdvancedOrgName
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization_name
            
            date_range = { 'from_date': {'dd':'03','mm':'04','yyyy':'2017'}, 'to_date': {'dd':'13','mm':'04','yyyy':'2017'}}
            status = [ApplicationConst.STATE_OFFLINE]
            keyword = Constant.BeamPlusName
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            #steps:
            admin_activity_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_activity_tab()\
                .search_activity(date_range, status, keyword, export_csv=True)
            
            activity_export_url = GmailUtility.get_activity_export_link(email_subject = EmailDetailConstants.ActivityExportTitle, receiver=org_admin.email_address)
            file_path = Utilities.download_activity_export_csv_file(activity_export_url)
            data_in_csv = CSV_Utilities.read_export_activity_csv(file_path)
            data_on_web = admin_activity_page.get_list_activity_items()
            
            # TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2171"
            self.assertTrue(data_in_csv == data_on_web, 'Inconsistency about the number of activity records between website and export csv')
        finally:
            TestCondition.delete_advanced_users([org_admin], organization_name)
            Utilities.delete_file(file_path)
            
            
    @pytest.mark.OnlyDesktop
    def test_c33701_export_activity_with_large_number_of_records(self):
        """
        @author: Thanh Le
        @date: 4/28/2017
        @summary: Export activity with large number of records
        @steps:
            1. Click on the "Activity" tab in the Beam manager.
            2. Choose a large date range so as to get at least 1000 records to display.
            3. Click on the "Export CSV" button.
        @expected:
            1. An email should be received with a button to download your requested activity export.
            2. The downloaded file should be a CSV file which includes all the records that were shown in the results screen of the "Activity" tab in the Beam manager.
        """
        try:
            # pre-condition
            organization_name = Constant.AdvancedOrgName
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization_name
            
            date_range = { 'from_date': {'dd':'22','mm':'04','yyyy':'2016'}, 'to_date': {'dd':'22','mm':'10','yyyy':'2017'}}
            status = [ApplicationConst.STATE_IN_A_CALL, ApplicationConst.STATE_OFFLINE, ApplicationConst.STATE_MISSED_CALLS, ApplicationConst.STATE_CONFIGURING, ApplicationConst.STATE_UPGRADING]
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            #steps:
            admin_activity_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_activity_tab()\
                .search_activity(date_range, status, export_csv=True)
            
            activity_export_url = GmailUtility.get_activity_export_link(email_subject = EmailDetailConstants.ActivityExportTitle, receiver=org_admin.email_address)
            file_path = Utilities.download_activity_export_csv_file(activity_export_url)
            data_in_csv = CSV_Utilities.read_export_activity_csv(file_path)
            data_on_web = admin_activity_page.get_list_activity_items()
            
            # TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2171"
            self.assertTrue(data_in_csv==data_on_web, 'Data show on Website does not match with CSV file.')
        finally:
            TestCondition.delete_advanced_users([org_admin], organization_name)
            Utilities.delete_file(file_path)            
            
           
    @pytest.mark.OnlyDesktop         
    def test_c33702_export_activity_with_no_records(self):
        """
        @author: Thanh Le
        @date: 5/5/2017
        @summary: Export activity with no records
        @steps:
            1. Click on the "Activity" tab in the Beam manager.
            2. Search for a random keyword so as to exclude all records. 0 records should be displayed in the results screen.
            3. Click on the "Export CSV" button.
        @expected:
            1. An email should be received with a button to download your requested activity export.
            2. The downloaded file should be a CSV file with no records, and only the headers present.
        """
        try:
            # pre-condition
            organization_name = Constant.AdvancedOrgName
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization_name
            
            date_range = { 'from_date': {'dd':'22','mm':'04','yyyy':'2015'}, 'to_date': {'dd':'22','mm':'10','yyyy':'2015'}}
            status = [ ApplicationConst.STATE_OFFLINE, ApplicationConst.STATE_UPGRADING]
            keyword = Constant.BeamPlusName
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            #steps:
            LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_activity_tab()\
                .search_activity(date_range, status, keyword, export_csv=True)
            
            activity_export_url = GmailUtility.get_activity_export_link(email_subject = EmailDetailConstants.ActivityExportTitle, receiver=org_admin.email_address)
            file_path = Utilities.download_activity_export_csv_file(activity_export_url)
            csv_empty = CSV_Utilities.does_csv_only_have_header(file_path)
            
            self.assertTrue(csv_empty, 'Exported CSV file has records or it has not headers.')
        finally:
            TestCondition.delete_advanced_users([org_admin], organization_name)
            Utilities.delete_file(file_path)
            
    
    @pytest.mark.OnlyDesktop
    def test_c33703_export_activity_with_different_statuses(self):
        """
        @author: Thanh Le
        @date: 5/5/2017
        @summary: Export activity with different statuses
        @steps:
            1. Click on the "Activity" tab in the Beam manager.
            2. Choose a random combination of statuses via the "Status" dropdown so as to narrow down your search results. If no records are displayed, extend your date range or choose different statuses.
            3. Click on the "Export CSV" button.
        @expected:
            1. An email should be received with a button to download your requested activity export.
            2. The downloaded file should be a CSV file which includes all the records that were shown in the results screen of the "Activity" tab in the Beam manager.
        """
        try:
            # pre-condition
            organization_name = Constant.AdvancedOrgName
            
            org_admin = User()                                            
            org_admin.generate_advanced_org_admin_data()
            org_admin.organization = organization_name
            
            date_range = { 'from_date': {'dd':'07','mm':'01','yyyy':'2017'}, 'to_date': {'dd':'16','mm':'01','yyyy':'2017'}}
            status = [ApplicationConst.STATE_OFFLINE, ApplicationConst.STATE_CONFIGURING, ApplicationConst.STATE_UPGRADING]
            keyword = Constant.BeamPlusName
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])

            #steps:
            admin_activity_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_activity_tab()\
                .search_activity(date_range, status, keyword, export_csv=True)
            
            activity_export_url = GmailUtility.get_activity_export_link(email_subject = EmailDetailConstants.ActivityExportTitle, receiver=org_admin.email_address)
            file_path = Utilities.download_activity_export_csv_file(activity_export_url)
            data_in_csv = CSV_Utilities.read_export_activity_csv(file_path)
            data_on_web = admin_activity_page.get_list_activity_items()
            
            #TODO: Test case failed due to bug INFR-2171
            self.assertTrue(data_in_csv==data_on_web, 'Data show on Website does not match with CSV file.')
        finally:
            TestCondition.delete_advanced_users([org_admin], organization_name)
            Utilities.delete_file(file_path)
            
            
    @pytest.mark.OnlyDesktop
    def test_c33808_tooltip_displays_when_clicking_on_an_item_of_the_activity_results(self):
        """
        @author: Thanh Le
        @date: 5/31/2017
        @summary: Tooltip displays when clicking on an item of the activity results
        @steps:
            1. Click on the "Activity" tab in the Beam manager.
            2. Do a keyword search to narrow down the activity results displayed (e.g. the name of a Beam pilot). If no results are shown try expanding your date range or choosing a different keyword.
            3. Click on an item of the activity results
        @expected:
            Tooltip displays
        """
        try:
            # pre-condition
            org_admin = User()                                            
            org_admin.advanced_org_admin_data()
            
            date_range = { 'from_date': {'dd':'10','mm':'02','yyyy':'2018'}, 'to_date': {'dd':'12','mm':'02','yyyy':'2018'}}
            status = ApplicationConst.STATE_IN_A_CALL
            keyword = Constant.BeamProNameUTF8
            
            #steps:
            admin_activity_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_activity_tab()\
                .search_activity(date_range, status, keyword, export_csv=False)\
                .click_activity_item()
            actual_content_tooltip = admin_activity_page.get_content_tooltip_displays()  
            expected_info = TestCondition.get_activity_time_range_for_status_in_call(date_range)
            expected_content_tooltip = Utilities.genarate_content_tooltip(expected_info, self._driver.driverSetting.language)
            #verify point 
            self.assertEqual(actual_content_tooltip, expected_content_tooltip, 
                             "Tooltip does not display correct")
        finally:
            pass

