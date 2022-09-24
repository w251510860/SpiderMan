import arrow
import pymongo

from SpiderMan import settings
from SpiderMan.utils.clean_data import clean_space
from SpiderMan.utils.tags import YY_tags


class SaveMongoPipeline:

    def __init__(self):
        self.client = pymongo.MongoClient(host=settings.MONGO_HOST, port=int(settings.MONGO_PORT))
        self.db = self.client[settings.MONGO_DB]
        self.col = self.db[settings.MONGO_COLL]

    def process_item(self, item, spider):
        item = dict(item)
        item['title'] = clean_space(item['title'])
        item['release_date'] = item.get('release_date', '')

        item['tag'] = YY_tags[int(item['tag']) - 1]
        item['mainbody_table'] = item['title']
        item["crawl_time"] = str(arrow.now())
        item["digest"] = item['title'] + item['release_date']
        filter = {"digest": item["digest"]}
        self.col.update_one(filter, {'$setOnInsert': item}, upsert=True)
        return item


class ResumeSaveMongoPipeline:

    def __init__(self):
        self.client = pymongo.MongoClient(host=settings.MONGO_HOST, port=int(settings.MONGO_PORT))
        self.db = self.client[settings.MONGO_DB]
        self.col = self.db[settings.MONGO_COLL]

    def process_item(self, item, spider):
        item = dict(item)
        item["crawl_time"] = str(arrow.now())
        # print(item)
        # self.col.insert_one(item)
        return item

class TestPipeline:

    @staticmethod
    def process_item(item, spider):
        # print(item)
        return item
