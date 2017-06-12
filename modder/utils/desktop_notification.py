# coding: utf-8
import os.path
import platform
import sys

if getattr(sys, 'frozen', False):
    desktop_icon = os.path.abspath(
        os.path.join(
            os.path.dirname(sys.executable), 'resources', 'icons8-Module-128.png'
        )
    )
else:
    desktop_icon = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 'gui', 'resources', 'icons8-Module-128.png'
        )
    )

if platform.system() == 'Darwin':
    from AppKit import NSImage
    from Foundation import NSUserNotificationDefaultSoundName
    import objc

    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title.decode('utf-8'))
        notification.setInformativeText_(text.decode('utf-8'))
        notification.setValue_forKey_(NSImage.alloc().initWithContentsOfFile_(desktop_icon), '_identityImage')

        if sound:
            notification.setSoundName_(NSUserNotificationDefaultSoundName)

        NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(notification)  # noqa

elif platform.system() == 'Windows':
    from win10toast import ToastNotifier

    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        ToastNotifier().show_toast(
            title.decode('utf-8'),
            text.decode('utf-8'),
            icon_path=desktop_icon
        )

elif platform.system() == 'Linux':
    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        pass
