# coding: utf-8
import platform

if platform.system() == 'Darwin':
    from Foundation import NSUserNotificationDefaultSoundName
    import objc

    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title.decode('utf-8'))
        notification.setInformativeText_(text.decode('utf-8'))

        if sound:
            notification.setSoundName_(NSUserNotificationDefaultSoundName)

        center = NSUserNotificationCenter.defaultUserNotificationCenter()
        center.deliverNotification_(notification)

elif platform.system() == 'Windows':
    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        pass

elif platform.system() == 'Linux':
    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        pass
