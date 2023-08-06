from dataclasses import dataclass, asdict
from datetime import datetime

from happy_python import dict_to_pretty_json


@dataclass
class ZySystemdTimerProp:
    """
    see 'man 5 systemd.timer'
    """
    timer_name: str
    unit_name: str
    timers_calendar: list[(str, str)]
    next_elapse: datetime  # 下次运行时间
    last_trigger: datetime  # 上次运行时间
    result: str
    persistent: bool
    wake_system: bool

    def asdict(self):
        return asdict(self)

    def asjson(self):
        return dict_to_pretty_json(self.asdict())
