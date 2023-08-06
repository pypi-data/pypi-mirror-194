import dbus
from happy_python import HappyLog

from zymod.systemd import ZySystemdManager


class ZySystemdUnit:
    def __init__(self, name: str):
        self.hlog = HappyLog.get_instance()
        self.name = name
        self.manager = ZySystemdManager()
        self.bus = dbus.SystemBus()
        self.obj_timer = self.bus.get_object(bus_name='org.freedesktop.systemd1',
                                             object_path=self.manager.get_unit(self.name))

        self.interface_props = dbus.Interface(object=self.obj_timer,
                                              dbus_interface='org.freedesktop.DBus.Properties')

    def get_prop(self, name: str):
        props = self.interface_props.GetAll('org.freedesktop.systemd1.Unit')

        return props[name]
