# coding: utf-8
import time

from modder import get_storage
from modder import on
# from modder import register


# @on('Modder.Started')
# @on('Modder.BeforeQuit')
# @on('Timer.Interval.Minute')
def hello_world(event):
    store = get_storage('hello_world')
    saved = store.load()
    if saved.get('timestamp', None):
        print 'Last saved timestamp in', store.name, ':', saved['timestamp']

    store.save({'timestamp': time.time()})
    print 'Hello Modder!', event


# register(hello_world, 'Modder.Started')
