import dbus

from zymod.systemd import ZySystemdUnitProp


class ZySystemdManager:
    def __init__(self):
        # CentOS7使用systemd v219，systemd v221才提供sd-bus支持，所以使用dbus
        self.bus = dbus.SystemBus()
        self.obj_systemd = self.bus.get_object(bus_name='org.freedesktop.systemd1',
                                               object_path='/org/freedesktop/systemd1')

        self.interface_manager = dbus.Interface(object=self.obj_systemd,
                                                dbus_interface='org.freedesktop.systemd1.Manager')

        self.interface_props = dbus.Interface(object=self.obj_systemd,
                                              dbus_interface='org.freedesktop.DBus.Properties')

    def list_units(self) -> list[ZySystemdUnitProp]:
        result: list[ZySystemdUnitProp] = []

        # 根据名称过滤结果的方法systemd v219不支持，比如 ListUnitsByPatterns
        for unit in self.interface_manager.ListUnits():
            result.append(ZySystemdUnitProp(primary_unit_name=str(unit[0]),
                                            desc=str(unit[1]),
                                            load_state=str(unit[2]),
                                            active_state=str(unit[3]),
                                            sub_state=str(unit[4]),
                                            followed=str(unit[5]),
                                            object_path=str(unit[6]),
                                            job_id=int(unit[7]),
                                            job_type=str(unit[8]),
                                            job_object_path=str(unit[9])))

        return result

    def get_unit(self, name: str):
        return self.interface_manager.GetUnit(name)

    def get_prop(self, name: str):
        props = self.interface_props.GetAll('org.freedesktop.systemd1.Manager')

        return props[name]
