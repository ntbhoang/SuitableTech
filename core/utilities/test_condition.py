from datetime import datetime
from datetime import timedelta
import json
from time import sleep

from common.constant import Constant, Platform
from common.stopwatch import Stopwatch
from core.suitabletechapis.device_api import DeviceAPI
from core.suitabletechapis.reservation_api import ReservationAPI
from core.suitabletechapis.device_group_api import DeviceGroupAPI
from core.suitabletechapis.organization_settings_api import OrganizationSettingAPI
from core.suitabletechapis.user_api import UserAPI
from core.suitabletechapis.user_group_api import UserGroupAPI
from core.suitabletechapis.beam_content_api import BeamContentAPI
from core.utilities.gmail_utility import GmailUtility
from core.utilities.utilities import Utilities, Calendar_Utilities
from data_test.dataobjects.user import User
from pages.suitable_tech.user.login_page import LoginPage
from pages.suitable_tech.user.password_setup_page import PasswordSetupPage
from pages.gmail_page.gmail_sign_in_page import GmailSignInPage
from pages.gmail_page.apps_connected_page import AppsConnectedPage
from pages.gmail_page.gmail_sign_up_page import GmailSignUpPage
from pages.suitable_tech.admin.advanced.dashboard.admin_dashboard_page import AdminDashboardPage
from core.webdriver.drivers.driver import Driver
from core.webdriver.drivers.driversetting import DriverSetting
from common.helper import Helper
import os
import threading
from pages.suitable_tech.user.signout_complete_page import SignoutCompletePage
import requests
from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage
from core.suitabletechapis.access_request_api import AccessRequestAPI
import random
from core.suitabletechapis.device_activity_api import DeviceActivityAPI

class TestCondition():
    SIMPLIFIED_ACCESS_TOKEN = ""
    BEAM_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\resources\\beams.json".replace("\\", os.path.sep)
    LOCALES_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\resources\\locales.json".replace("\\", os.path.sep)
    INFO_BEAM_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\resources\\info_beams.json".replace("\\", os.path.sep)
    GSSO_AND_NON_GSSO_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\resources\\google_accs_allow_st.json".replace("\\", os.path.sep)
    UNALLOWED_GSSO_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\resources\\google_accs_unallow_st.json".replace("\\", os.path.sep)
    ORG_AUTHENTICATION_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\resources\\org_authentication.json".replace("\\", os.path.sep)
    OKTA_XML_RESOURCE = Helper.base_dir() + "\\data_test\\testdata\\authentication\\Okta.xml".replace("\\", os.path.sep)
    RESOURCE_WAIT_TIMEOUT = 1800
    RESOURCE_POLLING_INTERVAL = 1
    RLOCK = threading.RLock()
    
    """   CREATE DATA   """        
    
        
    @staticmethod
    def login_and_change_language_using_api(email, password, language):
        """      
        @summary: login user account and changing the language   
        @param email: user email
        @param password: user password
        @param language: language 
        @author: Thanh Le       
        @created_date: August 30, 2016  
        """
        session = requests.Session()
        UserAPI.login_account(email, password, session)
        access_token = UserAPI.set_access_token(session)
        UserAPI.change_language(access_token, language, session)
        
    
    @staticmethod
    def get_calendar_key_via_api(email, password):
        """      
        @summary: login user account and changing the language   
        @param email: user email
        @param password: user password
        @param language: language 
        @author: Thanh Le       
        @created_date: August 30, 2016  
        """
        session = requests.Session()
        UserAPI.login_account(email, password, session)
        access_token = UserAPI.set_access_token(session)
        res = UserAPI.get_calendar_key(access_token)
        return res.json()['calendar_key']
        
        
    @staticmethod
    def create_advanced_normal_users(driver, user_array=[], activate_user=True, pass_safety_video=True):
        """      
        @summary: create new advanced normal users as precondition for test case   
        @param driver: WebDriver
        @param user_array: Array of users to be created
        @param activate_user: Set to True to activate all user. Set to False to only create new Users
        @author: Thanh Le       
        @created_date: August 30, 2016  
        """
        for user in user_array:
            TestCondition._create_advanced_normal_user(user)
            if(activate_user == True):
                TestCondition._activate_user(driver, user, pass_safety_video)
    
    
    @staticmethod
    def create_advanced_multi_org_normal_users(driver, user_array, organization_array, activate_user=True):
        """
        @summary: Create new advanced normal users as precondition for test case   
        @param driver: WebDriver
        @param user_array: Array of users to be created
        @param organization_array: Array of organization
        @param activate_user: Set to True to activate all user. Set to False to only create new Users
        @author: Thanh Le    
        @created_date: August 30, 2016       
        """
        for user in user_array:
            for index in range(len(organization_array)):
                user.organization = organization_array[index]
                if(index > 0):
                    activate_user = False
                TestCondition.create_advanced_normal_users(driver=driver, user_array=[user], activate_user=activate_user)
        
        
    @staticmethod
    def create_advanced_device_group_admin_on_multi_organization(driver, device_group_admin, device_group_name, device_list=[], organization_array=[Constant.AdvancedOrgName, Constant.AdvancedOrgName_2]):
        """      
        @summary: Create new device group admin in two different organization as precondition for test case   
        @param driver: WebDriver
        @param device_group_admin: A device group admin to be created
        @param device_group_name: Device group name
        @param device_list: Array of devices
        @param organization_array: List of organizations which device group is created
        @author: Khoi Ngo
        @created_date: August 30, 2016    
        """
        try:
            for org in organization_array:
                device_group_admin.organization = org
                device_group_admin.device_group = device_group_name
                TestCondition.create_device_group(device_group_name, device_list, org)
                TestCondition.create_advanced_device_group_admins(driver, [device_group_admin])
        except:
            raise Exception("Error while create device group admin on multi org.")
    

    @staticmethod
    def create_advanced_device_group_admins(driver, user_array):
        """      
        @summary: Create new device group admins as precondition for test case   
        @param driver: WebDriver
        @param user_array: Array of device group admins to be created
        @param admin_email: Email of the admin who grants device group permission for the new users. Leave it None to automatically create new org admin
        @param admin_password: Password of the admin who grants device group permission for the new users
        @param is_new_admin: Set to True is the Admin is new and not completed the video. Set to False if the Admin has already watched the video.
        @author: Thanh Le 
        @created_date: August 30, 2016            
        """
        for user in user_array:
            TestCondition._create_advanced_normal_user(user)
            TestCondition.set_advanced_device_group_admin(user.email_address, user.device_group, user.organization)
            TestCondition._activate_user(driver, user)
    
    @staticmethod
    def set_advanced_device_group_admins(driver, user_array):
        """      
        @summary: Create new device group admins as precondition for test case   
        @param driver: WebDriver
        @param user_array: Array of device group admins to be created
        @param admin_email: Email of the admin who grants device group permission for the new users. Leave it None to automatically create new org admin
        @param admin_password: Password of the admin who grants device group permission for the new users
        @param is_new_admin: Set to True is the Admin is new and not completed the video. Set to False if the Admin has already watched the video.
        @author: Thanh Le 
        @created_date: August 30, 2016            
        """
        for user in user_array:
            TestCondition.set_advanced_device_group_admin(user.email_address, user.device_group, user.organization)
            
            
    @staticmethod
    def create_advanced_organization_admins(driver, user_array, activate_user=True):
        """      
        @summary: Create new organization admins as precondition for test case
        @param driver: WebDriver   
        @param user_array: Array of organization admins to be created
        @param activate_user: Set to True to activate all user. Set to False to only create new Users
        @author: Thanh Le  
        @created_date: August 30, 2016         
        """
        try:
            for user in user_array:
                TestCondition._create_advanced_normal_user(user)
                if (activate_user):
                    TestCondition._activate_user(driver, user)
                    
                response = UserAPI.set_org_admin(user, user.organization)
                if(response.status_code != 200):
                    raise Exception("Error while setting a user {} to be organization admin. Reason: {}".format(user.email_address, response.reason))
        except:
            raise Exception("Error while granting Organization Admin permission for users")
    
    
    @staticmethod
    def create_advanced_multi_organization_admin(driver, user, organization_array=[Constant.AdvancedOrgName, Constant.AdvancedOrgName_2]):
        """      
        @summary: Create new organization admin in 2 advanced organizations
        @param driver: WebDriver   
        @param user: Organization admin to be created
        @param organization_array: Array of organizations
        @author: Thanh Le  
        @created_date: August 30, 2016            
        """
        for org in organization_array:
            user.organization = org 
            TestCondition.create_advanced_organization_admins(driver, [user])
                
    
    @staticmethod
    def create_advanced_temporary_user(driver, user, device_group, start_date=datetime.now(), end_date=(datetime.now() + timedelta(minutes=15)), answer_required=False, activate_user=False):
        """      
        @summary: Create new temporary user as precondition for test case   
        @param driver: WebDriver
        @param user: User to be created
        @param device_group: Device group to add user
        @param start_date: Start time
        @param end_date: End time
        @param answer_required: Whether or not calls by this user must be accepted on the receiving side
        @param activate_user: Set to True to activate user. Set to False to only create new User
        @author: Thanh Le 
        @created_date: August 30, 2016           
        """
        response = UserAPI.invite_new_temporary_user(user, device_group, start_date, end_date, answer_required)
        if(response.status_code != 201):
            raise Exception("Error while creating temporary user {}. Reason: {}".format(user.tostring(), response.reason))
        
        if activate_user:
            TestCondition._activate_user(driver, user, True, email_subject= "You've been invited to Beam into {}".format(user.organization))
    
    
    @staticmethod
    def create_advanced_non_gsso_user(driver, user):
        """      
        @summary: Create new non gsso user as precondition for test case   
        @param driver: WebDriver
        @param user: User to be created
        @author: Thanh Le 
        @created_date: August 30, 2016              
        """
        try:
            confirm_association_page = TestCondition.force_log_out(driver)\
                .goto_login_page()\
                .goto_google_signin_page()\
                .sign_in_with_non_gsso_account(user.email_address, user.password)\
                
            if confirm_association_page.is_page_displayed():
                login_page = confirm_association_page.change_auth(False)
                TestCondition.login_and_change_language_using_api(user.email_address, user.password, driver._driverSetting.language)
                login_page.login(user.email_address, user.password, simplifiedUser=False).logout()

            else:
                simplified_dashboard_page = SimplifiedDashboardPage(driver)
                simplified_dashboard_page.goto_your_account()\
                    .set_language(driver.driverSetting.language)\
                    .save_change()\
                    .disconect_from_google()\
                    .reset_password(user)\
                    .logout()
        except:
            driver.save_screenshot()
            raise Exception("Error while preparing a gsso user.")
        
    
    @staticmethod
    def create_advanced_gsso_user(driver, user):
        """      
        @summary: Create new gsso user as precondition for test case   
        @param driver: WebDriver
        @param user: User to be created
        @author: Thanh Le         
        @created_date: August 30, 2016 
        """
        from common.email_detail_constants import EmailDetailConstants
        try:
            confirm_page = TestCondition.force_log_out(driver)\
                .goto_login_page()\
                .goto_google_signin_page()\
                .sign_in_with_non_gsso_account(user.email_address, user.password)
                
            if confirm_page.is_page_displayed():
                confirm_page.accept_change_authentication()

            GmailUtility.delete_all_emails(receiver=user.email_address)
            if len(GmailUtility.get_messages(mail_subject=EmailDetailConstants.GoogleChangeAuthEmailTitle, receiver=user.email_address, sent_day=datetime.now()))>0:
                GmailUtility.delete_all_emails(receiver=user.email_address)
            
            admin_dashboard_page = AdminDashboardPage(driver)
            admin_dashboard_page.logout()          
        except:
            driver.save_screenshot()
            raise Exception("Error while preparing a gsso user.")
        
    
    @staticmethod
    def create_advanced_unallowed_gsso_user(driver, user):
        """      
        @summary: Create new un allowed gsso user as precondition for test case   
        @param driver: WebDriver
        @param user: User to be created
        @author: Thanh Le   
        @created_date: August 30, 2016       
        """
        try:
