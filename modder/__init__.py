# coding: utf-8
from .base import ModBase

MOD_REGISTRY = {}


def register(func, event_name):
    if event_name not in MOD_REGISTRY:
        MOD_REGISTRY[event_name] = []

    if func not in MOD_REGISTRY[event_name]:
        MOD_REGISTRY[event_name].append(func)