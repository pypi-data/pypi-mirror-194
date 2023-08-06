from dataclasses import dataclass, asdict

from happy_python import dict_to_pretty_json


@dataclass
class ZySystemdUnitProp:
    """
    see 'man org.freedesktop.systemd1'
    """
    primary_unit_name: str
    desc: str
    load_state: str
    active_state: str
    sub_state: str
    followed: str
    object_path: str
    job_id: int
    job_type: str
    job_object_path: str

    def asdict(self):
        return asdict(self)

    def asjson(self):
        return dict_to_pretty_json(self.asdict())
