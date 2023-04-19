from common.constant import Constant
from core.suitabletechapis.api_base import APIBase


class ReservationAPI(APIBase):
    _baseurl = Constant.APIBaseURL + "reservations/"
    
    
    @staticmethod
    def _get_event_info(event_id, organization=Constant.AdvancedOrgName):
        """
        @summary: This API allows get info of event
        @param event_id: id of event
        @param organization: org's name
        @return: response http request
        @author: Thanh Le
        @created_date: February 16, 2017
        """
        return APIBase.get_method(url=ReservationAPI._baseurl.format(Constant.OrgsInfo[organization]) + event_id, headers=APIBase.generate_header(organization))
        
    
    @staticmethod
    def _update_status_for_event(event_id, event_info, status, organization=Constant.AdvancedOrgName):
        url = ReservationAPI._baseurl.format(Constant.OrgsInfo[organization]) + event_id + '/'
        event_info = event_info.json()
        event_info['status'] = status
        data = event_info
        
        try:
            APIBase.put_method(url=url, headers=APIBase.generate_header(organization), data=data)
        except:
            raise("Could not update status for reservation")


    @staticmethod
    def delete_reservations(id_of_reservations_array, organization=Constant.AdvancedOrgName):
        """
        @summary: delete reservations
        @param id_of_reservations_array: array id of reservation
        @author: Quang Tran
        @created_date: Dec 06, 2017
        """
        for id_of_reser in id_of_reservations_array:
            url = ReservationAPI._baseurl.format(Constant.OrgsInfo[organization]) + str(id_of_reser) + "/"
            try:
                APIBase.delete_method(url, headers=APIBase.generate_header(organization))
            except:
                raise("Could not delete reservation")
            