#             TestCondition._remove_beam_from_connected_app(driver, user)
#             driver = TestCondition.reopen_browser(driver)
            TestCondition.create_advanced_non_gsso_user(driver, user)
#             driver = TestCondition.reopen_browser(driver)   
#             TestCondition._remove_beam_from_connected_app(driver, user)
            driver.quit()
        except:
            driver.save_screenshot()
            raise Exception("Error while preparing an unallowed gsso user.")
            
    
    @staticmethod
    def create_device_group(device_group_name, device_array=[], organization_name=Constant.AdvancedOrgName):
        """      
        @summary: Create new device group as precondition for test case   
        @param device_group_name: Device group name
        @param device_array: Array of devices
        @param organization_name: Organization which device group is created
        @author: Thanh Le    
        @created_date: August 30, 2016            
        """
        try:
            response = DeviceGroupAPI.create_device_group(device_group_name, device_array, organization_name)
            count = 0
            while count<5:
                if(response.status_code == 201):
                    break
                else:
                    response = DeviceGroupAPI.create_device_group(device_group_name, device_array, organization_name)
                    count = count + 1
            print("Create device group API status code: {}".format(response.status_code))
            if(response.status_code != 201):
                raise Exception("Error while creating Device Group {} for Organization {}. Reason: {}".format(device_group_name, organization_name, response.reason))
            else: 
                print("Crate device group {} successfully.".format(device_group_name))
        except Exception as ex:
            raise Exception("Error while creating device group. Message: " + str(ex))
        
    
    @staticmethod
    def create_user_group(group_name, user_array=[], organization_name=Constant.AdvancedOrgName):
        """      
        @summary: Create new user group in expected organization as precondition for test case   
        @param group_name: group name to be created
        @param user_array: users to add to user group
        @param organization_name: organization name
        @author: Thanh Le         
        @created_date: August 30, 2016 
        """
        try:
            user_email_array = []
            for user in user_array:
                user_email_array.append(user.email_address)
            
            response = UserGroupAPI.create_user_group(group_name, user_email_array, organization_name)
            if(response.status_code != 201):
                raise Exception("Error while creating User Group {} for Organization {}. Reason: {}. Content: {}".format(group_name, organization_name, response.reason, response.content))
            else: 
                print("Crate user group {} successfully.".format(group_name))
        except Exception as ex:
            raise Exception("Error while creating user group. Message: " + str(ex))
    
    
    @staticmethod
    def create_simplified_normal_users(driver, user_array, beam, activate_user=True, pass_safety_video=True):
        """      
        @summary: Create new simplified normal users as precondition for test case   
        @param driver: WebDriver
        @param user_array: Array of users to be created
        @param beam:  beam obj
        @param activate_user: Set to True to activate user. Set to False to only create new User
        @author: Thanh Le  
        @created_date: August 30, 2016        
        """
        TestCondition._set_access_token(Constant.SimplifiedAdminEmail, Constant.DefaultPassword)
        for user in user_array:
            TestCondition._create_simplified_normal_user(user=user, beam_id=beam.beam_id, organization=beam.beam_org)
            if activate_user:
                TestCondition._activate_user_temporary_password(driver, user, pass_safety_video, is_simplified=True)

    
    @staticmethod
    def create_simplified_organization_admin(driver, user):
        """      
        @summary: Create new simplified organization admin in 2 advanced organizations
        @param driver: WebDriver   
        @param user: Organization admin to be created
        @author: Thanh Le   
        @created_date: August 30, 2016         
        """
        TestCondition.set_language(driver, user)
        TestCondition._activate_user_temporary_password(driver, user, pass_safety_video = False, is_simplified=True)
    
        
    @staticmethod
    def create_simplified_device_admin(driver, user_array, beam, organization=Constant.SimplifiedOrgName, activate_user=True, pass_safety_video=True):
        """      
        @summary: Create new normal users as precondition for test case   
        @param driver: WebDriver
        @param user_array: Array of users to be created
        @param beam: beam obj
        @param organization: organization name 
        @param activate_user: Set to True to activate all user. Set to False to only create new Users
        @author: Thanh Le
        @created_date: August 30, 2016            
        """
        TestCondition._set_access_token(Constant.SimplifiedAdminEmail, Constant.DefaultPassword)
        
        for user in user_array:
            TestCondition._create_simplified_normal_user(user=user, beam_id = beam.beam_id, organization = organization)
            response = DeviceGroupAPI.set_simplified_device_admin(user.email_address, beam.beam_id, beam.beam_org, access_token=TestCondition.SIMPLIFIED_ACCESS_TOKEN)
            
            
            if(response.status_code != 200):
                    raise Exception("Error while creating simplified device admin. Reason: {}".format(response.reason))
            
            if activate_user:
                TestCondition._activate_user_temporary_password(driver, user, pass_safety_video, is_simplified=True)
    
    
    @staticmethod
    def create_new_google_account(driver, google_account):
        """      
        @summary: Create new google account
        @param driver: WebDriver
        @return: gmail account
        @author: Thanh Le
        @created_date: December 01, 2016        
        """
        try:
            is_gmail_created = GmailSignUpPage(driver).open().sign_up_gmail(google_account).\
                                agree_gmail_privacy_term().is_successful_message_displayed()
            if is_gmail_created:
                return google_account.emailAddress
            raise Exception ("Error while creating new Google account "+ str(google_account.emailAddress))
        except Exception as ex:
            driver.save_screenshot()
            raise ex


    """   DELETE DATA   """
    
    @staticmethod
    def delete_device_groups(device_group_array, organization_name=Constant.AdvancedOrgName):
        """      
        @summary: Delete device groups as postcondition for test case   
        @param device_group_array: device groups to be deleted
        @param organization_name: organization name
        @author: Thanh Le      
        @created_date: August 30, 2016      
        """
        print("***DELETE DEVICE GROUPS***\n")
        
        try:
            for device_group_name in device_group_array:
                response = DeviceGroupAPI.delete_device_group(device_group_name, organization_name)
                if(response.status_code != 204):
                    print("Error while deleting device group {}. Reason: {}".format(device_group_name, response.reason))
             
                print("Device group {} is deleted.".format(device_group_name))
        except Exception as ex:
            print("Error: Cannot delete device groups: " + str(device_group_array))
            print(str(ex))
            

    @staticmethod
    def delete_user_groups(user_group_array, organization=Constant.AdvancedOrgName):
        """      
        @summary: Delete user groups in expected organization as precondition for test case   
        @param user_group_array: group names to be delete
        @param organization: organization name
        @author: Thanh Le     
        @created_date: August 30, 2016       
        """
        print("***DELETE USER GROUPS***\n")
        
        try:
            for user_group_name in user_group_array:
                response = UserGroupAPI.delete_user_group(user_group_name, organization)
                if(response.status_code != 204):
                    print("Error while delete User Group for Organization {}. Reason: {}".format(organization, response.reason))
                
                print("User group {} is deleted.".format(user_group_name))
        except Exception as ex:
            print("Error: Cannot delete user groups: " + str(user_group_array))
            print(str(ex))
            
    
    @staticmethod
    def delete_advanced_users(user_array, organization=Constant.AdvancedOrgName):
        """      
        @summary: Delete users as postcondition for test case   
        @param user_array: users to be deleted
        @param organization: organization name
        @author: Thanh Le     
        @created_date: August 30, 2016            
        """
        print("***DELETE ADVANCED USERS***\n")
        try:
            for user in user_array:
                response = UserAPI.delete_user(user.email_address, organization)
                if(response.status_code != 204):
                    print("Error while deleting user {}. Reason: {}".format(user.email_address, response.reason))
             
                print("Advanced User {} is deleted.".format(user.email_address))
        except Exception as ex:
            print("Error: Cannot delete Advanced Users: " + str(user_array))
            print(str(ex))
        
    
    @staticmethod
    def delete_simplified_users(user_array, organization=Constant.SimplifiedOrgName):
        """      
        @summary: Delete users as postcondition for test case
        @param user_array: users to be deleted
        @param device_name: device which user is added
        @param organization: organization name
        @author: Thanh Le     
        @created_date: August 30, 2016            
        """
        print("***DELETE SIMPLIFIED USERS***\n")
        try:
            for user in user_array:
                response = UserAPI.delete_simplified_user(user.email_address, organization, TestCondition._get_access_token())
                if(response.status_code != 204):
                        print("Error while deleting simplified user {}. Reason: {}".format(user.email_address, response.reason))
                 
                print("Simplified User {} is deleted.".format(user.email_address))
        except Exception as ex:
            print("Error: Cannot delete Simplified Users: " + str(user_array))
            print(str(ex))
    
    
    @staticmethod
    def delete_beam_content(beam_content_array, organization=Constant.AdvancedOrgName):
        """
        @summary: this API is to delete beam content image
        @param filename: filename of image needs to remove
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: September 13, 2017
        """
        print("***DELETE BEAM CONTENTS***")
        
        try:
            for image_name in beam_content_array:
                response = BeamContentAPI.delete_beam_content(image_name, organization)
                if(response.status_code != 204):
                    print("Error while deleting beam content {}. Reason: {}".format(image_name, response.reason))
             
                print("Beam content {} is deleted.".format(image_name))
        except Exception as ex:
            print("Error: Cannot delete beam contents: " + str(beam_content_array))
            print(str(ex))       
        
    @staticmethod
    def delete_file(file_path):
        """      
        @summary: Delete file   
        @param file_path: path to the file
        @author: Thanh Le    
        @created_date: August 30, 2016          
        """
        try:
            if file_path:
                Utilities.delete_file(file_path)
        except Exception as ex:
            print("Error: Cannot delete file: " + file_path)
            print(str(ex))
    
    
    @staticmethod
    def delete_api_key(driver, key_name, organization_name=None):
        """
        @summary: This action use to handle while there is failure occur in test case cause the condition
                of GMailNonGSSOAuthenForwarded account is invalid.
        @param driver: Webdriver
        @param key_name: API key
        @param organization_name: organization_name
        @author: Thanh le
        @created_date: October 03, 2016
        """
        try:
            if organization_name is None:
                organization_name = Constant.AdvancedOrgName
                
            user = User()
            user.generate_advanced_org_admin_data()
            user.organization = organization_name
            TestCondition.create_advanced_organization_admins(driver, [user])
                
            LoginPage(driver).open()\
                .login_as_unwatched_video_user(user.email_address, user.password)\
                .goto_admin_dashboard_page_by_menu_item()\
                .goto_org_setting_page().delete_api_key(key_name)
                
            TestCondition.delete_advanced_users([user], user.organization)
        except Exception as ex:
            print("Error: Cannot delete APIKey: " + key_name)
            print(str(ex))
            
    
    @staticmethod
    def remove_all_user_groups(delete_user_group_template="LGVN User Group", organization=Constant.AdvancedOrgName):
        """      
        @summary: Remove all User Groups that match the keyword  
        @param delete_user_group_template: group name 
        @param organization: organization name 
        @author: Thanh Le     
        @created_date: October 03, 2016    
        """
        try:
            UserGroupAPI.delete_all_user_groups(delete_user_group_template, organization)
        except Exception as ex:
            print("Error: Cannot remove all User Groups with keyword: " + delete_user_group_template)
            print(str(ex))
    
    
    @staticmethod
    def remove_test_advanced_users(keyword_array=["logigear1+user", "logigear2+user"], organization=Constant.AdvancedOrgName):
        """      
        @summary: Remove all test advanced users
        @param keyword_array: array of users 
        @param organization: organization name
        @author: Thanh Le 
        @created_date: October 03, 2016         
        """
        try:
            for keywork in keyword_array:
                UserAPI.delete_all_users(keywork, organization)
        except Exception as ex:
            print("Error: Cannot remove all Advanced Users with keywords: " + str(keyword_array))
            print(str(ex))
            
    
    @staticmethod
    def delete_test_simplified_users(organization, beam_id, keyword_array=["logigear1+user", "logigear2+user"]):
        """      
        @summary: Remove all simplified test users
        @param organization: organization name
        @param beam_id: device id
        @param keyword_array: array of users 
        @author: Thanh Le 
        @created_date: October 03, 2016             
        """
        try:
            user_emails = DeviceGroupAPI.get_all_users_in_simplified_device_group(beam_id=beam_id, access_token=TestCondition._get_access_token(), organization=organization)
            user = User()
            for email in user_emails:
                for keywork in keyword_array:
                    if(keywork in email):
                        user.email_address = email
                        TestCondition.delete_simplified_users([user], organization)
        except Exception as ex:
            print("Error: Cannot remove all Simplified Users with keywords: " + str(keyword_array))
            print(str(ex))
               
    
    @staticmethod
    def remove_all_device_groups(delete_device_group_template="LGVN Device Group", organization=Constant.AdvancedOrgName):
        """      
        @summary: Remove all users in a Group User   
        @param delete_device_group_template: delete device group name
        @param organization: organization name 
        @author: Thanh Le 
        @created_date: October 03, 2016       
        """
        try:
            DeviceGroupAPI.delete_all_device_groups(delete_device_group_template, organization)
        except Exception as ex:
            print("Error: Cannot remove all Device Groups with keywords: " + delete_device_group_template)
            print(str(ex))
        
    @staticmethod
    def reject_all_access_requests(organization=Constant.AdvancedOrgName):
        """      
        @summary: Remove all users in a Group User
        @param delete_device_group_template: delete device group name
        @param organization: organization name
        @author: Thanh Le 
        @created_date: October 03, 2016
        """
        try:
            session = requests.Session()
            UserAPI.login_account(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword, session)
            AccessRequestAPI.reject_all_access_requests(session, organization)
        except Exception as ex:
            print("Error: Cannot reject all access requests")
            print(str(ex))

    """   MODIFY DATA   """

    @staticmethod
    def add_user_group_to_device_group(device_group_name, user_group_array=[], organization=Constant.AdvancedOrgName):
        """      
        @summary: Add User Groups to a Device Group   
        @param device_group_name: Device group name
        @param user_group_array: Array of user groups to be added
        @param organization: organization name
        @author: Thanh Le         
        @created_date: October 03, 2016  
        """
        try:
            for user_group in user_group_array:
                response = DeviceGroupAPI.add_user_group(device_group_name, user_group, organization)
                if(response.status_code != 201):
                    raise Exception("Error while adding User Group {} to Device Group {} for Organization {}. Reason: {}".format(user_group, device_group_name, organization, response.reason))
        except Exception as ex:
            raise Exception("Error while updating device group. Message: " + str(ex))

    
    @staticmethod
    def set_organization_setting(setting_name, setting_value, organization=Constant.AdvancedOrgName):
        """
        @summary: Set setting of organization
        @param setting_name: these values "organization name/default invite message/email notifications"
        @param setting_value: setting value
        @param organization: organization name
        @author: Thanh Le         
        @created_date: October 03, 2016  
        """
        try:
            response = OrganizationSettingAPI.update_an_organization_setting(setting_name, setting_value, organization)
            if(response.status_code != 200):
                raise Exception("Error while Update Organization Setting. Reason: {}".format(response.reason))
        except Exception as ex:
            print("Error: Cannot re-set {} to {} for organization {}.".format(setting_name, setting_value, organization))
            print(str(ex))

    
    @staticmethod
    def set_advanced_device_group_admin(user_email, device_group_name, organization):
        """      
        @summary: Set device for group device   
        @param user_email: email of user need to set device group admin
        @param device_group_name: device group name
        @param organization: organization name   
        @author: Thanh Le         
        @created_date: October 03, 2016        
        """
        response = DeviceGroupAPI.set_advanced_device_group_admin([user_email], device_group_name, organization)
        if(response.status_code != 200):
            raise Exception("Error while granting Device Group Admin permission for user {}. Reason: {}".format(user_email, response.reason))
    
    
    @staticmethod
    def set_language(driver, user, watched_video=True):
        """      
        @summary: Set language for user 
        @param driver: Webdriver
        @param user: user to be created
        @param watched_video: True if the user watched video, False if the user did not watch video
        @author: Khoi Ngo    
        @created_date: October 03, 2016         
        """
        login_page = TestCondition.force_log_out(driver).goto_login_page()
        if watched_video:
            after_login_page = login_page.login(user.email_address, user.password)
        else:
            after_login_page = login_page.login_as_unwatched_video_user(user.email_address, user.password)
         
        after_login_page.goto_your_account()\
            .set_language(driver.driverSetting.language)\
            .save_change()\
            .logout() 


    @staticmethod
    def set_advanced_beam_reservation_permisson(beam, reservation_permission):
        """
        @summary: set advanced beam reservation permission
        @param beam: beam object
        @param reservation_permission: reservation permission
        @author: thanh le
        @created: February 14 2017
        """
        permission_dict = {'Allowed':'allowed', 'By Request':'request_only', 'By Administrator':'admins_only', 'Not Allowed':'not_allowed'}
        try:
            TestCondition._update_advanced_beam_device(beam.beam_id, "reservations", permission_dict[reservation_permission], beam.beam_org)
        except Exception as ex:
            print("Error: Cannot set reservation permission for Beam {}.".format(beam.beam_name))
            print(str(ex))
    
    
    @staticmethod
    def restore_advanced_beam_name(beam):
        """
        @summary: restore advanced beam name 
        @param beam: beam obj
        @author: thanh.viet.le
        @created : October 01 2016 
        """
        try:
            TestCondition._update_advanced_beam_device(beam.beam_id, "name", beam.beam_name, beam.beam_org)
        except Exception as ex:
            print("Error: Cannot rename Beam {} to default".format(beam.beam_name))
            print(str(ex))
    
        
    @staticmethod
    def restore_advanced_beam_location(beam, location):
        """
        @summary: Restore advanced beam name 
        @param beam: beam obj
        @param location: location of beam
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            TestCondition._update_advanced_beam_device(beam.beam_id, "location", location)
        except Exception as ex:
            print("Error: Cannot restore location of Beam {} to default".format(beam.beam_name))
            print(str(ex))
        
            
    @staticmethod
    def restore_advanced_beam_labels(beam, label_array):
        """
        @summary: Restore advanced beam label 
        @param beam: beam obj
        @param label: Label of beam 
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            TestCondition._update_advanced_beam_device(beam.beam_id, "labels", label_array)
        except Exception as ex:
            print("Error: Cannot restore labels of Beam {} to default".format(beam.beam_name))
            print(str(ex))
        
            
    @staticmethod
    def restore_simplified_beam_name(beam):
        """
        @summary: Restore simplified beam name 
        @param driver: WebDriver 
        @param beam: Obj of beam
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            TestCondition._update_simplified_beam_device(beam, "name", beam.beam_name)
        except Exception as ex:
            print("Error: Cannot rename Beam {} to default".format(beam.beam_name))
            print(str(ex))
    
    
    @staticmethod
    def restore_simplified_beam_labels(beam, label_tag_list):
        """
        @summary: Restore simplified beam label
        @param driver: WebDriver 
        @param beam: Obj of beam
        @param label_tag_list: Label of beam
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            TestCondition._update_simplified_beam_device(beam, "labels", label_tag_list)
        except Exception as ex:
            print("Error: Cannot restore labels of Beam {} to default".format(beam.beam_name))
            print(str(ex))
        
    
    @staticmethod
    def restore_simplified_beam_location(beam, location):
        """
        @summary: Restore simplified beam location 
        @param driver: WebDriver 
        @param beam: Obj of beam
        @param location: location of beam 
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            TestCondition._update_simplified_beam_device(beam, "location", location)
        except Exception as ex:
            print("Error: Cannot restore location of Beam {} to default".format(beam.beam_name))
            print(str(ex))
        

    @staticmethod
    def prepare_unallowed_gsso_accounts(driver, organization = Constant.SimplifiedOrgName):
        """
        @summary: Add unallowed google acc to google_acc _unallow_st json file
        @param driver: WebDriver 
        @param organization: organization's name
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            data_file = open(TestCondition.UNALLOWED_GSSO_RESOURCE, "w")
            data_file.write(json.dumps({"objects": [Constant.UnallowedGSSOEmails]}))
        except:
            raise Exception("Error while preparing unallowed gsso accounts")
        finally:
            data_file.close()
            
            
    @staticmethod
    def prepare_allowed_gsso_accounts(driver, organization = Constant.SimplifiedOrgName):
        """
        @summary: Add allowed google acc to google_accs_allow_st resources file
        @param driver: WebDriver 
        @param organization: organization's name
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            data_file = open(TestCondition.GSSO_AND_NON_GSSO_RESOURCE, "w")
            data_file.write(json.dumps({"objects": [Constant.AllowedGSSOEmails]}))
        except:
            raise Exception("Error while preparing allowed gsso accounts")
        finally:
            data_file.close()
    
    
    @staticmethod
    def get_and_lock_an_allow_st_email():
        """
        @summary: Get allow email from data file (GSSO_AND_NON_GSSO_RESOURCE)
        @return: allow email
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        return TestCondition._get_and_lock_a_line(TestCondition.GSSO_AND_NON_GSSO_RESOURCE)
    
    
    @staticmethod
    def release_an_allow_st_email(email):
        """
        @summary: Release file data contains allow email by enter the email to value
        @param email: email address 
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            if email:
                TestCondition._unlock_a_line(TestCondition.GSSO_AND_NON_GSSO_RESOURCE, email)
        except Exception as ex:
            print("Error: Cannot release an allow ST email {}".format(email))
            print(str(ex))
            
    
    @staticmethod
    def get_and_lock_an_unallow_st_email():
        """
        @summary: Get unallow email from google_accs_unallow_st.json file
        @return: unallow st email
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        return TestCondition._get_and_lock_a_line(TestCondition.UNALLOWED_GSSO_RESOURCE)
    
    
    @staticmethod
    def release_an_unallow_st_email(email):
        """
        @summary: Release file data contains email by enter the email to value
        @param email: email address 
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            return TestCondition._unlock_a_line(TestCondition.UNALLOWED_GSSO_RESOURCE, email)
        except Exception as ex:
            print("Error: Cannot release an unallow ST email {}".format(email))
            print(str(ex))
    
    
    @staticmethod
    def get_and_lock_org_authentication():
        """
        @summary: Get authentication from data file (ORG_AUTHENTICATION_RESOURCE)
        @return: authentication
        @author: Khoi Ngo
        @created_date : October 03, 2017
        """
        return TestCondition._get_and_lock_a_line(TestCondition.ORG_AUTHENTICATION_RESOURCE)


    @staticmethod
    def release_org_authentication(auth):
        """
        @summary: Release file data contains allow email by enter the email to value
        @param email: email address
        @author: Thanh Le
        @created_date : October 03, 2017
        """
        try:
            return TestCondition._unlock_a_line(TestCondition.ORG_AUTHENTICATION_RESOURCE, auth)
        except Exception as ex:
            print("Error: Cannot release {}".format(auth))
            print(str(ex))


    @staticmethod
    def active_user_with_new_gmail(driver, user, is_simplified=False):
        """
        @summary: Active new account registry by a new gmail. Active via Gmail UI  
        @param driver: WebDriver
        @param user: user needs to active
        @param is_simplified: True is simplified user, True is advanced user
        @author: Thanh Le
        @created_date : October 03, 2016   
        """
        activation_link = GmailSignInPage(driver)\
            .open()\
            .log_in_gmail(user.email_address, user.password)\
            .goto_gmail_inbox_page(driver).get_active_link_email()

        account_settings_page = PasswordSetupPage(driver, activation_link).set_password(user.password)\
                    .goto_account_settings_page_by_menu_item()\
                    .set_language(driver.driverSetting.language)
                    
        user.activated = True
        
        if is_simplified:
            account_settings_page.set_first_last_name(user)
                
        account_settings_page.save_change()                
    
    
    @staticmethod
    def reopen_browser(driver):
        """      
        @summary: Reopen browser   
        @param driver: WebDriver needs to quit
        @return: new driver
        @author: Thanh Le
        @created_date : October 03, 2016   
        """     
        driver.quit()
        new_driver = Driver.get_driver(DriverSetting().load())
        new_driver.maximize_window()
        return new_driver
    
    
    @staticmethod
    def is_device_group_exist(device_group_name, organization):
        """      
        @summary: Check device group is exist.   
        @param device_group_name: Device group name
        @param organization: Organization which device group is created
        @return: True: Device group exist / False: Device group doesn't exist
        @author: Khoi Ngo  
        @created_date : October 03, 2016   
        """
        response = DeviceGroupAPI.get_device_group_id(device_group_name, organization)
        if response is None:
            return False
        return True
    
    
    @staticmethod
    def force_log_out(driver):
        """      
        @summary: Log out   
        @param driver: WebDriver 
        @return: home page
        @author: Thanh Le    
        @created_date : October 03, 2016        
        """
        try:
            return SignoutCompletePage(driver).open()
        except Exception as ex:
            driver.save_screenshot()
            raise Exception("Error: Cannot logout from Suitabletech: " + str(ex))
        
    
    """   PRIVATE METHODS   """
    
    @staticmethod
    def _remove_beam_from_connected_app(driver, user):
        """      
        @summary: Remove beam connected app out of account google   
        @param driver: WebDriver
        @param user: acc google
        @author: Thanh Le    
        @created_date : October 03, 2016         
        """          
        GmailSignInPage(driver).open().log_in_gmail(user.email_address, user.password)
        apps_connected_page = AppsConnectedPage(driver).open()
        if apps_connected_page.is_beam_connected():
            apps_connected_page.remove_beam_from_connected_apps()
    
            
    @staticmethod
    def _get_api_key(organization_name):
        """      
        @summary: Get api key of organization
        @param organization_name: organization name 
        @return: organization's api key   
        @author: Thanh Le       
        @created_date : October 03, 2016
        """
        return Constant.APIKeys[organization_name]
    
    
    @staticmethod
    def _re_get_access_token():
        """      
        @summary: Get access token
        @param driver: WebDriver 
        @return: access token
        @author: Thanh Le       
        @created_date : October 03, 2016   
        """
        TestCondition.SIMPLIFIED_ACCESS_TOKEN = ""
        return TestCondition._get_access_token()


    @staticmethod
    def _set_access_token(email, password):
        """      
        @summary: Set access token
        @param driver: WebDriver
        @param admin_email: admin's email address
        @param admin_password: admin's password
        @author: Thanh Le       
        @created_date : October 03, 2016   
        """
        TestCondition.SIMPLIFIED_ACCESS_TOKEN = ""
        session = requests.Session()
        UserAPI.login_account(email, password, session)
        TestCondition.SIMPLIFIED_ACCESS_TOKEN = UserAPI.set_access_token(session)
        
    
    @staticmethod
    def _get_access_token(timeout=30):
        """      
        @summary: Get access token
        @param timeout: waiting time is to get access token
        @return: access token
        @author: Thanh Le       
        @created_date : October 03, 2016   
        """
        sw = Stopwatch()
        sw.start()
        
        while(timeout > 0):
            if(TestCondition.SIMPLIFIED_ACCESS_TOKEN == ""):
                TestCondition._set_access_token(Constant.SimplifiedAdminEmail, Constant.DefaultPassword)
            response = UserAPI.get_info(Constant.SimplifiedOrgName, TestCondition.SIMPLIFIED_ACCESS_TOKEN)
            if(response.status_code == 200):
                return TestCondition.SIMPLIFIED_ACCESS_TOKEN
            elif(response.status_code == 401):
                TestCondition._set_access_token(Constant.SimplifiedAdminEmail, Constant.DefaultPassword)
            
            timeout -= sw.elapsed().total_seconds()
        
        raise Exception("Cannot get access token with account: {}/{}".format(Constant.SimplifiedAdminEmail, Constant.DefaultPassword))
        
    
    @staticmethod        
    def _create_advanced_normal_user(user):
        """      
        @summary: Create new advanced normal user   
        @param user: user to be created
        @author: Thanh Le       
        @created_date : October 03, 2016   
        """
        response = UserAPI.invite_advanced_user(user)
        if(response.status_code != 201):
            raise Exception("Error while creating advanced user {}. Reason: {}".format(user.tostring(), response.reason))
            

    @staticmethod        
    def _create_simplified_normal_user(user, beam_id, organization):
        """      
        @summary: Create new simplified normal user   
        @param driver: WebDriver
        @param user: user to be created
        @param device_name: device name
        @param organization: organization name
        @author: Thanh Le       
        @created_date : October 03, 2016     
        """
        count = 0
        while count<5:
            response = UserAPI.invite_simplified_user(user, beam_id, organization, TestCondition.SIMPLIFIED_ACCESS_TOKEN)
            if(response.status_code == 201):
                break
            count = count + 1
            
        if(response.status_code != 201):
            raise Exception("Error while creating simplified user {}. Reason: {}".format(user.tostring(), response.reason))

      
    @staticmethod
    def _activate_user(driver, user, pass_safety_video=True, email_subject="Welcome to Beam at"):
        """      
        @summary: Activate new user  
        @param driver: WebDriver 
        @param user: user to be activated
        @param is_temporary: Set to False if activate normal user. Set to True if activate temporary user
        @param is_simplified: Set to False if advanced user. Set to True if simplified user
        @author: Thanh Le       
        @created_date : October 03, 2016     
        """
        try:
            if not user.activated:
                # NOTE: creating user using API always sent email in English. Thus hardcode the email subjects.
                activation_link = GmailUtility.get_email_activation_link(email_subject=email_subject, receiver=user.email_address, sent_day=datetime.now())
                     
                TestCondition._set_password_for_new_user(activation_link, user, pass_safety_video)
                TestCondition.login_and_change_language_using_api(user.email_address, user.password, driver.driverSetting.language)
                
                # set user activated
                user.activated = True
                print("User {} is created with FN is {} and LN is {}.".format(user.email_address, user.first_name, user.last_name))
        except:
            raise Exception("Error while activating and setting language for user {}".format(user.email_address))
    
    
    @staticmethod
    def _get_user_temporary_password(user, is_temporary=False, localize=False):
        """
        @summary: Activate new user
        @param driver: WebDriver
        @param user: user to be activated
        @param is_temporary: Set to False if activate normal user. Set to True if activate temporary user
        @param is_simplified: Set to False if advanced user. Set to True if simplified user
        @author: Thanh Le
        @created_date : October 03, 2016
        """
        try:
            if not is_temporary:
                temporary_password = GmailUtility.get_temporary_password_for_normal_user(receiver=user.email_address, sent_day=datetime.now(), localize = localize)
            else:
                temporary_password = GmailUtility.get_temporary_password_for_temporary_user(receiver=user.email_address, sent_day=datetime.now(), localize = localize)
            return temporary_password
        except:
            raise Exception("Error while getting password for user {}".format(user.email_address))


    @staticmethod
    def _activate_user_temporary_password(driver, user, pass_safety_video = False, is_temporary=False, is_simplified=False, localize=False):
        """      
        @summary: Activate new user  
        @param driver: WebDriver 
        @param user: user to be activated
        @param is_temporary: Set to False if activate normal user. Set to True if activate temporary user
        @param is_simplified: Set to False if advanced user. Set to True if simplified user
        @author: Thanh Le       
        @created_date : October 03, 2016     
        """
        try:
            if not user.activated:
                # NOTE: creating user using API always sent email in English. Thus hardcode the email subjects.
                if not is_temporary:
                    if localize:
                        temporary_password = GmailUtility.get_temporary_password_for_normal_user(receiver=user.email_address, sent_day=datetime.now(), localize = localize)
                    else:
                        temporary_password = GmailUtility.get_temporary_password_for_normal_user(email_subject="Welcome to Beam at", receiver=user.email_address, sent_day=datetime.now())
                else:
                    if localize:
                        temporary_password = GmailUtility.get_temporary_password_for_temporary_user(receiver=user.email_address, sent_day=datetime.now())
                    else:
                        temporary_password = GmailUtility.get_temporary_password_for_temporary_user(email_subject="You've been invited to Beam", receiver=user.email_address, sent_day=datetime.now(), localize = localize)
                
                TestCondition._set_up_password_and_change_language_simplified_user(user, temporary_password, driver.driverSetting.language, pass_safety_video = False)
             
                # set user activated
                user.activated = True
                print("User {} is created.".format(user.email_address))
     
        except:
            raise Exception("Error while activating and setting language for user {}".format(user.email_address))
    
    
    @staticmethod
    def _set_password_for_new_user(activation_link, user, pass_safety_video):
        """
        @summary: This method is to set password for new advanced normal user
        @param activation_link: activation link is got from welcome email
        @param password: password 
        @author: Thanh Le       
        @created_date : October 03, 2016            
        """
        UserAPI.set_password(activation_link, user, pass_safety_video)

        
    @staticmethod
    def _set_up_password_and_change_language_simplified_user(user, temporary_password, language, pass_safety_video):
        """
        @summary: Change password to activate a simplified user
        @param email: email of simplified user
        @param temporary_password: temporary password is got from welcome email
        @param new_password: password that user wants to change
        @author: Thanh Le       
        @created_date : October 03, 2016    
        """
        session = requests.Session()
        response_1 = UserAPI.login_account(user.email_address, temporary_password, session)
        UserAPI.change_password(temporary_password, user, session, response_1, pass_safety_video = False)
        
        #TODO: Handle bug INFR-2573
        session_2 = requests.Session()
        response_2 = UserAPI.login_account(user.email_address, user.password, session_2)
        UserAPI.pass_safety_video(user, session_2, response_2)
        
        access_token = UserAPI.set_access_token(session_2)
        UserAPI.change_language(access_token, language, session_2)
        
       
    @staticmethod
    def _update_advanced_beam_device(beam_id, beam_property, property_value, organization=Constant.AdvancedOrgName):
        """
        @summary: Update advanced beam device
        @param beam_name: Original Beam Device Name
        @param beam_property: only choosing - name,location,labels,time zone,group
        @param property_value: value of edit property
        @param organization: The Organization which device was located.
        @author: Thanh Le       
        @created_date : October 03, 2016    
        """
        response = DeviceAPI.edit_advanced_device(beam_id, beam_property, property_value, organization)  
        
        if(response.status_code != 200):
            raise Exception("Error while updating {} property of beam {}. Reason: {}".format(beam_property, beam_id, response.reason))

    
    @staticmethod
    def _update_simplified_beam_device(beam, beam_property, property_value):
        """
        @summary: Update simplified beam device
        @param driver: WebDriver 
        @param beam_name: Original Beam Device Name
        @param beam_property: only choosing - name,location,labels
        @param property_value: value of edit property
        @param organization: The Organization which device was located.
        @author: Thanh Le       
        @created_date : October 03, 2016
        """
        response = DeviceAPI.edit_simplified_device(beam.beam_id, DeviceAPI.property_dict[beam_property], property_value, beam.beam_org, TestCondition._get_access_token())    
        
        if(response.status_code != 200):
            raise Exception("Error while updating {} property of beam {}. Reason: {}".format(beam_property, beam.beam_name, response.reason))
            
    
    @staticmethod
    def _get_and_lock_a_line(data_file_path):
        """
        @summary: Get and lock (remove data out of file) a line in file resource 
        @param data_file_path: file path of data file
        @return: value
        @author: Thanh Le       
        @created_date : October 03, 2016       
        """
        with TestCondition.RLOCK:
            return_value = None
            
            try:
                data_file = open(data_file_path, "r+")
                timeout = TestCondition.RESOURCE_WAIT_TIMEOUT
                sw = Stopwatch()
                sw.start()
                
                while not return_value and sw.elapsed().total_seconds() < timeout:
                    data = json.load(data_file)
                    items = data["objects"]
                    
                    if(len(items) > 0):
                        return_value = items.pop(0)
                        data_file.seek(0)
                        data_file.write(json.dumps(data))
                        data_file.truncate()
                        break
                    else:
                        data_file.close()
                        sleep(TestCondition.RESOURCE_POLLING_INTERVAL)
                        data_file = open(data_file_path, "r+")
                    
                if(not return_value):
                    raise Exception("There is no resource available after waiting for {} seconds.".format(timeout))
                else:
                    print("ACQUIRED RESOURCE >>> " + return_value)
            except:
                raise Exception("Error while modifying resource " + data_file_path)
            finally:
                data_file.close()
            
        return return_value
    
    
    @staticmethod
    def _unlock_a_line(data_file_path, value):
        """
        @summary: Unlock file by enter the value  
        @param data_file_path: file path of data file
        @param value: value to enter 
        @author: Thanh Le       
        @created_date : October 03, 2016  
        """
        with TestCondition.RLOCK:
            if value:
                try:
                    data_file = open(data_file_path, "r+")
                    data = json.load(data_file)
                    data["objects"].append(value)
                    data_file.seek(0)
                    data_file.write(json.dumps(data))
                    data_file.truncate()
                    print("RELEASE RESOURCE >>> " + value)
                except:
                    raise Exception("Error while modifying resource " + data_file_path)
                finally:
                    data_file.close()
                    
    
    @staticmethod
    def approve_reservation(calendar_client, reservation):
        """
        @summary: this method to change status of a reservation from request to confirmed
        @param reservation_id: id of reservation that need to change status
        @author: Thanh Le
        @created : February 16 2017 
        """
        try:
            event_id = Calendar_Utilities.get_event_id(calendar_client, reservation)
            event_info = ReservationAPI._get_event_info(event_id)
            ReservationAPI._update_status_for_event(event_id, event_info, 'confirmed')
            sleep(1)
        except Exception as ex:
            print("Error: Cannot update status for reservation")
            print(str(ex))
            
            
    @staticmethod
    def reject_reservation(calendar_client, reservation):
        """
        @summary: this method to change status of a reservation from request to confirmed
        @param reservation_id: id of reservation that need to change status
        @author: Thanh Le
        @created : February 16 2017 
        """
        try:
            event_id = Calendar_Utilities.get_event_id(calendar_client, reservation)
            event_info = ReservationAPI._get_event_info(event_id)
            ReservationAPI._update_status_for_event(event_id, event_info, 'rejected')
            sleep(1)
        except Exception as ex:
            print("Error: Cannot update status for reservation")
            print(str(ex))
   
   
#================================================= BEAM OBJEST==========================================================================================
    @staticmethod
    def get_and_lock_beam(org):
        """
        @summary: Get beam from resource file
        @param org: Org Name to get beam 
        @param lock: Lock=True if want to lock (remove data out of file) a line in file resource, Lock=False if only get a Beam 
        @return: available beam
        @author: Thanh Le
        @created:  October 03, 2016 
        """
        return TestCondition._get_and_lock_a_beam(TestCondition.BEAM_RESOURCE, org)


    @staticmethod
    def get_a_beam(org):
        """
        @summary: Get beam from resource file and the info of beam is not removed from file
        @param org: Org Name to get beam 
        @return: beam
        @author: Thanh Le
        @created:  October 03, 2017 
        """
        return TestCondition._get_and_lock_a_beam(TestCondition.INFO_BEAM_RESOURCE, org, lock=False)


    @staticmethod
    def get_and_lock_a_physical_beam(beam_name):
        """
        @summary: Get physical beam from resource file and the info of beam is removed from file
        @param org: Org Name to get beam 
        @return: beam
        @author: Thanh Le
        @created:  October 03, 2017 
        """
        return TestCondition._get_and_lock_a_physical_beam(TestCondition.BEAM_RESOURCE, beam_name)   
        
        
    @staticmethod
    def _get_and_lock_a_beam(data_file_path, beam_org, lock=True):
        """
        @summary: Get and lock (remove data out of file) a line in file resource 
        @param data_file_path: file path of data file
        @param beam_org: Org contain beams
        @param lock: True if want to lock (remove data out of file) a line in file resource, False if only get beam
        @return: beam 
        @author: Thanh Le       
        @created_date : October 03, 2016       
        """
        with TestCondition.RLOCK:
            from data_test.dataobjects.beam import Beam
            return_value = None
            
            try:
                data_file = open(data_file_path, "r+")
                timeout = TestCondition.RESOURCE_WAIT_TIMEOUT
                sw = Stopwatch()
                sw.start()
                 
                while not return_value and sw.elapsed().total_seconds() < timeout:
                    data_file.close()
                    sleep(TestCondition.RESOURCE_POLLING_INTERVAL)
                    data_file = open(data_file_path, "r+")
                    data = json.load(data_file)
                    items = data["objects"]
                    random.shuffle(items)
                    if(len(items) > 0):
                        for index, item in enumerate(items):
                            if item["org"] == beam_org:
                                print(index)
                                return_value = Beam()
                                return_value.initialize(item["id"], item["name"], item["org"])
                                if(lock):
                                    del items[index]
                                    data_file.seek(0)
                                    data_file.write(json.dumps(data))
                                    data_file.truncate()
                                    break
                                else:
                                    break
                    
                if not return_value:
                    print("There is no resource available after waiting for {} seconds.".format(timeout))
                    raise Exception("There is no resource available after waiting for {} seconds.".format(timeout))
                else:
                    if lock:
                        print("ACQUIRED RESOURCE >>> " + return_value.beam_name)
            except:
                raise Exception("Error while modifying resource " + data_file_path)
            finally:
                data_file.close()
            
        return return_value
    
    
    @staticmethod
    def _get_and_lock_a_physical_beam(data_file_path, beam_name, lock=True):
        """
        @summary: Get and lock a line in file resource 
        @param data_file_path: file path of data file
        @param beam_name: beam name
        @param lock: True if want to lock (remove data out of file) a line in file resource, False if only get beam
        @return: beam 
        @author: Thanh Le       
        @created_date : October 03, 2016       
        """
        with TestCondition.RLOCK:
            from data_test.dataobjects.beam import Beam
            return_value = None
            
            try:
                data_file = open(data_file_path, "r+")
                timeout = TestCondition.RESOURCE_WAIT_TIMEOUT
                sw = Stopwatch()
                sw.start()
                
                while not return_value and sw.elapsed().total_seconds() < timeout:
                    data_file.close()
                    sleep(TestCondition.RESOURCE_POLLING_INTERVAL)
                    data_file = open(data_file_path, "r+")
                    data = json.load(data_file)
                    items = data["objects"]
                    if(len(items) > 0):
                        for index, item in enumerate(items):
                            if item["name"] == beam_name:
                                print(index)
                                return_value = Beam()
                                return_value.initialize(item["id"], item["name"], item["org"])
                                if(lock):
                                    del items[index]
                                    data_file.seek(0)
                                    data_file.write(json.dumps(data))
                                    data_file.truncate()
                                    break
                                else:
                                    break
                    
                if(not return_value.beam_name):
                    raise Exception("There is no resource available after waiting for {} seconds.".format(timeout))
                else:
                    print("ACQUIRED RESOURCE >>> " + return_value.beam_name)
            except:
                raise Exception("Error while modifying resource " + data_file_path)
            finally:
                data_file.close()
            
        return return_value
    
    
    @staticmethod
    def release_a_beam(beam):
        """
        @summary: Release beam to resource file
        @param beam: Beam obj 
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            if beam:
                TestCondition._unlock_a_beam(TestCondition.BEAM_RESOURCE, beam)
            else:
                print("The testcase does not get any beam")
        except Exception as ex:
            print("Error: Cannot release Beam {}".format(beam.beam_name))
            print(str(ex))
    
    
    @staticmethod
    def _unlock_a_beam(data_file_path, beam):
        """
        @summary: re-add beam locked to resource file
        @param data_file_path: file path of data file
        @param beam: beam obj
        @author: Thanh Le       
        @created_date : October 03, 2016  
        """
        with TestCondition.RLOCK:
            if beam:
                try:
                    data_file = open(data_file_path, "r+")
                    data = json.load(data_file)
                    data["objects"].append({"name": beam.beam_name, "org": beam.beam_org, "id": beam.beam_id})
                    data_file.seek(0)
                    data_file.write(json.dumps(data))
                    data_file.truncate()
                    print("RELEASE RESOURCE >>> " + beam.beam_name)
                except:
                    raise Exception("Error while modifying resource " + data_file_path)
                finally:
                    data_file.close()
    
    @staticmethod
    def prepare_beam_resources(driver):
        """
        @summary: Get and add all beam to beam resources file
        @param organization: organization's name
        @author: Thanh Le
        @created_date : October 03, 2016 
        """
        try:
            access_token = TestCondition._get_access_token()
            data_file_1 = open(TestCondition.BEAM_RESOURCE, "w")
            data_file_2 = open(TestCondition.INFO_BEAM_RESOURCE, "w")
            items = []
            for i in range(3):
                if Constant.OrgName[i+1] != Constant.SimplifiedOrgName:
                    response = DeviceAPI.get_devices(Constant.OrgName[i+1])
                    for item in response.json()["objects"]:
                        items.append({"name": item["name"], "org": Constant.OrgName[i+1], "id": item["id"]})
                        
                else:
                    response = DeviceAPI.get_simplified_devices(Constant.OrgName[i+1], access_token)
                    for item in response.json()["objects"]:
                        items.append({"name": item["name"], "org": Constant.OrgName[i+1], "id": str(item["device_group"])})
             
            data_file_1.write(json.dumps({"objects": items}))
            data_file_2.write(json.dumps({"objects": items}))    
        except:
            raise Exception("Error while preparing advanced Beam resources")
        finally:
            data_file_1.close()
            data_file_2.close()


    @staticmethod
    def prepare_locales_resource(platform):
        """
        @summary: Write locales to resource file
        @param platform: running platform
        @author: Khoi.Ngo
        @Created_date: May 29, 2018
        """
        with open(TestCondition.LOCALES_RESOURCE, "w") as locales_file:
            if platform == Platform.MAC or platform == Platform.IOS:
                locales_file.write("""{"US" : "en_US.UTF-8", "FR" : "fr_FR.UTF-8"}""")
            else:
                locales_file.write("""{"US" : "us", "FR" : "fra"}""")


    @staticmethod
    def change_authentication_to_BeamOrGoogleAccount(organization=Constant.AdvancedOrgName):
        """
        @summary: Change authentication method to Beam or/and Google Account
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        response = OrganizationSettingAPI.change_authentication_to_BeamOrGoogleAccount(organization)
        if(response.status_code != 200):
            raise Exception("Error while changing authentication method. Reason: {}".format(response.reason))


    @staticmethod
    def change_authentication_to_OneLogin(organization=Constant.AdvancedOrgName):
        """
        @summary: Change authentication method to One Login
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        response = OrganizationSettingAPI.change_authentication_to_OneLogin(organization)
        if(response.status_code != 200):
            raise Exception("Error while changing authentication method. Reason: {}".format(response.reason))


    @staticmethod
    def change_authentication_to_Okta(organization=Constant.AdvancedOrgName):
        """
        @summary: Change authentication method to Okta
        @return: response http request
        @author: Khoi Ngo
        @created_date: October 9, 2017
        """
        okta_file = open(TestCondition.OKTA_XML_RESOURCE, 'r+')
        response = OrganizationSettingAPI.change_authentication_to_Okta(organization, okta_file.read())
        okta_file.close()
        if(response.status_code != 200):
            raise Exception("Error while changing authentication method. Reason: {}".format(response.reason))


    @staticmethod
    def invite_email_to_advance_org(driver, email):
        """
        @summary: invite accounts but do not active to org LogigearTest
        @author: Quang Tran
        @created_date: Nov 27, 2017
        """
        user = User()
        user.generate_advanced_normal_user_data()
        user.email_address = email
        user.first_name = ""
        user.last_name = ""
        TestCondition.create_advanced_normal_users(driver, [user], activate_user=False, pass_safety_video=False)


    @staticmethod
    def check_account_exitst(email, organization = Constant.AdvancedOrgName):
        """
        @summary: Check account exists or not, if not exists, it will invite account 
        @return: True if account exists
        @author: Quang Tran
        @created_date: Nov 27, 2017
        """
        response = UserAPI._get_user(email, organization)
        if (response.status_code == 200):
            return True


    @staticmethod
    def get_email_from_file_json(file_path_json_array):
        """
        @summary: Check account exists or not, if not exists, it will invite account
        @param file_path_json_array: list file json 
        @return: Return list email from list file json 
        @author: Quang Tran
        @created_date: Nov 27, 2017
        """
        list_email = []
        for file_path_json in file_path_json_array:
            data_file = open(file_path_json, "r+")
            data_file = json.load(data_file)
            list_email.append(data_file["objects"][0])
        return list_email


    @staticmethod
    def delete_all_reservation_in_device_group(device_group_name, organization = Constant.AdvancedOrgName):
        """
        @summary: delete all reservation in a device group
        @param device_group_name: name of device group
        @author: Quang Tran
        @created_date: Dec 27, 2017
        """
        try:
            id_of_reservations = DeviceGroupAPI().get_id_of_reservations_of_device_group(device_group_name, organization)
            ReservationAPI.delete_reservations(id_of_reservations, organization)
        except:
            raise Exception("Error while delete all reservation")


    @staticmethod
    def get_name_all_beams(beam_org):
        """
        @summary: get name of all beams in org
        @param beam_org: organization
        @return: list of name beam
        @author: Quang Tran
        @created_date: Dec 27, 2017
        """
        try:
            beams_array = []
            data_file = open(TestCondition.INFO_BEAM_RESOURCE, "r+")
            data = json.load(data_file)
            data_file.close()
            items = data["objects"]
            for item in items:
                if item["org"] == beam_org:
                    beams_array.append(item["name"])
            return beams_array
        except:
            raise Exception("Error while get beam at " + TestCondition.INFO_BEAM_RESOURCE)


    @staticmethod
    def setting_primary_contact_default(organization=Constant.AdvancedOrgName):
        """
        @summary: this API setting primary contact to default
        @author: Quang Tran
        @created_date: Dec 9, 2017
        """ 
        try:
            data = json.dumps(Constant.PrimaryContactDefaultInfo)
            OrganizationSettingAPI.setting_primary_contact(organization, data)
        except:
            raise Exception("Error while setting primary contact default ")


    @staticmethod
    def clear_all_info_in_primary_contact(organization=Constant.AdvancedOrgName):
        """
        @summary: this API setting primary contact to default
        @author: Quang Tran
        @created_date: Dec 9, 2017
        """ 
        try:
            data = {
                        "contact_info": {
                            "last_name": "",
                            "phone": "",
                            "postal_code": "",
                            "city": "",
                            "first_name": "",
                            "country": "",
                            "state": "",
                            "company_name": "",
                            "job_title": "",
                            "address_line_2": "",
                            "email": "",
                            "address_line_1": ""
                        }
                    }
            OrganizationSettingAPI.setting_primary_contact(organization, json.dumps(data))
        except:
            raise Exception("Error while setting primary contact default ")
        
        
    @staticmethod
    def get_all_email_users(organization=Constant.AdvancedOrgName, temp_only=False):
        """
        @summary: this API get all temporary users
        @author: Quang Tran
        @created_date: Dec 19, 2017
        """ 
        try:
            return UserAPI.get_all_email_users(organization, temp_only)
        except:
            raise Exception("Error while getting all email of users ")


    @staticmethod
    def get_activity_time_range_for_status_in_call(time_range, organization=Constant.AdvancedOrgName):
        """
        @summary: this API get all info about acitvity
        @author: Quang Tran
        @created_date: Feb 13, 2018
        """ 
        response = DeviceActivityAPI.get_activity_time_range_status_in_call(time_range, organization)
        activity_info = response.json()["objects"]
        return activity_info

