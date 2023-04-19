from common.constant import Constant
from core.suitabletechapis.api_base import APIBase
import json
import textwrap


class OrganizationSettingAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "settings/"
    setting_dict = {"organization name":"name", "default invite message":"default_invite_message", "email notifications":"notification_from_name"}
    
    @staticmethod
    def _patch_organization_setting(setting_name, setting_value, organization=Constant.AdvancedOrgName):
        """
        @summary: this API allows update org's information
        @param setting_name: name of field that need to update
        @param setting_value: value need to update
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        data_object = json.dumps({setting_name: setting_value})
        return APIBase.patch_method(url=OrganizationSettingAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization, 'application/json'), data=data_object)
   
    
    @staticmethod
    def update_an_organization_setting(setting_name, setting_value, organization=Constant.AdvancedOrgName):
        """
        @summary: this method call API to update org's information
        @param setting_name: name of field that need to update
        @param setting_value: value need to update
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        return OrganizationSettingAPI._patch_organization_setting(OrganizationSettingAPI.setting_dict[setting_name], setting_value, organization)


    @staticmethod
    def get_organization_setting(organization):
        """
        @summary: this API to get org setting info
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: August 05, 2016
        """

        return APIBase.get_method(url=OrganizationSettingAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization))


    @staticmethod
    def change_authentication_to_BeamOrGoogleAccount(organization):
        """
        @summary: this API allows change authentication method
        @param organization: org's name
        @return: response http request
        @author: Tan Le
        @created_date: September 05, 2017
        """
        org_setting_info_response = OrganizationSettingAPI.get_organization_setting(organization)
        org_setting_info = org_setting_info_response.json()
        org_setting_info.update({"auth_method": "standard","saml_settings":{},"sso_allow_guests":False})
        data = json.dumps(org_setting_info)
        return APIBase.patch_method(url=OrganizationSettingAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization, 'application/json'), data=data)


    @staticmethod
    def change_authentication_to_OneLogin(organization):
        """
        @summary: this API allows change authentication method
        @param organization: org's name
        @return: response http request
        @author: Tan Le
        @created_date: September 05, 2017
        """
        config_Onelogin_info = {"onelogin_appid": Constant.OneloginAppid, "onelogin_subdomain": Constant.OneloginSubdomain, "onelogin_fingerprint": Constant.OneloginFingerprint, "onelogin_certificate": textwrap.dedent(Constant.OneloginCertificate), "idp": Constant.idp["onelogin"]}
        org_setting_info_response = OrganizationSettingAPI.get_organization_setting(organization)
        org_setting_info = org_setting_info_response.json()
        org_setting_info.update({"saml_settings":{"one_login":config_Onelogin_info},"auth_method": "saml","sso_allow_guests":True})
        data = json.dumps(org_setting_info)
        return APIBase.patch_method(url=OrganizationSettingAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization, 'application/json'), data=data)


    @staticmethod
    def change_authentication_to_Okta(organization, okta_xml):
        """
        @summary: this API allows change authentication method
        @param organization: org's name
        @return: response http request
        @author: Khoi Ngo
        @created_date: October 9, 2017
        """ 
        config_Okta_info = {"xml": okta_xml, "idp": Constant.idp["okta"]}
        org_setting_info_response = OrganizationSettingAPI.get_organization_setting(organization)
        org_setting_info = org_setting_info_response.json()
        org_setting_info.update({"saml_settings":{"okta":config_Okta_info},"auth_method": "saml","sso_allow_guests":True})
        data = json.dumps(org_setting_info)
        return APIBase.patch_method(url=OrganizationSettingAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization, 'application/json'), data=data)


    @staticmethod
    def setting_primary_contact(organization, data):
        """
        @summary: this API setting primary contact to default
        @return: response http request
        @author: Quang Tran
        @created_date: Dec 9, 2017
        """ 
        return APIBase.patch_method(url=OrganizationSettingAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization, 'application/json'), data=data)

