from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, unique


@unique
class XSeconds(IntEnum):
    DAY = 86400
    HOUR = 3600
    MINUTE = 60
    SECOND = 1

    def get_unit_desc(self) -> str:
        units = {XSeconds.DAY: 'days', XSeconds.HOUR: 'h', XSeconds.MINUTE: 'min', XSeconds.SECOND: 'sec'}

        assert self in units.keys()

        return units[self]


@dataclass
class TimeDuration:
    day: int
    hour: int
    minute: int
    second: int

    def __str__(self):
        output = ''

        if self.day != 0:
            output += '%s days, ' % self.day

        if self.hour != 0:
            output += '%s h, ' % self.hour

        if self.minute != 0:
            output += '%s min, ' % self.minute

        if self.second != 0:
            output += '%s sec' % self.second

        return output[: len(output) - 2] if output.endswith(', ') else output

    def asdict(self):
        return {
            'Day': self.day,
            'Hour': self.hour,
            'Minute': self.minute,
            'Second': self.second,
        }


class TimeDurationCalculator:
    @staticmethod
    def __calculate(seconds: float, xs_index: int = 0) -> list[int]:
        xs_enums = [m for m in XSeconds]
        xs = xs_enums[xs_index]

        output = [int(seconds // xs.value)]

        if xs_index < (len(xs_enums) - 1):
            output += TimeDurationCalculator.__calculate(seconds % xs.value, xs_index + 1)

        return output

    @staticmethod
    def calculate(d1: datetime, d2: datetime) -> TimeDuration:
        td = d1 - d2 if d1 >= d2 else d2 - d1

        values = TimeDurationCalculator.__calculate(td.total_seconds())

        symbol_values = values

        for i in range(0, len(values)):
            if d1 < d2 and values[i] != 0:
                symbol_values[i] = -abs(values[i])
                break

        return TimeDuration(day=symbol_values[0],
                            hour=symbol_values[1],
                            minute=symbol_values[2],
                            second=symbol_values[3])
