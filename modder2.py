# coding: utf-8
import atexit
import glob
import importlib
import os.path
import queue
import threading
import time

import modder


class ModManager(object):

    def __init__(self, mod_directory=None):
        if not mod_directory:
            mod_directory = os.path.join(os.path.dirname(__file__), 'mods')
        self.mod_directory = mod_directory
        self.__pool = None

        self.check_mod_directory()
        self.load_mods()
        self.init_pool()

    def init_pool(self):
        '''Init pool container for mod executors'''
        if self.__pool is None:
            pool_size = 0
            for event, mods in modder.MOD_REGISTRY.items():
                pool_size += len(mods)

            self.__pool = modder.ExecutorPool(pool_size)

    def check_mod_directory(self):
        '''Make sure `mod_directory` is a valid Python package'''
        if not os.path.isdir(self.mod_directory):
            os.makedirs(self.mod_directory)

        package_init_file = os.path.join(self.mod_directory, '__init__.py')
        if not os.path.isfile(package_init_file):
            with open(package_init_file, 'w') as wf:
                wf.write('# coding: utf-8')

    def load_mods(self):
        '''Import all modules in `mod_directory`'''
        base_package = os.path.basename(self.mod_directory)
        for pyfile in glob.glob('{}/*.py'.format(base_package)):
            # Get module name out of file path
            pymodule_name = os.path.splitext(os.path.basename(pyfile))[0]
            # Import target module
            importlib.import_module('{}.{}'.format(base_package, pymodule_name))

    def execute(self, mod_func, event):
        '''Trigger a registered mod callable'''
        if callable(mod_func):
            mod_worker = threading.Thread(
                target=mod_func,
                name='{} on {} event'.format(mod_func.__name__, event.name),
                args=(event, )
            )
            mod_worker.daemon = True

            try:
                self.__pool.add(mod_worker)
            except modder.exceptions.Full:
                raise UserWarning(
                    'ExecutorPool currently full (maxsize {:d})'.format(self.__pool.maxsize)
                )
            else:
                mod_worker.start()

    def trigger(self, name):
        '''Trigger an event and broadcast it to all subscribed mods'''
        self.__pool.clean_up()

        if name in modder.EVENTS:
            if name in modder.MOD_REGISTRY:
                event = self.__generate_event(name)
                [self.execute(func, event) for func in modder.MOD_REGISTRY[name]]

    def __generate_event(self, name):
        '''Generate Event object with data'''
        if name.startswith('Modder.'):
            return modder.Event(name)
        elif name.startswith('Timer.'):
            return modder.Event(name, data={'timestamp': time.time()})
        else:
            return modder.Event(name)


def test():
    event_queue = queue.Queue()
    mod_manager = ModManager()
    event_queue.put('Modder.Started')

    timer_stop = threading.Event()
    timer_thread = modder.timer.TimerThread(event_queue, timer_stop)
    timer_thread.daemon = True
    timer_thread.start()

    def before_quit():
        timer_stop.set()
        mod_manager.trigger('Modder.BeforeQuit')

    atexit.register(before_quit)

    while 1:
        try:
            event_name = event_queue.get(timeout=1)
        except queue.Empty:
            pass
        else:
            if event_name in modder.EVENTS:
                mod_manager.trigger(event_name)


if __name__ == '__main__':
    test()
