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
            '-message', text,
            '-title', title,
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
            if result['activationType'] == 'actionClicked':
                webbrowser.open(url)
        else:
            subprocess.call(commandline)

elif platform.system() == 'Windows':
    if FROZEN:
        notifier_binary = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.executable), 'binaries', 'SnoreToast.exe'  # noqa
            )
        )
    else:
        notifier_binary = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..', 'binaries', 'SnoreToast.exe'  # noqa
            )
        )

    def desktop_notify(text, title=None, sound=False, url=None, timeout=10):
        title = title or 'Modder'
        commandline = [
            notifier_binary,
            '-appId', app_name,
            '-t', title,
            '-m', text,
            '-p', desktop_icon,
        ]

        if sound:
            commandline.extend(['-s', 'Notification.Default'])
        else:
            commandline.extend(['-silent'])

        if url:
            commandline.extend(['-w'])

            if subprocess.call(commandline) == 0:
                webbrowser.open(url)
        else:
            subprocess.call(commandline)

elif platform.system() == 'Linux':
    def desktop_notify(text, title=None, sound=False):
        title = title or 'Modder'

        pass
