from enum import Enum
from core import i18n
import os
from common.application_constants import ApplicationConst
from common.email_detail_constants import EmailDetailConstants
class I18NLanguage(Enum):
    default = 1
    ja_JP = 2
    fr_FR = 3
    
class I18NSupport(object):
    
    @staticmethod
    def set_language(language=I18NLanguage.default):
        """
        @summary: this method allows data language (Japan, French). using this data language to compare with the Suitable Technologies site
        @param language: the language we need to test (Englis, French, Japan. default value is English)
        @return: return data (string text, message, label, content email, ...) match with language
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        lc_dir = os.path.join(os.path.dirname(i18n.__file__), "locale")
        
        import gettext
        gettext.translation('appstring', localedir=lc_dir, languages=[language.name]).install()
        ApplicationConst.initialize()
        
        gettext.translation('date_time', localedir=lc_dir, languages=[language.name]).install()
        ApplicationConst.initialize_date_time_localization()
        
        gettext.translation('email_content', localedir=lc_dir, languages=[language.name]).install()
        EmailDetailConstants.initialize()
        
    
    @staticmethod
    def localize_date_time_string(english_text):
        """
        @summary: this method returns appropriate date time string based on language that you want
        @param english_text: language (Japan, French and English)
        @return return date time string following the language
        @author: Thanh Le
        @created_date: August 5, 2016
        """
        
        tmp = english_text
        
        for key, value in ApplicationConst._date_time_localized_values.items():
            tmp = tmp.replace(key, value)
        
        return tmp
    
    
