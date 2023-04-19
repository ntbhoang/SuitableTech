from common.constant import Constant
from data_test.dataobjects.invitation_settings import Invitation_Settings
from core.suitabletechapis.user_api import UserAPI

class User(object):
    
    def __init__(self):
        self.email_address = None
        self.first_name = ""
        self.last_name = ""
        self.device_group = None
        self.device_groups = []
        self.organization = None
        self.organizations = []
        self.user_group = None
        self.user_groups = []
        self.password = None
        self.confirm_password = None
        self.invitation_settings = Invitation_Settings()
        self.activated = None
        
        
    def generate_data(self, verified_domain = None):
        """
        @summary: set information for new account
        @param verify_domain: domain is verified 
        @author: Thanh.Viet.Le
        """
        from common.helper import Helper
        if verified_domain is None:
            self.email_address = Helper.generate_random_email()
        else:    
            self.email_address = Helper.generate_random_email_has_domain_verify(verified_domain)
        self.organization = Constant.AdvancedOrgName
        self.password = Helper.generate_random_password()
        self.confirm_password = self.password
        self.activated = False
        self.first_name = Helper.generate_random_first_name()
        self.last_name = Helper.generate_random_last_name()
    
    
    def generate_okta_user_data(self):
        """
        @summary: set information for okta account
        @author: Thanh.Viet.Le
        """
        from common.helper import Helper
        self.first_name = "LogiGear VN1"+Helper.generate_random_string()
        self.last_name = "Testing" + Helper.generate_random_string()
        self.email_address = Constant.OktaAccount
        self.organization = Constant.AdvancedOrgName
        self.password = Constant.OktaPassword
        
        
    def generate_org_admin_user_data(self):
        """
        @summary: set mixed user's information
        @author: Thanh.Viet.Le
        """
        self.email_address = Constant.AdvanceOrgAdminEmail
        self.first_name = "Huy Tran"
        self.organization = Constant.AdvancedOrgName
        self.organizations = [Constant.AdvancedOrgName, Constant.AdvancedOrgName_2, Constant.SimplifiedOrgName]
        self.device_groups = [Constant.BeamPlusMock2Name, Constant.BeamPlusMock3Name]
        self.password = Constant.DefaultPassword
        self.confirm_password = Constant.DefaultPassword
        self.activated = True # set True because we use account already activated
        
        
    def advanced_org_admin_data(self):
        """
        @summary: set mixed user's information
        @author: Thanh.Viet.Le
        """
        self.email_address = Constant.AdvanceOrgAdminEmail
        self.first_name = "Huy"
        self.last_name = "Tran"
        self.organization = Constant.AdvancedOrgName
        self.organizations = [Constant.AdvancedOrgName, Constant.AdvancedOrgName_2]
        self.device_groups = [Constant.BeamPlusMock2Name, Constant.BeamPlusMock3Name]
        self.password = Constant.DefaultPassword
        self.confirm_password = Constant.DefaultPassword
        self.activated = True # set True because we use account already activated
        
    def generate_advanced_normal_user_data(self, verified_domain = None):
        """
        @summary: set first name for advanced normal user account
        @author: Thanh.Viet.Le
        """
        self.generate_data(verified_domain)


    def generate_advanced_org_admin_data(self):
        """
        @summary: set first name for device group admin account
        @author: Thanh.Viet.Le
        """
        self.generate_data()
        
    
    def generate_advanced_device_group_admin_data(self):
        """
        @summary: set first name for device group admin account
        @author: Thanh.Viet.Le
        """
        self.generate_data()
    
    
    def generate_simplified_normal_user_data(self):
        """
        @summary: set informations for simplified device admin account
        @author: Thanh.Viet.Le
        """
        self.generate_data()
        self.organization = Constant.SimplifiedOrgName
        
    
    def generate_simplified_org_admin_data(self):
        """
        @summary: set informations for simplified org admin account
        @author: Thanh.Viet.Le
        """
        self.email_address = Constant.SimplifiedAdminEmail
        self.organization = Constant.SimplifiedOrgName
        self.organizations = [Constant.SimplifiedOrgName]
        self.device_groups = [Constant.BeamPlusMock2Name, Constant.BeamPlusMock3Name]
        self.password = Constant.DefaultPassword
        self.confirm_password = Constant.DefaultPassword
        self.activated = True # set True because we use account already activated
    
    
    def generate_mixed_org_admin_data(self):
        """
        @summary: set mixed user's information
        @author: Thanh.Viet.Le
        """
        self.email_address = Constant.MixedMultiOrgAdminEmail
        self.first_name = "Mixed Org Admin"
        self.organization = Constant.AdvancedOrgName
        self.organizations = [Constant.AdvancedOrgName, Constant.AdvancedOrgName_2, Constant.SimplifiedOrgName]
        self.device_groups = [Constant.BeamPlusMock2Name, Constant.BeamPlusMock3Name]
        self.password = Constant.DefaultPassword
        self.confirm_password = Constant.DefaultPassword
        self.activated = True # set True because we use account already activated
    
    
    def generate_non_gsso_user_data(self):
        """
        @summary: generate non gsso account
        @author: Thanh.Viet.Le
        """
        from core.utilities.test_condition import TestCondition
        self.email_address = TestCondition.get_and_lock_an_allow_st_email()
        self.password = Constant.DefaultPassword
    
    
    def generate_un_allowed_gsso_user_data(self):
        """
        @summary: generate unallow gsso account
        @author: Thanh.Viet.Le
        """
        from core.utilities.test_condition import TestCondition
        self.email_address = TestCondition.get_and_lock_an_unallow_st_email()
        self.password = Constant.DefaultPassword
    
    
    def get_displayed_name(self, simplified=False):        
        if simplified:
            user_info = UserAPI._get_user_info_in_simplified_org(self.email_address)
        else:
            user_info = UserAPI._get_user(self.email_address, self.organization)     
        
        user_info_json = user_info.json()
        if user_info_json['first_name'] == '' or user_info_json['last_name'] == '':
            return self.email_address
        return user_info_json['first_name'] + ' ' +  user_info_json['last_name']
        
     
    def tostring(self):
        return "email_address: {}\nfirst_name: {}\nlast_name: {}\ndevice_group: {}\nuser_group: {}\norganization: {}".format(self.email_address,
                                    self.first_name, self.last_name, self.device_group, self.user_group, self.organization)