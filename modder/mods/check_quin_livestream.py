# coding: utf-8
import random

from modder import on, get_storage, notify
import requests


def random_quin_nick():
    '''Return random nickname of Mr.Quin'''
    return random.choice((
        u'秦川', u'秦先森', u'秦喵喵', u'秦智障', u'川川子', u'机核摸鱼王奎恩',
        u'Quin', u'缺', u'缺哥哥', u'缺神', u'Q酱', u'二五仔',
    ))


def is_quin_live(live):
    '''Return proper text according to given JSON API response'''
    if live['error']:
        pass
    else:
        live = live['data']
        quin_live_url = 'http://douyu.com/quin'
        if live['room_status'] == '1':
            return (
                u'惊了！{}居然播了，不敢信。'
                u'而且有{}个猛男在看直播，整个房间都gay gay的。 {}'
            ).format(random_quin_nick(), live['online'], quin_live_url)
        elif live['room_status'] == '2':
            pass
        else:
            pass


@on('Timer.Interval.Minute')
def check_quin_livestream(event):
    storage = get_storage('check_quin_livestream')
    saved = storage.load()
    last_triggered = saved.get('last_triggered', 0)
    if saved.get('is_streaming', False):
        interval = 60 * 60  # 开播之后，每 60 分钟检查一次
    else:
        interval = 60 * 10  # 没开播时，每 10 分钟检查一次

    if event.timestamp - last_triggered < interval:
        return
    else:
        api_url = 'http://open.douyucdn.cn/api/RoomApi/room/3614'
        try:
            data = requests.get(
                api_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # noqa
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # noqa
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,ja-JP;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2,en;q=0.2',  # noqa
                    'DNT': '1',
                    'Host': 'open.douyucdn.cn',
                    'Upgrade-Insecure-Requests': '1',
                },
                timeout=5
            ).json()
        except:
            pass
        else:
            text = is_quin_live(data)
            storage.save({
                'is_streaming': bool(text),
                'last_triggered': event.timestamp,
            })
            if text:
                notify(text, title='直播通知', sound=True)
