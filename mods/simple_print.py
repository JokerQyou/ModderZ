# coding: utf-8
from modder import register


def hello_world(event):
    print 'Hello Modder!', event


register(hello_world, 'Modder.Started')