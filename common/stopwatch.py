from datetime import datetime

class Stopwatch(object):

    def __init__(self):
        self._start = None

    
    def start(self):
        if(self._start == None):
            self._start = datetime.now()

    
    def elapsed(self):
        return (datetime.now() - self._start)
    