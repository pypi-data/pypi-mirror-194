import time
from datetime import datetime

from zymod.systemd import ZySystemdUnit, ZySystemdTimerProp


class ZySystemdTimer(ZySystemdUnit):
    # 18446744073709551615
    SYSTEMD_MAX_INT = 2 ** 64 - 1

    def __init__(self, name: str):
        super().__init__(name)

    def __calc_next_elapse(self,
                           now_ts: float,
                           now_monotonic_ts: float,
                           next_usec: int,
                           next_monotonic_usec: int) -> float:
        """
        see 'usec_t calc_next_elapse(dual_timestamp *nw, dual_timestamp *next)'
        in 'src/systemctl/systemctl-list-units.c'
        """
        func_name = '__calc_next_elapse'
        self.hlog.enter_func(func_name)

        self.hlog.input('now_ts', now_ts)
        self.hlog.input('now_monotonic_ts', now_monotonic_ts)
        self.hlog.input('next_usec', next_usec)
        self.hlog.input('next_monotonic_usec', next_monotonic_usec)

        if next_usec == self.SYSTEMD_MAX_INT or next_monotonic_usec == self.SYSTEMD_MAX_INT:
            self.hlog.output('result', 0)

            self.hlog.exit_func(func_name)
            return 0

        next_ts = next_usec / (1000 ** 2)
        self.hlog.var('next_ts', next_ts)

        next_monotonic_ts = next_monotonic_usec / (1000 ** 2)
        self.hlog.var('next_monotonic_ts', next_monotonic_ts)

        if next_monotonic_ts == 0:
            self.hlog.output('result', next_ts)

            self.hlog.exit_func(func_name)
            return next_ts

        if next_monotonic_ts > now_monotonic_ts:
            converted = now_ts + (next_monotonic_ts - now_monotonic_ts)
        else:
            converted = now_ts - (now_monotonic_ts - next_monotonic_ts)

        self.hlog.var('converted', converted)

        result = min(converted, next_ts) if next_ts > 0 else converted
        self.hlog.output('result', result)

        self.hlog.exit_func(func_name)

        return result

    def get_timer_prop(self) -> ZySystemdTimerProp:
        func_name = 'get_timer_prop'
        self.hlog.enter_func(func_name)

        props = self.interface_props.GetAll('org.freedesktop.systemd1.Timer')

        next_elapse_ts = self.__calc_next_elapse(time.time(),
                                                 time.monotonic(),
                                                 props['NextElapseUSecRealtime'],
                                                 props['NextElapseUSecMonotonic'])
        next_elapse = datetime.fromtimestamp(next_elapse_ts)

        last_trigger_ts = props['LastTriggerUSec'] / (1000 ** 2)
        last_trigger = datetime.fromtimestamp(last_trigger_ts)

        timers_calendar: list[('', '')] = []

        for tc in props['TimersCalendar']:
            timers_calendar.append((str(tc[0]), str(tc[1])))

        result = ZySystemdTimerProp(timer_name=self.name,
                                    unit_name=str(props['Unit']),
                                    timers_calendar=timers_calendar,
                                    next_elapse=next_elapse,
                                    last_trigger=last_trigger,
                                    result=str(props['Result']),
                                    persistent=bool(props['Persistent']),
                                    wake_system=bool(props['WakeSystem']))
        self.hlog.output('result', result)

        self.hlog.exit_func(func_name)

        return result
