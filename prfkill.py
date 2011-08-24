#!/usr/bin/env python2

# prfkill - rfkill switch listener
#
# Copyright (C) 2011 Reza Jelveh

import gtk
import gobject

import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

types = dict()
types[1] = "WLAN"
types[2] = "Bluetooth"

appname = "prfkill"
appicon = "/usr/share/icons/ubuntu-mono-light/status/24/nm-device-wireless.svg"

class Display:
    def __init__(self, labels, wmname=appname):
        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.set_title(wmname)
        self.window.set_border_width(1)
        self.window.set_default_size(180, -1)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.window.connect("destroy", lambda x: self.window.destroy())
        timer = gobject.timeout_add(2000, lambda: self.window.destroy())

        table = gtk.Table(2, 2, True)

        icon = gtk.Image()
        icon.set_from_file(appicon)
        icon.show()

        table.attach(icon, 0, 1, 0, 2)

        # widgetbox.pack_start(icon)
        i = 0
        for str in labels:
            label = gtk.Label(str)
            # table.attach(icon, 0
            table.attach(label, 1, 2, i, 1+i)
            i += 1

        # self.window.add(widgetbox)
        table.show()
        self.window.add(table)
        self.window.show_all()

class RfkillAdapter:
    def get_device(self, device_name):
        device = bus.get_object("org.freedesktop.URfkill", device_name)
        props = device.GetAll('org.freedesktop.URfkill.Device',
                    dbus_interface="org.freedesktop.DBus.Properties")
        if props['hard']:
            label =  types[props['type']], ": hard locked"
        else:
            label =  types[props['type']], ": unlocked"

        return "".join(label)

    def device_removed_callback(self, device):
        print 'Device %s was removed' % (device)
        self.print_devices()

    def show_status(self, device):
        devices = self.iface.get_dbus_method('EnumerateDevices')()
        labels = []
        for device in devices:
            labels.append(self.get_device(device))
        Display(labels)


    def __init__(self):
        self.proxy = bus.get_object("org.freedesktop.URfkill",
                "/org/freedesktop/URfkill")
        self.iface = dbus.Interface(self.proxy, "org.freedesktop.URfkill")

        #addes two signal listeners
        self.iface.connect_to_signal('DeviceAdded', self.show_status)
        self.iface.connect_to_signal('DeviceChanged', self.show_status)
        # self.iface.connect_to_signal('DeviceRemoved', self.device_removed_callback)



#must be done before connecting to DBus
DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()

rf = RfkillAdapter()

#start the main loop
mainloop = gobject.MainLoop()
mainloop.run()
