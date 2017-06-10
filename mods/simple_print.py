# coding: utf-8
from modder import register, on


@on('Modder.Started')
@on('Modder.BeforeQuit')
@on('Timer.Interval.Minute')
def hello_world(event):
    print 'Hello Modder!', event


# register(hello_world, 'Modder.Started')
