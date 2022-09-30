import arrow
import pymongo

from SpiderMan import settings


class ProcurementSaveMongoPipeline:

    def __init__(self):
        self.client = pymongo.MongoClient(host=settings.MONGO_HOST, port=int(settings.MONGO_PORT))
        self.db = self.client[settings.MONGO_DB]
        self.col = self.db[settings.MONGO_COLL]

    def process_item(self, item, spider):
        item = dict(item)
        white_list = ['集采', '采购', '投标', '中标', '招标', '谈判', '候选', '谈判', '供应', '合同', '产品',
                      '器械', '耗材', '设备', '成交', '竞争', '预算', '磋商', '限价']
        item["digest"] = item['hospital_name'] + item['title'] + item['ori_url']
        for key_word in white_list:
            if key_word in item['mainbody']:
                filter = {"digest": item["digest"]}
                self.col.update_one(filter, {'$setOnInsert': item}, upsert=True)
                return item
        return item


class TestPipeline:

    @staticmethod
    def process_item(item, spider):
        # print(item)
        return item
