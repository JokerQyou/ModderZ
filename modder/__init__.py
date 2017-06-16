# coding: utf-8
import queue

from .event import CORE_EVENTS, Event
from .pool import ExecutorPool
from .storage import ModStorage, get_storage
from .timer import TimerThread
from .utils import desktop_notify

MOD_REGISTRY = {}
EVENT_QUEUE = queue.Queue()
GUI_MODE = False


def register(func, event_name):
    if event_name not in MOD_REGISTRY:
        MOD_REGISTRY[event_name] = []

    if func not in MOD_REGISTRY[event_name]:
        MOD_REGISTRY[event_name].append(func)


def on(event_name):

    def listener(func):
        register(func, event_name)

        return func

    return listener


def trigger(event_name, data=None):
    '''
    Trigger a mod-defined event.
    Notice: this function cannot trigger any core event.
    '''
    if event_name not in CORE_EVENTS:
        # TODO Support passing event data along with event name
        EVENT_QUEUE.put_nowait((event_name, data))


def notify(text, title=None, sound=False, url=None):
    '''Post a notification'''
    if GUI_MODE:
        desktop_notify(text, title=title, sound=sound, url=url)
    else:
        print title.decode('utf-8'), text.decode('utf-8')


__all__ = [
    'CORE_EVENTS', 'MOD_REGISTRY', 'EVENT_QUEUE',
    'register', 'on', 'trigger',
    'Event', 'TimerThread', 'ExecutorPool', 'ModStorage', 'get_storage',
    'exceptions',
]
