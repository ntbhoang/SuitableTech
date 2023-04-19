from pages.suitable_tech.user.login_page import LoginPage
from common.helper import Helper
from common.constant import Constant
from common.application_constants import ApplicationConst
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase

class SimpliedSiteAdminModeTest(TestBase):
    
    def test_c10927_change_device_location_1_x(self):
        """
        @author: Duy.Nguyen
        @date: 8/9/2016
        @summary: Change device location [1.X]
        @precondition: 
            Devices-Mod-Location
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            There is a device (Beam1) added.
        @steps:        
            1) Login to Suitabletech.com as simplified org admin and select "Manage Your Beams" from the user dropdown menu
            2) On "Manage Your Beams" page, select a device (Beam1) by clicking on the device icon
            3) Select "Edit Details" button to the right of the Beam Image
            4) Modify the "Location" information then select "Save Changes" button on "Edit Device" pop-up
            5) Back to "Manage Your Beams" page and select a device (Beam1) by clicking "Manage" button
            6) Select "Edit Details" button to the right of the Beam Image
            7) Delete the "Location" information then select "Save Changes" button

        @expected:
            (6) (8)
            _Verify that the message "The device was saved successfully." displays.
            _Verify that all changes are saved.     
        """
        
        try:
            # pre-condition:
            location = Helper.generate_random_string()
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            beam_name = beam.beam_name
               
            # step:
            simplied_detail_beam_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
                .goto_manage_beam_page(beam.beam_id)  
                          
            old_location = simplied_detail_beam_page.get_beam_location()
            simplied_detail_beam_page.set_beam_location(location)
            
            # verify point:
            self.assertEqual(simplied_detail_beam_page.get_beam_property(ApplicationConst.LBL_LOCATION_PROPERTY), location, "Assertion Error: The Location is not changed")            

        finally:
            # post-condition:
            simplied_detail_beam_page.clear_beam_location()
            TestCondition.restore_simplified_beam_location(beam=beam, location=old_location)
            
        
    def test_c10928_change_device_label_1_x(self):
        """
        @author: Duy.Nguyen
        @date: 8/9/2016
        @summary: Change device Label [1.X]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            There is a device (Beam1) added.
        @steps:        
            1) Login to Suitabletech.com as simplified org admin and select "Manage Your Beams" from the user dropdown menu
            2) On "Manage Your Beams" page, select a device (Beam1) by clicking on the device icon
            3) Select "Edit Details" button to the right of the Beam Image
            4) Modify the "Labels" information then select "Save Changes" button on "Edit Device" pop-up
            5) Back to "Manage Your Beams" page and select a device (Beam1) by clicking "Manage" button
            6) Select "Edit Details" button to the right of the Beam Image
            7) Delete the "Labels" information then select "Save Changes" button

        @expected:
            (6) (8)
            _Verify that the message "The device was saved successfully." displays.
            _Verify that all changes are saved.     
        """
        try:
            # pre-condition:
            beam_label = Helper.generate_random_label_name()
            beam_label_list = [beam_label]
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            beam_name = beam.beam_name
               
            # step:
            simplied_admin_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, True)\
            
            simplied_detail_beam_page = simplied_admin_dashboard_page.goto_manage_beam_page(beam.beam_id)            
            old_beam_label = simplied_detail_beam_page.get_beam_label_tag_list()
            simplied_detail_beam_page.set_beam_label_tag_list(beam_label_list)
            actual_beam_label = simplied_detail_beam_page.get_beam_property(ApplicationConst.LBL_LABEL_PROPERTY)
            
            # verify point:
            self.assertEqual(actual_beam_label, beam_label,
                              "Assertion Error: The Label is not changed")
                        
            simplied_detail_beam_page.clear_all_beam_label()
                        
            # verify point:
            self.assertEqual(simplied_detail_beam_page.get_beam_property(ApplicationConst.LBL_LABEL_PROPERTY), "None",
                             "Assertion Error: The Label is not cleared")
        finally:
            # post-condition:
            TestCondition.restore_simplified_beam_labels(beam=beam, label_tag_list=old_beam_label)
            
