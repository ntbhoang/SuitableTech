import os.path
import re
from time import sleep
import urllib.request
from datetime import datetime
import locale

from PIL import Image

from common.helper import Helper
from data_test import testdata
import shutil
import caldav
from caldav.lib import error
import random
from data_test.dataobjects.reservation import Reservation
from common.application_constants import ApplicationConst
from common.constant import Language, Locale


class Utilities(object):
     
    @staticmethod
    def copy_and_rename_file(driver, scrfile):
        """
        @summary: Copy a file and rename that file with other name
        @param scrfile: source file
        @return: Return another file name
        @author: Thanh Le
        @created_date: April 18, 2017 
        """
        randome_text = "_" + datetime.now().strftime("%b%d%Y%H%M%S") + "."
        temp_filename = (Utilities.get_file_name(scrfile)).split('.')        
        filename = randome_text.join(temp_filename)        
        dstfile = Utilities.get_test_image_file_path(driver, filename)                
        
        try:            
            shutil.copy(scrfile , dstfile)
        except Exception as e:
            print(str(e))                    
        
        return filename

    
    @staticmethod
    def are_strings_equal(string1, string2):
        """
        @summary: Compare 2 strings together
        @param string1: string to compare
        @param string2: string to compare
        @return: True if 2 strings match together 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        #import unicodedata
        #unicodedata.normalize('NFKD', string1).encode('ascii', 'ignore')
        #unicodedata.normalize('NFKD', string2).encode('ascii', 'ignore')
        return string1.replace(u"\xa0", u" ") == string2.replace(u"\xa0", u" ")
     
     
    @staticmethod
    def compare_text_from_file(driver, file1, file2):
        """
        @summary: Compare 2 files together
        @param file1: string to compare
        @param file2: string to compare
        @return: True if 2 files match together 
        @author: Thanh Le
        @created_date: April 17, 2017
        """ 
        down_file1 = Utilities.get_test_image_file_path(driver, file1)
        down_file2 = Utilities.get_test_image_file_path(driver, file2)
        read_file1 = open(down_file1, "r").read().replace('\r\n', '\n')
        read_file2 = open(down_file2, "r").read().replace('\r\n', '\n')
        return read_file1 == read_file2
     
                
    @staticmethod
    def compare_HTML_texts(string1, string2):
        """
        @summary: Compare 2 strings with html type together
        @param string1: HTML1 to compare
        @param string2: HTML2 to compare
        @return: True if 2 strings match together 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        first_string = " ".join(string1.split())
        second_string = " ".join(string2.split())
        return first_string == second_string
     
     
    @staticmethod
    def does_contain_whole_word(word):
        """
        @summary: Check string just contains word
        @param word: word 
        @return: True if string just contains word
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search
     
     
    @staticmethod
    def is_number(txt):
        """
        @summary: Check string is number
        @param txt: txt 
        @return: True if string is number 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        try: 
            float(txt)
            return True
        except ValueError:
            return False
         
         
    @staticmethod
    def does_contain(search_list, primary_list):
        """
        @summary: Check if the first list is a child collection of the second list
        @param search_list: search_list
        @param primary_list: primary_list
        @return: True if the first list is a child collection of the second list
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        for item in search_list:
            if not item in primary_list:
                return False
        return True
     
     
    @staticmethod
    def generate_temporary_access_time_label(date_label, starting_datetime=None, ending_datetime=None):
        """
        @summary: Generate temporary access time label
        @param date_label: date_label
        @param starting_datetime: starting datetime
        @param ending_datetime: ending datetime
        @return: access time lable
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        time_label = ApplicationConst.get_date_time_label("All day")
         
        if starting_datetime and ending_datetime:
            start_hr = str(int (starting_datetime.strftime("%I")))
            start_mn = starting_datetime.strftime("%M")
            start_mr = ApplicationConst.get_date_time_label(starting_datetime.strftime("%p")).lower()  # lower() only use for temporary
             
            end_hr = str(int (ending_datetime.strftime("%I")))
            end_mn = ending_datetime.strftime("%M")
            end_mr = ApplicationConst.get_date_time_label(ending_datetime.strftime("%p")).lower()  # lower() only use for temporary
             
            time_label = "{}:{} {} - {}:{} {}".format(start_hr, start_mn, start_mr, end_hr, end_mn, end_mr)
             
        item_label = "{} {}".format(date_label, time_label)        
         
        return item_label
 
 
    @staticmethod
    def generate_access_time_label(access_days, starting_datetime=None, ending_datetime=None):
        """
        @summary: Generate access time label
        @param access_days: access_days
        @param starting_datetime: starting datetime
        @param ending_datetime: ending datetime
        @return: access time lable
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        access_days = sorted(access_days, key=lambda c: c.value)
         
        time_label = ApplicationConst.get_date_time_label("All day")
         
        if starting_datetime and ending_datetime:
            start_hr = str(int (starting_datetime.strftime("%I")))
            start_mn = starting_datetime.strftime("%M")
            start_mr = ApplicationConst.get_date_time_label(starting_datetime.strftime("%p"))
             
            end_hr = str(int (ending_datetime.strftime("%I")))
            end_mn = ending_datetime.strftime("%M")
            end_mr = ApplicationConst.get_date_time_label(ending_datetime.strftime("%p"))
             
            time_label = "{}:{} {} - {}:{} {}".format(start_hr, start_mn, start_mr, end_hr, end_mn, end_mr)
         
        day_lbl = ""
        if(len(access_days) == 7):
            day_lbl = ApplicationConst.get_date_time_label("every day")
        else:
            day_lbl = ', '.join((ApplicationConst.get_date_time_label(d.name) for d in access_days))
             
        item_label = "{} {}".format(time_label, day_lbl)        
         
        return item_label   
     
     
    @staticmethod
    def get_test_image_file_path(driver, file_name, handle_upload_flag=False):
        """
        @summary: Get test image file path
        @param file_name: file name
        @return: file's path
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        #list_browsers = ['Firefox', 'Safari']
        browser_name = driver._driverSetting.browser_name
        if handle_upload_flag:
            if browser_name == 'Safari':
                file_name = "group1_" + file_name
            elif browser_name == 'IE' and file_name == 'img_small_moving.png':
                file_name = "IE_" + file_name
        return os.path.join(os.path.dirname(testdata.__file__), "images", file_name)
     
     
    @staticmethod
    def delete_file(file_path):
        """
        @summary: Delete file at path
        @param file_path: the file's path 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
     
     
    @staticmethod
    def does_file_existed(file_path):
        """
        @summary: Check file exist
        @param file_path: the file's path 
        @return: True if the file exist
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        try:
            folder, file_name = os.path.split(file_path)
            for file in os.listdir(folder):
                if file == file_name:
                    return True
             
        except:
            pass
        return False
     
     
    @staticmethod
    def delete_all_files(folder_path):
        """
        @summary: Delete all file contains in the folder
        @param folder_path: the folder's path 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        try:
            if(os.path.exists(folder_path)):
                shutil.rmtree(folder_path)
                os.makedirs(folder_path)
        except Exception as ex:
            print(str(ex))
     
     
    @staticmethod
    def correct_link(file_url):
        """
        @summary: Correct a file's path
        @param file_url: file url
        @return: correct path 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        head, tail = os.path.split(file_url)
        file_name = tail.split('?')[0]
        return head + "/" + file_name
     
     
    @staticmethod
    def get_file_name(file_url):
        """
        @summary: get file name from url
        @param file_url: the url contains file name
        @return: file's name
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        file_name = os.path.split(file_url)[1]
        file_name = file_name.split("?")[0]
        if not file_name:
            file_name = "empty.tmp"
        return file_name
     
     
    @staticmethod
    def download_file(driver, file_url):
        """
        @summary: download file from url
        @param file_url: file's url
        @return: file's path
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        file_name = Utilities.get_file_name(file_url)
        file_path = Utilities.get_test_image_file_path(driver, file_name)
        
        f = open(file_path, 'wb')
        f.write(urllib.request.urlopen(file_url).read())
        f.close()
         
        return file_path
     
     
    @staticmethod
    def trimmed_text(text_content):
        """
        @summary: Trim text
        @param text_content: text content
        @return: trimmed text
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        if text_content:
            text_content = re.sub(r'\\r|\\n|\r|\n', '', text_content).strip()
            text_content = text_content.replace(u'\xa0', u' ').replace(' :', ':')
            return text_content
        return None
     
     
    @staticmethod
    def normalize_text(text_content):
        """
        @summary: Normalize text
        @param text_content: text content
        @return: text
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        text_content = text_content.replace(u'\xa0', u' ')
        return text_content
     
     
    @staticmethod
    def wait_for_file_is_downloaded(file_path, timeout=300):
        """
        @summary: Wait for file downloaded
        @param file_path: file's path
        @param timeout: time is to wait for downloading successfully
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        count = 0
        t_sleep = 1
        max_count = int(timeout / t_sleep)
        does_file_exist = Utilities.is_file_existed(file_path)  
        file_size = Utilities.get_file_size(file_path)
         
        while(count < max_count):
            if(does_file_exist == False or file_size <= 0):
                sleep(t_sleep)  # sleep 1 seconds to wait downloading completed
                does_file_exist = Utilities.is_file_existed(file_path)  
                file_size = Utilities.get_file_size(file_path)
                count += 1
            else:
                return
     
     
    @staticmethod
    def is_file_existed(file_path):
        """
        @summary: Check file existed
        @param file_path: file's path
        @return: True if the file exists, False if the file does not exist
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        return os.path.isfile(file_path.replace("\\", os.path.sep))
           
             
    @staticmethod
    def get_file_size(file_path):
        """
        @summary: Get file's size
        @param file_path: file's path
        @return: file size
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        try:
            return os.path.getsize(file_path)
        except:
            return 0
 
    
    @staticmethod
    def download_activity_export_csv_file(url_file):
        file_name = 'test' + datetime.now().strftime("%Y%m%dT%H%M%S") + '.csv'
        file_path = os.path.join(os.path.dirname(testdata.__file__), "csv", file_name)
        f = open(file_path, 'wb')
        f.write(urllib.request.urlopen(url_file).read())
        f.close()

        return file_path


    @staticmethod
    def convert_duaration_time_to_string(seconds, running_language):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
    
        if seconds > 45:
            minutes += 1
        if(hours != 0 and minutes > 30) or minutes == 60:
            hours += 1
        if(days != 0 and hours > 12) or hours == 24:
            days += 1
        
        if days == 1:
            xday = ApplicationConst.get_date_time_label("a day")
            return xday
        elif days != 0:
            xday = ApplicationConst.get_date_time_label("days")
            if running_language == Language.JAPANESE:
                return '{}{}'.format(days, xday)
            else:
                return '{} {}'.format(days, xday)
        elif hours == 1:
            xhour = ApplicationConst.get_date_time_label("an hour")
            return xhour
        elif hours != 0:
            xhour = ApplicationConst.get_date_time_label("hours")
            if running_language == Language.JAPANESE:
                return '{}{}'.format(hours, xhour)
            else:
                return '{} {}'.format(hours, xhour)
        elif minutes == 1:
            xminute = ApplicationConst.get_date_time_label("minute")
            return xminute
        elif minutes != 0:
            xminute = ApplicationConst.get_date_time_label("minutes")
            if running_language == Language.JAPANESE:
                return '{}{}'.format(minutes, xminute)
            else:
                return '{} {}'.format(minutes, xminute)
        elif seconds <= 45:
            xsecond = ApplicationConst.get_date_time_label("a few seconds")
            return xsecond
    
    
    @staticmethod
    def convert_datetime_to_local_for_tooltip_content(datetime_string_UTC, running_language):
        
        from dateutil import tz
        UTC_timezone = tz.gettz('UTC')
        locale_timezone = tz.tzlocal()
        datetime_at_UTC = datetime.strptime(datetime_string_UTC, '%Y-%m-%dT%H:%M:%SZ')
        datetime_at_UTC = datetime_at_UTC.replace(tzinfo=UTC_timezone)
        datetime_at_locale = datetime_at_UTC.astimezone(locale_timezone)

        #hardcode at WIB of string
        if running_language == Language.ENGLISH:
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
            hour = datetime.strftime(datetime_at_locale,'%I')
            if hour.startswith("0"):
                return datetime_at_locale.strftime('%A, %B %d, %Y ')+ hour[-1:] + datetime_at_locale.strftime(':%M %p WIB')
            else:
                return datetime_at_locale.strftime('%A, %B %d, %Y %I:%M %p WIB')

        elif running_language == Language.FRENCH:
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.FR))
            result = datetime_at_locale.strftime('%A %d %B %Y %H:%M WIB') 
            locale.setlocale(locale.LC_ALL, Helper.read_locale(Locale.US))
            return result

        elif running_language == Language.JAPANESE:
            weekday_dict = {'Sunday':u'日曜日', 'Monday':u'月曜日', 'Tuesday':u'火曜日', 'Wednesday':u'水曜日',\
                        'Thursday': u'木曜日', 'Friday': u'金曜日', 'Saturday': u'土曜日'}

            month = datetime.strftime(datetime_at_locale,'%m')
            if month.startswith("0"):
                return u"{}年{}月{}日 {} {} WIB".format(datetime_at_locale.strftime("%Y"), month[-1:], datetime_at_locale.strftime("%d"),\
                                                        weekday_dict[datetime_at_locale.strftime("%A")], datetime_at_locale.strftime("%H:%M"))
            else:
                return u"{}年{}月{}日 {} {} WIB".format(datetime.strftime(datetime_at_locale,"%Y"), datetime.strftime(datetime_at_locale,"%m"), datetime.strftime(datetime_at_locale,"%d"),\
                                                        weekday_dict[datetime.strftime(datetime_at_locale,"%A")], datetime.strftime(datetime_at_locale,"%H:%M"))
                
    @staticmethod
    def genarate_content_tooltip(list_info, running_language):
        device_name = list_info[0]["device"]["name"]
        status = (list_info[0]["state"])[6:]
        status = (status.replace("_", " ")).capitalize()
        if status == "In call":
            status = ApplicationConst.STATE_IN_A_CALL
        pilot = list_info[0]["user"]["first_name"] +" "+ list_info[0]["user"]["last_name"]
        start = list_info[0]["start"]
        start_time = Utilities.convert_datetime_to_local_for_tooltip_content(start, running_language)
        end = list_info[0]["end"]
        end_time = Utilities.convert_datetime_to_local_for_tooltip_content(end, running_language)
        duration_seconds = (datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')).seconds
        duration = Utilities.convert_duaration_time_to_string(duration_seconds, running_language)

        return ApplicationConst.CONTENT_OF_TOOLTIP.format(device_name, status, pilot, start_time, end_time, duration)


class CSV_Utilities(object):
     
    @staticmethod
    def _generate_invalid_first_last_name_array():
        return ["'@%$#^%$&^%*&^()(*)*)&(*(^%%$$#%@$!/\")'",
                "***[(.)_(.)b]***",
                "Hello".zfill(135),
                "<script>alert('hello');</script>",
                "<jsscript>alert(\"Hello world!\");</jsscript>"]
     
         
    @staticmethod
    def _generate_valid_first_last_name_array():
        return ["'http://g.nordstromimage.com/imagegallery/store/product/Medium/3/_9488583.jpg'",
                "https://www.google.com/images/srpr/logo11w.png",
                "suitable01", "suitable02", "tester9488505",
                "<CTRL+ALT+DEL>", "^altDel", "CTRL+ALT+DEL",
                "^a", "<CTRL+a>",
                "^c", "<CTRL+c>",
                "'./ps -ef'",
                "www.cnn.com/video/live/live_asx.html",
                "'www.cnn.com/video/live/live_asx_1234.html'"]
     
     
    @staticmethod
    def generate_invalid_users(number_of_users):
        """
        @summary: Create a list contains invalid users
        @param number_of_users: number of invalid users need to create
        @return: array of invalid users
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        from random import randint
        valid_array = CSV_Utilities._generate_valid_first_last_name_array()
        invalid_array = CSV_Utilities._generate_invalid_first_last_name_array()
        invalid_length = len(invalid_array) 
        valid_length = len(valid_array)        
        results = []   
         
        count = 0
        while count < number_of_users:
            count += 1
            rand = randint(0, valid_length - 1)
            fn = valid_array[rand]            
            rand2 = randint(0, invalid_length - 1)
            ln = invalid_array[rand2]
            email = Helper.generate_random_email()
            results.append([email, fn, ln])
         
        return results
     
     
    @staticmethod
    def generate_valid_users(number_of_users, special_chracter=True):
        """
        @summary: Create a list contains valid users
        @param number_of_users: number of valid users need to create
        @param special_chracter: True if containing special chracter
        @return: array of valid users
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        from random import randint
        test_array = CSV_Utilities._generate_valid_first_last_name_array()
        length = len(test_array)        
        results = []   
         
        count = 0
        while count < number_of_users:
            if special_chracter:
                rand = randint(0, length - 1)
                fn = test_array[rand]
                rand2 = randint(0, length - 1)
                while rand2 == rand:
                    rand2 = randint(0, length - 1)
                ln = test_array[rand2]
            else:
                fn = "FN CSV" + Helper.generate_random_not_special_string()
                ln = "LN CSV" + Helper.generate_random_not_special_string()
            count += 1
            email = Helper.generate_random_email()
            results.append([email, fn, ln])
         
        return results
     
     
    @staticmethod
    def generate_users_in_csv(file_name, number_of_users=5, generate_valid_data=True, special_character=True):
        """
        @summary: Create a file contains list valid users
        @param number_of_users: number of users need to create
        @param generate_valid_data: Set True if generating valid user. Set False if generating invalid user
        @param special_chracter: True if containing special chracter
        @return: csv file path
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        import csv
        _quoting = csv.QUOTE_NONE
         
        if(generate_valid_data):
            if special_character:
                users = CSV_Utilities.generate_valid_users(number_of_users)
            else:
                users = CSV_Utilities.generate_valid_users(number_of_users, special_character)
            csv_file_path = os.path.join(os.path.dirname(testdata.__file__), file_name)
        else:
            users = CSV_Utilities.generate_invalid_users(number_of_users)
            csv_file_path = os.path.join(os.path.dirname(testdata.__file__), "invalid_users.csv")
            _quoting = csv.QUOTE_MINIMAL
         
        # users.append(["abc", "fnfnfn", "lnlnln"])
        with open(csv_file_path, 'w') as tested_csv_file:
            csv_writer = csv.writer(tested_csv_file, lineterminator="\n", quoting=_quoting)
            for user in users:
                csv_writer.writerow(user)
             
        return csv_file_path
     
     
    @staticmethod
    def find_all_users_in_csv(csv_file_path):
        """
        @summary: Get list users in csv file
        @param csv_file_path: csv file's path
        @return: array of users 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        results = []
        try:
            with open(csv_file_path) as fff:
                for line in fff:
                    email = line.split(',')[0].strip()
                    results.append(email)
        except:
            print("Failed to read data from CSV file.")
         
        return results
     
     
    @staticmethod
    def find_users_info_in_csv(csv_file_path):
        """
        @summary: Get users info in csv file
        @param csv_file_path: csv file's path
        @return: Array of info users
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        from data_test.dataobjects.user import User
        results = []
        try:
            with open(csv_file_path) as fff:
                for line in fff:
                    user = User()
                    user.email_address = line.split(',')[0].strip()
                    user.first_name = line.split(',')[1].strip()
                    user.last_name = line.split(',')[2].strip()
                    results.append(user)
        except:
            print("Failed to read data from CSV file.")
         
        return results
     
    
    @staticmethod
    def does_csv_only_have_header(file_path):
        import csv
        if os.path.isfile(file_path):
            try:
                with open(file_path) as csvfile:
                    reader = csv.DictReader(csvfile)
                    return (len(list(reader)) == 0 and len(reader.fieldnames) != 0)
            except:
                print("Error while reading CSV file.")
        else:
            print("File does not exist")
            
        
    @staticmethod
    def read_export_activity_csv(file_path):
        import csv
        if os.path.isfile(file_path):
            try:
                count = 0
                with open(file_path) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for _ in reader:
                        count += 1
                return reader.line_num - 1
            except:
                print("Error while reading CSV file.")
        else:
            print("File does not exist")
        
        
