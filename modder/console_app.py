# coding: utf-8
'''
Start a Modder2 instance without GUI support
'''
import atexit
import queue
import threading

from .manager import ModManager
from .timer import TimerThread


def main():
    event_queue = queue.Queue()
    mod_manager = ModManager()
    event_queue.put('Modder.Started')

    timer_stop = threading.Event()
    timer_thread = TimerThread(event_queue, timer_stop)
    timer_thread.daemon = True
    timer_thread.start()

    def before_quit():
        timer_stop.set()
        # TODO Fix `Modder.BeforeQuit` event not triggering
        mod_manager.trigger('Modder.BeforeQuit')

    atexit.register(before_quit)

    while 1:
        try:
            event_name = event_queue.get(timeout=1)
        except queue.Empty:
            pass
        else:
            mod_manager.trigger(event_name)


if __name__ == '__main__':
    main()
