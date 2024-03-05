#  This software shall not be used for commercial purposes, only for learning communication
#  Copyright (c) 2022-2023. All rights reserved.

import requests


headers = {
    "authority": "www.openstreetmap.org",
    "accept": "application/xml, text/xml, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1",
    "referer": "https://www.openstreetmap.org/way/683493246",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "x-csrf-token": "0tqfGCizVUekqhmzUJ_YVS1bSkrE1rUL5XLngcadKRvOuE1QIpAmWpaCqnzzncA-YMLt1Kv4PZzOPGVrhQOkbg",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "_osm_session": "e2ea0f67b5c4797e6d8aff16ab3401cc",
    "_osm_totp_token": "842439",
    "_pk_id.1.cf09": "b2aa76e92d0d8f5d.1677992930.",
    "_pk_ses.1.cf09": "1",
    "_osm_location": "115.7853|40.5227|13|M"
}
url = "https://www.openstreetmap.org/api/0.6/way/683493246/full"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
print(response)