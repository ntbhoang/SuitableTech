# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import json
import random
import string
from uuid import uuid4

from common.constant import Constant, Language, Locale
from common.email_detail_constants import EmailDetailConstants
from data_test import testdata
from data_test.dataobjects.message import Message
import re
from common.application_constants import ApplicationConst

from random import randint
from tzlocal import get_localzone
from pytz import timezone
import time
import locale
from core.suitabletechapis.user_api import UserAPI
from core.suitabletechapis.device_api import DeviceAPI

class Helper(object):
    
    _utf8chars = u"éêàáâơớờởùứîçアイウエオカキク ケコサシスセソ"
    
    @staticmethod
    def base_dir():
        """      
        @summary: Get base directory      
        @author: 
        """
        return os.path.dirname(os.path.dirname(__file__))
    
    
    @staticmethod
    def generate_calendar_reservation(email, calendar_key):
        reservations_info = {}
        reservations_info['user_name'] = email
        reservations_info['password'] = calendar_key
        reservations_info['url'] = 'https://stg1.suitabletech.com/cal/' + email
        return reservations_info
        
    @staticmethod
    def generate_random_string(length=10):
        """
        @summary: generate a random string having uppercase, lowercase, digits and utf8 characters  
        @param length: length of random string 
        @return: a random string 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """       
        randomstring = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + Helper._utf8chars) for _ in range(length))
        return re.sub("\s\s+" , " ", randomstring.strip())
    
    
    @staticmethod
    def generate_random_not_special_string(length = 6):
        """
        @summary: generate a random string only having uppercase, lowercase, digits
        @param length: length of random string 
        @return: a random string 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """   
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    

    @staticmethod
    def generate_random_device_group_name(length=10):
        """
        @summary: generate a device group name by adding a random string to "LGVN Device Group " 
        @param length: length of added random string 
        @return: device group name with format "LGVN Device Group " + random string 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """   
        return "LGVN Device Group " + Helper.generate_random_string(length)
    
    
    @staticmethod
    def generate_random_device_name(length=10):
        """
        @summary: generate a device name by adding a random string to "LGVN Device " 
        @param length: length of added random string 
        @return: device name with format "LGVN Device " + random string 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """   
        return "LGVN Device " + Helper.generate_random_string(length)
    
    
    @staticmethod
    def generate_random_label_name(length=10):
        """
        @summary: generate a label name by adding a random string to "LGVN Label " 
        @param length: length of added random string 
        @return: lable name with format "LGVN Label " + random string 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """   
        return "LGVN Label " + Helper.generate_random_string(length)


    @staticmethod
    def generate_random_user_group_name(length=10):
        return "LGVN User Group " + Helper.generate_random_string(length)


    @staticmethod
    def generate_random_first_name(length=3):
        return "LGVN FN " + Helper.generate_random_string(length)


    @staticmethod
    def generate_random_last_name(length=3):
        return "LGVN LN " + Helper.generate_random_string(length)
    
    
    @staticmethod
    def generate_random_email():
        """
        @summary: This method is used to generated a testing email 
        @return: an email with the following format logigear1+userYYDDmmHHMMSSfff@suitabletech.com
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        base_email = Constant.BaseEmails[random.randint(1,5)]
        date_time = datetime.strftime(datetime.now(), "%b%d%Y.%H%M%S")
        random_str = str(uuid4()).replace("-", "")[:randint(5, 15)]
        
        separator = "@"
        parts = base_email.split(separator)
        return (parts[0] + "+user{}.{}".format(random_str, date_time) + separator + parts[1]).lower()

 
    @staticmethod
    def generate_random_email_has_domain_verify(domain):
        """
        @summary: This method is used to generated a testing email 
        @return: an email with the following format logigear1+userYYDDmmHHMMSSfff@"domain".com
        @author: Thanh Le
        @created_date: Nov 16, 2017
        """
        base_email = Constant.BaseEmails[random.randint(1,5)]
        date_time = datetime.strftime(datetime.now(), "%b%d%Y.%H%M%S")
        random_str = str(uuid4()).replace("-", "")[:randint(5, 15)]
        
        separator = "@"
        parts = base_email.split(separator)
        return (parts[0] + "+user{}.{}".format(random_str, date_time) + separator + domain).lower()

        
    @staticmethod
    def generate_random_google_email():
        """
        @summary: This method is used to generated a new gmail 
        @return: The gmail with the following format lgvnsuitabletechYYDDmmHHMMSSfff@gmail.com
        @author: Thanh Le
        @created_date: December 01, 2016 
        """
        date_time = datetime.strftime(datetime.now(), "%b%d%Y.%H%M%S")
        return ("lgvnsuitabletech"+ date_time + "@gmail.com")
    
    
    @staticmethod
    def generate_random_password(length=25):
        """      
        @summary: Generate random password
        @param length: length of password  
        @return: password
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for _ in range(length))
    
    
    @staticmethod
    def generate_date_time(hour_delta=1, minute_delta=0, second_delta=0):
        """      
        @summary: Generate date time
        @param hour_delta: number of hours want to add 
        @param minute_delta: number of minute want to add 
        @param second_delta: number of second want to add 
        @return: generated datetime 
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0 ) + timedelta(days = 1, hours = hour_delta, minutes = minute_delta, seconds = second_delta)
    
    
    @staticmethod
    def generate_access_day():
        """      
        @summary: Generate tomorrow datetime 
        @return: tomorrow datetime 
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        return datetime.today() + timedelta(days=1)
    
    
    @staticmethod
    def generate_time_range_label(start_datetime, end_datetime):
        """      
        @summary: Generate a time range label 
        @param start_datetime: start time 
        @param end_datetime: end time
        @return: time range with format 12:30 AM - 1:45 PM 
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        result = "{}:{} {} - {}:{} {}".format(
                str(int (start_datetime.strftime("%I"))),
                start_datetime.strftime("%M"),
                ApplicationConst.get_date_time_label(start_datetime.strftime("%p")),
                str(int (end_datetime.strftime("%I"))),
                end_datetime.strftime("%M"),
                ApplicationConst.get_date_time_label(end_datetime.strftime("%p")))
        return result


    @staticmethod
    def get_data_from_csv_file(data_file_name):
        """      
        @summary: Get data from CSV file     
        @param data_file_name: data file name 
        @return: data in csv file
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        # Define constant
        csv_delim = ","
        end_line = "\n"
        
        # Read file and put to array
        file_path = os.path.dirname(testdata.__file__)
        f_stream = open(file_path + "\\" + data_file_name, "r")
        lines = f_stream.readlines()
        f_stream.close()
        
        # Get items from lines
        item = []
        result = []
        for i in range (1, len(lines)):
            lines[i] = lines[i].replace(end_line, "")
            item = lines[i].split(csv_delim)
            result.append(item)

        return result


    @staticmethod
    def download_dir():
        """      
        @summary: Get download directory       
        @return: path
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        return Helper.base_dir() + "\\data\\download".replace("\\", os.path.sep)

    
    @staticmethod
    def get_dict_value(dictionary, key, value, search_key):
        """      
        @summary: Get value in dictionary
        @param dictionary: dictionary name
        @param key: key
        @param value: value
        @param search_key: search key   
        @return: value of search key 
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        return next(item for item in dictionary if item.get(key) == value)[search_key]
        
        
    @staticmethod
    def analyze_start_time_and_end_time(start_time, end_time, running_locale):
        """      
        @summary: Analyze starting time and ending time 
        @param start_time: start time in calendar client system
        @param end_time: end time in calendar client system
        @return: Japanese time string 
        @author: Thanh Le
        @created_date: February 21 , 2017
        """
        if running_locale == Language.JAPANESE:
            return Helper.analyze_start_time_and_end_time_japanese(start_time, end_time)
        return Helper.format_start_time_and_end_time_on_website(start_time, end_time, running_locale)


    @staticmethod
    def analyze_start_time_and_end_time_japanese(start_time, end_time):
        """      
        @summary: Analyze starting time and ending time as Japanese
        @param start_time: start time in calendar client system
        @param end_time: end time in calendar client system
        @return: Japanese time string 
        @author: Thanh Le
        @created_date: February 21 , 2017
        """
        return Helper.format_start_time_and_end_time_on_website_japanese(start_time, end_time)
        
    
    @staticmethod
    def format_start_time_and_end_time_on_website(start_time, end_time, running_language):
        """      
        @summary: Format start time and end time as on website
        @param start_time: local start time
        @param end_time: local end time
        @param running_language: language
        @return: format start time and end time 
        @author: Thanh Le
        @created_date: March 15, 2017
        """    
        if running_language == Language.ENGLISH:
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
        elif running_language == Language.FRENCH:
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.FR))
        else:
            return Helper.format_start_time_and_end_time_on_website_japanese(start_time, end_time)
        
        header = start_time.strftime("%A %b %d")
        if header[-2:].startswith('0'):
            header = header[:-2] + header[-1:]
        
        ordinal_number = Helper.caculate_ordinal_number(start_time, running_language)
        header = header + ordinal_number
        
        e_start_time = Helper.format_time(start_time, running_language)
        e_end_time = Helper.format_time(end_time, running_language)
        
        if start_time.date() == end_time.date():
            e_end_time = Helper.format_time(end_time, running_language)
        else:
            e_end_time = end_time.strftime("%b %d")
            if e_end_time[-2:].startswith('0'):
                e_end_time = e_end_time[:-2] + e_end_time[-1:]
            end_time_ordinal_number = Helper.caculate_ordinal_number(end_time, running_language)
            
            e_end_time = e_end_time + end_time_ordinal_number + ' ' + Helper.format_time(end_time, running_language)
        
        locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
        return header + e_start_time + e_end_time  
    

    @staticmethod
    def format_start_time_and_end_time_on_website_japanese(start_time, end_time):
        """      
        @summary: Format start time and end time as on website for Japanese
        @param start_time: local start time
        @param end_time: local end time
        @return: format start time and end time as Japanese
        @author: Thanh Le
        @created_date: March 15, 2017
        """  
        weekday_dict = {'Sunday':u'日曜日', 'Monday':u'月曜日', 'Tuesday':u'火曜日', 'Wednesday':u'水曜日',\
                        'Thursday': u'木曜日', 'Friday': u'金曜日', 'Saturday': u'土曜日'}
        
        # header
        header = u"{} {}月 {}日".format(weekday_dict[start_time.strftime("%A")], Helper.convert_time_value(start_time.strftime("%m")),\
                                Helper.convert_time_value(start_time.strftime("%d")))
        
        e_start_time = u"{}:{}".format(start_time.strftime("%H"), start_time.strftime("%M"))
        
        if start_time.date() == end_time.date():
            e_end_time = u"{}:{}".format(end_time.strftime("%H"), end_time.strftime("%M"))
        else:
            e_end_time = u"{}月 {}日 {}:{}".format(Helper.convert_time_value(end_time.strftime("%m")), Helper.convert_time_value(end_time.strftime("%d")),\
                        end_time.strftime("%H"), end_time.strftime("%M"))
        
        return header + e_start_time + e_end_time
        
        
    @staticmethod
    def analyze_reservation_name(beam_name, language, by_request):
        if language == Language.ENGLISH:
            if by_request:
                return beam_name + " Reservation (Pending Approval)"
            else:
                return beam_name + " Reservation"
        elif language == Language.FRENCH:
            if by_request:
                return "Réservation de l'appareil " + beam_name + " (En attente d'approbation)"
            else:
                return "Réservation de l'appareil " + beam_name
        else:
            if by_request:
                return beam_name + "の予約（承認保留中）"
            else:
                return beam_name + "の予約"
    
    
    @staticmethod
    def convert_time_value(value):
        """      
        @summary: convert date or month 
        @param value: date/month
        @return: date/month
        @author: Thanh Le
        @created_date: February 21 , 2017
        """
        if value[:1] == "0":
            return value[-1:]
        return value


    @staticmethod
    def convert_am_pm_to_japanese(value):
        """      
        @summary: localize AM/PM to Japanese 
        @param value: AM/PM
        @return: AM/PM Japanese
        @author: Thanh Le
        @created_date: February 21 , 2017
        """
        if value == "AM":
            return u"午前"
        return u"午後"
        
    
    @staticmethod
    def format_time(date_time, running_locale):
        if running_locale == Language.ENGLISH:
            time_format = date_time.strftime("%I:%M %p")
            if time_format.startswith('0'):
                time_format = time_format[1:]
        elif running_locale == Language.FRENCH:
            time_format = date_time.strftime("%H:%M")
        
        return time_format
                
    
    @staticmethod
    def caculate_ordinal_number(date_time, running_locale):
        day = date_time.day
        
        if running_locale == Language.ENGLISH:
            if 4 <= day <= 20 or 24 <= day <= 30:
                return "th"
            else:
                return ["st", "nd", "rd"][day % 10 - 1]
        elif running_locale == Language.FRENCH:
            if day == 1:
                return 'er'
            else:
                return ''
    
    @staticmethod
    def get_utc_time_from_local_time(date_time):
        utc_timezone = timezone('Etc/UCT')
        local_tz = timezone(str(get_localzone()))
        local_dt = local_tz.localize(date_time)
        return local_dt.astimezone(utc_timezone)
        
        
    @staticmethod
    def convert_time_base_on_timezone(date_time, time_zone):
        #Convert date_time from local timezone to UTC 
        timestamp = time.mktime(date_time.timetuple())
        date_time = datetime.utcfromtimestamp(timestamp)
        
        #Convert date_time from UTC time to timezone on device        
        utc = timezone('UTC')
        date_time  = utc.localize(date_time)
        time_zone = timezone(time_zone)
        return date_time.astimezone(time_zone)
        
    @staticmethod
    def get_period_of_time_base_on_timezone():
        """      
        @summary: get period of time base on timezone (relating to fixed bug, test case c33707)
        @return: period time
        @author: Thanh Le
        @created_date: April 18 , 2017
        """
        local_tz = get_localzone()
        local_time = datetime.now(local_tz)
         
        time_zone = int(local_time.strftime('%z')[:-2])
        period_of_time = {}
        
        if time_zone > 0:
            period_of_time ['start'] = 0
            period_of_time ['end'] = time_zone - 1
        else:  
            period_of_time ['start'] = 24 + time_zone
            period_of_time ['end'] = 23
         
        return period_of_time
    
    
    @staticmethod
    def get_data_of_beam_link_date(language):
        """      
        @summary: Get the date of linking beam
        @param language: language
        @return: string date
        @author: Thanh Le
        @created_date: April 18 , 2017
        """
        if(language == 'ENGLISH'):
            link_date = 'Jun 2, 2016'
        elif (language == 'FRENCH'):
            link_date = '2 juin 2016'
        else:
            link_date = '2016/06/02' 
            
        return link_date


    @staticmethod
    def read_locale(locale):
        """
        @summary: read locale from file locales.json
        @param locale: locale
        @return: string locale
        @author: Khoi.Ngo
        @created_date: May 29, 2018
        """
        file_path = Helper.base_dir() + "\\data_test\\testdata\\resources\\locales.json".replace("\\", os.path.sep)
        with open(file_path, "r") as locales_file:
            locales = locales_file.read()
            locales = json.loads(locales)

        if locale == Locale.US:
            return locales[Locale.US]
        elif locale == Locale.FR:
            return locales[Locale.FR]


