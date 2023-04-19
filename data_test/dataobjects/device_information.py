
class DeviceInfo(object):
    
    def __init__(self, system_info, network_info):
        self._system_info = system_info
        self._network_info = network_info
    
    @property
    def system_info(self):
        return self._system_info
    
    @property
    def network_info(self):
        return self._network_info

class DeviceSystemInformation(object):
    
    def __init__(self, serial_number, uid, sofware_version):
        self._serial_number = serial_number
        self._uid = uid
        self._sofware_version = sofware_version
        
    @property
    def serial_number(self):
        return self._serial_number
    
    @property
    def uid(self):
        return self._uid 
    
    @property
    def sofware_version(self):
        return self._sofware_version

class DeviceNetworkInformation(object):
    
    def __init__(self, current_network, network_interfaces, relay_server):
        self._current_network = current_network
        self._network_interfaces = network_interfaces
        self._relay_server = relay_server
    
    @property
    def current_network(self):
        return self._current_network    
    @property
    def network_interfaces(self):
        return self._network_interfaces    
    @property
    def relay_server(self):
        return self._relay_server
    
class CurrentNetwork(object):
    
    def __init__(self, ssid, mac, frequency):
        self._ssid = ssid
        self._mac = mac
        self._frequency = frequency
    
    @property
    def ssid(self):
        return self._ssid
    @property
    def mac(self):
        return self._mac
    @property
    def frequency(self):
        return self._frequency    

class NetworkInterface(object):
    def __init__(self, name, type_name, mac, ip_address):
        self._name = name
        self._type_name = type_name
        self._mac = mac
        self._ip_address = ip_address
        
    @property
    def name(self):
        return self._name
    @property
    def type_name(self):
        return self._type_name
    @property
    def mac(self):
        return self._mac
    @property
    def ip_address(self):
        return self._ip_address
        
class RelayServer(object):
    def __init__(self, ip_address):
        self._ip_address = ip_address
    
    @property
    def ip_address(self):
        return self._ip_address
    

    