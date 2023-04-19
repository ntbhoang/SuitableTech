from test.testbase import TestBase
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from common.helper import Helper
from core.utilities.utilities import CSV_Utilities, Utilities
from common.constant import Constant, Language
from common.application_constants import ApplicationConst
from common.email_detail_constants import EmailDetailConstants
from core.utilities.gmail_utility import GmailUtility
from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
from pages.suitable_tech.user.login_page import LoginPage
    
class logigear_Web_Automation_Testing_Bugs_Test(TestBase):
        
    def test_c33156_verify_that_it_is_unable_to_add_existing_admin_to_device_group_administrators_again(self):
        """
        @author: Thanh.Le
        @date: 03/06/2017
        @summary: BUG_02: It is able to add existing admin to Device Group Administrators again.
        @steps:
            1. Login to https://staging.suitabletech.com/ with admin account
            2. Go to Dashboard page
            3. Select Beams -> Settings page of a device group
            4. Click button "Add administrators"
            5. Type an existing administrator account of this group
            
        @expected:          
            (5) The already added as admin user does not exist in "Available Users" list
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
                
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group_name
                
            TestCondition.create_device_group(device_group_admin.device_group)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
                
            # steps 
            added_admin_exist = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_beams_tab()\
                .select_device_group(device_group_name)\
                .goto_setting_tab()\
                .click_add_administrators_button()\
                .is_administrator_exists_in_available(device_group_admin)

            # verify point:
            self.assertFalse(added_admin_exist, "Assertion Error: The already added as admin user exist in \"Available Users\" list")
              
        finally:
            # post-condition       
            TestCondition.delete_device_groups([device_group_name])
                                
                                
    def test_c33157_verify_that_sign_out_page_displays_after_user_logs_out(self):
        """
        @author: Thanh.Le
        @date: 03/06/2017
        @summary: BUG_11: The Sign Out page is missing.
        @steps:
            1. Login to Suitabletech as the Advanced Admin (logigear1+advancedadmin@suitabletech.com /Logigear123) 
            2. Log out from the HomePage
            3. Login to Suitabletech as the Advanced Admin (logigear1+advancedadmin@suitabletech.com /Logigear123) again
            4. Go to dashboard page then log out
            
        @expected:          
            Sign Out page should display
        """
        try:
            # pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
                
            # steps
            signout_complete_page = LoginPage(self._driver).open()\
            .login(normal_user.email_address, normal_user.password)\
            .logout()
                    
            # verify point:    
            self.assertTrue(signout_complete_page.is_page_displayed(), "Assertion Error: The sign Out page doesn't display")
                
        finally:
            # post-condition       
            TestCondition.delete_advanced_users([normal_user])
    
    
    def test_c33207_Verify_that_user_can_delete_device_label(self):
        """
        @author: Thanh.Le
        @date: 03/06/2017
        @summary: BUG_12: The "Labels" textbox in Edit Device form works incorrectly.
                    When clicking 'x' button for deleting a label, we cannot save device info anymore.
    
        @precondition:
            There is a device (Beam) added with 2 labels (label1, label2)
            
        @steps:
            1. Login to Suitabletech as the org admin and select "Manage your Beams" to go to dashboard
            2. Go to "Beams" tab and select a device (Logigear Mock Beam+) and click "Edit" button
            3. Click 'x' button on 'label2'
            4. Click "Save Changes" button
            
        @expected:          
            The 'label2' should be remove successfully
        """
        try:
            # pre-condition
            device_group_name = Helper.generate_random_device_group_name()
            label1 = Helper.generate_random_string()   
            label2 = Helper.generate_random_string()   
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
                
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = device_group_name
                          
            TestCondition.create_device_group(device_group_name, device_array=[beam_name])
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
                
            beam_detail_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab()\
                .select_a_device(beam_name)
                    
            old_label_tag_list = beam_detail_page.get_beam_label_tag_list()
            beam_detail_page.set_beam_label_tag_list([label1, label2])
                
            # steps
            beam_detail_page.remove_beam_label(label2)
                
            # verify point:    
            self.assertFalse(beam_detail_page.is_beam_label_existed(label2), \
                            "Assertion Error: Failed to remove the label from device %s" % (beam_name))
                
        finally:
            # restore the previous value
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([admin_user])
            TestCondition.restore_advanced_beam_labels(beam, old_label_tag_list)
    
    
    def test_c33208_success_message_displays_when_changing_device_group(self):
        """
        @author: Thanh.Le
        @date: 03/06/2017
        @summary: Verify that there is one success message displays when changing device group in "Edit Device" successfully
        @desciption: BUG_15 There are two messages "The device was saved successfully." display when changing device group in "Edit Device" form then saving
        @steps:
            1. Login to Suitabletech as the org admin and select "Manage your Beams" to go to dashboard
            2. Go to "Beams" tab and select a device 
            3. Click "Edit" button and select a device group in "Group" textbox
            4. Click "Save Changes" button
             
        @expected:          
            There should be a message "The device was saved successfully." displays
        """
        try:
                
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            beam_name = beam.beam_name
    
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
                
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
                
            # steps
            admin_beam_details_page = LoginPage(self._driver)\
                .open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()\
                .select_a_device(beam_name)\
                .set_beam_group(device_group_name,False)
                    
            # verify point:    
            self.assertTrue(admin_beam_details_page.is_success_msg_displayed(), "The success message doesn't displays") 
                
        finally:
            # restore the previous value
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([org_admin])
   
    def test_c33210_the_success_message_displays_if_importing_valid_CSV_file_after_valid_CSV_file(self):
        """
        @author: Thanh.Le
        @date: 03/07/2017
        @summary: Bug24: Verify that only the success message displays if importing valid CSV file after valid CSV file 
        @desciption: The import contact error still displays with the import successful message.
        @precondition: 
            1. Create a correct import user CSV file "users.csv"
               
        @steps:
            1. Login to Suitabletech site with an org admin and select "Manage Your Beams" in drop-down list
            2. Select "Import Users" button
            3. On "Import Users" form, browse to the invalid file (maybe the image file)
            4. Select "Import Users" button again and browse to the valid CSV file in pre-condition
            5. Confirm on "Import Users" form to finish
             
        @expected:          
            - The success message displays and the error message disappears after importing correct users
        """
        try:
            # pre-consition
            org_admin = User()
            org_admin.advanced_org_admin_data()
              
            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group)
              
            user_group = Helper.generate_random_user_group_name()
            TestCondition.create_user_group(user_group)
              
            csv_file = CSV_Utilities.generate_users_in_csv('test_c33210.csv', 2)
            image_file_path = Utilities.get_test_image_file_path(self._driver, "img_small.png")
            
            # steps
            admin_dashboard_page = LoginPage(self._driver)\
                .open()\
                .login(org_admin.email_address, org_admin.password)\
            
            admin_dashboard_page.import_users_expecting_error(image_file_path)
                
            # verify point:
            self.assertTrue(admin_dashboard_page.is_error_msg_displayed(False), "the error message does not appears after importing incorrect users")
            
            admin_dashboard_page.import_users(csv_file, device_group, user_group, False, True)

            # verify point:
            self.assertTrue(admin_dashboard_page.is_success_msg_displayed(), "the success message disappears after importing incorrect users")
            self.assertFalse(admin_dashboard_page.is_error_msg_displayed(), "the error message appears after importing correct users")
               
        finally:
            all_users = CSV_Utilities.find_all_users_in_csv(csv_file)
            users_to_be_deleted = []
            for email in all_users:
                user = User()
                user.email_address = email
                user.organization = org_admin.organization
                users_to_be_deleted.append(user)
                  
            TestCondition.delete_advanced_users(users_to_be_deleted)
            TestCondition.delete_user_groups([user_group])
            TestCondition.delete_device_groups([device_group])
              
           
    def test_c33217_User_can_deselect_user_long_email_address(self):
        """
        @author: Thanh.Le
        @date: 03/08/2017
        @desciption:
            BUG_33 It is unable to deselect a user with a long email address on "Choose Users" form.
        @precondition: 
            1. Created a user with long email address (logigear1+advancedmultiorg@suitabletech.com)
            2. Create a user group (Default LGVN Users Group)
               
        @steps:
            1. Login to Suitabletech.com as an org admin and select "Manage Your Beams" on drop-down list to go dashboard page
            2. Go to "Users" tab and select a user group (Default LGVN Users Group)
            3. Click "Add Users" button
            4. Search for "Multi Org Advanced Admin" and click this user to push it into "Selected Users"
             
        @expected:          
            (4) The 'x' button should display for deselecting user
        """
          
        try:
            # pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
              
            user_group = Helper.generate_random_user_group_name()
            TestCondition.create_user_group(user_group)
              
            # steps
            choose_user_dialog = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_users_tab()\
                .goto_user_group_detail_page(user_group)\
                .open_add_user_dialog()\
                .select_user(normal_user.email_address)
                  
            # verify point:
            self.assertTrue(choose_user_dialog.is_remove_user_button_displayed(normal_user), "The 'x' button dooesn't display for deselecting user")
              
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_user_groups([user_group])
          

    def test_c33219_only_email_address_disyplay_on_request_nofitication_dasboard_if_request_access_beam_without_first_and_last_name(self):
        """
        @author: Thanh.Le
        @date: 03/08/2017
        @desciption:
            BUG_36 Blank name should display as email address on Dashboard > Notification tab if user requests access to Beam without entering First and Last name.
               
        @steps:
            1. Login to Suitabletech with an org admin and create a DeviceGroup (LGVN Liger Device Group)
            2. Go to Setttings tab of this device group and copy the URL under "Access Request" section (https://staging.suitabletech.com/r/CFUP7B/)
            3. Paste this URL to a browser window
            4. Enter email address and leave the First name and Last name blank
            5. Click 'Send' button
            6. Go to Dashboard page again
             
        @expected:          
            (6). It should display as "lgvn_advanced_jp_user01@mailinator.com requests to be added to group "LGVN Liger Device Group"
        """        
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group)
              
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.first_name = None
            normal_user.last_name = None
            normal_user.device_group = device_group
              
            # steps
            setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group)
              
            link_request = setting_page.toggle_request_access_notification()\
                .select_Dispplay_url_connect_invitation()\
                .get_link_access_request()
            request_access_page = setting_page.goto_request_access_page(link_request)
            request_access_page.send_request_beam_access(normal_user)
            admin_dashboard_page = AdminDashboardPage(self._driver).open()
              
            # verify point:
            self.assertTrue(admin_dashboard_page.is_access_request_displayed(normal_user), " Access request doesn't display when request without username")
        finally:
            TestCondition.delete_device_groups([device_group])
  
  
    def test_c33221_the_success_message_displays_when_editing_or_deleting_a_temporary_user_access_time(self):
        """
        @author: Thanh.Le
        @date: 03/08/2017
        @desciption:
            BUG_41 The error message "There was an error with your request. Please try again later." displays when editing or deleting a temporary user access time.
  
        @precondition: 
            Create a device group 'w Liger Device Group '
               
        @steps:
            1. Login to Suitabletech with an org admin (logigear1+advancedadmin@suitabletech.com/ Logigear123) and select "Manage Your Beams" to go to Dashboard page
            2. Select the device group in pre-condition and go to Access time tab
            3. Click "Invite a Temporary User" button
            4. Fill out the "Invite a Temporary User" form (Email: logigear1+temporaryuser.test070903@suitabletech.com) and click "Invite" button
            5. Click on the name of temporary user has just been created
            6. Edit Stating/ Ending time and click "Invite" button
             
        @expected:          
            (6). The error message don't display
        """      
        from core.i18n.i18n_support import I18NSupport  
        import re
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group)

            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
              
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)  
              
            tomorrow =  Helper.generate_access_day()
              
            new_starting_datetime = Helper.generate_date_time(hour_delta=7)
            new_ending_datetime = Helper.generate_date_time(hour_delta=16, minute_delta=30) 
              
            # steps
            access_time = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_access_times_tab_of_a_device_group(device_group)\
                .invite_temporary_user(normal_user, starting_datetime, ending_datetime, True, True)\
                  
            date_label = I18NSupport.localize_date_time_string( re.sub(' +',' ',tomorrow.strftime('%b %e, %Y')) )
            access_time_label = Utilities.generate_temporary_access_time_label(date_label, starting_datetime, ending_datetime)
            access_time.edit_temporary_access_times(normal_user, access_time_label, new_starting_datetime, new_ending_datetime, True, True)
              
            # verify point
            self.assertFalse(access_time.is_error_msg_displayed(), "The error message displays")
              
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_device_groups([device_group])
             
             
    def test_c33224_copy_to_clipboard_button_at_setting_tab_in_device_group_work_correctly(self):
        """
        @author: Thanh.Le
        @date: 03/09/2017
        @desciption:
            BUG_58 Fail to copy to clipboard access request url in Device Group setting page
  
        @precondition: 
            Create a device group 'w Liger Device Group '
               
        @steps:
            1. Login to Suitabletech with an Advanced Org Admin (thanh.viet.le@logigear/Logigear123) 
            2. Go to Dashboard page by clicking on 'Manage Your Beams' button
            3. Go to 'Beams' page
            4. Select any device group and select 'Settings' tab
            5. Click on 'Copy to Clipboard' button in 'Access Requests'
            6. Paste to the text editor (Notepad or TextEdit)
             
        @expected:          
            (6). Copy to Clipboard function should work correctly
        """ 
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group)
             
            admin_beam_setting = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group)\
                 
            access_request = admin_beam_setting.get_link_access_request()
            admin_beam_setting.select_Dispplay_url_connect_invitation()\
                .click_copy_to_clipboard_button()
             
            access_request_cp = admin_beam_setting.get_clip_board_value()
             
            self.assertEqual(access_request, access_request_cp, "Copy to Clipboard function doesn't work correctly")
             
        finally:
            TestCondition.delete_device_groups([device_group])
             
         
    def test_c33225_add_device_button_does_not_when_searching_with_non_existing_device_group(self):
        """
        @author: Thanh.Le
        @date: 03/09/2017
        @desciption:
            BUG_30 The 'Add Devices' button displays when searching a non-existing device group 
            if login with device group admin of a long name device group
  
        @precondition: 
            Create a device group 'w Liger Device Group '
               
        @steps:
            1. Use org admin to create a new device group (Tham Nguyen Device Group) 
                and do not add any Beam device to it
                 
            2. Creat a new device group admin is admin of the above group
                logigear1+devicegroupadminuser300801@suitabletech.com/ P@ssword
                 
            3. Login with this device group admin
             
            4. Go to Beams tab and search for non-existing device group
             
        @expected:          
            (2). The "Add Devices" button should be removed.
        """
        try:
            # pre-condition
            device_group = Helper.generate_random_device_group_name(25)
            TestCondition.create_device_group(device_group)
             
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = device_group
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])
             
            # steps
            admin_beam_device_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address, device_group_admin.password)\
                .goto_beams_tab()\
                .search("non-existing device group")
             
            # verify point
            self.assertFalse(admin_beam_device_page.is_add_devices_button_display(), "The 'Add Devices' button display")    
 
        finally:
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_device_groups([device_group])
             
             
    def test_c33227_verify_that_html_tags_does_not_display_on_activity_page(self):
        """
        @author: Thanh.Le
        @date: 03/13/2017
        @desciption:
            BUG_59 HTML tags show on summary content of Activity page when updating language to Japanese
  
        @precondition: 
            Create a device group 'w Liger Device Group '
               
        @steps:
            1. Login to Suitabletech with an Advanced Org Admin 
            2. Go to Account Settings and set Japanese language
            3. Go to Actitiy page (https://stg1.suitabletech.com/manage/#/activity/)
            4. Observe summary table
             
            Note: This bug only happens when setting language to Japanese.
        @expected:          
            HTML tag should not display
        """
        try:
            # steps
            activity_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_your_account()\
                .set_language(Language.JAPANESE)\
                .goto_activity_tab()
                
            # verify point
            self.assertFalse(self.is_html_tag_in_string(activity_page.get_summary_text()), "HTML tag display in summary")
            
        finally:
            pass


    def test_c33226_verify_that_error_message_displays_if_a_user_changes_device_group_image_after_another_user_deleted_this_device_group(self):
        """
        @author: Thanh.Le
        @date: 03/07/2017
        @summary: Verify that Error message "There was an error with your request. Please try again later." displays if a user changes device group image after another user deleted this device group 
        @precondition: Create a device group "Test Device Group 1"
        @steps:
            1. User A and user B login to Suitabletech with an Advanced Org Admin in different browser or machine
            2. User A and user B go to Setting tab of the device group "Test Device Group 1"
            3. User B deletes the device group "Test Device Group 1" 
            4. Wait for the delete completely.
            5. User A changes image of the device group "Test Device Group 1" 
            6. Note the error message
        @expected:
            Error message "There was an error with your request. Please try again later." displays
        
        @note: Ready to automate
        """
        
        try:
            # pre-condition 
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
              
            # steps
            settings_device_group_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group_name)
            
            #step 3: User B deletes the device group "Test Device Group 1"
            TestCondition.delete_device_groups([device_group_name])
            
            image_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
            upload_image_dialog = settings_device_group_page.open_upload_image_dialog().choose_file(image_path)

            # verify
            self.assertEqual(settings_device_group_page.get_error_message(), ApplicationConst.LBL_DELETE_ERROR_MESSAGE, 
                             "Assertion Error: Expected message is not displayed")
            
            upload_image_dialog.cancel()
        finally:
            pass

            
    def test_c33220_verify_that_default_invite_message_displays_correctly_on_welcome_invite_emails(self):
        """
        @author: Thanh.Le
        @date: 03/09/2017
        @summary: Verify that default invite message displays correctly on Welcome/Invite emails 
        @desciption: BUG_69 The default invite message does not display on Welcome/Invite emails
        @steps:
            1. Login to Suitabletech https://stg1.suitabletech.com with org admin user 
            (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Manage Dashboard > Organization > Settings and set "Hello" for Default Invite Message
            3. Go to Manage Dashboard and click on "Invite A New User" button 
            4. Fill all info (e.g. suitabletech3+userJan0112017LgvnTest@gmail.com)
            5. Turn on checkbox "Include the default invitation message" and click on "Invite" button 
            6. Open mailbox of invited user (suitabletech3@gmail.com) and check the content of Welcome email
        @expected:
            The the default invitation message should display on UI welcome/invite emails when turning on checkbox "Include the default invitation message".
        
        @note: Ready to automate
        """
        
        try:
            # pre-condition 
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.invitation_settings.include_the_default_invitation_message = True
            
            device_group_name = Helper.generate_random_device_group_name(5)
            TestCondition.create_device_group(device_group_name)
            
            temporary_user = User()
            temporary_user.generate_advanced_normal_user_data()
            temporary_user.device_group = device_group_name
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)
            
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
            
            # steps
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_org_setting_page().set_default_invite_message(Constant.DefaultMessage)\
                .goto_dashboard_tab().invite_new_user(normal_user)

            actual_emails = GmailUtility.get_messages(EmailDetailConstants.WelcomeEmailTitle.format(normal_user.organization), receiver=normal_user.email_address)
            
            # verify
            self.assertEqual(Constant.DefaultMessage, actual_emails[0]._text_content.splitlines()[5],
                             "Assertion Error: The default invite message display incorrectly {} in welcome email".format(actual_emails[0]._text_content.splitlines()[5]))
            
            admin_dashboard_page.invite_temporary_user(temporary_user, start_date=starting_datetime, end_date=ending_datetime, default_invitation=True, device_group=device_group_name)
            temporary_emails = GmailUtility.get_messages(EmailDetailConstants.WelcomeTemporaryUserEmailTitle.format(temporary_user.organization), receiver=temporary_user.email_address)
            
            # verify
            self.assertEqual(Constant.DefaultMessage, temporary_emails[0]._text_content.splitlines()[5],
                             "Assertion Error: The default invite message display incorrectly {} in welcome temporary email".format(actual_emails[0]._text_content.splitlines()[5]))
        finally:
            # post-condition
            TestCondition.delete_advanced_users([org_admin, normal_user, temporary_user])
            TestCondition.delete_device_groups([device_group_name])
            

    def test_c33223_verify_that_the_offline_and_available_text_at_status_device_is_localized(self):
        """
        @author: Thanh.Le
        @date: 03/10/2017
        @summary: Verify that the 'Offline' and 'Available' text at status device is localized to Japanese and Français in Manage Beams page 
        @desciption: BUG_60 The 'Offline' text at status device is not localized to Japanese and Français in Manage Beams page
        @steps:
            1. Login to Suitabletech with an Advanced Org Admin 
            2. Go to Account Settings and set Japanese/Français language
            3. Go to Manage Beams page
            4. Note status text in devices thumbnail
        @expected:
            (4) 'Offline' and 'Available' text are localized to Japanese and Français.
        
        @note: Ready to automate
        """
        try:
            # pre-condition 
            org_admin = User()
            org_admin.advanced_org_admin_data()
              
            # steps
            manage_beams_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_beams_tab()

            # verify
            self.assertTrue(manage_beams_page.are_offline_available_text_localized(),
                             "Assertion Error:  Offline/Available text is not localized to " + self._driver._driverSetting.language)
        finally:
            # post-condition
            pass
            
    def test_c33780_verify_that_simplified_org_admin_can_remove_a_normal_user_at_user_details_page(self):
        """
        @author: Thanh.Le
        @date: 05/16/2017
        @summary: Verify that Simplified Org Admin can remove a normal user at user details page.
        @desciption: BUG_100 Org Admin is unable to remove a normal user in Simplified Organization at user details page.
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as Simplified Organization Admin
            (thanh.viet.le@logigear.com/L0gigear123!)
            2. Go to Simplified Organization (LogiGear Test 2)
            3. Select a beam
            4. Click any user in "People with access to this Beam" list (thanh.viet.le@logigear.com) to view the user details page
            5. Click "Delete This User" button 
            6. Confirm delete
        @expected:
            - Success message should display.
            - The user should be removed from the Simplified Organization.
        
        @note: Ready to automate
        """
        try:
            # pre-condition 
            test_organization=Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            
            simplified_user = User()
            simplified_user.generate_simplified_normal_user_data()
            TestCondition.create_simplified_normal_users(self._driver, [simplified_user], beam, False)
            
            # steps
            simplified_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                .goto_manage_beam_page(beam.beam_id)\
                .goto_simplified_user_detail_page(simplified_user).remove_this_user()

            # verify
            self.assertEqual(simplified_dashboard_page.get_msg_success(), ApplicationConst.INFO_MSG_REMOVE_USER_FROM_ORG_SUCCESSFUL,
                             "Assertion Error: The success message does not display or localize")
            
            is_user_deleted = simplified_dashboard_page.goto_manage_beam_page(beam.beam_id).is_user_not_existed(simplified_user)
            self.assertTrue(is_user_deleted, "Assertion Error: The user {} is not delete successfully".format(simplified_user.email_address))            

        finally:
            # post-condition
            pass

    def test_c33782_verify_that_unlink_this_device_button_displays_on_edit_device_modal_when_logging_in_by_simplified_org_admin(self):
        """
        @author: Thanh.Le
        @date: 05/17/2017
        @summary: Verify that 'Unlink This Device' button displays on Edit Device modal when logging in by Simplified Organization Admin.
        @desciption: BUG_119 Missing 'Unlink This Device' button on Edit Device modal when logging in by Simplified Organization Admin.
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com 
            (thanh.viet.le@logigear.com/L0gigear123!)
            2. Select the Logigear Test 2 orginazition
            3. Click 'Manage' button of any Beams
            4. Click Edit Details button
        @expected:
            (4) The 'Unlink This Device' button should be displayed.
        
        @note: Ready to automate
        """
        try:
            # pre-condition 
            test_organization = Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            
            # steps
            simplified_beam_detail_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                .goto_manage_beam_page(beam.beam_id)

            # verify
            self.assertTrue(simplified_beam_detail_page.is_unlink_device_button_displayed(), "The 'Unlink This Device' button does not displayed.")         

        finally:
            # post-condition
            pass

    def test_c33209_verify_that_the_simplified_admin_cannot_access_and_manage_the_device_after_it_is_removed(self):
        """
        @author: Quang Tran
        @date: 01/18/2018
        @summary: Verify that the Simplified Admin cannot access and manage the device after it is removed
        @steps:
            1.Login to Suitabletech as a Simplified Org Admin (logigear1+simpleadmin@suitabletech.com/ Logigear123)
            2.Enter email address (logigear1+bug18@suitabletech.com) and click "Add User" button next to "Logigear Mock Beam+2" device
            3.Click on "Manage" button on device and select "Can manage" checkbox for the newly created user (logigear1+bug18@suitabletech.com)
            4.Go to mailbox and activate the invited user and observe that this user is now manage for "Logigear Mock Beam+2" device then logout 4 . Login to Suitabletech as a Simplified Org Admin (logigear1+simpleadmin@suitabletech.com/ Logigear123) and select "Manage Your Beams" in drop-down list to go "Manage Your Beams" page again
            5.Select "Manage" button on "Logigear Mock Beam+2" device then uncheck "Can manage" for (logigear1+bug18@suitabletech.com)
            6.Login again with (logigear1+bug18@suitabletech.com)
        @expected:
            (6) The"Manage Your Beam" does not display in drop-down list and no device added.
        
        @note: Ready to automate
        """
        try:
            #precondition
            beam = TestCondition.get_a_beam(org=Constant.SimplifiedOrgName)
            beam_name = beam.beam_name

            normal_user = User()
            normal_user.generate_simplified_normal_user_data()

            #steps
            beam_detail_page = LoginPage(self._driver).open()\
                    .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                    .add_user(normal_user, beam_name)\
                    .goto_manage_beam_page(beam.beam_id)\
                    .set_user_can_manage(normal_user)

            TestCondition._activate_user_temporary_password(self._driver, normal_user, pass_safety_video=True, localize=True)

            beam_detail_page = beam_detail_page.logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)

            #verify point
            self.assertTrue(beam_detail_page.can_manage_device(beam.beam_id), "User {} can not manage beam {}".format(normal_user.get_displayed_name(simplified=True), beam_name))

            beam_detail_page = beam_detail_page.logout_and_login_again(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, loginAgainAsNormalUser=True)\
                    .goto_manage_beam_page(beam.beam_id)\
                    .set_user_can_manage(normal_user, False)

            beam_detail_page = beam_detail_page.logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)

            #verify point
            self.assertFalse(beam_detail_page.can_manage_device(beam.beam_id), "User {} can manage beam {}".format(normal_user.get_displayed_name(simplified=True), beam_name))
        finally:
            #postcondition
            TestCondition.delete_simplified_users([normal_user])

