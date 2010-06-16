#!/usr/bin/python

import sys
import traceback

import gobject

import dbus
import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
import networkmanager
import networkmanager.device
import networkmanager.applet

def get_connection(svc, conn_spec):
    applet = networkmanager.applet.NetworkManagerSettings(svc)
    for conn in applet.ListConnections():
        cs = conn.GetSettings()
        if cs["connection"]["id"] == conn_spec:
            return conn
    print "Connection '%s' not found" % conn_spec
    return None

def get_connection_devtype(conn):
    cs = conn.GetSettings()
    return cs["connection"]["type"]

def get_device(dev_spec, hint):
    candidates = []
    devs = networkmanager.NetworkManager().GetDevices()
    for dev in devs:
        if dev._settings_type() == hint:
            candidates.append(dev)
    if len(candidates) == 1:
        return candidates[0]
    for dev in devs:
        if dev["Interface"] == dev_spec:
            return dev
    print "Device '%s' not found" % dev_spec
    return None

def activate_vzw():
    print "Reactivating VZW connection"
    svc = "org.freedesktop.NetworkManagerUserSettings"
    conn = get_connection(svc, "Verizon connection")
    hint = get_connection_devtype(conn)
    dev = get_device("ttyUSB0", hint)
    appath = "/"
    networkmanager.NetworkManager().ActivateConnection(svc, conn, dev, appath)

def state_change_handler(*args, **kwargs):
    opath = kwargs["path"]
    (new, old, reason) = args
    news = networkmanager.device.Device.State(new)
    olds = networkmanager.device.Device.State(old)
    reasons = ""
    if reason != 0:
        reasons = " reason %d" % networkmanager.device.Device.StateReason(reason)
    print "\tDevice State %s\t(%s, was %s%s)" % (news, opath, olds, reasons)
    # 3 means DISCONNECTED
    if new == 3:
        activate_vzw()

if __name__ == '__main__':

    svc = "org.freedesktop.NetworkManagerUserSettings"
    bus = dbus.SystemBus()
    conn = get_connection(svc, "Verizon connection")
    hint = get_connection_devtype(conn)
    try:
        vzw = get_device("ttyUSB0", hint)
        activate_vzw()
        vzw.connect_to_signal('StateChanged', state_change_handler, dbus_interface='org.freedesktop.NetworkManager.Device', path_keyword="path")
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    loop=gobject.MainLoop()
    loop.run()


