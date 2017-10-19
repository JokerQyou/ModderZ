# coding: utf-8
import wx

from modder import MOD_REGISTRY
from .base_frames import ManagerFrame


class ModManagerFrame(ManagerFrame):

    def __init__(self):
        super(ModManagerFrame, self).__init__(None)
        self.mod_list.InsertColumn(0, 'Name', format=wx.LIST_FORMAT_LEFT, width=200)
        self.mod_list.InsertColumn(1, 'Events', format=wx.LIST_FORMAT_LEFT, width=200)
        # self.mod_list.InsertColumn(2, 'File', format=wx.LIST_FORMAT_LEFT, width=100)

        mods = {}

        for eventname, modlist in MOD_REGISTRY.items():
            for mod in modlist:
                if mod not in mods:
                    mods[mod] = [eventname]
                else:
                    mods[mod].append(eventname)

        for mod, events in mods.items():
            self.mod_list.Append([mod.__doc__ or mod.__name__, ', '.join(events)])
