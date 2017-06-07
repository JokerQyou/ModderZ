# coding: utf-8
import logging

import win32com.client

from utils import get_logger

logger = get_logger(__name__, level=logging.DEBUG)


class SinkClass(object):
    def OnObjectReady(self, *args):
        logger.debug(u'OnObjectReady: %s', args)

    def OnCompleted(self, *args):
        logger.debug(u'OnCompleted: %s', args)

    def OnObjectPut(self, *args):
        logger.debug(u'ObObjectPut: %s', args)

    def OnProgress(self, *args):
        logger.debug(u'OnProgress: %s', args)


def monitor_process_events():
    wmi = win32com.client.GetObject(r'winmgmts:\\.\root\CIMV2')
    wmi_sink = win32com.client.DispatchWithEvents('WbemScripting.SWbemSink', SinkClass)
    wmi.ExecNotificationQueryAsync(
        wmi_sink, "SELECT *, TargetInstance FROM __InstancecreationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_Process'"
    )


if __name__ == '__main__':
    import win32api
    import win32con
    import win32security
    import wmi
    import time

    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for('creation')

    while 1:
        time.sleep(0.1)
        try:
            new_process = process_watcher()
            logger.debug(new_process)
        except:
            logger.exception('Failed to fetch')
