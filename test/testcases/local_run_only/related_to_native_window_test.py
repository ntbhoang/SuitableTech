from common.application_constants import ApplicationConst
from common.constant import Constant, Platform
from common.helper import Helper
from core.utilities.utilities import Utilities, Image_Utilities, CSV_Utilities
from data_test.dataobjects.user import User
from core.utilities.test_condition import TestCondition
from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
import pytest


class RelatedToNativeWindow_Test(TestBase):
    
    def _compare_value_two_array(self, arr1, arr2):
        return sorted(arr1) == sorted(arr2)
    
    
    def test_c11599_change_device_icon(self):
        """
        @author: Quang.Tran
        @date: 8/19/2016
        @summary: Change device icon
        @precondition: 
            Login as the Device Group Admin
          
        @steps:
            1) go to the "Manage your Beams" dashboard and click on the "Beams" tab
            2) click on a device in the "Devices" section
            3) Hover your mouse over the pencil in the image icon; you should see a "Change image..." message
            4) Choose file to upload and save it
        @expected:
            Icon should be replaced with newly selected Icon
            Note:
                --> Test different file formats for pictures (e.g. png, jpg, gif?)
                -->Try different file sizes:
                i. small (2kbytes)
                ii. Med (500kbytes)
                iii. Large (10000kbytes)
                iv. Corrupt File
        """
        try:
            # pre-condition
            new_device_group_name = Helper.generate_random_device_group_name()
            corrupted_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_corrupt.jpg")
            small_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_small.png")
            medium_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_med.jpg")
            large_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_large.jpg")
            gif_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_gif.gif")

            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            device_name = beam.beam_name
            device_list = [device_name]

            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name

            TestCondition.create_device_group(admin_user.device_group, device_list)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])

            # steps
            admin_beams_detail_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab().select_a_device(device_name)

            # 1. corrupt file
            admin_beams_detail_page.remove_image_icon()

            dialog = admin_beams_detail_page.open_upload_image_dialog()
            dialog.choose_file(corrupted_image_file_path)
            self.assertFalse(dialog.is_crop_tracker_displayed(), "Assertion Error: The crop-tracker is displayed on corrupted image.")
            dialog.cancel()

            # 2. small image
            admin_beams_detail_page.set_image_icon(small_image_file_path)
            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_small_moving.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with small image (<10kbytes)!")

            # 3. medium image
            admin_beams_detail_page.change_image_icon(medium_image_file_path)

            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_med_moving.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with medium image (~500kbytes)!")

            # 4. large image
            admin_beams_detail_page.change_image_icon(large_image_file_path)

            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_large_moving.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with medium image (~10000kbytes)!")

            #5. gif image
            admin_beams_detail_page.change_image_icon(gif_image_file_path)

            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_actual = Image_Utilities.convert_png_to_jpg(img_actual)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_gif_moving.jpg", True)

            are_equal = Image_Utilities.are_images_similar(img_expected, img_actual)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with gif image!")
            admin_beams_detail_page.remove_image_icon()
 
        finally:
            # post-condition
            TestCondition.release_a_beam(beam)
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])
  
  
    def test_c11655_change_device_icon(self):
        """
        @author: Duy.Nguyen
        @date: 7/29/2016
        @summary: Change Device Icon 
        @precondition: 
        Login as device admin in the simplified "Manage your Beams" 
        @steps:        
            1) Select the "Manage" box under the desired device image icon
            2) Click on the grey pencil icon in the device image box --> "Change image..."
            3) Upload file and then save changes
              
        @expected:
            Verify that the icon is replaced with the new icon    
        """
        try:
            #pre-condition
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
              
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
                      
            # steps:
            manage_page = LoginPage(self._driver).open()\
                    .login(simplified_dev_admin.email_address, simplified_dev_admin.password, True)\
                    .goto_manage_beam_page(beam.beam_id).change_image_icon(file_path)   
              
            # verify result
            image_url = manage_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)
      
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Assertion Error: The device image is not set!")
          
        finally:
            #post-condition:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_file(img_actual)
            TestCondition.delete_simplified_users([simplified_dev_admin], test_organization)
              
                  
    def test_c11269_change_device_icon(self):
        """            
        @author: Quang Tran
        @date: 08/18/2016
        @precondition:
            n/a
          
        @steps:
        1. From your organization's Site Admin 2.0 Dashboard.
        2. Select the "Beam" drop down menu, then select the "all beams" link
        3. Select any Beam
        4. Select the "Change Image" button below the current image
        5. Browse to an image on your computer to add as a new device Icon
        6. Crop the image as you see fit
        7. Select the "Save" button to submit the results.
  
        @expected:
            (4) Icon should be replaced with newly selected Icon
  
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            device_name = beam.beam_name
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
            admin_user = User()                                            
            admin_user.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver, [admin_user])
              
            # steps
            admin_beams_detail_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab().select_a_device(device_name)\
                .change_image_icon(file_path)
                  
            # verify points
            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)
      
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Assertion Error: The device icon is not set!")
        finally:
            TestCondition.release_a_beam(beam)
            TestCondition.delete_advanced_users([admin_user])
            try:
                if img_actual:
                    Utilities.delete_file(img_actual)
            except:
                pass
      
      
    def test_c10988_change_device_icon_2_x(self):
        """
        @author: Quang.Tran
        @date: 08/19/2016
        @summary: Change device Icon [2.X] 
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
        @steps:
            1. Select Beams, Device (N/A: Group or All Beams)
            2. Select a Beam
            3. Click on the thumbnail image to upload a new image from your HDD
                a. Try different file sizes:
                    i. small (2kbytes)
                    ii. Med (500kbytes)
                    iii. Large (10000kbytes)
                    iv. Corrupt File
            4. Crop Image to desired size (square)
            5. Click Apply to assign the new image.
  
        @expected:
            Verify All Changes are saved by exiting and reentering menu 
        """
        try:
            # pre-condition
            beam = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            device_name = beam.beam_name

            corrupted_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_corrupt.jpg")
            small_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_small.png")
            medium_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_med.jpg")
            large_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_large.jpg")
            gif_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_gif.gif")
              

            admin_beams_detail_page = LoginPage(self._driver)\
                .open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_beams_tab().select_a_device(device_name)

            #steps
            #1. corrupt file
            admin_beams_detail_page.remove_image_icon()

            dialog = admin_beams_detail_page.open_upload_image_dialog()
            dialog.choose_file(corrupted_image_file_path)
            self.assertFalse(dialog.is_crop_tracker_displayed(), "Assertion Error: The crop-tracker is displayed on corrupted image.")
            dialog.cancel()

            # 2. small image
            admin_beams_detail_page.set_image_icon(small_image_file_path, resize_tracker = True)

            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_small_resize.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with small image (<10kbytes)!")

            # 3. medium image
            admin_beams_detail_page.change_image_icon(medium_image_file_path, resize_tracker = True)

            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_med_resize.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with medium image (~500kbytes)!")

            # 4. large image
            admin_beams_detail_page.change_image_icon(large_image_file_path, resize_tracker = True)
            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_large_resize.png", True)
            admin_beams_detail_page.remove_image_icon()

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with medium image (~10000kbytes)!")
            #5. gif image
            admin_beams_detail_page.change_image_icon(gif_image_file_path)

            image_url = admin_beams_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_actual = Image_Utilities.convert_png_to_jpg(img_actual)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_gif_moving.jpg", True)

            are_equal = Image_Utilities.are_images_similar(img_expected, img_actual)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with gif image!")
            admin_beams_detail_page.remove_image_icon()

        finally:
            TestCondition.release_a_beam(beam)
          
          
    def test_c10989_change_usergroup_icon_2_x(self):
        """
        @author: Quang.Tran
        @date: 08/17/2016
        @summary: Change UserGroup Icon [2.X] 
        @precondition: 
            Use the following Admin Test Organization - Accounts used for Suitable Tech Manual/Automation Testing:
                http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestOrgs
            Add a user group (UserGroupA)
        @steps:
            1) Login to Suitabletech.com as an org admin and then select "Manage Your Beams"
            2) Go to "Users" tab and select the "Create New User Group" button
            3) Select the pencil button on the user group image
            4) Select "Choose file…" button on "Upload New Profile Image" form
            5) Click on "Save" button
  
        @expected:
            (4) The "Select the area you would like to use" message appears.
            (5) Verify that the icon of user group is changed to the selected picture. 
        """
        try:
            # pre-condition
            img_actual = None
            user_group_name = Helper.generate_random_user_group_name()
            admin_user = User()                                            
            admin_user.generate_advanced_org_admin_data()
              
            TestCondition.create_advanced_organization_admins(self._driver, [admin_user])
            TestCondition.create_user_group(user_group_name)
              
            file_path = Utilities.get_test_image_file_path(self._driver, "img3.jpg")
  
            user_group_detail_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_users_tab()\
                .goto_user_group_detail_page(user_group_name)
  
            # steps   
            dialog = user_group_detail_page.open_upload_image_dialog()
            dialog.choose_file(file_path)
            message = dialog.get_crop_tracker_message()
            dialog.move_crop_tracker()
            dialog.submit()            
            user_group_detail_page.wait_for_icon_updated()
              
            # verify point: compare images by pixels
            image_url = user_group_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            if self._driver._driverSetting.platform == Platform.WINDOWS or self._driver._driverSetting.platform == Platform.MAC:
                img_expected = Utilities.get_test_image_file_path(self._driver, "img3_moving_mobile.png", True)
            else:
                img_expected = Utilities.get_test_image_file_path(self._driver, "img3_moving.png", True)
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
              
            self.assertEqual(ApplicationConst.LBL_IMAGE_CROP_TRACKER, message,
                "Assertion Error: The crop tracker message is not displayed.")
            self.assertTrue(are_equal, "Assertion Error: The user group icon is not set!")
              
        finally:
            TestCondition.delete_advanced_users([admin_user])
            TestCondition.delete_user_groups([user_group_name])
                  
            try:
                if img_actual:
                    Utilities.delete_file(img_actual)
            except:                
                pass
              

    @pytest.mark.OnlyDesktop
    def test_c11095_import_users_from_csv_file_with_valid_input_fields(self):
        """
        @author: Quang Tran
        @date: 8/19/2016
        @summary: Import Users from CSV file - with input fields that contain Malicious tags that are allowed to be imported
        @precondition: 
            Steps To Complete Task: Import Contacts from CSV file
             
                From your organization's Site Admin 2.0 Dashboard, select the "Import Contacts" button
                Browse to your provided CSV contact import file
                Select the file and click next
             
            Note:
            You will have a chance to confirm the list of contacts and customize the invitation email in the next step.
            1. The system will process the input file, and present the contacts in the following format:
            • New contacts are highlighted in green (see Green Arrow below).
            • You may un-check a contact if you don't want to import them.
            • Existing contacts are grayed out and won't be imported.(see Orange Arrow below).
            • Rows with errors are red. (see Red Arrow below).
             
                On this form you will also be presented with options to add the imported contacts to an existing Device and or Contact group.
                To complete the import select "Confirm" button
             
            Example of import file with Malicious tags input strings:
            email,firstName,lastName
            suitabletester2+9488500@gmail.com,'http://g.nordstromimage.com/imagegallery/store/product/Medium/3/_9488583.jpg',https://www.google.com/images/srpr/logo11w.png
            suitabletester2+9488501@gmail.com,suitable01,'http://g.nordstromimage.com/imagegallery/store/product/Medium/3/_9488583.jpg\'
            suitabletester2+9488502@gmail.com,suitable02,<CTRL+ALT+DEL>
            suitabletester2+9488503@gmail.com,^altDel, CTRL+ALT+DEL
            suitabletester2+9488504@gmail.com,^a, <CTRL+a>
            suitabletester2+9488505@gmail.com,'./ps -ef',tester9488505
            suitabletester2+9488506@gmail.com,www.cnn.com/video/live/live_asx.html,tester9488505
 
        @steps:
            1) Select Contacts from the Admin menu
            2) Select import Users
            3) Browser to your CSV user import file (See attached file)
            Note:
            You will have a chance to confirm the list of users and customize the invitation email in the next step.
        @expected:
            The import tool should allow you to add all users
 
        """
         
        try:
            # pre-condition
            is_imported_completed = False 
            all_users = None
            new_device_group = Helper.generate_random_device_group_name()
            new_user_group = Helper.generate_random_user_group_name()
            org_admin = User()
            org_admin.advanced_org_admin_data()
            csv_file = CSV_Utilities.generate_users_in_csv('test_c11095.csv', 2)
             
            TestCondition.create_device_group(new_device_group)
            TestCondition.create_user_group(new_user_group)
 
            # steps
            admin_users_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .goto_users_tab()
                 
            admin_users_page.import_users(csv_file, new_device_group, new_user_group)\
             
            all_users = CSV_Utilities.find_all_users_in_csv(csv_file)
            if all_users:
                is_imported_completed = admin_users_page.are_users_existed(all_users)

            # verify result
            self.assertTrue(is_imported_completed, "Assertion Error: Importing users from CSV failed!")
             
        finally:            
            # post-condition:
            users_to_be_deleted = []
            for email in all_users:
                user = User()
                user.email_address = email
                user.organization = org_admin.organization
                users_to_be_deleted.append(user)
                 
            TestCondition.delete_advanced_users(users_to_be_deleted)
            TestCondition.delete_user_groups([new_user_group])
            TestCondition.delete_device_groups([new_device_group])
             
 
    def test_c11096_import_users_from_csv_file_with_input_fields_that_contain_malicious_tags_that_will_error_out_when_uploaded(self):
        """
        @author: Khoi Ngo
        @date: 8/22/2016
        @summary: Import Users from CSV file - with input fields that contain Malicious tags that will error out when uploaded
        @precondition: 
            Steps To Complete Task: Import Contacts from CSV file
                From your organization's Site Admin 2.0 Dashboard, select the "Import Contacts" button
                Browse to your provided CSV contact import file
                Select the file and click next
            Note:
            You will have a chance to confirm the list of contacts and customize the invitation email in the next step.
            1. The system will process the input file, and present the contacts in the following format:
            • New contacts are highlighted in green (see Green Arrow below).
            • You may un-check a contact if you don't want to import them.
            • Existing contacts are grayed out and won't be imported.(see Orange Arrow below).
            • Rows with errors are red. (see Red Arrow below).
                On this form you will also be presented with options to add the imported contacts to an existing Device and or Contact group.
                To complete the import select "Confirm" button
            Example of import file with Malicious tags input strings:
            email,firstName,lastName
            suitabletester2+9488502@gmail.com,'@%$#^%$&^%*&^()(*)*)&(*(^%%$$#%@$!/")',tester9488502
            suitabletester2+9488507@gmail.com,"Hello".zfill(135),tester9488507
            suitabletester2+9488506@gmail.com,<script>alert("hello");</script>,tester9488506
        @steps:
            1. Select Contacts from the Admin menu
            2. Select import Users
            3. Browser to your CSV user import file (See attached file)
        @expected:
            The Admin web import tool will error out and will not allow the import
        """
        try:
            # precondtion
            import os
            from data_test import testdata
            data = os.path.join(os.path.dirname(testdata.__file__), "test_c11096.csv")
             
            org_admin = User()
            org_admin.generate_advanced_org_admin_data()
            TestCondition.create_advanced_organization_admins(self._driver, [org_admin])
             
            # steps
            admin_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)\
                .import_users_expecting_error(data)
                 
            # verify point
            self.assertEqual(admin_page.get_error_message(), ApplicationConst.LBL_IMPORT_CONTACT_ERROR_MESSAGE, "Assertion Error: Expected error message is not displayed")
            #There was an error importing your contacts.
        finally:
            TestCondition.delete_advanced_users([org_admin])
         
         
    def test_c11334_import_users_from_csv_file_existing_user_names(self):
        """
        @author: tham.nguyen
        @date: 8/22/2016
        @summary: Import Users from CSV file - Existing User Names
        @precondition: 
            Steps To Complete Task: Import Contacts from CSV file
                1. From your organization's Site Admin 2.0 Dashboard, select the "Import Contacts" button
                2. Browse to your provided CSV contact import file
                3. Select the file and click next
            Note:
            You will have a chance to confirm the list of contacts and customize the invitation email in the next step.
            1. The system will process the input file, and present the contacts in the following format:
            • New contacts are highlighted in green (see Green Arrow below).
            • You may un-check a contact if you don't want to import them.
            • Existing contacts are grayed out and won't be imported.(see Orange Arrow below).
            • Rows with errors are red. (see Red Arrow below).
                1. On this form you will also be presented with options to add the imported contacts to an existing Device and or Contact group.
                2. To complete the import select "Confirm" button
            Example: Sample duplicate User CSV file:
            suitabletester2+duplicatetester1@gmail.com,duplicate1,tester1
            suitabletester2+duplicatetester2@gmail.com,duplicate2,tester2
            suitabletester2+duplicatetester3@gmail.com,duplicate3,tester3
            suitabletester2+duplicatetester4@gmail.com,duplicate4,tester4
        @steps:
            1. Select Contacts from the Admin menu
            2. Select import Users
            3. Browser to your CSV user import file (See attached file) and click next
            4. Select existing Device Group: "DeviceGroupTest-A" and User Group: "UsersGroupTest01 to imported contacts into.
            5. Verify all users are imported into the correct Device Group: "DeviceGroupTest-A" & User Group: "UsersGroupTest01".
                Example:
                Name : duplicate4 tester4 
                Email : suitabletester2+duplicatetester4@gmail.com
                Administrator: No
                User Groups : UsersGroupTest01 
                Device Groups: DeviceGroupTest-A
            6. Browser to the same CSV user import file used in Step 3 (See attached file) and click next
            7. Select existing Device Group: "DeviceGroupTest-B" and User Group: "UsersGroupTest02 to imported contacts into.
            Note:
            You will have a chance to confirm the list of users and customize the invitation email in the next step.
        @expected:
            1. Verify all previously imported users are still present in the Step 4 Device Group: "DeviceGroupTest-A" & User Group: "UsersGroupTest01".
            2. Verify the same existing users from step 4 are imported into the correct Device Group: "DeviceGroupTest-B" & User Group: "UsersGroupTest02".
            Example:
            Name : duplicate4 tester4 
            Email : suitabletester2+duplicatetester4@gmail.com
            Administrator: No
            User Groups : UsersGroupTest01, UsersGroupTest02 
            Device Groups: DeviceGroupTest-A, DeviceGroupTest-B
        """
        try:
            # pre-condtion
            beam1 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            device1 = beam1.beam_name
            beam2 = TestCondition.get_and_lock_beam(Constant.AdvancedOrgName)
            device2 = beam2.beam_name
              
            new_device_group_1 = Helper.generate_random_device_group_name()
            new_device_group_2 = Helper.generate_random_device_group_name()
              
            new_user_group_1 = Helper.generate_random_user_group_name()
            new_user_group_2 = Helper.generate_random_user_group_name()
                          
            org_admin = User()
            org_admin.advanced_org_admin_data()
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            org_admin.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
              
            csv_file = CSV_Utilities.generate_users_in_csv('test_c11334.csv', 2, special_character=False)
              
            TestCondition.create_device_group(new_device_group_1, [device1])
            TestCondition.create_device_group(new_device_group_2, [device2])
              
            TestCondition.create_user_group(new_user_group_1)
            TestCondition.create_user_group(new_user_group_2)
              
            admin_dashboard_page = LoginPage(self._driver).open()\
                .login(org_admin.email_address, org_admin.password)
                  
            # steps
            admin_users_page = admin_dashboard_page.import_users(csv_file, new_device_group_1, new_user_group_1).goto_users_tab()
            users = CSV_Utilities.find_users_info_in_csv(csv_file)
              
            group_all_users = ApplicationConst.LBL_ALL_USERS_GROUP

            # verify points
            for u in users:
                lst_device_groups_in_user = []
                lst_user_groups_in_user = []
                detail_user_page = admin_users_page.goto_user_detail_page(u)
                lst_device_groups_in_user = detail_user_page.get_device_groups()
                flag = self._compare_value_two_array([new_device_group_1], lst_device_groups_in_user)
                self.assertTrue(flag, "Device groups '{}' that user '{}' belongs don't match device '{}'"\
                                            .format(lst_device_groups_in_user, u.email_address, [new_device_group_1]))
                  
                lst_user_groups_in_user = detail_user_page.get_user_groups()
                flag = self._compare_value_two_array([group_all_users, new_user_group_1], lst_user_groups_in_user)
                self.assertTrue(flag, "User groups '{}' that user '{}' belongs don't match user groups '{}'"\
                                            .format(lst_user_groups_in_user, u.email_address, [new_user_group_1]))
                admin_users_page = detail_user_page.goto_users_tab()
                  
            admin_users_page = admin_users_page.goto_dashboard_tab().import_users(csv_file, new_device_group_2, new_user_group_2).goto_users_tab()
              
            for u in users:
                device_groups_in_user = []
                lst_user_groups_in_user = []
                detail_user_page = admin_users_page.goto_user_detail_page(u)
                device_groups_in_user = detail_user_page.get_device_groups()
                flag = self._compare_value_two_array([new_device_group_1, new_device_group_2], device_groups_in_user)
                self.assertTrue(flag,
                        "Device groups '{}' that user '{}' belongs don't match device '{}'"\
                        .format(device_groups_in_user, u.email_address, [new_device_group_1, new_device_group_2]))            
                  
                lst_user_groups_in_user = detail_user_page.get_user_groups()
                flag = self._compare_value_two_array([group_all_users, new_user_group_1, new_user_group_2], lst_user_groups_in_user)
                self.assertTrue(flag, "User groups '{}' that user '{}' belongs don't match user groups '{}'".format(lst_device_groups_in_user, u.email_address, [new_user_group_1, new_user_group_2]))
                admin_users_page = detail_user_page.goto_users_tab()
                  
        finally:
            # post-condition
            TestCondition.release_a_beam(beam1)
            TestCondition.release_a_beam(beam2)
            TestCondition.delete_user_groups([new_user_group_1, new_user_group_2])
            TestCondition.delete_device_groups([new_device_group_1, new_device_group_2, temp_device_group_name])
            TestCondition.delete_advanced_users(users)
  
     
    def test_c10953_change_user_icon(self):
        """
        @author: Quang Tran
        @date: 8/17/2016
        @summary: Change User Icon 
        @precondition: 
            Login as a normal user
        @steps:
            1) Go to the "Manage your Beams" dashboard, from the dropdown menu displaying your name in the top right corner, select account settings
            2) Click on the grey pencil in the icon below "Your Default Profile Image"
            3) Upload new image, adjust area
            4) Hit "Save"   
        @expected:
            Verify the picture changes to the image you uploaded (may need to refresh browser tab).
  
        """
        try:
            img_actual = ""
            user = User()
            user.generate_advanced_normal_user_data()
            # create device group
            temp_device_group_name = Helper.generate_random_device_group_name()
            user.device_group = temp_device_group_name
            TestCondition.create_device_group(temp_device_group_name)
              
            TestCondition.create_advanced_normal_users(self._driver, [user])
            #TODO Fail on mobie INFR-2636

            account_setting_page = LoginPage(self._driver).open()\
                .login(user.email_address, user.password)\
                .goto_your_account()
              
            # steps
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
            account_setting_page.remove_user_icon().change_user_icon(file_path)        
              
            # verify result
            image_url = account_setting_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)
      
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Assertion Error: The user profile image is not set!")
                        
        finally:
            TestCondition.delete_file(img_actual)
            TestCondition.delete_advanced_users([user])
            TestCondition.delete_device_groups([temp_device_group_name])


    def test_c33876_default_icon_will_apply_for_each_organizations_if_user_doesnt_set_icon_for_each_organizations(self):
        """
        @author: Khoi Ngo
        @date: 9/29/2017
        @summary: Verify that default icon will apply for each organization if user doesn't set
        @precondition:
            Invite a new user into 2 orgs (Org1 and Org2). Then activating new user.
        @steps:
            1. Login new user
            2. Go to Account Settings page
            3. Change Default Profile Image
            4. Logout and login as org admin
            5. Check profile image of new user displays correctly
        @expected:
            (5) Default Profile Image will display for both orgs
  
        """
        try:
            #pre-condition:
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            normal_user.organization = Constant.AdvancedOrgName_2
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            #steps:
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
            user_detail_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account()\
                .change_user_icon(file_path)\
                .logout()\
                .goto_login_page()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .goto_user_detail_page(normal_user)

            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)    
            image_url = user_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Default Profile Image doesn't display for advance org 1")

            user_detail_page.goto_another_org(Constant.AdvancedOrgName_2)\
                .goto_users_tab()\
                .goto_user_detail_page(normal_user)

            img_actual_2 = Utilities.download_file(self._driver, image_url)
            are_equal = Image_Utilities.are_images_similar(img_actual_2, img_expected)
            self.assertTrue(are_equal, "Default Profile Image doesn't display for advance org 2")
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_file(img_actual)
            TestCondition.delete_file(img_actual_2)


    def test_c33877_user_icons_apply_correctly_for_each_organizations(self):
        """
        @author: Khoi Ngo
        @date: 10/2/2017
        @summary: Verify that user icons apply correctly for each organizations
        @precondition:
            Invite a new user into 2 orgs (Org1 and Org2). Then activating new user.
        @steps:
            1. Login new user
            2. Go to Account Settings page
            3. Change Profile Image for each organizations
            4. Logout and login as org admin
            5. Check profile image of new user displays
        @expected:
            (5) Profile Image apply correctly for each organizations
  
        """
        try:
            #pre-condition:
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            normal_user.organization = Constant.AdvancedOrgName_2
            TestCondition.create_advanced_normal_users(self._driver, [normal_user])
            #steps:
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
            file_path_2 = Utilities.get_test_image_file_path(self._driver, "img3.jpg")
            user_detail_page = LoginPage(self._driver).open()\
                .login(normal_user.email_address, normal_user.password, simplifiedUser=True)\
                .goto_your_account()\
                .change_user_icon(file_path, Constant.AdvancedOrgName)\
                .change_user_icon(file_path_2, Constant.AdvancedOrgName_2)\
                .logout()\
                .goto_login_page()\
                .login(Constant.AdvanceOrgAdminEmail,Constant.DefaultPassword)\
                .goto_users_tab()\
                .goto_user_detail_page(normal_user)

            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)    
            image_url = user_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Profile image of new user displays incorrectly on advance org 1")

            user_detail_page.goto_another_org(Constant.AdvancedOrgName_2)\
                .goto_users_tab()\
                .goto_user_detail_page(normal_user)

            img_expected_2 = Utilities.get_test_image_file_path(self._driver, "img3_moving.png", True)    
            image_url_2 = user_detail_page.get_icon_link()
            img_actual_2 = Utilities.download_file(self._driver, image_url_2)
            are_equal = Image_Utilities.are_images_similar(img_actual_2, img_expected_2)
            self.assertTrue(are_equal, "Profile image of new user displays incorrectly on advance org 2")
        finally:
            TestCondition.delete_advanced_users([normal_user])
            TestCondition.delete_file(img_actual)
            TestCondition.delete_file(img_actual_2)


    def test_c11347_non_admin_user_beam_account_home_download_the_beam_desktop_software(self):
        """
        @author: Tham Nguyen
        @date: 08/15/2016
        @summary: Non-Admin User Beam Account Home - Download the Beam Desktop Software
        @precondition:           
            Use the following Test users and Organizations - Accounts used for Suitable Tech Manual/Automation Testing:
            http://wiki.suitabletech.com/display/SUIT/QA+Test+Accounts#QATestAccounts-TestUserAccounts
              
            There is an Simplified Org Admin
              
            1) Login to Suitabletech with the Simplified Org Admin account
            2) On Manage Your Beams page, enter user's email address which would like to invite and select "Add User" button
            3) Go to mailbox of this user and active it and login to Suitabletech site
            4) Complete see video            
        @steps:
            Steps To Complete Task:
            1)Select on drop-down menu "Account Settings > Home"
            2)Click the "Download the Beam Desktop Software" button
            3)Click "Download" button on "Suggested Installer"       
        @expected:          
            (3) Verify that you get the download dialog after selecting the "Download" button under the "Suggested Installer".
        """
          
        try:
            # pre-condition:
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
             
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()

            # steps
            download_page = LoginPage(self._driver).open()\
                    .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                    .goto_manage_beam_page(beam.beam_id)\
                        .create_completed_simplified_normal_user(normal_user)\
                    .goto_login_page()\
                    .login_as_unwatched_video_user(normal_user.email_address, normal_user.password)\
                    .watch_video(normal_user, simplified=False)\
                    .goto_your_account()\
                    .goto_simplify_normal_user_home()\
                    .goto_download_page()
                  
            self.assertEqual(200, download_page.get_download_link_status(), "Beam Desktop Software is not downloaded.")
        finally:
            # post-condition
            TestCondition.delete_simplified_users([normal_user])
              
  
    def test_c10993_change_device_icon(self):
        """
        @author: Duy.Nguyen
        @date: 8/23/2016
        @summary: Change Device Icon
        @precondition: 
        @steps:        
            1) From your organization's Site Admin 2.1 Dashboard.
            2) Verify that you can select the the following to drill down into the devices properties page:
                Option 1: Select "Manage" button
                Option 2: Select Beam image icon
            3) Select the "Change Image" button on right of the current image
            4) Browse to an image on your computer to add as a new device Icon
            5) Crop the image as you see fit
            6) Select the "Save" button to submit the results.
  
        @expected:
            Icon should be replaced with newly selected Icon
        """
        try:
            # pre-condition
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
  
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
              
            # steps: 
            manage_page = LoginPage(self._driver).open()\
                    .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser=True)\
                    .goto_manage_beam_page(beam.beam_id).change_image_icon(file_path)   
              
            # verify result
            image_url = manage_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)
      
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Assertion Error: The user profile image is not set!")
          
        finally:
            # post-condition:    
            try:
                if img_actual:
                    Utilities.delete_file(img_actual)
            except:
                pass        
 
 
    def test_c11719_change_device_group_image (self):
        """
        @author: Thanh Le
        @date: 4/26/2017
        @summary: Change Device Group Image
        @precondition: 
            Login to Suitabletech.com and navigate to the Manage Your Beams advanced UI as a Device Group Admin.
          
        @steps:
            1) Login to Suitabletech.com and navigate to the Manage Your Beams advanced UI.
            2) Go to the "Beams" tab in the "Manage your Beams" dashboard
            3) Select a device group and go to the "Settings" tab
            4) Scroll down to the bottom of the page and click on the pencil icon adjacent to the Profile Image field
            5) Upload a file and save changes
            6) Confirm that a green pop up stating "Device group settings were saved successfully" appears on the screen
        @expected:
            Verify that the device group icon has changed by clicking the "Beams" tab and visually inspecting the device group icon.
            Note:
                --> Test different file formats for pictures (e.g. png, jpeg, gif?)
                -->Try different file sizes:
                i. small (2kbytes)
                ii. Med (500kbytes)
                iii. Large (10000kbytes)
                iv. Corrupt File
        @note The testcase is in Device Group Admin 0.41
        """
        try:
            # pre-condition
            new_device_group_name = Helper.generate_random_device_group_name()
            corrupted_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_corrupt.jpg")
            small_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_small.png")
            medium_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_med.jpg")
            large_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_large.jpg")
            gif_image_file_path = Utilities.get_test_image_file_path(self._driver, "img_gif.gif")
             
            admin_user = User()
            admin_user.generate_advanced_device_group_admin_data()
            admin_user.device_group = new_device_group_name
             
            TestCondition.create_device_group(admin_user.device_group)
            TestCondition.create_advanced_device_group_admins(self._driver, [admin_user])
             
            # steps

            device_group_detail_page = LoginPage(self._driver).open()\
                .login(admin_user.email_address, admin_user.password)\
                .goto_beams_tab()\
                .select_device_group(new_device_group_name)\
                .goto_setting_tab()
                                 
            # 1. corrupt file
            dialog = device_group_detail_page.open_upload_image_dialog()
            dialog.choose_file(corrupted_image_file_path)
            self.assertFalse(dialog.is_crop_tracker_displayed(), "The crop-tracker is displayed on corrupted image.")
            dialog.cancel()
             
            # 2. small image
            device_group_detail_page.set_image_icon(small_image_file_path)
            image_url = device_group_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_small_moving.png", True)
         
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)
              
            self.assertTrue(are_equal, "The device icon is not set with small image (<10kbytes)!")
             
            # 3. medium image
            device_group_detail_page.change_image_icon(medium_image_file_path)
            
            image_url = device_group_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_med_moving.png", True)
       
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)
               
            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with medium image (~500kbytes)!")
              
            # 4. large image
            device_group_detail_page.change_image_icon(large_image_file_path)
            
            image_url = device_group_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_large_moving.png", True)
      
            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            Utilities.delete_file(img_actual)
              
            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with large image (~10000kbytes)!")

            #5. gif image
            device_group_detail_page.change_image_icon(gif_image_file_path)

            image_url = device_group_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_actual = Image_Utilities.convert_png_to_jpg(img_actual)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img_gif_moving.jpg", True)

            are_equal = Image_Utilities.are_images_similar(img_expected, img_actual)
            Utilities.delete_file(img_actual)

            self.assertTrue(are_equal, "Assertion Error: The device icon is not set with gif image!")
            device_group_detail_page.remove_image_icon()

        finally:
            TestCondition.delete_device_groups([new_device_group_name])
            TestCondition.delete_advanced_users([admin_user])
             
             
    def test_c33781_verify_that_profile_image_is_uploaded_successfully_at_user_details_page_in_simplified_organization(self):
        """
        @author: Thanh.Le
        @date: 05/17/2017
        @summary: Verify that profile image is uploaded successfully at user details page in Simplified Organization.
        @desciption: BUG_105 The image is not uploaded successfully when changing profile image at  user details page in Simplified Organization.
        @steps:
            1. Login to Suitabletech site https://stg1.suitabletech.com as Simplified Organization Admin
            (thanh.viet.le@logigear.com/Logigear123)
            2. Go to Simplified Organization (LogiGear Test 2)
            3. Select a beam
            4. Click any user in "People with access to this Beam" list to view the user details page
            5. Click "Change image" icon
            6. Choose an image at "Upload New Profile Image" dialog
        @expected:
            - The image should be uploaded successfully.
          
        @note: Ready to automate
        """
        try:
            # pre-condition 
            test_organization=Constant.SimplifiedOrgName
            beam = TestCondition.get_a_beam(test_organization)
            file_path = Utilities.get_test_image_file_path(self._driver, "img2.jpg")
              
            simplified_user = User()
            simplified_user.generate_simplified_normal_user_data()
            TestCondition.create_simplified_normal_users(self._driver, [simplified_user], beam, False)
              
            # steps
            simplified_user_detail_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser = True)\
                .goto_manage_beam_page(beam.beam_id)\
                .goto_simplified_user_detail_page(simplified_user)\
                .set_image_icon(file_path)

            # verify
            image_url = simplified_user_detail_page.get_icon_link()
            img_actual = Utilities.download_file(self._driver, image_url)
            img_expected = Utilities.get_test_image_file_path(self._driver, "img2_moving.png", True)

            are_equal = Image_Utilities.are_images_similar(img_actual, img_expected)
            self.assertTrue(are_equal, "Assertion Error: The device icon is not set!")

        finally:
            # post-condition
            TestCondition.delete_simplified_users([simplified_user])
            try:
                if img_actual:
                    Utilities.delete_file(img_actual)
            except:
                pass


    def test_c11346_non_admin_user_beam_account_home_dashboard(self):
        """
        @author: Quang Tran
        @date: 01/15/2018
        @summary: Non-Admin User Beam Account Home- Dashboard
        @steps:
            1.Login to Suitabletech with the Simplified Org Admin account
            2.On Manage Your Beams page, enter user's email address which would like to invite and select "Add User" button
            3.Go to mailbox of this user and active it and login to Suitabletech site
            4.Select on drop-down menu "Account Settings > Home"
        @expected:
            (4) 
            a. Verify that you have the following user action buttons visible and click able:
            _Download the Beam Desktop Software
            _Get Help
            _Add a Beam
            _View Documentation
            b. Verify that all Beam accessible to that non-Admin User is listed with the following properties:
            Name : <Beam Name>
            Location : <text string>
            Labels : <text string>
            Time Zone : <Country>/<Region>
            Connected Status: <Available/Configuring/Off-line/etc..>
            Battery Status : <xx%> <Charging>
        """
        try:
            #pre-condition
            normal_user = User()
            normal_user.generate_advanced_normal_user_data()
            
            beam = TestCondition.get_a_beam(Constant.SimplifiedOrgName)
            beam_name = beam.beam_name
    
            #steps
            simplified_dashboard_page = LoginPage(self._driver).open()\
                .login(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, simplifiedUser = True)\
                .add_user(normal_user, beam_name)
        
            TestCondition._activate_user_temporary_password(self._driver, normal_user, pass_safety_video=True, localize=True)
    
            simplified_dashboard_page = simplified_dashboard_page.logout_and_login_again(normal_user.email_address, normal_user.password, loginAgainAsNormalUser=True)

            #verify point
            self.assertTrue(simplified_dashboard_page.is_page_displayed(), 
                            "Download the Beam Desktop Software and Get Help link is not displayed.")
            self.assertTrue(simplified_dashboard_page.is_beam_displayed(beam_name), 
                            "Beam {} is not displayed on dashboard page")

        finally:
            #post condition
            TestCondition.delete_simplified_users([normal_user])

