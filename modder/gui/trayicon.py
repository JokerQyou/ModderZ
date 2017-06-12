# coding: utf-8
import os.path
import platform

import wx


def create_menu_item(menu, label, func=None):
    menu_item = wx.MenuItem(menu, -1, label)
    if callable(func):
        menu.Bind(wx.EVT_MENU, func, id=menu_item.GetId())
    else:
        menu_item.Enable(False)

    menu.AppendItem(menu_item)
    return menu_item


class TrayIcon(wx.TaskBarIcon):
    icon_fpath = os.path.join(
        os.path.dirname(__file__), 'resources', 'icons8-Module-64.png'
    )

    def __init__(self, frame=None):
        super(TrayIcon, self).__init__()
        self._frame = frame or wx.Frame(None)
        self.SetIcon(wx.Icon(self.icon_fpath, wx.BITMAP_TYPE_PNG))

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Modder')
        menu.AppendSeparator()

        mods_count = wx.GetApp()._manager.count
        create_menu_item(menu, '{:d} mods loaded'.format(mods_count), self.on_manage_mods)
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def on_manage_mods(self, evt):
        pass

    def on_exit(self, evt):
        wx.CallAfter(self.Destroy)
        self._frame.Close()
