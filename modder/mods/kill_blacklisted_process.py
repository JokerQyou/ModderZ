# coding: utf-8
import platform
import psutil

from modder import on
from modder import notify

if platform.system() == 'Windows':
    blacklist = [
        'CompatTelRunner.exe',
    ]
else:
    blacklist = []


@on('Modder.Started')
@on('Timer.Interval.Minute')
@on('Process.Created')
def kill_blacklisted_processes(event):
    if not blacklist:
        return

    if event.name == 'Process.Created':
        if event.process_name in blacklist:
            try:
                psutil.Process(pid=event.pid).kill()
            except:
                notify(
                    '未能杀死黑名单进程 {:s}。'.format(event.process_name),
                    title='进程黑名单'
                )
            else:
                notify(
                    '实时杀死黑名单进程 {:s}。'.format(event.process_name),
                    title='进程黑名单'
                )
    else:
        targets = filter(lambda p: p.name() in blacklist, psutil.process_iter())
        killed_count = 0
        total_count = len(list(targets))

        for process in targets:
            try:
                process.kill()
            except:
                pass
            else:
                killed_count += 1

        if any([killed_count, total_count]):
            notify(
                '杀死了 {:d} 个黑名单进程，共检测到 {:d} 个。'.format(killed_count, total_count),
                title='进程黑名单'
            )
