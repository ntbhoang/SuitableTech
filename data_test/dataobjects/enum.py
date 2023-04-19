from enum import Enum

class WeekDays(Enum):
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7
    
    def __cmp__(self, other):
        if self.value() > other.value():
            return 1
        elif self.value() < other.value():
            return -1
        else:
            return 0

class AccessTimesEventType(Enum):
    AllMembers = 1
    Member = 2
    
    def get_title(self):
        if self.value() == 1:
            return "AllMembers"
        else:
            return "Member"
