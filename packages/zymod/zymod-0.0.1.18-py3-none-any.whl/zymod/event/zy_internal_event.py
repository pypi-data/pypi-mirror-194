from happy_python import HappyLog

from zymod.event import ZyEventLevel


class ZyInternalEvent(Exception):
    def __init__(self, level: ZyEventLevel, summary: str, description: str, trigger: str):
        super().__init__(self, '%s: %s' % (summary, description))

        self.level = level
        self.summary = summary
        self.description = description
        self.trigger = trigger

        self.hlog = HappyLog.get_instance()

        self.hlog.debug('ZyInternalEvent->%s' % self.asdict())

    def asdict(self) -> dict:
        return {
            "level": self.level.value,
            "summary": self.summary,
            "description": self.description,
            "trigger": self.trigger
        }
