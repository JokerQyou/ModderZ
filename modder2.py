# coding: utf-8
import atexit
import glob
import importlib
import inspect
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
        self.mods = []
        self.mod_definitions = []

        self.check_mod_directory()
        self.load_mods()
        self.init_mods()

    def check_mod_directory(self):
        '''Make sure `mod_directory` is a valid Python package'''
        if not os.path.isdir(self.mod_directory):
            os.makedirs(self.mod_directory)

        package_init_file = os.path.join(self.mod_directory, '__init__.py')
        if not os.path.isfile(package_init_file):
            with open(package_init_file, 'w') as wf:
                wf.write('# coding: utf-8')

    def load_mods(self):
        '''
        Import all modules in `mod_directory`,
        and load all ModBase subclasses into memory.
        '''
        base_package = os.path.basename(self.mod_directory)
        for pyfile in glob.glob('{}/*.py'.format(base_package)):
            # Get module name out of file path
            pymodule_name = os.path.splitext(os.path.basename(pyfile))[0]
            # Import target module
            pymodule = importlib.import_module('{}.{}'.format(base_package, pymodule_name))

            # Store all ModBase subclass definitions
            for name in dir(pymodule):
                reference = getattr(pymodule, name)
                if not name.startswith('_'):
                    if inspect.isclass(reference) and issubclass(reference, modder.ModBase):
                        self.mod_definitions.append(reference)

    def init_mods(self):
        '''Instanciate all ModBase subclasses'''
        for cls in self.mod_definitions:
            if issubclass(cls, modder.ModBase):
                self.mods.append(cls())

    def execute(self, mod_func, event):
        '''Trigger a registered mod method'''
        # TODO Use a threadpool or something to async execute funtions
        if callable(mod_func):
            mod_func(event)

    def trigger(self, name):
        '''Trigger an event and broadcast it to all subscribed mods'''
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
