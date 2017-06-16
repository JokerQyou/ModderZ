# coding: utf-8
import atexit
import platform

from modder import on, trigger

if platform.system() == 'Windows':
    import pythoncom
    import wmi

    @on('Modder.Started')
    def watch_process_creation(event):
        pythoncom.CoInitialize()
        atexit.register(pythoncom.CoUninitialize)

        wmi_root = wmi.WMI()
        process_watcher = wmi_root.Win32_Process.watch_for(
            notification_type='Creation',
            delay_secs=2
        )
        try:
            while 1:
                try:
                    new_process = process_watcher()
                    trigger(
                        'Process.Created',
                        data={
                            'caption': new_process.wmi_property('Caption').value,
                            'process_name': new_process.wmi_property('Name').value,
                            'executable_path': new_process.wmi_property('ExecutablePath').value,
                            'pid': new_process.wmi_property('ProcessId').value,
                        }
                    )
                except Exception as e:
                    print 'innter error:', e
                    pass
        except Exception as e:
            print 'outter error:', e
            pass
        finally:
            pythoncom.CoUninitialize()
else:
    pass
