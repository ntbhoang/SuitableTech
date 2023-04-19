import datetime
import random

class Reservation(object):
    
    def __init__(self):
        self.beam_name = None
        self.user_displayed_name = None
        self.start_time = None
        self.end_time = None

    def generate_start_time_and_end_time(self):
        random_day = random.randrange(1, 9)
        plus_day = random.randrange(0, 1)
        plus_hour= random.randrange(1, 12)
        
        self.start_time = (datetime.datetime.now() + datetime.timedelta(days=random_day, hours = plus_hour))
        self.end_time = (datetime.datetime.now() + datetime.timedelta(days=(random_day + plus_day), hours= plus_hour + 1))
        
    
    def generate_start_time_and_end_time_in_the_past(self):
        random_day = random.randrange(1, 9)
        plus_day = random.randrange(0, 1)
        
        self.start_time = (datetime.datetime.now() + datetime.timedelta(days = -(random_day)))
        self.end_time = (datetime.datetime.now() + datetime.timedelta(days=(-(random_day) + plus_day), hours=1))
        
    
    def generate_start_time_and_end_time_in_period_of_time(self, start, end):
        """      
        @summary: generate start time and end time in period of time (relating to fixed bug, test case c33707)
        @param start: start of period
        @param end: end of period 
        @author: Thanh Le
        @created_date: April 18 , 2017
        """
        random_hour = random.randrange(start, end)
        random_day = random.randrange(1, 9)
        plus_day = random.randrange(0, 1)
        
        start_date = (datetime.datetime.now() + datetime.timedelta(days=random_day)).strftime('%Y-%m-%d')
        start_hour = str(random_hour) + ":00:00"
        
        self.start_time = datetime.datetime.strptime(start_date + " " + start_hour,'%Y-%m-%d %H:%M:%S')
        self.end_time = self.start_time + datetime.timedelta(days=plus_day, hours=1)
    
    
    def generate_edit_start_time_and_end_time(self):
        num = {}
        random_day = random.randrange(1, 9)
        plus_day = random.randrange(0, 2)
        
        num['start_time'] = (self.start_time + datetime.timedelta(days=random_day))
        num['end_time'] = (self.start_time + datetime.timedelta(days=(random_day + plus_day), hours=1))
        
        return num


    @staticmethod
    def update_event_time(event, edit_time):
        data_event = event.data.split("\n")
        tmp_event = ""
        for dat in data_event:
            print(dat)
            if "DTSTART" not in dat and "DTEND" not in dat:
                tmp_event = tmp_event + dat + "\n"
            else:
                if "DTSTART" in dat:
                    tmp_event = tmp_event + "DTSTART:" + edit_time['start_time'] + "\n"
                else:
                    tmp_event = tmp_event + "DTEND:" + edit_time['end_time'] + "\n"
            
        event.data = tmp_event
        
        return event
    
    