from common.constant import Constant
from random import randint
from common.helper import Helper

class GoogleAccount(object):
    
    def __init__(self):
        """
        @summary: constructor 
        @author: Thanh Le
        @created_date: December 01, 2016
        """        
        self.firstName = None
        self.lastName = None
        self.emailAddress = None
        self.password = None
        self.confirmPassword = None
        self.birthMonth = None
        self.birthDay = None
        self.birthYear = None
        self.gender = None
        
        
    def generate_google_account_data(self):
        """
        @summary: set information for new google account
        @author: Thanh Le
        @created_date: December 01, 2016
        """
        self.firstName = Constant.GGAccFirstName
        self.lastName = Constant.GGAccLastName
        self.emailAddress = Helper.generate_random_google_email()
        self.password = Constant.DefaultPassword
        self.confirmPassword = Constant.DefaultPassword
        self.birthMonth = Constant.GGAccMonth
        self.birthDay = randint(1,30)
        self.birthYear = randint(1900, 2000)
        self.gender = Constant.GGAccGender
    