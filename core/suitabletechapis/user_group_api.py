from common.constant import Constant
from core.suitabletechapis.api_base import APIBase
import json


class UserGroupAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "user-groups/"
    
    @staticmethod
    def _get_user_group(user_group_id="", organization=Constant.AdvancedOrgName):
        """
        @summary: This API allows get user group info
        @param user_group_id: id of user group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        return APIBase.get_method(url=UserGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + user_group_id, headers=APIBase.generate_header(organization))

    @staticmethod
    def _delete_user_group(user_group_id, organization=Constant.AdvancedOrgName):
        """
        @summary: This API allows delete user group
        @param user_group_id: id of user group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        return APIBase.delete_method(url=UserGroupAPI._baseurl.format(Constant.OrgsInfo[organization]) + user_group_id, headers=APIBase.generate_header(organization))
   
    
    @staticmethod
    def create_user_group(name, user_email_array, organization=Constant.AdvancedOrgName):
        """
        @summary: This method allows create user group
        @param name: user group name
        @param user_email_array: list email need to add into group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        data_object = json.dumps({'name': name, 'users': user_email_array})
        headers = { 'Content-Type': 'application/json'}
        headers.update(APIBase.generate_header(organization))
        return APIBase.post_method(url=UserGroupAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=headers, data=data_object)


    @staticmethod
    def delete_all_user_groups(keyword="LGVN User Group", organization=Constant.AdvancedOrgName):
        """
        @summary: This method allows delete all user groups
        @param keyword: user group name
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        try:
            response = UserGroupAPI._get_user_group(organization=organization)
            for item in response.json()["objects"]:
                if keyword in item["name"]:
                    UserGroupAPI.delete_user_group(item["name"], organization)
                    print("Deleting User Group: {}".format(item["name"]))
        except Exception as ex:
            raise ex
  
        
    @staticmethod
    def _get_user_groups(organization=Constant.AdvancedOrgName):
        """
        @summary: This API allows get info of user group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        return APIBase.get_method(url=UserGroupAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization))
    
    
    @staticmethod
    def get_user_group_id(user_group_name, organization=Constant.AdvancedOrgName):
        """
        @summary: This method allows get id of a user group
        @param user_group_name: name of user group
        @param organization: org's name
        @return: user group id
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        try:
            get_user_groups_response = UserGroupAPI._get_user_groups(organization)
            for user_group in get_user_groups_response.json()["objects"]:
                if user_group["name"] == user_group_name:
                    return user_group["id"]
            
        except Exception as ex:
            raise ex
        
        
    @staticmethod
    def delete_user_group(user_group_name, organization=Constant.AdvancedOrgName):
        """
        @summary: This method allows delete a user group
        @param user_group_name: name of user group
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        try:
            user_group_id = UserGroupAPI.get_user_group_id(user_group_name, organization)
            return UserGroupAPI._delete_user_group(user_group_id, organization)
        except Exception as ex:
            raise ex