class EmailDetailHelper(object):
    _language = Language.ENGLISH
    
    @staticmethod
    def set_language(language):
        """      
        @summary: Set language   
        @param language: ENGLISH/JAPANESE/FRENCH 
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        EmailDetailHelper._language = language
    
    
    @staticmethod
    def generate_google_change_auth_email(receiver_email):
        """      
        @summary: Generate an expected "Your authentication method has been changed" template for asserting with the actual email        
        @param receiver_email: User Email object that receive email        
        @return: Message object
        @note: Because this email contains a random activation code so we cannot assert the trimmed_text_content directly. Instead, we should use re.match to check the content
                Please see the below example:            
                result = re.match(tmp_mail.trimmed_text_content, actual_msg[0].trimmed_text_content, re.I|re.M)
                self.assertTrue(result, "Assertion Error: Email content does not display as expected")
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        
        msg = Message()
        msg.set_subject(EmailDetailConstants.GoogleChangeAuthEmailTitle)
        content = EmailDetailConstants.GoogleChangeAuthEmailContent.format(receiver_email, Constant.SuitableTechURL)
        
        msg.set_text_content(content)
        return msg    
    
    
    @staticmethod
    def generate_connect_google_change_auth_email(receiver_email):
        """
        @summary: Generate an expected "Your authentication method has been changed" template for asserting with the actual email
        @param receiver_email: User Email object that receive email    
        @note: This email template only use when asserting email when change authentication from ST -> GSSO
        @author: Duy Nguyen
        @created_date: August 16, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.GoogleChangeAuthEmailTitle)
        content = EmailDetailConstants.GoogleChangeAuthConnectEmailContent.format(receiver_email)
        
        msg.set_text_content(content)
        return msg 
        
        
    @staticmethod
    def generate_welcome_email(user, admin_full_name=None, simplified=False, resent=False):
        """      
        @summary: Generate an expected "Welcome to Beam at <Org Name>" template for asserting with the actual email        
        @param user: User object that receive welcome email
        @param admin_full_name: Admin full name
        @return: Message object
        @note: Because this email contains a random activation code so we cannot assert the trimmed_text_content directly. Instead, we should use re.match to check the content
                Please see the below example:            
                result = re.match(tmp_mail.trimmed_text_content, actual_msg[0].trimmed_text_content, re.I|re.M)
                self.assertTrue(result, "Assertion Error: Email content does not display as expected")
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        raw_title = EmailDetailConstants.WelcomeEmailTitle
        default_message = Constant.DefaultMessage
        download_install_software_link = EmailDetailConstants.DownloadInstallSoftwareLink

        user_name = UserAPI.get_displayed_name(user, simplified).replace("+", "(.{1})")
        user_email_address = user.email_address.replace("+", "(.{1})")
        
        msg.set_subject(raw_title.format(user.organization))
        admin_full_name = admin_full_name.replace("+", "(.{1})")
        if simplified:
            if resent:
                raw_content = EmailDetailConstants.ResentWelcomeSimplifiedEmailContent
            else:
                raw_content = EmailDetailConstants.WelcomeSimplifiedEmailContent

            content = raw_content.format(user_name,
                                         admin_full_name,
                                         user.organization,
                                         default_message,
                                         download_install_software_link,
                                         user_email_address,
                                         admin_full_name)
        else:
            if user.invitation_settings.include_the_default_invitation_message is False:
                default_message = ''
            if user.invitation_settings.include_a_link_to_the_beam_software is False:
                download_install_software_link = ''

            content = EmailDetailConstants.WelcomeEmailContent.format(user_name,
                                         admin_full_name,
                                         user.organization,
                                         default_message,
                                         Constant.SuitableTechURL,
                                         user_email_address,
                                         download_install_software_link,
                                         admin_full_name)
        msg.set_text_content(content)
        return msg


    @staticmethod
    def generate_welcome_existing_email(user, admin_full_name=None, simplified=False):
        """      
        @summary: Generate an expected "Welcome to Beam at <Org Name>" template for asserting with the actual email. The email has existed in an org in advance and you create the same email in another org
        @param user: User object that receive welcome email
        @param admin_full_name: Admin full name
        @return: Message object
        @note: Please see the below example:            
                self.assertEqual(expected_message.trimmed_text_content, lst_emails[0].trimmed_text_content, "Assertion Error: Email content does not display as expected")
        @author: Tham Nguyen
        @created_date: August 05, 2016
        """
        msg = Message()
        user_name = UserAPI.get_displayed_name(user, simplified)
        msg.set_subject(EmailDetailConstants.WelcomeEmailTitle.format(user.organization))
        content = EmailDetailConstants.WelcomeExistingEmailContent.format(user_name, \
                                                                          admin_full_name, \
                                                                          user.organization, \
                                                                          user.email_address, \
                                                                          admin_full_name)
        
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_welcome_admin_copy_email(user, admin_full_name=None):
        """      
        @summary: Generate an expected "Welcome to Beam at <Org Name> (copy)" email template for asserting with the actual email        
        @param user: User object that receive welcome email
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.WelcomeAdminCopyEmailTitle.format(user.organization))

        user_email_address = user.email_address
        admin_full_name = admin_full_name
        
        default_message = Constant.DefaultMessage
        if user.invitation_settings.include_the_default_invitation_message is False:
            default_message = ''
        
        download_install_software_link = EmailDetailConstants.DownloadInstallSoftwareLink
        if user.invitation_settings.include_a_link_to_the_beam_software is False:
            download_install_software_link = ''

        content = EmailDetailConstants.WelcomeAdminCopyEmailContent.format(user_email_address,
                                                                            UserAPI.get_displayed_name(user), 
                                                                            admin_full_name,
                                                                            user.organization,
                                                                            default_message,
                                                                            user_email_address,
                                                                            download_install_software_link,
                                                                            admin_full_name)
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_request_access_email(device_group_name, requester, request_message=None):
        """      
        @summary: Generate an expected "[Beam] Someone is requesting access to your Beams" email template for asserting with the actual email        
        @param device_group_name: device group name that user requests access
        @param requester: User object that requests access
        @param request_message: Request message
        @return: Message object
        @note: Because this email contains a random activation code so we cannot assert the trimmed_text_content directly. Instead, we should use re.match to check the content
                Please see the below example:            
                result = re.match(tmp_mail.trimmed_text_content, actual_msg[0].trimmed_text_content, re.I|re.M)
                self.assertTrue(result, "Assertion Error: Email content does not display as expected")
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.BeamRequestAccessEmailTitle)
        
        user_info = requester.email_address.replace("+", "(.{1})")
        user_name = requester.first_name + " " + requester.last_name
        if EmailDetailHelper._language == Language.JAPANESE:
            user_info = r"{}（{}）".format(user_name, user_info)
        else:
            user_info = r"{} \({}\)".format(user_name, user_info)
        
        if(request_message == None or request_message == ""):
            request_message = ""
        else:
            request_message = EmailDetailConstants.RequestMessageLabel.format(request_message)
            
        content = EmailDetailConstants.BeamRequestAccessEmailContent.format(user_info, \
                                                                            device_group_name, \
                                                                            request_message, \
                                                                            Constant.SuitableTechURL, \
                                                                            Constant.SuitableTechURL, \
                                                                            Constant.SuitableTechURL)
                                                                            
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_added_to_device_group_email(device_group_name, admin_full_name=None):
        """      
        @summary: Generate an expected "[Beam] You have been added to <device group>" email template for asserting with the actual email        
        @param device_group_name: device group name that user requests access
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AddedToDeviceGroupEmailTitle.format(device_group_name))
        
        content = EmailDetailConstants.AddedToDeviceGroupEmailContent.format(device_group_name,
                                                                            admin_full_name,
                                                                            device_group_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_notification_added_to_device_group_email(device_group_name, admin_full_name=None, user_full_name=None):
        """      
        @summary: Generate an expected "[Beam] A user was added to <device group>" email template for asserting with the actual email        
        @param device_group_name: device group name that user requests access
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.NotificationAddedToDeviceGroupEmailTitle.format(device_group_name))
        
        content = EmailDetailConstants.NotificationAddedToDeviceGroupEmailContent.format(device_group_name,admin_full_name,user_full_name,device_group_name,Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    

    @staticmethod
    def generate_removed_from_device_group_email(device_group_name, admin_full_name=None):
        """      
        @summary: Generate an expected "[Beam] You have been removed from <device group>" email template for asserting with the actual email        
        @param device_group_name: device group name that user requests access
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.RemovedFromDeviceGroupEmailTitle.format(device_group_name))
        content = EmailDetailConstants.RemovedFromDeviceGroupEmailContent.format(device_group_name,
                                                                            admin_full_name,
                                                                            device_group_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_manage_device_group_email(device_group_name, admin_full_name=None):
        """      
        @summary: Generate an expected "[Beam] You can now manage <device group>" email template for asserting with the actual email        
        @param device_group_name: device group name that user requests access
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.ManageDeviceGroupEmailTitle.format(device_group_name))
        content = EmailDetailConstants.ManageDeviceGroupEmailContent.format(device_group_name,
                                                                            admin_full_name,
                                                                            device_group_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg


    @staticmethod
    def generate_removed_from_org_admin_email(organization_name=None, admin_full_name=None):
        """      
        @summary: Generate an expected "[Beam] You are no longer an administrator for <Organization name>" email template for asserting with the actual email        
        @param organization_name: organization name
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 02, 2016
        """
        if organization_name is None:
            organization_name = Constant.AdvancedOrgName
        msg = Message()
        msg.set_subject(EmailDetailConstants.RemovedFromOrgAdminEmailTitle.format(organization_name))
        content = EmailDetailConstants.RemovedFromOrgAdminEmailContent.format(organization_name,
                                                                            admin_full_name,
                                                                            organization_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_added_to_org_admin_email(organization_name, admin_full_name):
        """      
        @summary: Generate an expected "[Beam] You are now an administrator of <Organization name>" email template for asserting with the actual email        
        @param organization_name: organization name
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AddedToOrgAdminEmailTitle.format(organization_name))
        content = EmailDetailConstants.AddedToOrgAdminEmailContent.format(organization_name,
                                                                            admin_full_name,
                                                                            organization_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg

    
    @staticmethod
    def generate_welcome_temporary_user_email(user, start_time, end_time, device_list=None, admin_full_name=None, language=Language.ENGLISH):
        """      
        @summary: Generate an expected "You've been invited to Beam into <Org_Name>" email template for asserting with the actual email        
        @param user: User object that requests access
        @param start_time: Start time (A combination of date and time e.g. datetime.combine(date(2016, 8, 9), time(12, 00)) )
        @param end_time: End time (A combination of date and time e.g. datetime.combine(date(2016, 8, 9), time(12, 00)) )
        @param device_list: list of all devices in a the invited device group
        @param admin_full_name: Admin full name
        @return: Message object
        @note: Because this email contains a random activation code so we cannot assert the trimmed_text_content directly. Instead, we should use re.match to check the content
                Please see the below example:            
                result = re.match(tmp_mail.trimmed_text_content, actual_msg[0].trimmed_text_content, re.I|re.M)
                self.assertTrue(result, "Assertion Error: Email content does not display as expected")
        @author: Thanh Le
        @created_date: August 09, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.WelcomeTemporaryUserEmailTitle.format(user.organization))
        
        beam_number = ""
        beams_list = ""
        if(device_list):
            device_list.sort()
            for device in device_list:
                beams_list += u"{} ((.*)){}".format(device.replace("+", "(.{1})"), u"\r\n\r\n")
            
            if(len(device_list) == 1):
                beam_number = EmailDetailConstants.InvitationEmailDeviceList_Single
            elif(len(device_list) > 1):
                beam_number = EmailDetailConstants.InvitationEmailDeviceList_Multiple.format(len(device_list))

        
        _start_time = EmailDetailHelper._convert_to_email_datetime(start_time)
        _end_time = EmailDetailHelper._convert_to_email_datetime(end_time)
        admin_full_name = admin_full_name.replace("+", "(.{1})")
                                                                  
        content = EmailDetailConstants.WelcomeTemporaryUserEmailContent.format(UserAPI.get_displayed_name(user).replace("+", "(.{1})"),
                                                                            admin_full_name,
                                                                            user.organization,
                                                                            Constant.SuitableTechURL,
                                                                            user.email_address.replace("+", "(.{1})"),
                                                                            beam_number,
                                                                            beams_list,
                                                                            _start_time,
                                                                            _end_time,
                                                                            admin_full_name)
        
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_access_time_has_changed_email(device_group_name, admin_full_name=None,new_starting_datetime=None,new_ending_datetime=None):
        """      
        @summary: Generate an expected "[Beam] Your access time for <device group> has changed" email template for asserting with the actual email        
        @param device_group_name: device group name that beam is removed from
        @param admin_full_name: Admin full name who removed beam
        @return: Message object
        @author: Thanh Le
        @created_date: August 10, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.TemporaryAccessTimeHasChangedTitle.format(device_group_name))
        
        starting_datetime = EmailDetailHelper._convert_to_email_datetime(new_starting_datetime)
        ending_datetime = EmailDetailHelper._convert_to_email_datetime(new_ending_datetime)
        
        content = EmailDetailConstants.TemporaryAccessTimeHasChangedContent.format(device_group_name,
                                                                            admin_full_name,
                                                                            device_group_name,
                                                                            starting_datetime,
                                                                            ending_datetime,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg

        
    @staticmethod
    def _convert_to_email_datetime(date_time):
        """      
        @summary: Convert email datetime to default format           
        @param date_time: date time
        @return: datetime with French format 
        @author: Duy Nguyen
        @created_date: August 10, 2016
        """
        if EmailDetailHelper._language == Language.JAPANESE:
            return EmailDetailHelper._convert_to_email_datetime_ja_JP(date_time)
        elif EmailDetailHelper._language == Language.FRENCH:
            return EmailDetailHelper._convert_to_email_datetime_fr_FR(date_time)
        else:
            return EmailDetailHelper._convert_to_email_datetime_default(date_time)
    
    
    @staticmethod
    def _convert_to_email_datetime_default(date_time):
        """      
        @summary: Convert email datetime to default format           
        @param date_time: date time
        @return: datetime with default format 
        @author: Duy Nguyen
        @created_date: August 10, 2016
        """
        if len(date_time.strftime('%B'))<6:
            result = re.sub(' +',' ',date_time.strftime('%B %e, %Y, '))
        else:
            result = re.sub(' +',' ',date_time.strftime('%b. %e, %Y, '))
            result = result.replace("Sep", "Sept")
        
        if(datetime.strftime(date_time, "%p") == "PM"):
            am_pm = "p.m."
        else:
            am_pm = "a.m."
        
        hh = datetime.strftime(date_time, "%I")
        mm = datetime.strftime(date_time, "%M")
        
        if(hh[0] == "0"):
            hh = hh[1]
            
        if(mm == "00"):
            mm = " "
        else:
            mm = ":" + mm + " "
        
        am_pm = hh + mm + am_pm
        
        if(am_pm == "12 p.m."):
            am_pm = "noon"
        result += am_pm
        return result.strip()
    
    
    @staticmethod
    def _convert_to_email_datetime_fr_FR(date_time):
        """      
        @summary: Convert email datetime to French format           
        @param date_time: date time
        @return: datetime with French format 
        @author: Duy Nguyen
        @created_date: August 10, 2016
        """
        key = "MON%.2d" % (date_time.month)
        month_as_text =  ApplicationConst.get_date_time_label(key)
        result = re.sub(' +',' ',date_time.strftime('%e {} %Y %H:%M'))
        result = result.format(string.capwords(month_as_text))
        return result.strip()
    
    
    @staticmethod
    def _convert_to_email_datetime_ja_JP(date_time):
        """      
        @summary: Convert email datetime to Japanese format           
        @param date_time: date time 
        @return: datetime with Japanese format 
        @author: Duy Nguyen
        @created_date: August 10, 2016
        """
        _day = str(int(datetime.strftime(date_time, "%d")))
        _month = str(int(datetime.strftime(date_time, "%m")))
        _year = datetime.strftime(date_time, "%Y")
        _hour = str(int(datetime.strftime(date_time, "%H")))
        _minute = datetime.strftime(date_time, "%M")
        result = u"{}年{}月{}日{}:{}".format(_year, _month,_day,_hour,_minute)
        return result.strip()
    

    @staticmethod
    def generate_reservation_for_beam_was_create_email(beam, user_reserves_beam=None, user_is_reserved_for=None, start_time=None, end_time=None):
        """      
        @summary: Generate an expected "[Beam] A reservation for {} was created" email template for asserting with the actual email        
        @param 
        @param 
        @return: Message object
        @author: Tan Le
        @created_date: September 19, 2017
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AReservationForBeamWasCreateTitle.format(beam.beam_name))
        
        user_reserves_beam = UserAPI.get_displayed_name(user_reserves_beam)
        user_is_reserved_for = UserAPI.get_displayed_name(user_is_reserved_for)
        start_time_email  = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(start_time, beam.beam_id)
        end_time_email = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(end_time, beam.beam_id)
        
        if EmailDetailHelper._language == Language.JAPANESE:
            content = EmailDetailConstants.AReservationForBeamWasCreateContent.format(beam.beam_name,
                                                                                user_reserves_beam,
                                                                                user_is_reserved_for,
                                                                                beam.beam_name,
                                                                                user_is_reserved_for,
                                                                                beam.beam_name,
                                                                                start_time_email,
                                                                                end_time_email)          
        else:         
            content = EmailDetailConstants.AReservationForBeamWasCreateContent.format(beam.beam_name,
                                                                                user_reserves_beam,
                                                                                beam.beam_name,
                                                                                user_is_reserved_for,
                                                                                user_is_reserved_for,
                                                                                beam.beam_name,
                                                                                start_time_email,
                                                                                end_time_email)
        
        msg.set_text_content(content)
        return msg
        
        
    @staticmethod
    def generate_reject_reservation_email(beam, admin_reject_reservation=None, start_time=None, end_time=None):
        """      
        @summary: Generate an expected "[Beam] Your reservation for {} was rejected" email template for asserting with the actual email        
        @param 
        @param 
        @return: Message object
        @author: Tan Le
        @created_date: September 21, 2017
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AReservationIsRejectedTitle.format(beam.beam_name))
        
        admin_reject_reservation = UserAPI.get_displayed_name(admin_reject_reservation)

        start_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(start_time, beam.beam_id)
        end_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(end_time, beam.beam_id)
        content = EmailDetailConstants.AReservationIsRejectedContent.format(beam.beam_name,
                                                                            admin_reject_reservation,
                                                                            beam.beam_name,
                                                                            beam.beam_name,
                                                                            start_time,
                                                                            end_time)

        msg.set_text_content(content)
        return msg
    

    @staticmethod
    def generate_approve_reservation_email(beam, admin_approve_reservation=None, start_time=None, end_time=None):
        """      
        @summary: Generate an expected "[Beam] A reservation for {} was created" email template for asserting with the actual email        
        @param 
        @param 
        @return: Message object
        @author: Tan Le
        @created_date: September 21, 2017
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AReservationIsApprovedTitle.format(beam.beam_name))
        
        admin_approve_reservation = UserAPI.get_displayed_name(admin_approve_reservation)

        start_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(start_time, beam.beam_id)
        end_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(end_time, beam.beam_id)
        content = EmailDetailConstants.AReservationIsApprovedContent.format(beam.beam_name,
                                                                            admin_approve_reservation,
                                                                            beam.beam_name,
                                                                            beam.beam_name,
                                                                            start_time,
                                                                            end_time)
        
        msg.set_text_content(content)
        return msg
    

    @staticmethod
    def generate_remove_reservation_email(beam, user_remove_reservation=None, start_time=None, end_time=None):
        """      
        @summary: Generate an expected "[Beam] A reservation for {} was created" email template for asserting with the actual email        
        @param 
        @param 
        @return: Message object
        @author: Tan Le
        @created_date: September 21, 2017
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AReservationIsRemovedTitle.format(beam.beam_name))
        
        user_remove_reservation = UserAPI.get_displayed_name(user_remove_reservation)
        start_time_email  = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(start_time, beam.beam_id)
        end_time_email = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(end_time, beam.beam_id)
        
        content = EmailDetailConstants.AReservationIsRemovedContent.format(beam.beam_name,
                                                                            user_remove_reservation,
                                                                            beam.beam_name,
                                                                            beam.beam_name,
                                                                            start_time_email,
                                                                            end_time_email)
        
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def _convert_to_email_datetime_as_device_timezone(date_time, beam_id):
        """      
        @summary: Convert email datetime to default format           
        @param date_time: date time
        @return: datetime with French format 
        @author: Duy Nguyen
        @created_date: August 10, 2016
        """
        device_timezone = DeviceAPI.get_advanced_device_info(beam_id).json()['time_zone']
        datetime_on_device = Helper.convert_time_base_on_timezone(date_time, device_timezone)
        time_zone = str(datetime.strftime(datetime_on_device, "%Z"))
        if time_zone == "EST":
            time_zone = "AEST"

        if EmailDetailHelper._language == Language.JAPANESE:
            datetime_in_email = EmailDetailHelper._convert_to_email_datetime_ja_JP(datetime_on_device) + " "+ time_zone
            return datetime_in_email
        elif EmailDetailHelper._language == Language.FRENCH:
            datetime_in_email = EmailDetailHelper._convert_to_email_datetime_fr_FR(datetime_on_device) + " "+ time_zone
            return datetime_in_email
        else:
            datetime_in_email = EmailDetailHelper._convert_to_email_datetime_default(datetime_on_device) + " "+ time_zone
            return datetime_in_email
                                
                                
    @staticmethod
    def generate_add_to_user_group_email(user_group_name, admin_full_name=None):
        """      
        @summary: Generate an expected "You have been add to the group <User_Group_Name>" email template for asserting with the actual email        
        @param user_group_name: user group name 
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Duy Nguyen
        @created_date: August 10, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.AddToUserGroupEmailTitle.format(user_group_name))
        
        content = EmailDetailConstants.AddToUserGroupEmailContent.format(user_group_name,
                                                                            admin_full_name,
                                                                            user_group_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg


    @staticmethod
    def generate_password_changed_email(user_email_address):
        """      
        @summary: Generate an expected "Your password has changed" email template for asserting with the actual email        
        @param user_email_address: Email address of changing password user
        @return: Message object
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        
        msg = Message()
        msg.set_subject(EmailDetailConstants.PasswordChangedEmailTitle)
        content = EmailDetailConstants.PasswordChangedEmailContent.format(user_email_address, Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg


    @staticmethod
    def generate_password_reset_email(user_email_address):
        """      
        @summary: Generate an expected "Beam Password Reset" email template for asserting with the actual email        
        @param user_email_address: Email address of setting password user
        @return: Message object
        @note: Because this email contains a random activation code so we cannot assert the trimmed_text_content directly. Instead, we should use re.match to check the content
                Please see the below example:            
                result = re.match(tmp_mail.trimmed_text_content, actual_msg[0].trimmed_text_content, re.I|re.M)
                self.assertTrue(result, "Assertion Error: Email content does not display as expected")
        @author: Thanh Le
        @created_date: August 15, 2016
        """
        
        msg = Message()
        msg.set_subject(EmailDetailConstants.PasswordResetEmailTitle)
        content = EmailDetailConstants.PasswordResetEmailContent.format(Constant.SuitableTechURL,
                                                                        user_email_address.replace("+", "(.{1})"))
        msg.set_text_content(content)
        return msg

    
    @staticmethod
    def generate_can_now_accept_sessions_email(user, admin_full_name=None):
        """      
        @summary: Generate an expected "[Beam] You can now accept sessions for <Device Group>" email template for asserting with the actual email        
        @param user: User object 
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.CanNowAcceptSessionsEmailTitle.format(user.device_group))
        content = EmailDetailConstants.CanNowAcceptSessionsEmailContent.format(user.device_group,
                                                                                admin_full_name,
                                                                                user.device_group,
                                                                                Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_can_no_longer_accept_sessions_email(user, admin_full_name=None):
        """      
        @summary: Generate an expected "[Beam] You can no longer accept sessions for <Device_Group_Name>" email template for asserting with the actual email        
        @param user: User object 
        @param admin_full_name: Admin full name
        @return: Message object
        @author: Thanh Le
        @created_date: August 16, 2016
        """
        msg = Message()
        msg.set_subject(EmailDetailConstants.CanNoLongerAcceptSessionsEmailTitle.format(user.device_group))
        content = EmailDetailConstants.CanNoLongerAcceptSessionsEmailContent.format(user.device_group,
                                                                                    admin_full_name,
                                                                                    user.device_group,
                                                                                    Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    
    
    @staticmethod
    def generate_delete_device_group_email(user,organization_name):
        """      
        @summary: Generate an expected " [Beam] A device group was removed from <Organization Name>" email template for asserting with the actual email        
        @param user: User object 
        @param organization_name: Organization name
        @return: Message object
        @author: Duy Nguyen
        @created_date: September 15, 2016
        """    
        msg = Message()
        msg.set_subject(EmailDetailConstants.DeleteDeviceGroupEmailTitle.format(organization_name))
        content = EmailDetailConstants.DeleteDeviceGroupEmailContent.format(organization_name, organization_name, user.device_group, Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg
    

    @staticmethod
    def generate_beam_removed_from_device_group_email(device_group_name, admin_full_name = None, beam_name = None):
        """      
        @summary: Generate an expected "[Beam] A Beam was removed from <device group>" email template for asserting with the actual email        
        @param device_group_name: device group name that beam is removed from
        @param admin_full_name: Admin full name who removed beam
        @param beam_name: Beam name
        @return: Message object
        @author: Thanh Le
        @created_date: August 09, 2016
        """
        if beam_name == None:
            beam_name = Constant.BeamPlusMock4Name
        msg = Message()
        
        if 'BeamPro' in beam_name:
            name = 'Pro'
        else:
            name = ''
            
        msg.set_subject(EmailDetailConstants.BeamRemovedFromDeviceGroupTitle.format(name, device_group_name))
        
        content = EmailDetailConstants.BeamRemovedFromDeviceGroupContent.format(name,device_group_name,
                                                                            admin_full_name,
                                                                            beam_name,
                                                                            device_group_name,
                                                                            Constant.SuitableTechURL)
        msg.set_text_content(content)
        return msg


    @staticmethod
    def generate_reservation_for_beam_has_change(beam, user_admin,old_start_time=None,old_end_time=None, changed_start_time=None, change_end_time=None):
    #require beam, admin change,old_start_time, old_end_time changed start time, change end time

        msg = Message()
        msg.set_subject(EmailDetailConstants.AReservationIsChangedTitle.format(beam.beam_name))

        start_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(old_start_time, beam.beam_id)
        start_time=start_time[0:len(start_time)-4].strip()
        end_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(old_end_time, beam.beam_id)
        changed_start_time = EmailDetailHelper._convert_to_email_datetime_as_device_timezone(changed_start_time, beam.beam_id)
        changed_start_time = changed_start_time[0:len(changed_start_time)-4].strip()
        changed_end_time= EmailDetailHelper._convert_to_email_datetime_as_device_timezone(change_end_time, beam.beam_id)
        content = EmailDetailConstants.AReservationIsChangedContent.format(beam.beam_name,
                                                                            user_admin,
                                                                            beam.beam_name,
                                                                            beam.beam_name,
                                                                            start_time,
                                                                            end_time,
                                                                            changed_start_time,
                                                                            changed_end_time)

        msg.set_text_content(content)
        return msg
