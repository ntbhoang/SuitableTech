class Beam(object):
    #Beam attributes   
    def __init__(self):
        self._beam_id = None
        self._beam_name = None
        self._org = None # pro / plus
    
    
    def initialize(self, beam_id, beam_name, org):
        """
        @summary: Get beam data from beam.json file and lock this beam
        @param beam_type: beam type to get
        @author: thanh.viet.le
        @created: December 22, 2016
        """
        self._beam_id = beam_id
        self._beam_name = beam_name
        self._org = org
        
        
    @property
    def beam_id(self):
        return self._beam_id
    @property
    def beam_name(self):
        return self._beam_name
    @property
    def beam_org(self):
        return self._org
    
    
    def set_beam_id(self, beam_id):
        self._beam_id = beam_id
    
    
    def set_beam_name(self, beam_name):
        self._beam_name = beam_name
    
    
    def set_beam_org(self, org):
        self._org = org
        
