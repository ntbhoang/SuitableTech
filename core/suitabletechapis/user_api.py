from common.constant import Constant
from core.suitabletechapis.api_base import APIBase
from core.suitabletechapis.device_group_api import DeviceGroupAPI
from core.suitabletechapis.user_group_api import UserGroupAPI
import json
from datetime import datetime
import requests
from lxml import html


class UserAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "users/"
    _non_temporary_url = Constant.APIBaseURL + "users/?include_temporary=false"
    _invite_url = Constant.APIBaseURL + "invite/"
    _temporary_access = Constant.APIBaseURL + "temporary-access/"
    _setting_url = Constant.SuitableTechURL + "/admin-api/2/settings/"
    _info_url = Constant.SuitableTechURL + "/admin-api/2/info/"
    _login_account = Constant.SuitableTechURL + "/accounts/login/"
    _access_token = Constant.SuitableTechURL + "/accounts/token/"

    @staticmethod
    def _convert_to_json(user, organization=Constant.AdvancedOrgName):
        """
        @summary: this method is used to create a json data for user
        @param user: user instance
        @param organization: org's name
        @return: json data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        device_groups = []
        user_groups = []
        
        if user.device_group:
            device_groups.append(DeviceGroupAPI.get_device_group_id(user.device_group, organization))
        if user.user_group:
            user_groups.append(UserGroupAPI.get_user_group_id(user.user_group, organization))
        
        data_object = {'email_address': user.email_address,
                       'from_name': user.organization,
                       'device_groups': device_groups,
                       'user_groups': user_groups}
        return json.dumps(data_object)
    
    
    @staticmethod
    def _get_user(user_email="", organization=Constant.AdvancedOrgName):
        """
        @summary: This API allows get info of user
        @param user_email: email user
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        if organization is None:
            organization = Constant.AdvancedOrgName
        return APIBase.get_method(url=UserAPI._baseurl.format(Constant.OrgsInfo[organization]) + user_email + '/', headers=APIBase.generate_header(organization))
    
    
    @staticmethod
    def _get_users(params="", organization=Constant.AdvancedOrgName):
        """
        @summary: This API allows get all users in org
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = UserAPI._baseurl.format(Constant.OrgsInfo[organization]) + '?' + params
        return APIBase.get_method(url=url, headers=APIBase.generate_header(organization))
    
    
    @staticmethod
    def _get_user_info_in_simplified_org(email):
        session = requests.Session()
        UserAPI.login_account(Constant.SimplifiedAdminEmail, Constant.DefaultPassword, session)
        access_token = UserAPI.set_access_token(session)
        
        url = UserAPI._baseurl.format(Constant.OrgsInfo[Constant.SimplifiedOrgName]) + email + '/'
        headers = { 'Authorization': access_token }
        return session.get(url=url, headers=headers)
        
    
    @staticmethod
    def delete_user(user_email="", organization=Constant.AdvancedOrgName):
        """
        @summary: this API allows delete user
        @param user_email: email user
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = UserAPI._baseurl.format(Constant.OrgsInfo[organization]) + user_email + '/'
        return APIBase.delete_method(url=url, headers=APIBase.generate_header(organization))


    @staticmethod
    def invite_advanced_user(user):
        """
        @summary: this API allows invite user on advance mode
        @param user: user instance
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        session = requests.Session()
        UserAPI.login_account(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword, session)
        access_token = UserAPI.set_access_token(session)
        headers = {'Content-Type': 'application/json', 'Authorization': access_token}
        return APIBase.post_method(url=UserAPI._invite_url.format(Constant.OrgsInfo[user.organization]), headers=headers, data=UserAPI._convert_to_json(user, user.organization))


    @staticmethod
    def invite_simplified_user(user, beam_id, organization, access_token):
        """
        @summary: this API allows invite a user on simplified mode
        @param user: user instance
        @param beam_id: device's id
        @param organization: org's name
        @param access_token: access token after logging account
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        data = json.dumps({'email_address': user.email_address, 'device_groups': [beam_id]})
        return APIBase.post_method(url=UserAPI._invite_url.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization), data=data)
  
    
    @staticmethod
    def invite_new_temporary_user(user, device_group, start_date, end_date, answer_required):
        """
        @summary: This API allows invite a temporary user
        @param user: user instance
        @param device_group: device's name
        @param start_date: date start
        @param end_date: date end
        @param answer_required: answer for question
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        
        _device_group_id = DeviceGroupAPI.get_device_group_id(device_group, user.organization)
        _start_date = datetime.strftime(start_date, "%Y-%m-%dT%H:%M:%S")
        _end_date = datetime.strftime(end_date, "%Y-%m-%dT%H:%M:%S")
        data_object = {'email_address':user.email_address, 'device_group': _device_group_id, 'start': _start_date, 'end': _end_date, 'answer_required': answer_required}
        data = json.dumps(data_object)
        headers = { 'Content-Type': 'application/json' }
        headers.update(APIBase.generate_header(user.organization))
        return APIBase.post_method(url=UserAPI._temporary_access.format(Constant.OrgsInfo[user.organization]), headers=headers, data=data)
    
    
    @staticmethod
    def set_org_admin(user, organization=Constant.AdvancedOrgName):
        """
        @summary: this API allows set admin for org
        @param user_email: email user
        @param organization: org's name
        @return:response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        data = json.dumps({'is_admin': True,
                           'first_name':user.first_name,
                           'last_name':user.last_name })
        return APIBase.patch_method(UserAPI._baseurl.format(Constant.OrgsInfo[organization]) + user.email_address + "/", headers=APIBase.generate_header(organization, 'application/json'), data=data)
    
    
    @staticmethod
    def delete_all_users(keyword="logigear1+user", organization=Constant.AdvancedOrgName):
        """
        @summary: this method allows delete all users in org
        @param keyword: specific text into email user (e.g: logigear1+user20161312@logigear.com --> keyword = logigear1+user)
        @param organization: org's name
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        response = UserAPI._get_users("", organization)

        for item in response.json()["objects"]:
            if keyword in item["email_address"]:
                UserAPI.delete_user(item["email_address"], organization)
                print("Deleting User: {}".format(item["email_address"]))
     
                
    @staticmethod
    def get_info(organization, access_token):
        """
       @summary: this API to get information of Simplified Org
       @param organization: org's name
       @param access_token: access token after logging account
       @author: Thanh Le
       @created_date: August 05, 2016
       """

        return APIBase.get_method(url=UserAPI._info_url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization))
       
       
    @staticmethod    
    def set_password(activation_link, user, pass_safety_video):
        """
       @summary: this API to set password for new user
       @param activation_link: activation_link
       @param password: password
       @author: Thanh Le
       @created_date: May 29, 2017
       """
        session = requests.Session()
        response_1 = session.get(activation_link)
        if(response_1.status_code != 200):
            raise Exception("Error while getting token at activation page. Reason: {}".format(response_1.reason))
            return
        csrfmiddlewaretoken_1 = html.fromstring(response_1.text).xpath("//*[@name='csrfmiddlewaretoken']")[0].value
          
        headers_1 = {"Referer":activation_link}
        data_1 = {"csrfmiddlewaretoken":csrfmiddlewaretoken_1, "new_password1":user.password, "new_password2":user.password}
        response_2 = session.post(activation_link, headers = headers_1, data = data_1)
        if(response_2.status_code != 200):
            raise Exception("Error while setting password for new user. Reason: {}".format(response_2.reason))
        
        if pass_safety_video:
            UserAPI.pass_safety_video(user, session, response_2)
    
    
    @staticmethod    
    def change_password(old_password, user, session, response, pass_safety_video):
        """
       @summary: this API to set password for new user
       @param user: user needs to change password
       @param old_password: old_password
       @param new_password: new_password
       @author: Thanh Le
       @created: May 30, 2017
       """
        change_password_url = "https://stg1.suitabletech.com/accounts/password_change/"
        csrfmiddlewaretoken_1 = html.fromstring(response.text).xpath("//*[@name='csrfmiddlewaretoken']")[0].value
        
        header_change_password = {"Referer":change_password_url}
        data_change_password = {"csrfmiddlewaretoken":csrfmiddlewaretoken_1,
                      "new_password1":user.password,
                      "new_password2":user.password,
                      "old_password":old_password}
         
        response_2 = session.post(change_password_url, headers = header_change_password, data = data_change_password)
        
        if pass_safety_video:
            UserAPI.pass_safety_video(user, session, response_2)
    
    
    @staticmethod
    def pass_safety_video(user, session, response):
        """
       @summary: this API to pass safety for new user
       @param user: user needs to pass safety video
       @param session: session
       @param response: response
       @author: Tan Le
       @created: Dec 20, 2017
       """
        csrfmiddlewaretoken = html.fromstring(response.text).xpath("//*[@name='csrfmiddlewaretoken']")[0].value
        header = {"Referer":"https://stg1.suitabletech.com/welcome/"}
        data = {"csrfmiddlewaretoken":csrfmiddlewaretoken, "accept_risks":"on", "first_name":user.first_name, "last_name":user.last_name}
        response_video = session.post("https://stg1.suitabletech.com/welcome/", headers = header, data = data)
        if(response_video.status_code != 200):
            raise Exception("Error while passing safetyvideo. Reason: {}".format(response.reason))
        
        
    @staticmethod
    def login_account(email, password, session):
        r = session.get(UserAPI._login_account)
        csrfmiddlewaretoken = html.fromstring(r.text).xpath("//*[@name='csrfmiddlewaretoken']")[0].value
        
        headers = {'Referer':'https://stg1.suitabletech.com/accounts/login/?next=/accounts/home/'}
        form_data = {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'password': password,
            'username': email,
            'next': '/accounts/home/'
            }
        return session.post(url=UserAPI._login_account, headers=headers, data=form_data)
        
        
    @staticmethod
    def set_access_token(session):
        headers = {'X-CSRFToken': session.cookies['csrftoken'], 'Referer': 'https://stg1.suitabletech.com/manage/130/'}
        data = {
            'client_id': 'AaYV4palQjKafAN7BMyUQsuxuQEFGRLtGPzeL8dJ',
            'grant_type': 'password'
            }
        response = session.post(url=UserAPI._access_token, headers=headers, data=data)
        res = json.loads(response.text)
        
        return res['token_type'] + ' ' + res['access_token']
        
    
    @staticmethod
    def change_language(access_token, language, session):
        languages = {'ENGLISH': 'en', 'FRENCH': 'fr', 'JAPANESE': 'ja'}
        
        settings_info = UserAPI.get_account_settings_info(access_token, session)
        settings_info = json.loads(settings_info.text)
        settings_info['language'] = languages[language]
        if settings_info['first_name']=="" and settings_info['last_name']=="":
            del settings_info["first_name"]
            del settings_info["last_name"]
        data = json.dumps(settings_info)
        
        headers = {'Authorization': access_token, 'Content-Type':'application/json'}
        response = session.put(url=UserAPI._setting_url, headers=headers, data=data)
        if response.status_code != 200:
            raise Exception("Error while send request to change language for user.")


    @staticmethod
    def get_account_settings_info(access_token, session):
        headers = {'Authorization': access_token}
        return session.get(url=UserAPI._setting_url, headers=headers)
        
        
    @staticmethod
    def get_list_users(organization):
        response = UserAPI._get_users('include_temporary=false', organization)
        return response.json()["objects"]
    
    
    @staticmethod
    def get_list_users_base_domain(domain, organization):
        response = UserAPI._get_users('include_temporary=false', organization)
        arr_return = []
        for item in response.json()["objects"]:
            if domain in item["email_address"]:
                arr_return.append(item)
        return arr_return
    
    @staticmethod
    def get_displayed_name(user, simplified=False):
        """
        @summary: get user's display name
        @return: return user's display name = <firstname> <lastname>
        @author: Thanh.Viet.Le
        """        
        if simplified:
            user_info = UserAPI._get_user_info_in_simplified_org(user.email_address)
        else:
            user_info = UserAPI._get_user(user.email_address)     
        
        user_info_json = user_info.json()
        if user_info_json['first_name'] == '' and user_info_json['last_name'] == '':
            return user.email_address
        return user_info_json['first_name'] + ' ' +  user_info_json['last_name']
    
        
    @staticmethod
    def get_calendar_key(access_token):
        url = 'https://stg1.suitabletech.com/admin-api/2/settings/'
        headers = {'Authorization': access_token}
        return APIBase.get_method(url=url, headers=headers)


    @staticmethod
    def delete_simplified_user(user_email, organization, access_token):
        """
        @summary: this API to delete a user on simplified mode
        @param user_email: email user
        @param beam_id: device's id
        @param organization: org's name
        @param access_token: access token after logging account
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        url = UserAPI._baseurl.format(Constant.OrgsInfo[organization]) + user_email + '/'
        return APIBase.delete_method(url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization))


    @staticmethod
    def get_all_email_users(organization, temp):
        """
        @summary: this API get all temporary users
        @param organization: org's name
        @return: response http request
        @author: Quang Tran
        @created_date: Dec 19, 2017
        """
        list_user = []
        response = UserAPI._get_users(organization)
        if temp == True:
            for item in response.json()["objects"]:
                if item["is_temporary"] == True:
                    list_user.append(item["email_address"])
        else:
            for item in response.json()["objects"]:
                list_user.append(item["email_address"])
        return list_user

