from common.helper import Helper
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from common.application_constants import ApplicationConst
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from common.constant import Constant, Platform
import pytest

class User_Group_Test(TestBase):
    
    def test_c10918_rename_usergroup_1_x(self):
        """
        @author: khoi.ngo
        @date: 7/26/2016
        @summary: Rename UserGroup [1.X]
        @precondition: Use the Admin Test Organization
        @steps:
            1. Go to the "Users" tab under the "Manage your Beams" dashboard
            2. Click on a user group icon under the "User Groups" section
            3. Click the "edit" box under the user group title
            4. Change the "Name" string to desired name; click save changes

        @expected:
            User group should automatically update.
        """
        try:
            #pre-condition            
            user_group_name = Helper.generate_random_user_group_name()
            new_user_group_name = Helper.generate_random_user_group_name()
            
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            
            TestCondition.create_user_group(user_group_name)
             
            #steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)  
            user_group_detail = admin_dashboard_page.goto_users_tab()\
                .goto_user_group_detail_page(user_group_name)\
                .change_group_name(new_user_group_name) 

            self.assertTrue(user_group_detail.is_success_msg_displayed(), "Message success is not displayed")              
            self.assertTrue(user_group_detail.is_user_group_name_displayed(new_user_group_name), "Assertion Error: User group's name was not changed.")

            users_tab = user_group_detail.goto_users_tab().is_user_group_existed(new_user_group_name)
            self.assertTrue(users_tab, "User group is not displayed")
            
        finally:
            #post-condition
            TestCondition.delete_user_groups([new_user_group_name])
    
    
    def test_c10917_create_usergroup_1_x(self):
        """
        @author: Quang Tran
        @date: 08/04/2016
        @summary: Create UserGroup [1.X]
        @precondition: 
        @steps:
            Steps to complete create a user group:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and select "Create New User Group" button
            3. Enter name of user group to "Name" field and click "Create User Group" button
            4. Click on "Users" tab again to reload User page
            5. Search for the newly created User Group in step #3 above

        @expected:
            (3). The user group with name entered at step #3 is created for adding user.
            (5). The newly created User Group is presented in user group list.
        """
        try:       
            #steps
            user_group_name = Helper.generate_random_user_group_name()
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_users_tab().create_new_user_group(user_group_name)
            
            #verify point
            self.assertEqual(user_group_detail_page.get_msg_success(), ApplicationConst.INFO_MSG_CREATE_USER_GROUP_SUCCESSFUL, 
                             "Assertion Error: Expected message is not displayed")
            
            is_user_group_name_displayed = user_group_detail_page.is_user_group_name_displayed(user_group_name)
            self.assertTrue(is_user_group_name_displayed, "Assertion Error: The user group {} cannot be created.".format(user_group_name))
            
            if is_user_group_name_displayed:
                admin_users_page = user_group_detail_page.goto_users_tab()
                self.assertTrue(admin_users_page.is_user_group_existed(user_group_name), 
                    "Assertion Error: The user group {} cannot be found in the user group list.".format(user_group_name))
        finally:
            #post-condition:
            TestCondition.delete_user_groups([user_group_name])
    
    
    def test_c10919_delete_usergroup_1_x(self):
        """
        @author: khoi.ngo
        @date: 7/26/2016
        @summary: Delete UserGroup [1.X]
        @precondition: Use the Admin Test Organization
        @steps:
            1. Go to the "Users" tab under the "Manage your Beams" dashboard
            2. Click on a user group icon under the "User Groups" section
            3. Click the "Delete this group" red box in the top right corner of the screen
            4. You should see a message box; click okay (see attached image)

        @expected:
            The user group should be deleted right away.
        """        
        #pre-condition            
        user_group_name = Helper.generate_random_user_group_name()                
        org_admin = User()
        org_admin.generate_org_admin_user_data()
        
        TestCondition.create_user_group(user_group_name)
            
        #steps
        user_tab = LoginPage(self._driver).open()\
            .login(org_admin.email_address, org_admin.password)\
            .goto_users_tab()
            
        admin_user_page = user_tab.goto_user_group_detail_page(user_group_name)\
            .delete_user_group(wait_for_completed=False)
        
        #verify point
        self.assertEqual(admin_user_page.get_msg_success(), ApplicationConst.INFO_MSG_DELETE_USER_GROUP_SUCCESSFUL, 
                         "Assertion Error: Expected message is not displayed")
        self.assertTrue(admin_user_page.is_user_group_not_existed(user_group_name), 
                        "Assertion Error: User group is still displayed")
    
    
    def test_c10920_add_user_to_usergroup_1_x(self):
        """
        @author: Quang Tran
        @date: 08/04/2016
        @summary: Create UserGroup [1.X]
        @precondition: 
            Create a User Group (UserGroupA) following these steps:
            
                Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
                Go to "Users" tab and select "Create New User Group" button
                Enter name of user group to "Name" field and click "Create User Group" button
            
            Invite a new user UserA
        @steps:
            Steps To Complete Task: Add user to user group
            
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and search for a user group (UserGroupA) in pre-condition
            3. Select this user group and click on "Add Users" button
            4. Search for UserA and select "Add Selected Users" button

        @expected:
            (3) Verify that user is added under the "Users in this group" list.
            (4) Verify that the user group name is added to "User Groups" of UserA's detail page.
        """
        try:
            #pre-condition
            device_group = Helper.generate_random_device_group_name()
            organization = Constant.AdvancedOrgName
            TestCondition.create_device_group(device_group_name=device_group, device_array=[], organization_name=organization)
            new_user_group_name = Helper.generate_random_user_group_name()
            TestCondition.create_user_group(new_user_group_name)
            
            new_user = User()
            new_user.generate_advanced_normal_user_data()
            new_user.device_group = device_group
            new_user.user_group = None     
            new_user.organization = organization       
            TestCondition.create_advanced_normal_users(self._driver, [new_user])
            
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            
            #steps
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()\
                .goto_user_group_detail_page(new_user_group_name).add_user_to_group(new_user.email_address)
            
            #verify point
            is_user_added = user_group_detail_page.is_user_existed(new_user.get_displayed_name())
            self.assertTrue(is_user_added, "Assertion Error: The new user {} cannot be added to user group {}.".format(new_user.email_address, new_user_group_name))
            
            actual_group_name = ApplicationConst.LBL_ALL_USERS_GROUP + ", " + new_user_group_name
            
            admin_user_detail_page = user_group_detail_page.goto_users_tab().goto_user_detail_page(new_user)
            actual_new_user_group = admin_user_detail_page.get_user_info(ApplicationConst.LBL_USER_GROUPS)
            actual_new_user_group = actual_new_user_group.replace(u'\xa0', u' ')
            self.assertEqual(actual_group_name, actual_new_user_group, 
                             "Assertion Error: The user group name {} is not added to \"User Groups\" of user {}.".format(new_user_group_name, new_user.email_address ))
            
        finally:
            #post-condition:
            TestCondition.delete_user_groups([new_user_group_name])
            TestCondition.delete_advanced_users([new_user])
            TestCondition.delete_device_groups([device_group], organization)


    def test_c10921_remove_user_from_usergroup_1_x(self):
        """
        @author: khoi.ngo
        @date: 08/05/2016
        @summary: Remove user from UserGroup [1.X]
        @precondition: 
            Create a User Group (UserGroupA) following these steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and select "Create New User Group" button
            3. Enter name of user group to "Name" field and click "Create User Group" button
            
            Invite a new user UserA and add this user to above user group (UserGroupA)
        @steps:
        
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and search for exist user group in pre-condition
            3. Click on this user group button
            4. Select "Removed" red button on the user icon
            5. Click on "Ok" button on warning message
        @expected:
            _Verify that user is removed from "Users in this group" list.
            _Verify that the user group is not in "User Groups" of UserA's detail page.
        """
        try:
            # precondition
            user_group_name = Helper.generate_random_user_group_name()
            new_user = User()
            new_user.generate_advanced_normal_user_data()
            new_user.user_group = user_group_name
            
            device_group_name = Helper.generate_random_device_group_name()
            new_user.device_group = device_group_name
            TestCondition.create_device_group(device_group_name)
            
            TestCondition.create_user_group(user_group_name)
            TestCondition.create_advanced_normal_users(self._driver, [new_user])
            
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            org_admin.device_group = device_group_name
            
            # steps
            user_group_detail = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()\
                .goto_user_group_detail_page(user_group_name).remove_user(new_user.get_displayed_name())\
            
            is_user_not_existed = user_group_detail.is_user_not_existed(new_user.get_displayed_name())
            
            #verify point
            self.assertTrue(is_user_not_existed, "Assertion Error: User still exists in this group")
            
            actual_group_name = ApplicationConst.LBL_ALL_USERS_GROUP
            
            user_detail_page = user_group_detail.goto_users_tab().goto_user_detail_page(new_user)
            actual_user_groups = user_detail_page.get_user_groups()
            self.assertEqual([actual_group_name], actual_user_groups, "Assertion Error: User is still in User group " + user_group_name)
        
        finally:
            # post-condition
            TestCondition.delete_advanced_users([new_user])
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group_name])
   
                
    @pytest.mark.OnlyDesktop
    def test_c10992_view_usergroup_in_list_and_icon_viewing_mode(self):
        """
        @author: Thanh Le
        @date: 08/05/2016
        @summary: Create UserGroup [1.X]
        @precondition: 
            Have a user group (UserGroupA) with a user (UserA) added
        @steps:
            1) Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2) Go to "Users" tab
            3) Select icon view button on the top right to view icon mode
            4) Select list view button on the top right to view in list mode

        @expected:
            Verify Users-Groups/Users are all visible in a usable manner:
            1. Size of Icons are correct
            2. Text sizes
        """
        try:
            #pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            new_user = User()
            new_user.generate_advanced_normal_user_data()            
            org_admin = User()
            org_admin.generate_org_admin_user_data()
            # create device group
            device_group_name = Helper.generate_random_device_group_name()
            new_user.device_group = device_group_name
            org_admin.device_group = device_group_name
            TestCondition.create_device_group(device_group_name)
            
            TestCondition.create_advanced_normal_users(self._driver, [new_user])
            TestCondition.create_user_group(user_group_name, [new_user])
                   
            #steps            
            user_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab().search_for_user(new_user.email_address)

            user_list_view_size = user_page.switch_to_list_view()\
                .get_item_size_in_list_view(new_user.get_displayed_name())
            user_group_list_view_size = user_page.get_item_size_in_list_view(user_group_name)
            
            user_icon_view_size = user_page.switch_to_icon_view()\
                .get_item_size_in_icon_view(new_user.get_displayed_name())
            user_group_icon_view_size = user_page.get_item_size_in_icon_view(user_group_name)
            
            # verify points
            self.assertTrue(user_icon_view_size > user_list_view_size,
                            "Assertion Error: Unable to switch from icon view to list view.")
            self.assertTrue(user_group_icon_view_size > user_group_list_view_size,
                            "Assertion Error: Unable to switch from icon view to list view.")
        finally:
            #post-condition:
            TestCondition.delete_advanced_users([new_user])            
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_device_groups([device_group_name])
            
    
    def test_c11097_move_an_existing_user_from_usergroup_a_to_another_usergroup_b_2_x(self):
        """
        @author: Thanh Le
        @date: 08/05/2016
        @summary: Move an existing User from UserGroup A to another UserGroup B [2.X]
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            
            Add UserGroupA
            Add UserGroupB
            Create UserA
        @steps:
            1) Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2) Go to "Users" tab and select the existing user group (UserGroupA)
            3) Add existing user (UserA) to this user group (UserGroupA)
            4) Go to "User " tab and select another existing user group (UserGroupB) and also add UserA to this group
            5) Go to the initial user group (UserGroupA) and remove the user (A)
            6) Go to UserGroup B and search for the just removed UserA from initial user group

        @expected:
            (6 The removed user from initial user group (UserGroupA) still exist in the other user group (UserGroupB).

            Note:
            General Business logic vitrification for DeviceGroup(s)
            - DeviceGroup(s) are containers for a single or multiple Device(s)
            - Single User(s) can be members of a DeviceGroup outside of a UserGroup via a Default or Custom Access Time Schedule(s)/Template(s), allowing User(s) access to associated Device(s)
            - Single or multiple UserGroup(s) can be members of a DeviceGroup via a Default or Custom Access Time Schedule(s)/Template(s), allowing User(s) access to associated Device(s)
            - Single User can be a members of DeviceGroup(s) via a Default or Custom Access Time Schedule(s)/Template(s), allowing User(s) access to associated Device(s)
            - Single Default or multiple custom Access Time Schedule(s)/Template(s) can be members of a DeviceGroup
            - Single or multiple Temporary Access Time Schedule(s) can be attached to a DeviceGroup
            - Device(s) status Notifications to User(s) can be associated with a DeviceGroup
            - Session Answer Notifications to User(s) to accept call answer requests can be associated with a DeviceGroup
        """
                
        try:
            #pre-condition
            admin_user = User()                                            
            admin_user.generate_org_admin_user_data()
            new_user = User()
            new_user.generate_advanced_normal_user_data()            
            user_group_a = Helper.generate_random_user_group_name()
            user_group_b = Helper.generate_random_user_group_name()
            # create device group
            device_group_name = Helper.generate_random_device_group_name()
            new_user.device_group = device_group_name
            admin_user.device_group = device_group_name
            TestCondition.create_device_group(device_group_name)
            
            TestCondition.create_advanced_normal_users(self._driver, [new_user], False)
            TestCondition.create_user_group(user_group_a, [new_user])
            TestCondition.create_user_group(user_group_b, [new_user])
                               
            #steps
            user_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_users_tab()\
                .goto_user_group_detail_page(user_group_a).remove_user(new_user.get_displayed_name())\
                .goto_users_tab().goto_user_group_detail_page(user_group_b)
            
            #verify point
            self.assertTrue(user_page.is_user_existed(new_user.get_displayed_name()),
                            "Assertion Error: User is NOT existed!" )
        finally:
            #post-condition:
            TestCondition.delete_advanced_users([new_user])
            TestCondition.delete_user_groups([user_group_a, user_group_b])
            TestCondition.delete_device_groups([device_group_name])
            
            
    def test_c33847_Add_all_users_to_userGroup(self):
        """
        @author: tham.nguyen
        @date: 08/17/2016
        @summary: SuitableTech Account existed previously Non-First time user authorized
        @precondition:
            Create a User Group (UserGroupA) following these steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and select "Create New User Group" button
            3. Enter name of user group to "Name" field and click "Create User Group" button
        @steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and search for a user group (UserGroupA) in pre-condition
            3. Select this user group and click on "Add All Users" item under the Add Users button
            4. Confirm action on Confirmation popup
            
        @expected:
            Verify that all users are added under the "Users in this group" list.
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            organization = Constant.AdvancedOrgName_2
            
            org_admin = User()                                            
            org_admin.generate_org_admin_user_data()
            org_admin.organization = organization
            
            TestCondition.create_user_group(user_group_name, organization_name=organization)

            # steps
            admin_users_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_another_org(organization)\
                .goto_users_tab()\
                .goto_user_group_detail_page(user_group_name)\
                .click_add_user_button_and_select(ApplicationConst.LBL_MENU_ADD_ADD_ORGANIZATION_USERS)

            # verify points
            self.assertTrue(admin_users_page.is_all_users_added(org_admin.organization),
                    "All users are not added under the \"Users in this group\" list")
        finally:
            # post-condition
            TestCondition.delete_user_groups([user_group_name], organization)
            
            
    def test_c33848_Remove_all_users_from_UserGroup(self):
        """
        @author: tham.nguyen
        @date: 08/17/2016
        @summary: SuitableTech Account existed previously Non-First time user authorized
        @precondition:
            Create a User Group (UserGroupA) following these steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and select "Create New User Group" button
            3. Enter name of user group to "Name" field and click "Create User Group" button
            4. Add some users into this group
        @steps:
            1. Login to Suitabletech.com as an org admin and select Manage Your Beams from the user dropdown menu
            2. Go to "Users" tab and search for a user group (UserGroupA) in pre-condition
            3. Select this user group and click on "Remove All Users" item under the Add Users button
            4. Confirm action on Confirmation popup
            
        @expected:
            Verify that all users are removed under the "Users in this group" list.
        """
        try:
            # pre-condition
            user_group_name = Helper.generate_random_user_group_name()
            organization = Constant.AdvancedOrgName
            
            new_user = User()
            new_user.generate_advanced_normal_user_data()
            new_user.user_group = None     
            new_user.organization = organization       
            TestCondition.create_advanced_normal_users(self._driver, [new_user])
            
            org_admin = User()                                            
            org_admin.generate_org_admin_user_data()
            org_admin.organization = organization
            
            TestCondition.create_user_group(user_group_name)

            # steps
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()\
                .goto_user_group_detail_page(user_group_name)\
                .add_user_to_group(new_user.email_address)\
            
            #verify point
            is_user_added = user_group_detail_page.is_user_existed(new_user.get_displayed_name())
            self.assertTrue(is_user_added, "Assertion Error: The new user {} cannot be added to user group {}.".format(new_user.email_address, user_group_name))

            user_group_detail_page.click_add_user_button_and_select(ApplicationConst.LBL_MENU_REMOVE_ALL_USERS)
            
            is_user_added = user_group_detail_page.is_user_existed(new_user.get_displayed_name())
            self.assertFalse(is_user_added, "Assertion Error: The new user {} cannot be removed out of user group {}.".format(new_user.email_address, user_group_name))
        finally:
            # post-condition
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_advanced_users([new_user])


    def test_c33901_cannot_create_usergroup_that_already_existed(self):
        """
        @author: Khoi Ngo
        @date: 10/16/2017
        @summary: Verify that admin cannot create UserGroup that already existed
        @steps:
            1. Login as org admin
            2. Go to Users page
            3. Click Create New User Group button
            4. Enter name then click Create User Group
            5. Click Create New User Group button again
            6. Create User Group with the same name at step 4
        @expected:
            (6) 'A user group with that name already exists.' message displays.
        """

        try:
            user_group_name = Helper.generate_random_user_group_name()
            # steps
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .create_new_user_group(user_group_name)\
                .goto_users_tab()\
                .create_new_user_group(user_group_name)

            actual_msg = user_group_detail_page.get_error_message()
            self.assertTrue(user_group_detail_page.is_error_msg_displayed(),
                            "Error message doesn't display")
            self.assertEqual(actual_msg, ApplicationConst.INFO_MSG_USER_GROUP_EXISTED,
                             "Error message content is not correct")
        finally:
            TestCondition.delete_user_groups([user_group_name])


    def test_c33902_add_new_user_to_usergroup(self):
        """
        @author: Khoi Ngo
        @date: 10/17/2017
        @summary: Verify that admin can add new user to UserGroup
        @precondition:
            - Create new UserGroup
        @steps:
            1. Login as org admin
            2. Go to Users page
            3. Select new UserGroup at precondition
            4. Click Add Users button
            5. Click Invite a New User button
            6. Enter email address and click Invite User button
            7. Click Add Selected Users button
        @expected:
            (6) Verify that user is added under the "Users in this group" list.
            (7) Verify that the user group name is added to "User Groups" of user's detail page.
        """

        try:
            user_group_name = Helper.generate_random_user_group_name()
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            # pre-condition
            TestCondition.create_user_group(user_group_name)

            # steps
            choose_user_dialog = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .select_user_group(user_group_name)\
                .open_add_user_dialog()\
                .invite_new_user(normal_user)
            self.assertTrue(choose_user_dialog.is_user_displayed_in_selected_list(normal_user.email_address),
                            "User is not added under the 'Users in this group' list")

            user_detail_page = choose_user_dialog.add_selected_user()\
                .goto_user_detail_page(normal_user)
            actual_user_groups = user_detail_page.get_user_info(ApplicationConst.LBL_USER_GROUPS)
            self.assertTrue(user_group_name in actual_user_groups,
                            "the user group name is not added to User Groups of user's detail page")
        finally:
            TestCondition.delete_user_groups([user_group_name])
            TestCondition.delete_advanced_users([normal_user])


    @pytest.mark.OnlyDesktop
    def test_c33908_pagination_page_works_correctly(self):
        """
        @author: Khoi Ngo
        @date: 10/18/2017
        @summary: Verify that pagination page works correctly
        @precondition:
            - Create some User Groups (greater than 10)
        @steps:
            1. Login as org admin
            2. Go to Users page
            3. Select show 10 Items option
            4. Go to each page of User Groups section
        @expected:
            (3) The pagination control displays
            (4) Each page displays correctly the number of User Groups
        """

        try:
            # pre-condition
            user_group_names = []
            for order in range(0, 10):
                user_group_names.append(Helper.generate_random_user_group_name())
                TestCondition.create_user_group(user_group_names[order])

            # steps
            admin_users_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_users_tab()\
                .click_items_button_and_select(ApplicationConst.LBL_10_ITEMS)
            self.assertTrue(admin_users_page.is_pagination_displayed(),
                            "The pagination control doesn't display")
            self.assertTrue(admin_users_page.is_page_display_user_groups_number_correctly(ApplicationConst.LBL_10_ITEMS),
                            "Each page displays the number of User Groups incorrectly")
        finally:
            TestCondition.delete_user_groups(user_group_names)


    def test_c33912_add_device_group_for_user_group_on_Edit_User_Group_modal_2_x(self):
        """
        @author: Khoi Ngo
        @date: 19/10/2017
        @summary: Add device group for user group on Edit User Group modal
        @precondition: 
            Create an user group
            Create a device group
        @steps:
            1) Login as org admin
            2) Go to Users page
            3) Select User Group that is created at precondition
            4) Click Edit button
            5) Enter Device Group name at precondition into Device Groups field
            6) Choose Device Group and click Save Changes
            7) Go to Members page Device Group
        @expected:
            (6)
            - Success message displays
            - Device Group name displays on Device Groups field of User Group              
            (7) User Group displays on Members page of Device Group
        """
        try:
            # pre-condition
            user_group = Helper.generate_random_user_group_name()
            TestCondition.create_user_group(user_group)

            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)

            # steps
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_users_tab()\
                .select_user_group(user_group)\
                .add_device_group_to_user_group(device_group_name)
 
            # verify point
            msg_success = user_group_detail_page.is_success_msg_displayed()
            self.assertTrue(msg_success, 
                            "No message displayed when add device group {} successfully".format(device_group_name))
            self.assertIn(device_group_name, user_group_detail_page.get_property(ApplicationConst.LBL_DEVICE_GROUPS_PROPERTY),
                            "Device group {} didn't display after add to group".format(device_group_name))

            members_device_group = user_group_detail_page.goto_device_group_detail_page(device_group_name).goto_members_tab()
            self.assertTrue(members_device_group.is_user_group_existed(user_group), 
                            "User group {} not displayed in member tab of device group".format(user_group))

        finally:
            # post-condition
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_user_groups([user_group])


    def test_c33945_users_that_have_verified_domains_are_in_the_saml_users_user_group(self):
        """
        @author: Khoi Ngo
        @date: 17/11/2017
        @summary: Users that have verified domains are in the Saml Users user group
        @precondition:
            Exist a SSO org having verified domain
            Create org admin for the org
        @steps:
            1. Login staging site as the org admin
            2. Invite a user that email domain is verified domain
            3. Go to Users tab
            4. Select SAML user group
        @expected:
            Users that have verified domains are in the Saml Users user group.
        """
        try:
            # pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data("logigear.com")
            auth = TestCondition.get_and_lock_org_authentication()
            TestCondition.change_authentication_to_OneLogin()
            
            # steps
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .invite_new_user(normal_user).goto_users_tab().select_user_group(ApplicationConst.LBL_SAML_USERS_GROUP)
            # verify point
            self.assertTrue(user_group_detail_page.is_user_existed(normal_user.get_displayed_name()), 
                            "Users that have verified domains aren't in the Saml Users user group.")
        finally:
            # post-condition
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.release_org_authentication(auth)


    def test_c34005_search_and_sort_work_correctly_in_user_group_details(self):
            """
            @author: Khoi Ngo
            @date: 3/01/2018
            @summary: Search and sort functions work correctly in UserGroup details.
            @precondition:
                Login as org admin or device group admin
                Have a User Group with several user members
            @steps:
                1. Login staging site as the org admin
                2. Go to Users tab
                3. Select the User Group in preconditions
                4. Sort by First Name, Last Name, Username
                5. Search for an user in the User Group
            @expected:
                1. Verify that Sort by First Name, Last Name, Username work correctly
                2. Verify that Search works correctly
            """
            try:
                #pre-condition:
                user_group = Helper.generate_random_user_group_name()
                user_member_1 = User()
                user_member_2 = User()
                user_member_3 = User()
                user_member_1.generate_advanced_normal_user_data()
                user_member_2.generate_advanced_normal_user_data()
                user_member_3.generate_advanced_normal_user_data()

                TestCondition.create_advanced_normal_users(self._driver, [user_member_1, user_member_2, user_member_3])
                TestCondition.create_user_group(user_group, [user_member_1, user_member_2, user_member_3])

                # steps for icon view
                user_group_details_page = LoginPage(self._driver).open()\
                    .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                    .goto_users_tab()\
                    .goto_user_group_detail_page(user_group)

                # verify search works correctly
                self.assertTrue(user_group_details_page.check_search_user_work_correctly(user_member_1), "Assert Error: Search function works incorrectly")

                if self._driver.driverSetting.platform == Platform.WINDOWS or self._driver.driverSetting.platform == Platform.MAC:
                #TO DO: This is failed by INFR-2721
                # verify points Sort by
                    self.assertTrue(user_group_details_page.check_sort_by_work_correctly(), "Assertion Error: Sort function with icon view works incorrectly.")

                # steps for list view
                    user_group_details_list_view = user_group_details_page.switch_to_list_view()
                # verify points Sort table
                    self.assertTrue(user_group_details_list_view.check_table_users_can_sort(), "Assertion Error: Table is not sorted correctly.")

            finally:
                TestCondition.delete_advanced_users([user_member_1, user_member_2, user_member_3])
                TestCondition.delete_user_groups([user_group])

