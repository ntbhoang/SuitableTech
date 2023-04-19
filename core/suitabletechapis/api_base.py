import requests
from common.constant import Constant


class APIBase(object):
    _timeout = 45
    
    @staticmethod
    def get_method(url="", headers=None, params=None):
        """
        @summary: send a GET http request and get the response data
        @param url: Url REST address
        @param header: header values with format dictionary
        @param params: parameter values with format dictionary
        @return: response data of http request
        @author: Duy Nguyen
        @created_date: August 05, 2016        
        """
        try:
            response = requests.get(url, headers=headers, params=params, timeout=APIBase._timeout)
            return response
        except Exception as ex:
            raise ex
    
    
    @staticmethod
    def post_method(url="", headers=None, data=None):
        """
        @summary: send a POST http request and get the response data
        @param url: Url REST address
        @param header: header values with format dictionary
        @param data: data value with format json object
        @return: response data of http request
        @author: Duy Nguyen
        @created_date: August 05, 2016
        """
        try:
            response = requests.post(url, headers=headers, data=data, timeout=APIBase._timeout)
            return response
        except Exception as ex:
            raise ex
    
    
    @staticmethod
    def delete_method(url=None, headers=None, data=None): 
        """
        @summary: send a DELETE http request and get the response data        
        @param: url: Url REST address
        @param header: header values with format dictionary
        @param data: data value with format json object
        @return:   response data of http request
        @author: Duy Nguyen
        @created_date: August 05, 2016
        """
        try:
            response = requests.delete(url, headers=headers, data=data, timeout=APIBase._timeout)
            return response
        except Exception as ex:
            raise ex
        
        
    @staticmethod
    def patch_method(url=None, headers=None, data=None):
        """
        @summary: send a PATCH http request and get the response data
        @param: url: Url REST address
        @param header: header values with format dictionary
        @param data: data value with format json object
        @return: response data of http request
        @author: Duy Nguyen
        @created_date: August 05, 2016
        """

        try:
            response = requests.patch(url, headers=headers, data=data, timeout=APIBase._timeout)
            return response
        except Exception as ex:
            raise ex


    @staticmethod
    def put_method(url=None, headers=None, data=None):
        """
        @summary: send a PUT http request and get the response data
        @param: url: Url REST address
        @param header: header values with format dictionary
        @param data: data value with format json object
        @return:   response data of http request
        @author: Duy Nguyen
        @created_date: August 05, 2016
        """
        try:
            response = requests.put(url, headers=headers, data=data, timeout=APIBase._timeout)
            return response
        except Exception as ex:
            raise ex
        
        
    @staticmethod
    def generate_header(organization=Constant.AdvancedOrgName, content_type=None):
        """
        @summary: Generate Key based on organization (LogiGear Test, LogiGear Test 3). This Key is used when call APIs of Advance mode
        @param organization: organization. Default value = "LogiGear Test"
        @return: Authorization
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        if content_type == None:
            return {'Authorization': Constant.APIKeys[organization]}
        return {'Authorization': Constant.APIKeys[organization], 'Content-Type': content_type}


    @staticmethod
    def generate_simplified_header(access_token, organization, content_type='application/json'):
        """
        @summary: Generate Key for organization LogiGear Test 2. This Key is used when call APIs
        @param access_token: access token
        @param organization: organization name
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        return {'Authorization': access_token, 'X-Organization': Constant.OrgsInfo[organization], 'Content-Type': content_type}
