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
        item["digest"] = item['hospital_name'] + item['title'] + item['ori_url']
        filter = {"digest": item["digest"]}
        self.col.update_one(filter, {'$setOnInsert': item}, upsert=True)
        return item


class TestPipeline:

    @staticmethod
    def process_item(item, spider):
        # print(item)
        return item
