# coding: utf-8
'''
Start a Modder2 instance without GUI support
'''
import atexit
from queue import Empty
import threading

from . import EVENT_QUEUE
from .manager import ModManager
from .timer import TimerThread


def main():
    mod_manager = ModManager()
    EVENT_QUEUE.put(('Modder.Started', None))

    timer_stop = threading.Event()
    timer_thread = TimerThread(EVENT_QUEUE, timer_stop)
    timer_thread.daemon = True
    timer_thread.start()

    def before_quit():
        timer_stop.set()
        # TODO Fix `Modder.BeforeQuit` event not triggering
        mod_manager.trigger('Modder.BeforeQuit')

    atexit.register(before_quit)

    while 1:
        try:
            event_name, event_data = EVENT_QUEUE.get(timeout=1)
        except Empty:
            pass
        else:
            mod_manager.trigger(event_name, data=event_data)


if __name__ == '__main__':
    main()
