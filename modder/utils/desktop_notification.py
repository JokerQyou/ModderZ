# coding: utf-8
import json
import os.path
import platform
import subprocess
import sys
import webbrowser

FROZEN = getattr(sys, 'frozen', False)
app_name = 'Modder'

if FROZEN:
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
    if FROZEN:
        notifier_binary = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.executable), 'binaries', 'terminal-notifier'  # noqa
            )
        )
    else:
        notifier_binary = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', 'binaries', 'terminal-notifier'  # noqa
            )
        )

    def desktop_notify(text, title=None, sound=False, url=None, timeout=10):
        title = title or app_name
        default_action = 'View'
        commandline = [
            notifier_binary,
            '-message', u_(text),
            '-title', u_(title),
            '-appIcon', desktop_icon,
            '-contentImage', desktop_icon,
            '-json',  # Return JSON data
        ]

        if sound:
            commandline.extend(['-sound', 'default'])
        if url:
            commandline.extend([
                '-open', url,
                # If the user has set terminal-notifier style to
                # 'notification' and passed `url`, the notification will stay
                # until user click, close or choose an action.
                # So here we'll give it a timeout
                '-timeout', str(int(timeout)),
                '-actions', default_action,
            ])

        result = json.loads(subprocess.check_output(commandline))

        # Make the action button open the same URL
        if url and result['activationType'] == 'actionClicked':
            webbrowser.open(url)

elif platform.system() == 'Windows':
    import wx

    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        wx.GetApp()._tray.ShowBalloon(u_(title), u_(text))

elif platform.system() == 'Linux':
    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        pass
