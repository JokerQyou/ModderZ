# coding: utf-8
import os.path
import time

from modder import get_storage
from modder import on
# from modder import register


# @on('Modder.Started')
# @on('Modder.BeforeQuit')
# @on('Timer.Interval.Minute')
@on('my_event')
def hello_world(event):
    print 'Hello Modder from', os.path.basename(__file__), event

    store = get_storage('hello_world_2')
    saved = store.load()
    if saved.get('timestamp', None):
        print 'Last saved timestamp in', store.name, ':', saved['timestamp']

    store.save({'timestamp': time.time()})


# register(hello_world, 'Modder.Started')