class Image_Utilities(object):
 
    @staticmethod
    def are_images_similar(image_filepath1, image_filepath2, percentage_accuracy=90):
        """
        @summary: Calculate the similarity between 2 images      
        @param image_filepath1: local path of image1 
        @param image_filepath2: local path of image2
        @param percentage_accuracy: percentage accuracy
        @return: True if the 2 images are similar, False if the 2 images are not similar
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        try:
            similarity = Image_Utilities.image_similarity_vectors_via_numpy(image_filepath1, image_filepath2)
            if similarity * 100 >= percentage_accuracy:
                return True
        except:
            return False
         
        return False

     
    @staticmethod
    def get_thumbnail(image, size=(128, 128), stretch_to_fit=False, greyscale=False):
        """
        @summary: Get a smaller version of the image - makes comparison much faster/easier
        @param image: image 
        @param size: size
        @param stretch_to_fit: Set True if stretching the image to fit
        @param greyscale: Set True if converting the image to grayscale
        @return: image
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        if not stretch_to_fit:
            image.thumbnail(size, Image.ANTIALIAS)
        else:
            image = image.resize(size);  # for faster computation
        if greyscale:
            image = image.convert("L")  # Convert it to grayscale.
        return image
     
 
    @staticmethod
    def image_similarity_bands_via_numpy(filepath1, filepath2):
        """
        @summary: Image similarity bands via numpy
        @param filepath1: local path of image1 
        @param filepath2: local path of image2
        @return: 
        @author: Thanh Le
        @created_date: August 05, 2016 
        """
        import numpy
         
        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)
      
        # create thumbnails - resize em
        image1 = Image_Utilities.get_thumbnail(image1)
        image2 = Image_Utilities.get_thumbnail(image2)
         
        # this eliminated unqual images - though not so smarts....
        if image1.size != image2.size or image1.getbands() != image2.getbands():
            return -1
        similarity = 0
        for band_index in enumerate(image1.getbands()):
            m1 = numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size)
            m2 = numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size)
            similarity += numpy.sum(numpy.abs(m1 - m2))
        return similarity


    @staticmethod
    def image_similarity_vectors_via_numpy(filepath1, filepath2):
        """
        @summary: Image similarity vectors via numpy
        @param filepath1: local path of image1 
        @param filepath2: local path of image2
        @return: a float between 0 and 1 that indicated the percent similarity of the two images
        @note: One of the things is that if you wanted to compute how similar two images are, 
            you’d treat their pixels as vectors, normalize them, then take their dot product. 
            The result is a float between 0 and 1 that indicated the percent similarity of the two images. 
            This process is called the 'normalized cross correlation'. 
            After you got that number, it was a matter of setting a threshold as to what you wanted to accept as similar or not. 
        @author: Tan Le
        @created_date: June 22, 2017 
        """
        # source: https://www.cs.hmc.edu/~jlevin/ImageCompare.py
        # may throw: Value Error: matrices are not aligned . 
        im1 = Image.open(filepath1)
        im2 = Image.open(filepath2)
      
        randPix = im1.getpixel((0,0))
        maxSum = []
        diff = []
        for channel in range(len(randPix)):
            diff += [0.0]
            maxSum += [0.0]
        width = im1.size[0]
        height = im1.size[1]
        for i in range(width):
            for j in range(height):
                pixel1 = im1.getpixel((i,j))
                pixel2 = im2.getpixel((i,j))
                for channel in range(len(randPix)):
                    maxSum[channel] += 255
                    diff[channel] += abs(pixel1[channel] - pixel2[channel])
        ret = ()
        for channel in range(len(randPix)):
            ret = ret + (diff[channel]/maxSum[channel],)
        tmp = 1 - (ret[0] + ret[1] + ret[2])/3
        return tmp


    @staticmethod
    def convert_png_to_jpg(image_filepath_png):
        """
        @summary: Convert image png to jpg
        @param image_filepath_png: local path of image png
        @return: local path ò image jpg
        @author: Tan Le
        @created_date: Nov 10, 2017 
        """
        img = Image.open(image_filepath_png)
        rgb_img = img.convert('RGB')
        image_filepath_jpg = image_filepath_png[:-3]+ "jpg"
        rgb_img.save(image_filepath_jpg)
        Utilities.delete_file(image_filepath_png)
        return image_filepath_jpg


