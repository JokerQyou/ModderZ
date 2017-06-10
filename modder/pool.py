# coding: utf-8
from threading import Thread
from multiprocessing import Process

from .exceptions import Full


class ExecutorPool(object):
    '''A simple container designed to contain Thread or Process instances'''

    def __init__(self, maxsize=-1):
        super(ExecutorPool, self).__init__()

        self.__size = int(maxsize)
        self.__pool = []

    @property
    def maxsize(self):
        '''Get size capability of pool, -1 means no limit'''
        return self.__size

    @property
    def size(self):
        '''Get current number of items in pool'''
        return len(self.__pool)

    def add(self, item):
        '''Add item to pool, raise `Full` if pool is full'''
        if not isinstance(item, (Thread, Process, )):
            raise TypeError('ExecutorPool cannot contain type {}'.format(type(item)))

        if self.__size == -1:
            self.__pool.append(item)
        else:
            if len(self.__pool) >= self.__size:
                raise Full('Container is full ({:d} items currently)'.format(self.size))
            else:
                self.__pool.append(item)

    def __non_alive(self, item):
        '''Detect whether given item is not alive'''
        if isinstance(item, (Thread, Process, )):
            return item.is_alive()
        else:
            return False

    def clean_up(self):
        '''Clean up all non-alive item in pool'''
        pool = filter(self.__non_alive, self.__pool)
        if not isinstance(pool, list):
            pool = list(pool)

        self.__pool = pool

    def __repr__(self):
        return '<ExecutorPool maxsize={:d} at 0x{:02x}>'.format(self.maxsize, id(self))

    __str__ = __repr__
