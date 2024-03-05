#  This software shall not be used for commercial purposes, only for learning communication
#  Copyright (c) 2022-2023. All rights reserved.
import sys

sys.path.append('.')
import pymongo

import settings


def save_data(item):
    client = pymongo.MongoClient(host=settings.MONGO_HOST, port=int(settings.MONGO_PORT))
    db = client[settings.MONGO_DB]
    col = db[settings.MONGO_COLL]
    white_list = ['集采', '采购', '投标', '中标', '招标', '谈判', '候选', '谈判', '供应', '合同', '产品',
                  '器械', '耗材', '设备', '成交', '竞争', '预算', '磋商', '限价']
    item["digest"] = item['hospital_name'] + item['title'] + item['ori_url']
    if item.get('mainbody'):
        for key_word in white_list:
            if key_word in item['mainbody']:
                print(item["title"])
                filter = {"digest": item["digest"]}
                col.update_one(filter, {'$setOnInsert': item}, upsert=True)
                return item
    return item
