from common.constant import Constant
from core.suitabletechapis.api_base import APIBase


class BeamContentAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "beam-content/"


    @staticmethod
    def get_beam_content_info(organization=Constant.AdvancedOrgName):
        return APIBase.get_method(url=BeamContentAPI._baseurl.format(Constant.OrgsInfo[organization]), headers=APIBase.generate_header(organization))
    
    
    @staticmethod
    def get_beam_content_id(image_name, organization=Constant.AdvancedOrgName):
        """
        @summary: this API is to get beam content id
        @param filename: filename of image needs to get
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: September 13, 2017
        """
        beam_content_info_response = BeamContentAPI.get_beam_content_info()
        beam_content_info = beam_content_info_response.json()["objects"]
        for items in beam_content_info:
            if items["name"] == image_name:
                return items["id"]
        print("There is no beam content having {} name".format(image_name))


    @staticmethod
    def delete_beam_content(image_name, organization=Constant.AdvancedOrgName):
        """
        @summary: this API is to delete beam content image
        @param filename: filename of image needs to remove
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: September 13, 2017
        """
        beam_content_id = BeamContentAPI.get_beam_content_id(image_name, organization)
        url = BeamContentAPI._baseurl.format(Constant.OrgsInfo[organization]) + beam_content_id + "/"
        return APIBase.delete_method(url,headers=APIBase.generate_header(organization))

