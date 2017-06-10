# coding: utf-8
from .event import EVENTS, Event
from .pool import ExecutorPool
from .storage import ModStorage, get_storage
from .timer import TimerThread

MOD_REGISTRY = {}


def register(func, event_name):
    if event_name not in EVENTS:
        raise UserWarning(
            '{} cannot be registered because {} is not a valid event'.format(func, event)
        )
        return

    if event_name not in MOD_REGISTRY:
        MOD_REGISTRY[event_name] = []

    if func not in MOD_REGISTRY[event_name]:
        MOD_REGISTRY[event_name].append(func)


def on(event_name):

    def listener(func):
        if event_name in EVENTS:
            register(func, event_name)

        return func

    return listener


__all__ = [
    'EVENTS', 'MOD_REGISTRY',
    'register', 'on',
    'Event', 'TimerThread', 'ExecutorPool', 'ModStorage', 'get_storage',
    'exceptions',
]
