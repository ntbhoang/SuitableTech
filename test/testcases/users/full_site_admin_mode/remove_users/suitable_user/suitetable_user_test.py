from common.constant import Constant
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from common.helper import Helper
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
import pytest

class SuitetableUser_Test(TestBase):
    @pytest.mark.onlyDesktop
    def test_c10942_remove_user_1_x(self):
        
        """
        @author: Thanh.Le
        @date: 7/27/2016
        @summary: Remove User from Org [1.X]
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Login as an org admin
        @steps
            Delete A User from the Organization:
            1. Login as a device group admin, go to the "Manage your Beams" dashboard and click on the "Users" tab
            2. Need to test function from "User Groups" and "Users" sections
            a) Click on a "User Group" > select a user from "Users in this group"
            b) Click on a user in the "Users" section > 
            3) select the red "Remove from Organization" button on the right side
            4) confirm decision in pop-up
        @expected Result
            Verify that the user is removed from the org
        """
        try:
            #preconditions:
            user_group_name = Helper.generate_random_user_group_name(5)
            TestCondition.create_user_group(user_group_name)
            
            user1 = User()
            user1.generate_advanced_normal_user_data()
            
            user2 = User()     
            user2.generate_advanced_normal_user_data()
            user2.user_group = user_group_name
            
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            user1.device_group = temp_device_group_name
            user2.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
            
            TestCondition.create_advanced_normal_users(self._driver, [user1, user2], False)
            
            user1_displayed_name = user1.get_displayed_name()
            user2_displayed_name = user2.get_displayed_name()
            
            #steps:
            user_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .remove_user_from_organization(user1)
            
            #verify point:
            self.assertTrue(user_page.is_user_not_existed(user1.email_address, user1_displayed_name),"Assertion Error: User is still existed!")                                        
            user_page.goto_user_group_detail_page(user_group_name).remove_user_from_organization(user2)
             
            self.assertTrue(user_page.is_user_not_existed(user2.email_address,user2_displayed_name),"Assertion Error: User is still existed!")
        finally:
            TestCondition.delete_device_groups([temp_device_group_name])
            TestCondition.delete_user_groups([user_group_name])
    
    
    def test_c10945_verify_removed_user_can_still_log_in_1_x(self):
        """
        @author: Thanh.Le
        @date: 7/29/2016
        @summary: Verify removed user can still log in [1.X]
        @preconditions:
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Standard user has device group access to two orgs.
        @steps
            1) Go to "Users" tab under "Manage your Beams" dashboard
            2) Select a user
            3) click the red "Remove from organization" button at the top right hand of the screen
        @expected Result
            Verify that the removed user is still able to login
            Verify that the user has no access to the beams of the org from which he/she was removed
            Verify that if removed user has access to more than one org, he/she should still have access to the org from which he/she was not removed
        """
        try:
            #pre-condition
            device_group = Helper.generate_random_device_group_name()
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
            TestCondition.create_device_group(device_group_name=device_group, device_array=[beam_name], organization_name=Constant.AdvancedOrgName)
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=Constant.AdvancedOrgName_2)
            
            user = User()
            user.generate_advanced_normal_user_data()  
            user.device_group = device_group               
            TestCondition.create_advanced_multi_org_normal_users(driver=self._driver, user_array=[user], organization_array=[Constant.AdvancedOrgName, Constant.AdvancedOrgName_2], activate_user=True)
            
            #steps
            normal_user_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .remove_user_from_organization(user)\
                .logout_and_login_again(user.email_address, user.password, True)
            
            #verify points            
            self.assertTrue(normal_user_page.is_page_displayed(), 
                            "Assertion Error: User '{}' is NOT logged in after it was removed".format(user.email_address))
            
            account_settings_page = normal_user_page.goto_your_account()
                        
            self.assertFalse(account_settings_page.is_org_title_displayed(Constant.AdvancedOrgName),
                             "Assertion Error: User still has accessed to the org '{}'".format(Constant.AdvancedOrgName))
            self.assertTrue(account_settings_page.is_org_title_displayed(Constant.AdvancedOrgName_2),
                            "Assertion Error: User has no access to the org '{}'".format(Constant.AdvancedOrgName_2))
        finally:
            #post-condition    
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([user], Constant.AdvancedOrgName_2)
            TestCondition.delete_device_groups([device_group], Constant.AdvancedOrgName)
            TestCondition.delete_device_groups([device_group], Constant.AdvancedOrgName_2)

