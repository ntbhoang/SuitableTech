import os
from time import sleep
import time
from datetime import datetime
from apiclient import discovery
from googleapiclient import errors
import httplib2
from oauth2client import client
from oauth2client import tools
import oauth2client
from common.constant import Constant
from common.stopwatch import Stopwatch
from core.utilities.utilities import Utilities
from data_test import testdata
from data_test.dataobjects.message import Message
from common.application_constants import ApplicationConst
from common.email_detail_constants import EmailDetailConstants


SCOPES = 'https://mail.google.com'
CLIENT_SECRET_FILE = 'google_api_client_secret.json'
APPLICATION_NAME = 'SuitableTechAutomation'
DEFAULT_EMAIL_WAIT_TIME_OUT = 120
    

class _GoogleInboxHandler(object):
    
    _mail_service = None
    
    def __init__(self, credential_file_name, user_id):
        self.credential_file_name = credential_file_name
        self.user_id = user_id
    
    
    def _get_credentials(self):
        """
        @summary: Gets valid user credentials from storage.
                    If nothing has been stored, or if the stored credentials are invalid,
                    the OAuth2 flow is completed to obtain the new credentials.
        @return: credentials, the obtained credential.
        @note: copied from Google document
        @author: Thanh le 
        @created_date: August 15, 2016
        """
        flags = None

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
            
        # copy file gmail-python-data.json to '.credentials' folder
        filename1 = os.path.sep.join([os.path.dirname(testdata.__file__), "google", self.credential_file_name])
        filename2 = os.path.sep.join([credential_dir, self.credential_file_name])
            
        source_file = open(filename1, "r")
        source_content = source_file.read()
        source_file.close()
        
        dest_file = open(filename2, 'w')
        dest_file.truncate()
        dest_file.write(source_content)
        dest_file.close()
            
        credential_path = os.path.join(credential_dir, self.credential_file_name)
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            file_name = os.path.dirname(testdata.__file__) + "\\google\\".replace("\\", os.path.sep) + CLIENT_SECRET_FILE
            flow = client.flow_from_clientsecrets(file_name, SCOPES, login_hint=self.user_id)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
        return credentials


    def get_google_service(self):
        """
        @summary: create GoogleService object, which is used to access Gmail storage.
        @return: mail service
        @author: Thanh le 
        @created_date: August 15, 2016
        """
        if(not self._mail_service):
            credentials = self._get_credentials()
            http = credentials.authorize(httplib2.Http())
            self._mail_service = discovery.build('gmail', 'v1', http=http)
        return self._mail_service
    
       
    def get_messages(self, user_id="me", query="", timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get a list of Messages from the user's mailbox.
        @param user_id: base email address
        @param query: query
        @return: list of messages
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        sw = Stopwatch()
        sw.start()    
        messages = []
        
        try:
            messages = self._get_messages(user_id, query)
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)
        except ConnectionResetError:
            print("ConnectionResetError occurs. Re-getting messages")
            sleep(3)
            messages = self._get_messages(user_id, query)
        except ConnectionAbortedError:
            print("ConnectionAbortedError occurs. Re-getting messages")
            while((not messages) and sw.elapsed().total_seconds() < timeout):
                messages = self._get_messages(user_id, query)
                time.sleep(1)
        
        return messages
    
    
    def _get_messages(self, user_id="me", query=""):  
        """
        @summary: get a list of Messages from the user's mailbox.
        @param user_id: base email address
        @param query: query
        @return: list of messages
        @author: Thanh Le
        @created_date: August 05, 2016
        """      
        results = self.get_google_service().users().messages().list(userId=user_id, q=query).execute() # "newer_than:3h"
        messages = []
        if 'messages' in results:
            messages.extend(results['messages'])
    
        while 'nextPageToken' in results:
            page_token = results['nextPageToken']
            response = self.get_google_service().users().messages().list(userId=user_id, q=query, pageToken=page_token).execute() # + "newer_than:3h"
            messages.extend(response['messages'])
            if len(messages) > 100:
                break
            
        return messages
    
    
    def get_message(self, user_id="me", message_id=None):
        """
        @summary: get raw data of a message by a specified ID
        @param usser_id: base email address
        @param message_id: message id
        @return: message
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        if(not message_id):
            return None
        try:
            message = self.get_google_service().users().messages().get(userId=user_id, id=message_id, format='raw').execute()
            return message
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)

         
    def delete_message(self, user_id="me", message_id=None):
        """
        @summary: delete message with specific ID
        @param usser_id: base email address
        @param message_id: message id
        @author: Duy Nguyen
        @created_date: August 05, 2016
        """
        if(not message_id):
            return None
        try:
            self.get_google_service().users().messages().delete(userId=user_id, id=message_id).execute()
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)
            
    
    def delete_all_messages(self, user__id="me", query=""):
        """
        @summary: Delete all emails in user's inbox
        @param usser_id: base email address
        @param message_id: message id
        @author: Thanh Le
        @created_date: August 05, 2016
        """
        messages = {
            'ids': []
        }
        temp = True

        try:
            while temp:
                raw_messages = self.get_messages(user__id, query)
                messages['ids'].extend([str(d['id']) for d in raw_messages])
                if(messages["ids"] != []):
                    self.get_google_service().users().messages().batchDelete(userId=user__id, body=messages).execute()
                    messages["ids"].clear()
                else:
                    temp = False
        except Exception as ex:
            print("There is a error while deleting all user emails. Error: " + str(ex))
        
           
class GmailUtility(object):
    
    gmail_handler_1 = _GoogleInboxHandler('gmail-python-credential-1.json', Constant.BaseEmails[1])
    gmail_handler_2 = _GoogleInboxHandler('gmail-python-credential-2.json', Constant.BaseEmails[2])
    gmail_handler_3 = _GoogleInboxHandler('gmail-python-credential-3.json', Constant.BaseEmails[3])
    gmail_handler_4 = _GoogleInboxHandler('gmail-python-credential-4.json', Constant.BaseEmails[4])
    gmail_handler_5 = _GoogleInboxHandler('gmail-python-credential-5.json', Constant.BaseEmails[5])
    lgvn_non_gsso_gmail_handler = _GoogleInboxHandler('lgvn-non-gsso-credential.json', Constant.AllowedGSSOEmails[0])
    lgvn_unallowed_gsso_gmail_handler = _GoogleInboxHandler('lgvn-gsso-credential.json', Constant.UnallowedGSSOEmails[0])

    
    @staticmethod
    def get_default_base_email(user_email):
        """
        @summary: get email address from 
        @param user_email: email name 
        @return: return full email address
        @author: Thanh Le
        @created_date: August 20, 2016
        """
        if user_email:            
            if "logigear1" in user_email:
                return Constant.BaseEmails[1]
            elif "logigear2" in user_email:
                return Constant.BaseEmails[2]
            elif "suitabletech3" in user_email:
                return Constant.BaseEmails[3]
            elif "suitabletech4" in user_email:
                return Constant.BaseEmails[4]
            elif "suitabletech5" in user_email:
                return Constant.BaseEmails[5]
            elif Constant.AllowedGSSOEmails == user_email:
                return Constant.AllowedGSSOEmails
            elif Constant.UnallowedGSSOEmails == user_email:
                return Constant.UnallowedGSSOEmails
    
    
    @staticmethod
    def get_gmail_handler(user_email):
        """
        @summary: create obj email handle 
        @param user_email: email name 
        @return: Obj of Gmail handle class with email address
        @author: Thanh Le
        @created_date: August 20, 2016        
        """
        email_default = GmailUtility.get_default_base_email(user_email)
        if email_default == Constant.BaseEmails[1]:
            return GmailUtility.gmail_handler_1
        elif email_default == Constant.BaseEmails[2]:
            return GmailUtility.gmail_handler_2
        elif email_default == Constant.BaseEmails[3]:
            return GmailUtility.gmail_handler_3
        elif email_default == Constant.BaseEmails[4]:
            return GmailUtility.gmail_handler_4
        elif email_default == Constant.BaseEmails[5]:
            return GmailUtility.gmail_handler_5
        elif email_default == Constant.AllowedGSSOEmails:
            return GmailUtility.lgvn_non_gsso_gmail_handler
        elif email_default == Constant.UnallowedGSSOEmails:
            return GmailUtility.lgvn_unallowed_gsso_gmail_handler
    
    
    @staticmethod
    def get_messages(mail_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get list messages match with params. using in test case
        @param mail_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: list messages
        @author: Thanh Le
        @created_date: August 20, 2016 
        """
        sw = Stopwatch()
        sw.start()
        ls_messages = None
        
        while((not ls_messages) and sw.elapsed().total_seconds() < timeout):
            ls_messages = GmailUtility._get_messages(mail_subject, sender, reply_to, receiver, sent_day)
            if not ls_messages:
                time.sleep(2)
                
        if(ls_messages == None):
            print ("*** No email match with expected condition ***")
            ls_messages = [] 
    
        return ls_messages
    
    
    @staticmethod
    def _get_messages(mail_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None):
        """
        @summary: get list messages match with params
        @param mail_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @return: list messages
        @author: Thanh Le
        @created_date: August 20, 2016         
        """
        frm = ""
        to = ""
        subj = ""
        ls_messages = []
        try:
            if mail_subject == None :
                mail_subject = ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE
            if mail_subject:
                subj = u"subject:\"{}\" ".format(mail_subject)
            if sender:
                frm = u"from:{} ".format(sender)
            if receiver:
                to = u"to:{} ".format(receiver)
            
            query_ = u"{}{}{}".format(subj, frm, to)

            default_base_email = GmailUtility.get_default_base_email(receiver)
            fetched_messages = GmailUtility.get_gmail_handler(receiver).get_messages(user_id=default_base_email, query=query_)
            
            if not fetched_messages:
                return None
            
            for g_message in fetched_messages:
                print ("*** get emails matching subject and sender ***")
                detail = GmailUtility.get_gmail_handler(receiver).get_message(user_id=default_base_email, message_id=g_message["id"])           
                wrapped_msg = Message()
                wrapped_msg.initialize(detail)
                wrapped_subject = Utilities.trimmed_text(wrapped_msg.subject)
                mail_subject = Utilities.trimmed_text(mail_subject)
                if wrapped_subject == mail_subject or (mail_subject in wrapped_subject):
                    if receiver:
                        if not (receiver in wrapped_msg.receiver):
                            continue
                    if sent_day:
                        if not wrapped_msg.is_sent_in_day(sent_day):
                            continue
                    if reply_to:
                        if not (reply_to in wrapped_msg._reply_to.lower()):
                            continue
                    
                    ls_messages.append(wrapped_msg)
            
        except Exception as e:
            print(e)
            return None
        
        return ls_messages
        
        
    @staticmethod
    def does_email_exist(mail_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: check email exist
        @param mail_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: true if email exist | false if email not exist
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        lst_messages = []
        while(not lst_messages and sw.elapsed().total_seconds() < timeout):
            lst_messages = GmailUtility.get_messages(mail_subject, sender, reply_to, receiver, sent_day)
                
        if lst_messages:
            return True
        
        return False
         
         
    @staticmethod
    def does_copy_email_exist(lst_copy_emails, expected_copy_email):
        """
        @summary: check copy email exist (Check copy email content)
        @param lst_copy_emails: list copy emails  
        @param expected_copy_email: expected copy email
        @return: true if email exist | false if email not exist
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        for g_message in lst_copy_emails:
            if(g_message.trimmed_text_content == expected_copy_email.trimmed_text_content):
                return True
            
        return False      
            
                
    @staticmethod
    def get_email_activation_link(email_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get activity link contain in the email
        @param email_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: activation link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        print("Getting activation link of user " + receiver)
        sw = Stopwatch()
        sw.start()
        mail_content = None
        activation_link = None
        
        if(email_subject == None):
            email_subject = ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE
            
        while(not activation_link and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(email_subject, sender, reply_to, receiver, sent_day)
        
            if mail_content != None:
                lines = mail_content.splitlines(False)
                
                for line in lines:
                    if line.startswith(Constant.SuitableTechURL + "/accounts/reset"):
                        activation_link = line
                        return activation_link
            
            sleep(3)  # sleep a few seconds to wait for email arrival.        
        
        raise Exception("Welcome email did not send to user")
    
    
    @staticmethod
    def get_temporary_password_for_normal_user(email_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT, localize = False):
        """
        @summary: get Temporary password contain in the email
        @param email_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: activation link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        mail_content = None
        temporary_password = None
        
        if(email_subject == None):
            email_subject = ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE
            
        while(not temporary_password and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(email_subject, sender, reply_to, receiver, sent_day)
        
            if mail_content != None:
                lines = mail_content.splitlines(False)
                if localize:
                    temppraryTitle = EmailDetailConstants.TemporaryPassword
                else:
                    temppraryTitle = "Temporary password"
                for line in lines:
                    if line.startswith(temppraryTitle):
                        if('： ' in line):
                            temporary_password = line.split('： ')[1]
                        else:
                            temporary_password = line.split(': ')[1]
                        
                        return temporary_password
            
            sleep(3)  # sleep a few seconds to wait for email arrival.        
        
        raise Exception("Welcome email did not send to user")
    

    @staticmethod
    def get_temporary_activation_link(sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT, email_subject=None):
        """
        @summary: get temporary activity link contain in the email
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: Temporary Activation link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        mail_content = None
        activation_link = None
        if(email_subject == None):
            email_subject = ApplicationConst.LBL_WELCOME_TEMPORARY_USER_EMAIL_TITLE
            
        while(not activation_link and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(email_subject, sender, reply_to, receiver, sent_day)
        
            if mail_content != None:
                lines = mail_content.splitlines(False)
                
                for line in lines:
                    if line.startswith(Constant.SuitableTechURL + "/accounts/reset"):
                        activation_link = line
                        return activation_link
                    
        raise Exception("Welcome Temporary email did not send to user")
    
    
    @staticmethod
    def get_temporary_password_for_temporary_user(email_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT, localize=False):
        """
        @summary: get Temporary password contain in the email
        @param email_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: activation link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        mail_content = None
        temporary_password = None
        
        if(email_subject == None):
            email_subject = ApplicationConst.LBL_WELCOME_TEMPORARY_USER_EMAIL_TITLE
            
        while(not temporary_password and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(email_subject, sender, reply_to, receiver, sent_day)
        
            if mail_content != None:
                lines = mail_content.splitlines(False)
                if localize:
                    temporaryTitle = EmailDetailConstants.TemporaryPassword
                else:
                    temporaryTitle = "Temporary password"
                for line in lines:
                    if line.startswith(temporaryTitle):
                        temporary_password = line.split(': ')[1]
                        return temporary_password
            
            sleep(3)  # sleep a few seconds to wait for email arrival.        
        
        raise Exception("Welcome email did not send to user")

        
    @staticmethod
    def get_approve_request_link(sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get approve request link contain in the email
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: approve request link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        mail_content = None
        
        while(not mail_content and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(EmailDetailConstants.BeamRequestAccessEmailTitle, sender, reply_to, receiver, sent_day)
        
        if mail_content:
            lines = mail_content.splitlines(False)
            
            for line in lines:
                if line.startswith(Constant.SuitableTechURL + "/r/") and line.endswith("/a/"):                    
                    return line
            
        raise Exception("Request Access email did not send to user")
    
    
    @staticmethod
    def get_reject_request_link(sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get reject request link contain in the email
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: reject request link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        mail_content = None
        
        while(not mail_content and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(EmailDetailConstants.BeamRequestAccessEmailTitle, sender, reply_to, receiver, sent_day)
                
        if mail_content:
            lines = mail_content.splitlines(False)
            
            for line in lines:
                if line.startswith(Constant.SuitableTechURL + "/r/") and line.endswith("/r/"):                    
                    return line
            
        raise Exception("Request Access email did not send to user")
    
    
    @staticmethod
    def get_reset_password_link(mail_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get reset password link contain in the email
        @param mail_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: reset password link
        @author: Thanh Le
        @created_date: August 20, 2016  
        """
        sw = Stopwatch()
        sw.start()
        mail_content = None
        
        while(not mail_content and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(mail_subject, sender, reply_to, receiver, sent_day)
                
        if mail_content:
            lines = mail_content.splitlines(False)
            
            for line in lines:
                if line.startswith(Constant.SuitableTechURL + "/accounts/reset"):
                    return line
            
        raise Exception("Password Reset email did not send to user")
        
        
    @staticmethod
    def get_email_content(mail_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get an email content
        @param mail_subject: Email's subject 
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: email content 
        @author: Thanh Le
        @created_date: August 20, 2016 
        """
        sw = Stopwatch()
        sw.start()
        lst_messages = []
        while(not lst_messages and sw.elapsed().total_seconds() < timeout):
            lst_messages = GmailUtility.get_messages(mail_subject, sender, reply_to, receiver, sent_day)
                
        if lst_messages:
            return lst_messages[0].text_content
        
        return None
    
    
    @staticmethod
    def delete_emails(mail_subject=None, sender=None, reply_to=None, receiver=None, sent_day=None, timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: delete all email with same subject, sender, receiver)
        @param mail_subject: Email's subject 
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @author: Duy Nguyen
        @created_date: August 20, 2016 
        """
        frm = ""
        to = ""
        subj = ""
        if mail_subject:
            subj = u"subject:'{}' ".format(mail_subject)
        if sender:
            frm = u"from:{} ".format(sender)
        if receiver:
            to = u"to:{} ".format(receiver)
        
        query_ = u"{}{}{}".format(subj, frm, to)
        default_base_email = GmailUtility.get_default_base_email(receiver)
        
        sw = Stopwatch()
        sw.start()
        fetched_messages=[]
        while (not fetched_messages and sw.elapsed().total_seconds() < timeout):
            fetched_messages = GmailUtility.get_gmail_handler(receiver).get_messages(user_id=default_base_email, query=query_)
        
        if not fetched_messages:
            return None
        
        for g_message in fetched_messages:
            detail = GmailUtility.get_gmail_handler(receiver).get_message(user_id=default_base_email, message_id=g_message["id"])           
            wrapped_msg = Message()
            wrapped_msg.initialize(detail)
            if sent_day:
                if not wrapped_msg.is_sent_in_day(sent_day):
                    continue
            if receiver:
                if wrapped_msg._to != receiver:
                    continue
            if reply_to:
                if wrapped_msg._reply_to != reply_to:
                    continue
            GmailUtility.get_gmail_handler(receiver).delete_message(user_id=default_base_email, message_id=g_message["id"])


    @staticmethod
    def delete_all_emails(receiver):
        """
        @summary: delete all emails
        @param receiver: email to
        @author: Duy Nguyen
        @created_date: August 20, 2016 
        """

        default_base_email = GmailUtility.get_default_base_email(receiver)
        GmailUtility.get_gmail_handler(receiver).delete_all_messages(default_base_email)


    @staticmethod
    def get_activity_export_link(email_subject=None, sender=None, reply_to=None, receiver=None, sent_day=datetime.now(), timeout=DEFAULT_EMAIL_WAIT_TIME_OUT):
        """
        @summary: get activity export csv link from email
        @param email_subject: Email's subject
        @param sender: email from
        @param reply_to: email reply
        @param receiver: email to
        @param sent_day: time send email
        @param timeout: time wait to get email
        @return: activity export csv link
        @author: Thanh Le
        @created_date: May 03, 2017  
        """
        print("Getting activity export link from email: " + receiver)
        sw = Stopwatch()
        sw.start()
        mail_content = None
        activity_export_link = None
        
        if(email_subject == None):
            email_subject = "[Beam] Your activity export for LogiGear Test is ready for download"
            
        while(not activity_export_link and sw.elapsed().total_seconds() < timeout):
            mail_content = GmailUtility.get_email_content(email_subject, sender, reply_to, receiver, sent_day)
        
            if mail_content != None:
                lines = mail_content.splitlines(False)
                
                for line in lines:
                    if line.startswith(Constant.SuitableTechURL + "/media/activity_exports"):
                        return line
            
            sleep(3)  # sleep a few seconds to wait for email arrival.        
        
        raise Exception("Email is not send to user.")
    
