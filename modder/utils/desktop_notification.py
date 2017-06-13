# coding: utf-8
import os.path
import platform
import sys

if getattr(sys, 'frozen', False):
    desktop_icon = os.path.abspath(
        os.path.join(
            os.path.dirname(sys.executable),
            'resources', 'icons8-Module-128.png'
        )
    )
else:
    desktop_icon = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..', 'gui', 'resources', 'icons8-Module-128.png'
        )
    )


def u_(s):
    '''str => unicode'''
    if isinstance(s, str):
        return s.decode('utf-8')
    elif isinstance(s, unicode):
        return s
    return str(s).decode('utf-8')


if platform.system() == 'Darwin':
    from AppKit import NSImage
    from Foundation import NSUserNotificationDefaultSoundName
    import objc

    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(u_(title))
        notification.setInformativeText_(u_(text))
        # This is a private API to replace notification icon,
        # ref: https://stackoverflow.com/a/24940893
        notification.setValue_forKey_(NSImage.alloc().initWithContentsOfFile_(desktop_icon), '_identityImage')  # noqa

        if sound:
            notification.setSoundName_(NSUserNotificationDefaultSoundName)

        NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(notification)  # noqa

elif platform.system() == 'Windows':
    import wx

    # from win10toast import ToastNotifier

    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        wx.GetApp()._tray.ShowBalloon(u_(title), u_(text))

        # ToastNotifier().show_toast(
        #     u_(title),
        #     u_(text),
        #     icon_path=desktop_icon
        # )

elif platform.system() == 'Linux':
    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        pass
