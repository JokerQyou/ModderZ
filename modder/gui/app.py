# coding: utf-8
import wx
import modder
import modder.manager

from .trayicon import TrayIcon


class ModderGuiApp(wx.App):

    def OnInit(self):
        self._manager = modder.manager.ModManager()
        self._tray = TrayIcon()

        self._manager.trigger('Modder.Started')
        return True

    def OnExit(self):
        self._manager.trigger('Modder.BeforeQuit')
