import json
import socket

import requests
import ssl


url = 'https://pocketuni.net:443/index.php?app=api&mod=Event&act=queryActivityDetailById'

"""
POST /index,php?app=api&mod=Event&act=queryActivityDetailByld
"""


def run():
    socket.setdefaulttimeout(30)
    ssl._create_default_https_context = ssl._create_unverified_context
    session = requests.Session()
    headers = {
        "Content-Length": "111",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "pocketuni.net",
        "Connection": "Keep-Alive",
        "User-Agent": "client:Android version:6.9.92 Product:M2012K11C",
        "OsVersion": "13",
        "Cookie": "PHPSESSID=14ffc556409c0f7165c2",
        "Cookie2": "$Version=1",
        "Accept-Encoding": "gzip",
    }

    data = {
        'oauth_token': '54378d08ebaaea2893836511b737a257',
        'oauth_token_secret': '313b2a37c37baffe7969cfb0c52c84f7',
        'actiId': '4555393'
    }

    response = session.post(url=url, json=data, headers=headers)
    if response is not None and response.status_code == 200:
        data = response.content
        content_encoding = response.headers.get('Content-Encoding')
        if content_encoding is not None and content_encoding.strip() != '' and content_encoding.lower() in ['gzip',
                                                                                                            'deflate']:
            # data = gzip.decompress(data)
            pass
        content_type = response.headers.get('Content-Type')
        if content_type is not None and 'charset=' in content_type:
            encoding = content_type.split(';')[-1].split('=')[-1]
        else:
            encoding = response.apparent_encoding
        if encoding is not None and encoding.strip() != '':
            # print(encoding)
            data = data.decode(encoding=encoding)
        else:
            data = data.decode('UTF-8')
        # print(content_encoding, len(data))
        cookies = response.cookies
        cookie_res = ''
        for cookie in cookies:
            cookie_res += cookie.name + '=' + cookie.value + ';'
        if session is not None:
            session.close()
        if response is not None:
            response.close()
        return 'success'
    else:
        if session is not None:
            session.close()
        if response is not None:
            response.close()
        return 'failure'


if __name__ == '__main__':
    # run()
    f = '{"code":1,"message":"\\u6388\\u6743\\u5931\\u8d25","content":[]}'
    d = json.loads(f)
    print(d['message'])

#  This software shall not be used for commercial purposes, only for learning communication
#  Copyright (c) 2022-2023. All rights reserved.
