from common.constant import Constant
from core.suitabletechapis.api_base import APIBase


class AccessRequestAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "access-requests/"
    _reject_url = "https://stg1.suitabletech.com/r/{}/r/"

    @staticmethod
    def get_all_access_requests_secrets(session, organization):
        """
        @summary: this API to get secret field of all access request on 1 organization
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: September 06, 2017
        """
        try:
            reponse = session.get(url=AccessRequestAPI._baseurl.format(Constant.OrgsInfo[organization]), headers = APIBase.generate_header(organization))
            secretList = []
            for item in reponse.json()["objects"]:
                secretList.append(item["secret"])
            return secretList
        except Exception as ex:
            print("Error: Cannot get 'secret' of access requests")
            print(str(ex))

    @staticmethod
    def reject_all_access_requests(session, organization = Constant.AdvancedOrgName):
        """
        @summary: this API to reject all access request on 1 organization
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: September 06, 2017
        """
        secretList = AccessRequestAPI.get_all_access_requests_secrets(session, organization)

        for secret in secretList:
            session.get(url=AccessRequestAPI._reject_url.format(secret))

