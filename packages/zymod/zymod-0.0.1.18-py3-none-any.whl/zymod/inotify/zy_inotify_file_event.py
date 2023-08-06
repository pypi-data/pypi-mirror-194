import asyncio
import functools
import signal

import pyinotify
from happy_python import HappyLog

from zymod.inotify import ZyFileEventEnum


class ZyInotifyFileEvent:
    class EventHandler(pyinotify.ProcessEvent):
        def __init__(self, callback, pevent=None, **kargs):
            super().__init__(pevent, **kargs)

            self.__hlog = HappyLog.get_instance()
            self.__callback = callback

        def process_default(self, event):
            self.__hlog.var('event', event)

            self.__callback(event)

    def __init__(self):
        self.__hlog = HappyLog.get_instance()
        self.__loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__loop)

        self.__signal_handlers()

        self.__wm = pyinotify.WatchManager()

        self.__notifiers: list[pyinotify.AsyncioNotifier] = []

    def add_watch(self, file: str, events: list[ZyFileEventEnum], callback):
        handler = ZyInotifyFileEvent.EventHandler(callback=callback)

        # default_proc_fun参数在多个watch时，只有最后一个生效，此处禁止使用。
        notifier = pyinotify.AsyncioNotifier(self.__wm, self.__loop)
        self.__notifiers.append(notifier)

        mask: int = 0

        # 至少有一个事件
        assert events

        for e in events:
            mask |= e.value

        self.__wm.add_watch(file, mask, proc_fun=handler)

    def run_forever(self):
        try:
            self.__loop.run_forever()
        finally:
            self.__loop.close()

    def stop(self):
        if self.__loop.is_running():
            self.__loop.stop()

            for notifier in self.__notifiers:
                try:
                    notifier.stop()
                except OSError:
                    pass

    def __ask_exit(self, arg_signame):
        self.__hlog.info("got signal %s: exit" % arg_signame)
        self.stop()

    def __signal_handlers(self):
        # SIGINT: Interrupt from keyboard
        # SIGTERM: Termination signal
        for signame in {'SIGINT', 'SIGTERM'}:
            self.__loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(self.__ask_exit, signame))
