from common.constant import Constant
from core.suitabletechapis.api_base import APIBase
import json


class DeviceAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "devices/"
    _get_simplified_beam_info_url = Constant.APIBaseURL + "device-groups/"
    
    property_dict = {'name':'name', 'location':'location', 'labels':'tags', 'time zone':'time_zone', 'group':'device_group', 'device_group':'device_group', 'reservations':'reservations'}
    
    
    @staticmethod
    def _put_device(organization, beam_id, headers, setting_name, setting_value):
        """
        @summary: this API to change device info on advance mode
        @param beam_id: id of device
        @param headers: headers request
        @param setting_name: property (labels, location, name) that you want to change
        @param setting_value: value that you want to change
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        device_info_response = DeviceAPI.get_advanced_device_info(beam_id)
        device_info = device_info_response.json()
        device_info.update({setting_name: setting_value})
        data = json.dumps(device_info)
            
        if beam_id:
            beam_id += "/"
        url = DeviceAPI._baseurl.format(Constant.OrgsInfo[organization]) + beam_id
        return APIBase.put_method(url=url, headers=headers, data=data)
    
    
    @staticmethod
    def get_devices(organization=Constant.AdvancedOrgName):
        """
        @summary: this API to get all devices of organization
        @param organization: org name that we need to get devices
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = DeviceAPI._baseurl.format(Constant.OrgsInfo[organization])
        return APIBase.get_method(url=url, headers=APIBase.generate_header(organization))


    @staticmethod
    def get_advanced_device_info(beam_id, organization=Constant.AdvancedOrgName):
        """
        @summary: this API to get device info
        @param beam_id: beam_id
        @param organization: org name that we need to get devices
        @return: http response data
        @author: Tan Le
        @created_date: August 15, 2017
        """
        url = DeviceAPI._baseurl.format(Constant.OrgsInfo[organization]) + beam_id + "/"
        return APIBase.get_method(url, headers=APIBase.generate_header(organization))
    
    @staticmethod
    def get_simplified_device_info(beam_id, organization, access_token):
        """
        @summary: this API to change device info of a device on simplified mode
        @param beam_name: device's name
        @param organization: org's name
        @param access_token: access token after logging account
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = DeviceAPI._baseurl.format(Constant.OrgsInfo[organization]) + "?device_group="+ beam_id + "&inline=device_group"
        return APIBase.get_method(url, headers=APIBase.generate_simplified_header(access_token, organization))
    
    
    @staticmethod
    def get_simplified_devices(organization, access_token):
        """
        @summary: this APT to get all device on simplified mode
        @param organization: org's name
        @param access_token: access token after logging account
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        url = DeviceAPI._baseurl.format(Constant.OrgsInfo[organization])
        return APIBase.get_method(url, headers=APIBase.generate_simplified_header(access_token, organization))
    
    
    @staticmethod
    def edit_advanced_device(beam_id, device_property, property_value, organization=Constant.AdvancedOrgName):
        """
        @summary: this method to change device info on Advance mode
        @param beam_id: beam's id
        @param device_property: property (labels, location, name) that you want to change
        @param property_value: value that you want to change
        @param organization: org's name
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        return DeviceAPI._put_device(organization, beam_id, headers=APIBase.generate_header(organization, content_type="application/json"), setting_name=DeviceAPI.property_dict[device_property], setting_value=property_value)


    @staticmethod
    def get_simplified_beam_id(beam_name, organization, access_token):
        """
        @summary: this method to get device id of a device in simplified mode
        @param beam_name: name of beam
        @param organization: org's name
        @param access_token: access token after logging account
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        response = DeviceAPI.get_simplified_devices(organization, access_token)
        devices = response.json()["objects"]
        for device in devices:
            if device["name"] == beam_name:
                return device["device_group"]
        return None
    
    
    @staticmethod
    def get_advanced_beam_id(device_name, organization):
        """
        @summary: this method to get device id of a device in advenced mode
        @param device_name: name of device
        @param organization: org's name
        @return: http response data
        @author: Thanh Le
        """
        response = APIBase.get_method(url=DeviceAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization))
        devices = response.json()["objects"]
        for device in devices:
            if device["name"] == device_name:
                return device["id"]
    
        return None
    
    
    @staticmethod
    def edit_simplified_device(beam_id, device_property, property_value, organization, access_token):    
        """        
        @summary: API to change device info on simplified mode
        @param beam_id: device's id
        @param device_property: labels or location or name
        @param property_value: value of (labels or location or name) that you want to update
        @param organization: org's name
        @param access_token: access token after logging account
        @return: http response data
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        device_info = DeviceAPI.get_simplified_device_info(beam_id, organization, access_token)
        device_info = device_info.json()["objects"][0]
        device_id = device_info["id"]
        device_info["device_group"] = beam_id
        device_info.update({device_property: property_value})
        data = json.dumps(device_info)
        return APIBase.put_method(DeviceAPI._baseurl.format(Constant.OrgsInfo[organization]) + device_id + "/", headers=APIBase.generate_simplified_header(access_token, organization), data=data)
    
    
    @staticmethod
    def get_simplified_device_names(organization, access_token):
        """
        @summary: this API to get all name of devices
        @param organization: org's name
        @param access_token: access token after logging account
        @return: array devices name
        @created_date: August 05, 2016
        """
        response = DeviceAPI.get_simplified_devices(organization, access_token)
        devices = response.json()["objects"]
        list_names = []
        for device in devices:
            list_names.append(device["name"])
    
        return list_names
