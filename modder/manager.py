# coding: utf-8
import glob
import importlib
import os.path
import sys
import threading
import time

from . import EVENTS
from . import MOD_REGISTRY
from .event import Event
from .exceptions import Full
from .pool import ExecutorPool


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
            for event, mods in MOD_REGISTRY.items():
                pool_size += len(mods)

            self.__pool = ExecutorPool(pool_size)

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
        sys.path.append(os.path.dirname(self.mod_directory))

        base_package = os.path.basename(self.mod_directory)
        for pyfile in glob.glob('{}/*.py'.format(self.mod_directory)):
            # Get module name out of file path
            pymodule_name = os.path.splitext(os.path.basename(pyfile))[0]
            # Import target module
            if not pymodule_name.startswith('_'):
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
            except Full:
                raise UserWarning(
                    'ExecutorPool currently full (maxsize {:d})'.format(self.__pool.maxsize)
                )
            else:
                mod_worker.start()

    def trigger(self, name):
        '''Trigger an event and broadcast it to all subscribed mods'''
        self.__pool.clean_up()

        if name in EVENTS:
            if name in MOD_REGISTRY:
                event = self.__generate_event(name)
                [self.execute(func, event) for func in MOD_REGISTRY[name]]

    def __generate_event(self, name):
        '''Generate Event object with data'''
        if name.startswith('Modder.'):
            return Event(name)
        elif name.startswith('Timer.'):
            return Event(name, data={'timestamp': time.time()})
        else:
            return Event(name)
