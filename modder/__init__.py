# coding: utf-8
from boltons.funcutils import wraps
from .base import ModBase
from .event import EVENTS, Event

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
