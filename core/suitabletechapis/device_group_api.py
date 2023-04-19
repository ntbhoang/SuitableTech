from common.constant import Constant
import json
from core.suitabletechapis.api_base import APIBase
from core.suitabletechapis.device_api import DeviceAPI
from core.suitabletechapis.user_group_api import UserGroupAPI


class DeviceGroupAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "device-groups/"
    _device_group_memberships = Constant.APIBaseURL + "device-group-memberships/"
    _access_request_url = "https://stg1.suitabletech.com/admin-api/2/organizations/129/access-requests/"
    _delete_request_url = "https://stg1.suitabletech.com/r/{}/r/"
    property_dict = {'name': 'name', 'location': 'location', 'labels': 'tags', 'time zone': 'time_zone', 'group': 'device_group'}
    _reservations_url = Constant.APIBaseURL + "reservations/?device__in=" + Constant.DeviceIDs[Constant.BeamPlusMock1Name] + "," \
                        + Constant.DeviceIDs[Constant.BeamPlusMock4Name] + ","\
                        + Constant.DeviceIDs[Constant.BeamPlusMock5Name] + ","\
                        + Constant.DeviceIDs[Constant.BeamPlusMock6Name] + ","\
                        + Constant.DeviceIDs[Constant.BeamPlusName] + ","\
                        + Constant.DeviceIDs[Constant.BeamProNameUTF8]\
                        + "&device_group={}"
    
    @staticmethod
    def delete_all_device_groups(keyword="LGVN Group", organization=None):    
        """
        @summary: this method to delete all devices of group
        @param keyword: group name
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        if organization is None:
            organization = Constant.AdvancedOrgName
            
        response = DeviceGroupAPI._get_device_groups(organization)
        for item in response.json()["objects"]:
            if keyword in item["name"]:
                DeviceGroupAPI.delete_device_group(item["name"], organization)
                print("Deleting Device Group: {}".format(item["name"]))
                     
           
    @staticmethod
    def _get_device_groups(organization=None):
        """
        @summary: this API to get info devices of group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        if organization is None:
            organization = Constant.AdvancedOrgName
            
        return APIBase.get_method(url=DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization))
    
    
    @staticmethod
    def create_device_group(name, device_array, organization=None):
        """
        @summary: this API to create device group
        @param name: group name
        @param device_array: list device to add into group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        if organization is None:
            organization = Constant.AdvancedOrgName
        response = DeviceAPI.get_devices(organization)
        if response.status_code != 200:
            response = DeviceAPI.get_devices(organization)
        beam_id_list = []
        
        if device_array:
            for item in response.json()["objects"]: 
                if item["name"] in device_array:
                    beam_id_list.append(item["id"])
        if device_array != [] and beam_id_list == []:
            raise Exception("Cannot find the devices {} to add into device group".format(', '.join(device_array)))
        
        data_object = json.dumps({'name': name, 'devices': beam_id_list})
        headers = {'Content-Type': 'application/json'}
        headers.update(APIBase.generate_header(organization))
        return APIBase.post_method(url=DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=headers, data=data_object)       


    @staticmethod
    def get_devices_from_device_group(device_group_name, organization=Constant.AdvancedOrgName):
        """
        @summary: this method to get devices from device group
        @param device_group_name: name of device group
        @param organization: org's name
        @return: list devices  
        @note: Now, only support for advanced organization. Includes {LogiGear Test, LogiGear Test 3}
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        device_group = DeviceGroupAPI.get_advanced_device_group(device_group_name, organization)
        return device_group['devices']


    @staticmethod
    def add_device_to_device_group(device_group_name, device_array, organization=Constant.AdvancedOrgName):
        """
        @summary: this method to add device into device group
        @param device_group_name: name of device group
        @param device_array: list device need to add
        @param organization: org's name
        @return: reponse http request'
        @note: Now, only support for advanced organization. Includes {LogiGear Test, LogiGear Test 3}
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        deviceID = str(DeviceAPI.get_advanced_beam_id(device_group_name, organization))
        try:
            device_group_id = str(DeviceGroupAPI.get_device_group_id(device_group_name, organization))
            if device_group_id is not None:
                beam_id_list = DeviceGroupAPI.get_devices_from_device_group(device_group_name, organization)
                if device_array:  # checking is not None
                    for device_name in device_array:
                        if device_name is not None:
                            beam_id_list.append(deviceID)
        
                data_object = json.dumps({'devices':beam_id_list})
                return APIBase.patch_method(url=DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + device_group_id + "/", headers=APIBase.generate_header(organization), data=data_object)
        except:
            raise Exception("Failed while adding device to device group")


    @staticmethod
    def get_device_group_id(device_group_name, organization=None):
        """
        @summary: this method to get device group id
        @param device_group_name: group name
        @param organization: org's name
        @return: id of device group
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        if organization is None:
            organization = Constant.AdvancedOrgName
            
        get_device_groups_response = DeviceGroupAPI._get_device_groups(organization)
        for device_group in get_device_groups_response.json()["objects"]:
            if device_group["name"] == device_group_name:
                return device_group["id"]
        return None


    @staticmethod
    def get_advanced_device_group(device_group_name, organization):
        """
        @summary: this method to get info of devices in group. This method apply for advance mode

        @param: param device_group_name: name of device group
        @param organization: org's name
        @return: device group information if device group exist, if not return None
        @author: Thanh Le
        @param device_group_name: name of device group
        @param organization: org's name
        @return: device group information if device group exist, if not return None
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        get_device_groups_response = DeviceGroupAPI._get_device_groups(organization)

        for device_group in get_device_groups_response.json()["objects"]:
            if device_group["name"] == device_group_name:
                return device_group
        return None


    @staticmethod
    def delete_device_group(device_group_name, organization=None):
        """
        @summary: this API to delete device group
        @param device_group_name: name of device group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        if organization is None:
            organization = Constant.AdvancedOrgName
            
        get_device_group_id = DeviceGroupAPI.get_device_group_id(device_group_name, organization)
        return APIBase.delete_method(url=DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + get_device_group_id + "/", headers=APIBase.generate_header(organization))


    @staticmethod
    def change_device_group_name(device_group_name, new_device_group_name, organization=None):
        """
        @summary: this API to change device group's name
        @param device_group_name: Current name of device group
        @param new_device_group_name: New name of device group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: December 21, 2016
        """
        if organization is None:
            organization = Constant.AdvancedOrgName
            
        get_device_group_id = DeviceGroupAPI.get_device_group_id(device_group_name, organization)
        
        data_object = json.dumps({'name':new_device_group_name})
        return APIBase.patch_method(url=DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + get_device_group_id + "/", headers=APIBase.generate_header(organization), data=data_object)

                   
    @staticmethod
    def add_user_group(device_group_name, user_group_name, organization=None):
        """
        @summary: this API to add user group into device group
        @param device_group_name: name of device group
        @param user_group_name: name of user group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        device_group_id = DeviceGroupAPI.get_device_group_id(device_group_name, organization)
        user_group_id = UserGroupAPI.get_user_group_id(user_group_name, organization)
        
        data_object = json.dumps([{'device_group': device_group_id, 'user_group': user_group_id}])
        headers = { 'Content-Type': 'application/json' }
        headers.update(APIBase.generate_header(organization))
        return APIBase.patch_method(url=DeviceGroupAPI._device_group_memberships.format(Constant.OrgsInfo[organization]), headers=headers, data=data_object)
    
    
    @staticmethod
    def _get_simplified_device_group(beam_id, access_token, organization):
        """
        @summary: this API to get info of a device on simplified device group
        @param device_group_name: name of device group
        @param access_token: access token after logging account
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + beam_id + "/"
        return APIBase.get_method(url=url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization))

        
    @staticmethod
    def _get_simplified_device_group_more_detail(beam_id, access_token, organization):
        """
        @summary: this API to get all info of devices on simplified device group
        @param device_group_name: name of device group
        @param access_token: access token after logging account
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = DeviceGroupAPI._device_group_memberships.format(Constant.OrgsInfo[organization]) + "?device_group=" + beam_id
        return APIBase.get_method(url=url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization))


    @staticmethod
    def _get_simplified_user_id(user_email, beam_id, organization, access_token):
        """
        @summary: this API to get user id of simplified device group
        @param user_email: email user
        @param beam_id: device's id
        @param organization: org's name
        @param access_token: access token after logging account
        @return: user's id if user exists if not, return None
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        response = DeviceGroupAPI._get_simplified_device_group_more_detail(beam_id=beam_id, access_token=access_token, organization=organization)        
        for user_info in response.json()["objects"]:
            if user_info["user"] == user_email:
                return str(user_info["id"])    
        return None
    
    
    @staticmethod
    def set_simplified_device_admin(user_email, beam_id, organization, access_token):
        """
        @summary: this API to set admin for a device on simplified mode
        @param user_email: email user
        @param beam_id: device's id
        @param organization: org's name
        @param access_token: access token after logging account
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        response_info = DeviceGroupAPI._get_simplified_device_group(beam_id, access_token=access_token, organization=organization)
        origin_data = response_info.json()
        origin_data["admins"].append(user_email)
        data_object = json.dumps(origin_data)
        url = DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + beam_id + "/"
        response = APIBase.put_method(url=url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization, content_type='application/json'), data=data_object)
        #Handle fail set admin DG simp by API
        response_info = DeviceGroupAPI._get_simplified_device_group(beam_id, access_token=access_token, organization=organization)
        origin_data = response_info.json()
        if user_email not in origin_data["admins"]:
            origin_data["admins"].append(user_email)
            data_object = json.dumps(origin_data)
            response = APIBase.put_method(url=url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization, content_type='application/json'), data=data_object)
        return response

    @staticmethod
    def set_advanced_device_group_admin(user_email_array, device_group_name, organization):
        """
        @summary: API to set admins user for a device group
        @param user_email_array: list user email
        @param device_group_name: name of device group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        device_group_info = DeviceGroupAPI.get_advanced_device_group(device_group_name, organization)
        is_admins = device_group_info['admins']
        is_admins = user_email_array + is_admins
        device_group_info.update({'admins': is_admins})
        url = DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + device_group_info["id"] + "/"
        data = json.dumps(device_group_info)
        headers = {'Content-Type': 'application/json'}
        headers.update(APIBase.generate_header(organization))
        return APIBase.put_method(url=url, headers=headers, data=data)
    
    
    @staticmethod
    def get_all_users_in_simplified_device_group(beam_id, access_token, organization):
        """
        @summary: this method to get all users info of simplified device group
        @param deviceid: device's id
        @param access_token: access token after logging account
        @param organization: org's name
        @return: information of users
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        response = DeviceGroupAPI._get_simplified_device_group_more_detail(beam_id=beam_id, access_token=access_token, organization=organization)
        users = []        
        for user_info in response.json()["objects"]:
            users.append(user_info["user"])            
        return users
    

    @staticmethod
    def edit_simplified_device_group(beam_id, device_property, property_value, organization, access_token):
        """
        @summary: this API to edit info of a device on simlified device group
        @param device_name: device's name
        @param device_property: device's property that you want to change
        @param property_value: value of property
        @param organization: org's name
        @param access_token: access token after logging account
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        response = DeviceGroupAPI._get_simplified_device_group(beam_id=beam_id, access_token=access_token, organization=organization)
        origin_data = response.json()
        origin_data[DeviceGroupAPI.property_dict[device_property]] = property_value
        data_object = json.dumps(origin_data)
        url = DeviceGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + beam_id + "/"
        return APIBase.put_method(url=url, headers=APIBase.generate_simplified_header(access_token=access_token, organization=organization), data=data_object)


    @staticmethod
    def get_list_answer_request_users(device_group_name, organization = None):
        """
        @summary: Get all user in Session Answer
        @author: Khoi Ngo
        @created_date: October 25, 2017
        """
        if organization is None:
            organization = Constant.AdvancedOrgName
        device_group_info = DeviceGroupAPI.get_advanced_device_group(device_group_name, organization)
        request_users = device_group_info['answer_users']

        return request_users


    @staticmethod
    def get_id_of_reservations_of_device_group(device_group_name, organization = Constant.AdvancedOrgName):
        """
        @summary: Get all reservations in device group
        @author: Quang Tran
        @created_date: Dec 06, 2017
        """
        id_reservation = []
        device_group_id = DeviceGroupAPI.get_device_group_id(device_group_name)
        url = DeviceGroupAPI._reservations_url.format(Constant.OrgsInfo[organization], device_group_id)
        reponse = APIBase.get_method(url, headers=APIBase.generate_header(organization))
        for id_of_reser in reponse.json()["objects"]:
            id_reservation.append(id_of_reser["id"])
        return id_reservation
        

