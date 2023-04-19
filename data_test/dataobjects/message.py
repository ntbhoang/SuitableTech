from googleapiclient import errors
import base64
import email
from datetime import datetime

class Message(object):
    
    def __init__(self):
        self._id = None
        self._origin_messsage = None
        self._date = None
        self._html_content = None
        self._text_content = None
        self._subject = None
        self._from = None
        self._to = None
        self._reply_to = None
            
    def initialize(self, origin__message):
        self._id = origin__message['id']
        self._origin_messsage = origin__message
        try:
            if('raw' in origin__message):                
                self._parse_message_content(origin__message['raw'])
                
        except errors.HttpError as error:
            print('An error occurred: %s' % error )
            
    def __cmp__(self, other):
        """
        @description: used for comparation method, by date. newer date will be put in previous index.
        """
        if not self._date:
            return 1
        
        if self._date > other._date:
            return -1
        elif self._date < other._date:
            return 1
        else:
            return 0
        
    @property
    def origin_message(self):
        return self._origin_messsage
    
    @property
    def date(self):
        return self._date
    
    @property
    def html_content(self):
        return self._html_content
    
    @property
    def text_content(self):
        return self._text_content
    
    def set_text_content(self, text_content):
        self._text_content = text_content
    
    @property
    def subject(self):
        return self._subject
    
    def set_subject(self, subject): 
        self._subject = subject
    
    @property
    def sender(self):
        return self._from
    
    @property
    def reply_to(self):
        # in SuitableTech project, the sender account is always 'support@suitabletech.com'
        # the real 'sender' is put in the field 'reply-to' 
        return self._reply_to
    
    @property
    def receiver(self):
        return self._to
    
    @property
    def trimmed_text_content(self):
        from core.utilities.utilities import Utilities
        return Utilities.trimmed_text(self._text_content)
    
    
    def is_sent_in_day(self, date_):
        """
        @summary: check the current date with selected date (date_). 
        @param date_: Date want to check
        @return: TRUE if current date different with selected date otherwise FALSE
        @author: Thanh Le 
        """
        if not self._date:
            return False
        
        return self._date.strftime("%d%m%Y") == date_.strftime("%d%m%Y")
    
    def _parse_message_content(self, raw_msg):
        """
        @description: extract information from the raw content of an email, include Subject, From, To, HTML-content 
        """
        msg_str =  base64.urlsafe_b64decode(raw_msg.encode('ASCII'))                
        mime_msg = None
        if(type(msg_str).__name__ == 'bytes'):
            mime_msg = email.message_from_bytes(msg_str)
        else:
            mime_msg = email.message_from_string(msg_str)
        
        if("Subject" in mime_msg):
            hdr = email.header.make_header(email.header.decode_header(mime_msg['Subject']))
            self._subject = str(hdr)
        
        if("From" in mime_msg):
            frm = email.header.make_header(email.header.decode_header(mime_msg['From']))
            self._from = str(frm)
        
        if("Reply-To" in mime_msg):
            rep_to  = email.header.make_header(email.header.decode_header(mime_msg['Reply-To']))
            self._reply_to = str(rep_to)
        
        if("To" in mime_msg):
            to = email.header.make_header(email.header.decode_header(mime_msg['To']))
            self._to = str(to)
        
        sent_date = email.header.make_header(email.header.decode_header(mime_msg['Date']))
        self._date = self._parse_date(str(sent_date) )
        
        for part in mime_msg.walk():
            if part.get_content_type() == "text/html": # ignore attachments/html
                body = part.get_payload(decode=True)
                self._html_content = body.decode('utf-8')
            elif part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True) #to control automatic email-style MIME decoding (e.g., Base64, uuencode, quoted-printable)
                self._text_content = body.decode()
        return self
    
    def _parse_date(self, date_as_text):
        """
        @summary: parse date to format Tue, 26 Jul 2016 08:08:08 +0000
        @param date_as_text: date need to be parse
        @return: return date as format Tue, 26 Jul 2016 08:08:08 +0000
        @author: Thanh Le
        """
        return datetime.strptime(date_as_text, "%a, %d %b %Y %H:%M:%S %z") # Tue, 26 Jul 2016 08:08:08 +0000
