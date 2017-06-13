# coding: utf-8
import wx

from .base_frames import ManagerFrame


class ModManagerFrame(ManagerFrame):

    def __init__(self):
        super(ModManagerFrame, self).__init__(None)

        self.mod_list.InsertColumn(0, 'Name', format=wx.LIST_FORMAT_LEFT, width=50)
        self.mod_list.InsertColumn(1, 'Events', format=wx.LIST_FORMAT_LEFT, width=150)
        self.mod_list.InsertColumn(2, 'File', format=wx.LIST_FORMAT_LEFT, width=100)