class Calendar_Utilities(object):

    @staticmethod
    def add_calendar_account(calendar_reservations_info):
        try:
            client = caldav.DAVClient(calendar_reservations_info['url'], username = calendar_reservations_info['user_name'], password = calendar_reservations_info['password'])
            # wating for sync data
            time_counter = 0
            while time_counter < 10:
                sleep(1)
                time_counter = time_counter + 1
                principal = client.principal()
                calendars = principal.calendars()
                if len(calendars) > 0:
                    break
            return client
        except Exception as ex:
            raise Exception('Could not add calendar account!' + str(ex))
    
    
    @staticmethod
    def does_calendar_account_added(calendar_client):
        if calendar_client.__class__.__name__ == 'DAVClient':
            return True
        else:
            return False


    @staticmethod
    def is_calendar_existed(calendar_client, beam_name):
        try:
            principal = calendar_client.principal()
            calendars = principal.calendars()
            
            for calendar in calendars:
                if(calendar.name == beam_name):
                    return True
            return False
        except Exception as ex:
            print("Could not get calendar data" + str(ex))
    
    
    @staticmethod
    def does_reservation_existed(calendar_client, reservation):
        calendar = Calendar_Utilities.get_data_of_a_calendar(calendar_client, reservation.beam_name)
        event = Calendar_Utilities.get_event_base_on_start_time(calendar, reservation.start_time)
        
        if event == 'No events exist in the calendar!':
            return False
        return True
    
    
    @staticmethod
    def add_calendar_event(calendar_client, reservation_data):
        try:
            Calendar_Utilities._add_calendar_event(calendar_client, reservation_data)
        except error.AuthorizationError or error.PutError:
            sleep(2)
            Calendar_Utilities._add_calendar_event(calendar_client, reservation_data)
        except Exception as ex:
            raise Exception('Could not add event!' + str(ex))


    @staticmethod
    def _add_calendar_event(calendar_client, reservation_data):
        start_time = Helper.get_utc_time_from_local_time(reservation_data.start_time).strftime("%Y%m%dT%H%M%SZ")
        end_time = Helper.get_utc_time_from_local_time(reservation_data.end_time).strftime("%Y%m%dT%H%M%SZ")
        stamp_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        event_id = datetime.utcnow().strftime("%Y%m%d") + str(random.randrange(100000, 999999, 6))
          
        event_info=(
            """BEGIN:VCALENDAR
            PRODID:suitabletech.com
            VERSION:2.0
            CALSCALE:GEORGIAN
            BEGIN:VEVENT
            DTSTAMP:{}
            DTSTART:{}
            DTEND:{}
            SUMMARY:LGVN Test
            UID:{}
            X-RADICALE-NAME:{}
            END:VEVENT
            END:VCALENDAR
            """).format(stamp_time, start_time, end_time, event_id, event_id).replace(' ', '')
        
        print(event_info)
        principal = calendar_client.principal()
        calendars = principal.calendars()
        
        for calendar in calendars:
            if(calendar.name == reservation_data.beam_name):
                event = calendar.add_event(event_info)
                return event
         
         
    @staticmethod
    def delete_reservation(calendar_client, reservation):
        try:
            calendar = Calendar_Utilities.get_data_of_a_calendar(calendar_client, reservation.beam_name)
            event = Calendar_Utilities.get_event_base_on_start_time(calendar, reservation.start_time)
            event.delete()
        except Exception as ex:
            raise("Could not delete event!" + str(ex))
        
    
    @staticmethod
    def get_event_id(calendar_client, reservation):
        calendar = Calendar_Utilities.get_data_of_a_calendar(calendar_client, reservation.beam_name)
        event = Calendar_Utilities.get_event_base_on_start_time(calendar, reservation.start_time)
        return Calendar_Utilities._get_event_id(event)
    
    
    @staticmethod
    def get_event_base_on_start_time(calendar, start_time):
        list_events = calendar.events()
        st_start_time = Helper.get_utc_time_from_local_time(start_time).strftime("%Y%m%dT%H%M%SZ")
        
        if list_events:
            for event in list_events:
                data_array = event.data.split('\n')
                for a in data_array:
                    if(a.startswith('DTSTART:')):
                        if a.split('DTSTART:')[1].strip()[:-3] == st_start_time[:-3]:
                            return event
            return None
        else:
            return 'No events exist in the calendar!'
        
    
    @staticmethod
    def get_event_name(calendar_client, reservation):
        calendar = Calendar_Utilities.get_data_of_a_calendar(calendar_client, reservation.beam_name)
        event = Calendar_Utilities.get_event_base_on_start_time(calendar, reservation.start_time)
        return Calendar_Utilities._get_event_name(event)
    
                        
    @staticmethod
    def _get_event_id(event):
        data_array = event.data.split('\n')
        
        for a in data_array:
            if a.startswith('UID:'):
                return a.split(':')[1].strip()
                           
    
    @staticmethod
    def _get_event_name(event):
        data_array = event.data.split('\n')
        
        for a in data_array:
            if a.startswith('SUMMARY:'):
                return a.split(':')[1].strip()
            
            
    @staticmethod
    def get_data_of_a_calendar(calendar_client, calendar_name):
        principal = calendar_client.principal()
        calendars = principal.calendars()
        
        for calendar in calendars:
            if calendar.name == calendar_name:
                return calendar
                

    @staticmethod
    def modify_reservation_time(calendar_client, reservation, edit_time):
        calendar = Calendar_Utilities.get_data_of_a_calendar(calendar_client, reservation.beam_name)
        event = Calendar_Utilities.get_event_base_on_start_time(calendar, reservation.start_time)
        edit_time['start_time'] = Helper.get_utc_time_from_local_time(edit_time['start_time']).strftime("%Y%m%dT%H%M%SZ")
        edit_time['end_time'] = Helper.get_utc_time_from_local_time(edit_time['end_time']).strftime("%Y%m%dT%H%M%SZ")
    
        if event:
            event_after_update_time = Reservation().update_event_time(event, edit_time)
            response = None
            try:
                principal = calendar_client.principal()
                calendars = principal.calendars()
                _respone = None
                 
                try:
                    for calendar in calendars:
                        if(calendar.name == reservation.beam_name):
                            _respone = calendar.add_event(event_after_update_time.data)
                except Exception as ex:
                    return str(ex).strip("\n\nb''")
         
                if response:
                    return _respone
    
            except Exception as ex:
                raise Exception("Could not update event!" + str(ex))


class Authetication_Utilities(object):

    @staticmethod
    def read_file_Oktaxml():
        OktaXML = open(os.path.join("..","..","..","data","testdata","authentication","Okta.xml"))
        return OktaXML.read()

