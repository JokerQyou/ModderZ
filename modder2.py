# coding: utf-8
import glob
import importlib
import inspect
import os.path
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

    def execute(self, mod_func, event_name):
        '''Trigger a registered mod method'''
        # TODO Use a threadpool or something to async execute funtions
        if callable(mod_func):
            mod_func(event_name)

    def trigger(self, name):
        '''Trigger an event and broadcast it to all subscribed mods'''
        if name in modder.MOD_REGISTRY:
            [self.execute(func, name) for func in modder.MOD_REGISTRY[name]]


def test():
    manager = ModManager()
    manager.load_mods()
    manager.init_mods()
    manager.trigger('Modder.Started')
    time.sleep(10)
    manager.trigger('Modder.BeforeQuit')


if __name__ == '__main__':
    test()