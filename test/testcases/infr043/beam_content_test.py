from test.testbase import TestBase
from core.utilities.test_condition import TestCondition
from data_test.dataobjects.user import User
from common.helper import Helper
from pages.suitable_tech.user.login_page import LoginPage
from core.utilities.utilities import Utilities, Image_Utilities
from common.application_constants import ApplicationConst
from common.constant import Constant


class Beam_Content_0_43_Test(TestBase):
    
    def test_c33724_device_group_admin_is_able_to_view_and_change_the_Beam_Content(self):
        """
        @author: Thanh.Le
        @date: 05/03/2017
        @summary: Device group admin is able to view and change the Beam Content
        """
        try:
            # pre-condtion:
            img_file_name = "img2.jpg"
                         
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
            advance_device_group_admin = User()
            advance_device_group_admin.device_group = device_group_name
            advance_device_group_admin.generate_advanced_device_group_admin_data()
            TestCondition.create_advanced_device_group_admins(self._driver, [advance_device_group_admin])
            
            org_settings_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()
                          
            beam_content_dialog = org_settings_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            beam_content_dialog.choose_file(img_file_copied)
            beam_content_dialog.click_done()
            
            login_page = org_settings_page.logout().goto_login_page()
              
            # steps
            device_group_settings_page = login_page.login(advance_device_group_admin.email_address, advance_device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(device_group_name)
                
            beam_content_dialog = device_group_settings_page.open_beam_content_dialog()
            
            # verify point
            self.assertTrue(beam_content_dialog.is_image_displays(filecopied), 'Device group admin cannot view Beam Content.')
              
            beam_content_dialog.choose_beam_content_image(filecopied)
            
            # verify point
            self.assertTrue(device_group_settings_page.is_beam_content_image_display(5), "Beam Content Image does not display.")
        finally:
            TestCondition.delete_beam_content([filecopied])
            TestCondition.delete_device_groups([device_group_name])
            Utilities.delete_file(img_file_copied) 
    
    
    def test_c33726_verify_the_beam_content_available_for_advanced_orgs(self):
        """
        @author: Thanh.Le
        @date: 04/28/2017
        @summary: Beam Content available for advanced orgs
        @precondition: 
            Must have access to organization admin account
            Must be on server with "show_beam_content" waffle switch turned on.             
        @steps:
            1. Login to Beam Manager as an admin
            2. Go to Organization Settings tab
            3. See the Beam Content sub section and Manage Beam Content button at the bottom.
        @expected:
            The Manage Beam Content button is available.
            This should not show up if one is not logged in as an admin.
        """
        try:
            #precondition
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            normal_user.device_group = device_group_name
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            
            #steps
            account_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()          
                
            #verify point:
            self.assertTrue(account_setting_page.is_beam_content_section_displayed(), 
                            "Manager Content Beam section doesn't display on the Settings page.")   
            
            user_organization_setting_page = account_setting_page.goto_settings_tab_of_a_device_group(device_group_name)\
                .add_administrator(normal_user)\
                    .logout()\
                .goto_login_page()\
                    .login(normal_user.email_address, normal_user.password)\
                
            #verify point:
            self.assertFalse(user_organization_setting_page.is_organization_menu_displayed(5), "Organization menu still displays")
        finally:
            TestCondition.delete_device_groups([device_group_name])
            TestCondition.delete_advanced_users([normal_user])
            
            
    def test_c33727_verify_that_the_image_is_shown_in_the_list_of_Beam_Contents(self):
        """
        @author: Thanh.Le
        @date: 04/28/2017
        @summary: Beam Content can be uploaded
        @precondition: 
            Must have access to organization admin account
            Must be on server with "show_beam_content" waffle switch turned on.
            Must use an Advanced mode organization              
        @steps:
            1. Login in to the Beam Manager as an admin
            2. Go to the Organization Settings tab
            3. Click Manage Beam Content
            4. Click "Choose file.." button
            5. Select an image and upload.
        @expected:
            Verify that the image is shown in the list of Beam Contents.
        """
        try:
            # precondition
            img_file_name = "img2.jpg"     
           
            #steps
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()          
                
            #upload an image
            dialog_beam_content = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            dialog_beam_content.choose_file(img_file_copied)            
            
            #verify point
            self.assertTrue(dialog_beam_content.is_image_displays(filecopied), "Image does not display after uploading")
        finally:
            TestCondition.delete_beam_content([filecopied])
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)              
            except:
                pass  
               
   
    def test_c33728_verify_the_beam_content_image_was_removed(self):
        """
        @author: Thanh.Le
        @date: 04/28/2017
        @summary: Beam Content can be deleted
        @precondition: 
            Must have access to organization admin account
            Must be on server with "show_beam_content" waffle switch turned on.
            Must use an Advanced mode organization
            Must have Beam Content uploaded              
        @steps:
            1. Login in to the Beam Manager as an admin
            2. Go to the Organization Settings tab
            3. Click Manage Beam Content
            4. Click the trash icon next to an image
            5. Click Continue in the confirm modal
        @expected:
            Verify the Beam Content image was removed.
        """
        try:
            # precondition
            img_file_name = "img2.jpg"     
             
            #steps
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()          
                
            #upload an image
            dialog_beam_content = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            dialog_beam_content.choose_file(img_file_copied)                        
            dialog_beam_content.delete_image_beam_content(filecopied)
            
            #verify point
            self.assertFalse(dialog_beam_content.is_image_displays(filecopied, 5), "Image still displays after deleting")
        finally:            
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)                
            except:
                pass


    def test_c33729_deleting_beam_content_deletes_beam_content_usages_as_well (self):
        """
        @author: Thanh Le
        @date: 4/27/2017
        @summary: Deleting Beam Content deletes Beam Content usages as well
        @precondition: 
            - Must have access to organization admin account
            - Must be on server with "show_beam_content" waffle switch turned on.
            - Must use an Advanced mode organization
            - Must have Beam Content uploaded
         
        @steps:
            1. Login in to the Beam Manager as an admin
            2. Go to a Device Group's Setting page
            3. Click Set Beam Content button
            4. Select a Beam Content image and click Continue
            
            The Beam Content Image should display in the settings.
            
            5. Go to another Device Group's Setting page
            6. Click Set Beam Content button
            7. Click the Trash icon next to the current beam content for the previous device group.
            8. Click Continue from the confirm modal
            9. Close the Manage Beam Content modal
        @expected:
            The Confirm Delete Beam Content modal window should have mentioned the 1 use.
            The selected Device Group should no longer have Beam Content.
        """
        
        try:
            #pre-condtion:
            img_file_name = "img2.jpg"
                         
            device_group_name = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name)

            device_group_name_2 = Helper.generate_random_device_group_name()
            TestCondition.create_device_group(device_group_name_2)
             
            #steps
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(device_group_name)
                
            beam_content_dialog = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            beam_content_dialog.choose_file(img_file_copied)
            beam_content_dialog.choose_beam_content_image(filecopied)
           
            #verify point
            self.assertTrue(user_device_group_setting_page.is_beam_content_image_display(5), "Beam Content Image does not display.")
            
            beam_content_dialog = user_device_group_setting_page.goto_settings_tab_of_a_device_group(device_group_name_2)\
                                                            .open_beam_content_dialog()
                                                            
            actual_message = beam_content_dialog.click_delete_image_icon(filecopied).get_dialog_message()            
            expected_message = ApplicationConst.WARN_MSG_REMOVE_DEVICES_GROUP

            #verify point
            self.assertEqual(actual_message, expected_message, "Delete Beam Content modal window is not mentioned the 1 use")
            
            user_device_group_setting_page = beam_content_dialog.click_continue_button()\
                                            .goto_settings_tab_of_a_device_group(device_group_name)
            
            #verify point
            self.assertFalse(user_device_group_setting_page.is_beam_content_image_display(5), "Beam Content Image still displays.")
        finally:
            TestCondition.delete_device_groups([device_group_name])
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)
            except:
                pass


    def test_c33869_device_group_admin_is_able_to_remove_beam_content(self):
        """
        @author: Thanh Le
        @date: 9/21/2017
        @summary: Check if device group admin is able to remove beam content or not
        @precondition:
            - Create new device group and device group admin.
            - Upload some images for Beam Content.

        @steps:
            1. Login as device group admin
            2. Select device group
            3. Go to Settings tab
            4. Click Set Beam Content button
            5. Select a image and click Continue button
            6. Click Edit icon
            7. Click Remove Beam Content button
        @expected:
            (7) Beam Content image is removed.
        """

        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = new_device_group_name

            #pre-condtion:
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            img_file_name = "img2.jpg"
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)

            beam_content_dialog = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            beam_content_dialog.choose_file(img_file_copied).click_cancel_button().logout()

            #steps
            admin_beam_setting_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address,device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)\
                .open_beam_content_dialog()\
                .choose_beam_content_image(filecopied)\
                .remove_beam_content_image()
            
            self.assertTrue(admin_beam_setting_page.is_beam_content_image_removed(),"Beam Content image still displays")
        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_beam_content([filecopied])
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)
            except:
                pass


    def test_c33870_device_group_admin_is_able_to_change_beam_content_image(self):
        """
        @author: Thanh Le
        @date: 9/22/2017
        @summary: Check if device group admin is able to change beam content image or not
        @precondition:
            - Create new device group and device group admin.
            - Upload some images for Beam Content.

        @steps:
            1. Login as device group admin
            2. Select device group
            3. Go to Settings tab
            4. Click Set Beam Content button
            5. Select a image and click Continue button
            6. Click Edit icon
            7. Click change image link
            8. Select another image and click Continue
            9. Click Save button
        @expected:
            (9) Beam Content image is changed.
        """

        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = new_device_group_name

            #pre-condtion:
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            img_file_name = "img2.jpg"
            img_file_name_2 = "img_large.jpg"
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)

            beam_content_dialog = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)

            img_file_2 = Utilities.get_test_image_file_path(self._driver, img_file_name_2)
            filecopied_2 = Utilities.copy_and_rename_file(self._driver, img_file_2)
            img_file_copied_2 = Utilities.get_test_image_file_path(self._driver, filecopied_2)

            beam_content_dialog.choose_file(img_file_copied)\
                .choose_file(img_file_copied_2)\
                .click_cancel_button()\
                .logout()

            #steps
            admin_beam_setting_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address,device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)\
                .open_beam_content_dialog()\
                .choose_beam_content_image(filecopied)

            old_image_url = admin_beam_setting_page.get_beam_content_icon_link()
            old_image = Utilities.download_file(self._driver, old_image_url)

            admin_beam_setting_page.update_beam_content(new_image_name=filecopied_2)
            new_image_url = admin_beam_setting_page.get_beam_content_icon_link()
            new_image = Utilities.download_file(self._driver, new_image_url)

            are_equal = Image_Utilities.are_images_similar(old_image, new_image)
            self.assertFalse(are_equal, "Assertion Error: Beam Content image is not changed")
        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_beam_content([filecopied])
            TestCondition.delete_beam_content([filecopied_2])
            Utilities.delete_file(old_image)
            Utilities.delete_file(new_image)
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)
                if img_file_copied_2:
                    Utilities.delete_file(img_file_copied_2)
            except:
                pass


    def test_c33871_device_group_admin_is_able_to_update_schedule_for_beam_content(self):
        """
        @author: Thanh Le
        @date: 9/25/2017
        @summary: Check if device group admin is able to update schedule for beam content or not
        @precondition:
            - Create new device group and device group admin.
            - Upload some images for Beam Content.

        @steps:
            1. Login as device group admin
            2. Select device group
            3. Go to Settings tab
            4. Click Set Beam Content button
            5. Select a image and click Continue button
            6. Click Edit icon
            7. Update schedule
            8. Click Save button
        @expected:
            (8) Schedule is updated.
        """

        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = new_device_group_name

            #pre-condtion:
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            img_file_name = "img2.jpg"
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)

            beam_content_dialog = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)
            beam_content_dialog.choose_file(img_file_copied).click_cancel_button().logout()

            #steps
            admin_beam_setting_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address,device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)\
                .open_beam_content_dialog()\
                .choose_beam_content_image(filecopied)

            display_days = "monday,tuesday,thursday"
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)
            admin_beam_setting_page.update_beam_content(display_days, starting_datetime, ending_datetime)

            self.assertTrue(admin_beam_setting_page.is_beam_content_days_updated(display_days),"Beam content day is not updated")
            self.assertTrue(admin_beam_setting_page.is_beam_content_time_updated(starting_datetime, ending_datetime),"Beam content time is not updated")
        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_beam_content([filecopied])
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)
            except:
                pass


    def test_c33872_data_isnt_saved_if_clicking_on_cancel_button_after_changing_schedule(self):
        """
        @author: Thanh Le
        @date: 9/25/2017
        @summary: Check if data isn't saved after clicking cancel button
        @precondition:
            - Create new device group and device group admin.
            - Upload some images for Beam Content.

        @steps:
            1. Login as device group admin
            2. Select device group
            3. Go to Settings tab
            4. Click Set Beam Content button
            5. Select a image and click Continue button
            6. Click Edit icon
            7. Update schedule
            8. Click Cancel button
        @expected:
            (8) Data isn't saved.
        """

        try:
            new_device_group_name = Helper.generate_random_device_group_name()
            device_group_admin = User()
            device_group_admin.generate_advanced_device_group_admin_data()
            device_group_admin.device_group = new_device_group_name

            #pre-condition:
            TestCondition.create_device_group(new_device_group_name)
            TestCondition.create_advanced_device_group_admins(self._driver, [device_group_admin])

            img_file_name = "img2.jpg"
            user_device_group_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)

            beam_content_dialog = user_device_group_setting_page.open_beam_content_dialog()
            img_file = Utilities.get_test_image_file_path(self._driver, img_file_name)
            filecopied = Utilities.copy_and_rename_file(self._driver, img_file)
            img_file_copied = Utilities.get_test_image_file_path(self._driver, filecopied)

            beam_content_dialog.choose_file(img_file_copied)\
                .click_cancel_button()\
                .logout()

            #steps
            admin_beam_setting_page = LoginPage(self._driver).open()\
                .login(device_group_admin.email_address,device_group_admin.password)\
                .goto_settings_tab_of_a_device_group(new_device_group_name)\
                .open_beam_content_dialog()\
                .choose_beam_content_image(filecopied)

            old_image_url = admin_beam_setting_page.get_beam_content_icon_link()
            old_image = Utilities.download_file(self._driver, old_image_url)

            display_days = "monday,tuesday,thursday"
            starting_datetime = Helper.generate_date_time(hour_delta=9)
            ending_datetime = Helper.generate_date_time(hour_delta=15, minute_delta=30)

            admin_beam_setting_page.update_beam_content(display_days, starting_datetime, ending_datetime, cancel=True)

            new_image_url = admin_beam_setting_page.get_beam_content_icon_link()
            new_image = Utilities.download_file(self._driver, new_image_url)

            are_equal = Image_Utilities.are_images_similar(old_image, new_image)
            self.assertTrue(are_equal, "Assertion Error: Beam Content image is changed")
            self.assertTrue(admin_beam_setting_page.is_beam_content_days_default_value(),"Beam content day is updated")
            self.assertFalse(admin_beam_setting_page.is_beam_content_time_updated(starting_datetime, ending_datetime),"Beam content time is updated")
        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([device_group_admin])
            TestCondition.delete_beam_content([filecopied])
            Utilities.delete_file(old_image)
            Utilities.delete_file(new_image)
            try:
                if img_file_copied:
                    Utilities.delete_file(img_file_copied)
            except:
                pass

