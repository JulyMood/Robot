# -*- coding: utf-8 -*-
from settings import _WEIBO_ACCESS_TOKEN, _WEINO_DOMAIN
import requests


def send(context, pic):
    # status中必须包含安全域名
    status = context.encode('utf8') + _WEINO_DOMAIN
    url = 'https://api.weibo.com/2/statuses/share.json'
    data = {'access_token': _WEIBO_ACCESS_TOKEN, 'status': status}
    files = {'pic': open(pic, 'rb')}
    response = requests.post(url, data=data, files=files)
    return response.status_code
