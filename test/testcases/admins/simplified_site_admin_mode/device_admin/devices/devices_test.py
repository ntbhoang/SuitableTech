from common.constant import Constant
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from pages.suitable_tech.user.login_page import LoginPage
from data_test.dataobjects.user import User
from test.testbase import TestBase
from common.application_constants import ApplicationConst


class Device_Test(TestBase):
    
    def test_c11656_add_or_change_device_location_1_x(self):
        """
        @author: Duy.Nguyen
        @date: 7/29/2016
        @summary: Add/Change device location [1.X] 
        @precondition: 
        Login as device admin in the simplified "Manage your Beams"
        @steps:        
            1) Select the "Manage" box under the desired device image icon
            2) Select the "Edit Details" box adjacent to the device image icon
            3) Add/change the "Location" field and save changes
            
        @expected:
            Verify All Changes are saved by exiting and reentering menu        
        """
        try:
            # pre-condition:
            location = Helper.generate_random_string()
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)

            # steps:
            simplied_detail_beam_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)
            
            old_location = simplied_detail_beam_page.get_beam_location()
            
            simplied_detail_beam_page.set_beam_location(location)
            # verify point
            self.assertEqual(simplied_detail_beam_page.get_beam_property(ApplicationConst.LBL_LOCATION_PROPERTY), location, "Assertion Error: The Location is not changed")
            
        finally:
            # post-condition:
            TestCondition.delete_simplified_users([simplified_dev_admin], simplified_dev_admin.organization)
            TestCondition.restore_simplified_beam_location(beam = beam, location=old_location)
            

    def test_c11657_add_or_change_device_label_1_x(self):
        """
        @author: Duy.Nguyen
        @date: 7/29/2016
        @summary: Add/Change device Label [1.X]
        @precondition: 
        Login as device admin in the simplified "Manage your Beams"
        @steps:        
            1) Select the "Manage" box under the desired device image icon
            2) Select the "Edit Details" box adjacent to the device image icon
            3) Add/change the "Label" field and save changes
            
        @expected:
            Verify All Changes are saved by exiting and reentering menu        
        """
        try:
            # pre-condition:
            label = Helper.generate_random_label_name()
            label_list = [label]
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            beam_name = beam.beam_name
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)
                    
            # steps:
            simplied_detail_beam_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password,True)\
                .goto_manage_beam_page(beam.beam_id)      
                      
            old_label = simplied_detail_beam_page.get_beam_label_tag_list()
            simplied_detail_beam_page.set_beam_label_tag_list(label_list)
            
            # verify point
            self.assertTrue(simplied_detail_beam_page.is_beam_label_displayed(label),
                            "Assertion Error: The label is not changed")
            
        finally:
            # post-condition:  
            TestCondition.delete_simplified_users([simplified_dev_admin], test_organization)
            TestCondition.restore_simplified_beam_labels(beam, old_label)
            
            
    def test_c11659_cannot_unlink_a_beam(self):
        """
        @author: Duy.Nguyen
        @date: 7/29/2016
        @summary: Change Device Icon 
        @precondition: 
        Login as device admin in the simplified "Manage your Beams"
        @steps:        
            1) Select the "Manage" box under the desired device image icon
            2) Select the "Edit Details" box adjacent to the device image icon
            
        @expected:
            Verify that as an Simplified Device Admin you do not have the option to "Unlink this Device..".  
        """
        try:
            # pre-condition
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            beam_name = beam.beam_name
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)
                    
            # steps:
            simplied_detail_beam_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)
            
            # verify point
            self.assertFalse(simplied_detail_beam_page.is_unlink_device_button_displayed(),
                             "Assertion Error: The Unlink this Device.. is existed")
        finally:
            # post-condition        
            TestCondition.delete_simplified_users([simplified_dev_admin], test_organization)


    def test_c11658_can_change_device_name_1_x(self):
        """
        @author: Thanh Le
        @date: 08/23/2016
        @summary: Can change Device name (1.X)  
        @precondition:           
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            
            Login as device admin for simplified "Manage your Beams"

        @steps:        
            1) Click on the "Manage" box under the device image
            2) Click on the "Edit Details" to the right of the device image
            3) Edit the textbox adjacent to the "Name"; save changes
            
        @expected:
            Verify that the name of the device changed by refreshing the browser 
        """
        
        try:            
            # precondition
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_and_lock_beam(test_organization)
            beam_name = beam.beam_name
            
            simplified_dev_admin = User()
            simplified_dev_admin.generate_simplified_normal_user_data()
            simplified_dev_admin.device_group = beam_name
            
            TestCondition.create_simplified_device_admin(
                                driver=self._driver,
                                user_array=[simplified_dev_admin],
                                beam=beam,
                                organization=simplified_dev_admin.organization)
                    
            # steps:
            beam_detail_page = LoginPage(self._driver).open()\
                .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                .goto_manage_beam_page(beam.beam_id)
            
            new_name = beam_name + Helper.generate_random_string(4)
            beam_detail_page.set_beam_name(new_name)
            
            # verify point
            self.assertEqual(new_name, beam_detail_page.get_beam_property(ApplicationConst.LBL_LOCATION_NAME),
                                "Assertion Error: New Beam name \"{}\" is not displayed after updating".format(new_name))
        finally:
            # post-condition
            TestCondition.restore_simplified_beam_name(beam = beam)
            TestCondition.release_a_beam(beam)
            TestCondition.delete_simplified_users([simplified_dev_admin], test_organization)
            
