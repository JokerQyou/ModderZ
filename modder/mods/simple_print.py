# coding: utf-8
import os.path

# from modder import get_storage
from modder import on, trigger
# from modder import register


@on('Modder.Started')
# @on('Modder.BeforeQuit')
# @on('Timer.Interval.Minute')
def hello_world(event):
    print 'Hello Modder from', os.path.basename(__file__), event
    trigger('my_event')


# register(hello_world, 'Modder.Started')
