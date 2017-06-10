# coding: utf-8
import os.path

import sqlitedict

__db__ = os.path.join(os.path.expanduser('~'), '.modder.sqlite')


class ModStorage(object):
    '''Store persistent key/value pairs for a mod'''

    def __init__(self, mod_name):
        super(ModStorage, self).__init__()

        self.__name = mod_name

    @property
    def name(self):
        return self.__name

    def save(self, dict_):
        '''Save `dict_`'''
        with sqlitedict.SqliteDict(__db__, tablename=self.__name) as db:
            db.update(dict_)
            db.commit()

    def load(self):
        '''Load saved data'''
        dict_ = {}
        with sqlitedict.SqliteDict(__db__, tablename=self.__name) as db:
            dict_.update(db)

        return dict_


get_storage = ModStorage
