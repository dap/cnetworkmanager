# -*- coding: utf-8 -*-

import dbus
from dbusclient import DBusClient, object_path
from dbusclient.func import *
from device import Device
from activeconnection import ActiveConnection
from base import Base
from util import Enum

# gratuitous convertor to test writable properties
def english_to_bool(v):
    if v == "yes":
        return True
    elif v == "no":
        return False
    return v

class NetworkManager(Base):
    """networkmanager
    
    The NM client library
    
     Methods:
    GetDevices ( ) → ao
    ActivateConnection ( s: service_name, o: connection, o: device, o: specific_object ) → o
    DeactivateConnection ( o: active_connection ) → nothing
    Sleep ( b: sleep ) → nothing
    
     Signals:
    StateChanged ( u: state )
    PropertiesChanged ( a{sv}: properties )
    DeviceAdded ( o: device_path )
    DeviceRemoved ( o: device_path )
    
     Properties:
    WirelessEnabled - b - (readwrite)
    WirelessHardwareEnabled - b - (read)
    ActiveConnections - ao - (read)
    State - u - (read) (NM_STATE)
    
     Enumerated types:
    NM_STATE
    """

    SERVICE = "org.freedesktop.NetworkManager"
    OPATH = "/org/freedesktop/NetworkManager"
    IFACE = "org.freedesktop.NetworkManager"

    def __init__(self):
        super(NetworkManager, self).__init__(self.SERVICE, self.OPATH, default_interface=self.IFACE)


    class State(Enum):
        UNKNOWN = 0
        ASLEEP = 1
        CONNECTING = 2
        CONNECTED = 3
        DISCONNECTED = 4

    "TODO find a good term for 'adaptor'"

#from dbusclient.adaptors import *

NetworkManager._add_adaptors(
    GetDevices = MA(seq_adaptor(Device._create)),
    ActivateConnection = MA(ActiveConnection, identity, object_path, object_path, object_path),
    DeactivateConnection = MA(void, object_path),

    State = PA(NetworkManager.State),
    WirelessEnabled = PA(bool, english_to_bool),
    WirelessHardwareEnabled = PA(bool),
    ActiveConnections = PA(seq_adaptor(ActiveConnection)),

    StateChanged = SA(NetworkManager.State),
    )

