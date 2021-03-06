# coding: utf-8
import threading
import time


class TimerThread(threading.Thread):
    def __init__(self, queue, stop_event):
        super(TimerThread, self).__init__()
        self.__queue = queue
        self.__stopped = stop_event
        self.__wait = 1

        now = time.time()
        self.__last_trigger_minute = now
        self.__last_trigger_hour = now
        self.__last_trigger_day = now

    def run(self):
        while not self.__stopped.wait(self.__wait):
            now = time.time()
            passed_minute = now - self.__last_trigger_minute
            passed_hour = now - self.__last_trigger_hour
            passed_day = now - self.__last_trigger_day

            if passed_minute >= 60:
                self.__last_trigger_minute = now
                self.__queue.put(('Timer.Interval.Minute', None))

            if passed_hour >= 3600:
                self.__last_trigger_hour = now
                self.__queue.put(('Timer.Interval.Hour', None))

            if passed_day >= 86400:
                self.__last_trigger_day = now
                self.__queue.put(('Timer.Interval.Day', None))
