from core.suitabletechapis.api_base import APIBase
from common.constant import Constant


class DeviceActivityAPI(APIBase):
    _baseurl = Constant.APIBaseURL+"device-activity/"

    @staticmethod
    def get_activity_time_range_status_in_call(time_range, organization=Constant.AdvancedOrgName):
        
        from_date = time_range["from_date"]["yyyy"]+"-"+time_range["from_date"]["mm"]+"-"+time_range["from_date"]["dd"]
        to_date = time_range["to_date"]["yyyy"]+"-"+time_range["to_date"]["mm"]+"-"+time_range["to_date"]["dd"]
        url = DeviceActivityAPI._baseurl.format(Constant.OrgsInfo[organization])+"?end__gte=+"\
                            +from_date+"T00:00:00&limit=500&start__lte="\
                            +to_date+"T23:59:59&state__in=STATE_IN_CALL&streamlined=1"
        return APIBase.get_method(url, headers=APIBase.generate_header(organization))

