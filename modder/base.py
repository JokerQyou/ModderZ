# coding: utf-8


class ModBase(object):
    name = 'ModBase'

    def __init__(self):
        pass

    def __repr__(self):
        return '<{}>'.format(self.name)

    __str__ = __repr__