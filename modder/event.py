# coding: utf-8

EVENTS = (
    'Modder.Started',  # Modder core started
    'Modder.BeforeQuit',  # Modder is quitting
    'Timer.Interval.Minute',  # Triggered every minute
    'Timer.Interval.Hour',  # Triggered every hour
    'Timer.Interval.Day',  # Triggered every day
)


class Event(object):

    def __init__(self, name, data=None):
        self.__name = name
        self.__data = data or {}

    @property
    def name(self):
        return self.__name

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError('No such attribute {}'.format(name))

    def __repr__(self):
        return '<Event {} at 0x{:02x}>'.format(self.__name, id(self))

    __str__ = __repr__
