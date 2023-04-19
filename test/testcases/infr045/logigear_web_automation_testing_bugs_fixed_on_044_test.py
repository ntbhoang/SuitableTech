from test.testbase import TestBase
from common.helper import Helper
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User 
from pages.suitable_tech.user.login_page import LoginPage


class Logigear_web_automation_testing_bugs_fixed_on_044_Test(TestBase):


    def test_c33947_device_group_admin_cannot_invite_users_to_user_groups_outside_of_their_device_group(self):
        """
        @author: Quang Tran
        @date: 11/20/2017
        @summary: Device Group Admin cannot invite users to User Groups outside of their Device Group
        @precondition:
            Create a device group
            Create a device group admin for the device group
            Create a user group

        @steps:
            1. Login the staging site with device group admin
            2. Go to Users tab
            3. Select the user group outside of his device group
        @expected:
            Add Users button is not displayed.
        """
        try:
            #pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
    
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
    
            user_group_name = Helper.generate_random_user_group_name()
            TestCondition.create_user_group(user_group_name)
    
            #steps
            user_detail_page = LoginPage(self._driver).open()\
                    .login(device_group_admin.email_address, device_group_admin.password)\
                    .goto_users_tab()\
                    .select_user_group(user_group_name)
    
            #verify point
            self.assertFalse(user_detail_page.is_add_user_button_displayed(3), 
                             "Add User button still displayed")

        finally:
            #post-condition
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_user_groups([user_group_name])

