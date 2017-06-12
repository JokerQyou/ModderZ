# coding: utf-8
from queue import Empty
import threading

import wx
import modder
import modder.manager

from .trayicon import TrayIcon


class ModderGuiApp(wx.App):

    def OnInit(self):
        modder.GUI_MODE = True

        self._manager = modder.manager.ModManager()
        self._tray = TrayIcon()

        self._timer_stop_event = threading.Event()
        self._timer_thread = modder.TimerThread(modder.EVENT_QUEUE, self._timer_stop_event)
        self._timer_thread.daemon = True
        self._timer_thread.start()

        self._modder_thread = threading.Thread(
            target=self._process_mod_event_queue, name='Modder.wxApp.ModderThread'
        )
        self._modder_thread.daemon = True

        modder.EVENT_QUEUE.put_nowait('Modder.Started')
        self._modder_thread.start()
        return True

    def _process_mod_event_queue(self):
        while 1:
            try:
                event_name = modder.EVENT_QUEUE.get(timeout=1)
            except Empty:
                pass
            else:
                self._manager.trigger(event_name)

    def OnExit(self):
        self._timer_stop_event.set()
        self._manager.trigger('Modder.BeforeQuit')
