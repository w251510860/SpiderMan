import re

import pymongo
import scrapy
from scrapy.http.response.html import HtmlResponse

import settings
from procurement.Base import ProcurementBaseSpider


class Procurement10(ProcurementBaseSpider):
    name = "Procurement_13"
    base_link = ''
    hospital_name = '苏州市立医院'
    def start_requests(self):
        # 初始页
        urls = []
        for i in range(26):
            list_url = 'http://smh.cc/api2020/api/news/getNewsInfo?hospital=1010&category=32&tag=&size=8&pageNum={}&type=0&status=1&_=1657282609378'.format(i + 1)
            urls.append(list_url)
        print(urls)
        params = {
            # "hospital": "1010",
            # "category": "32",
            # "tag": "",
            # "size": "8",
            # "pageNum": "1",
            # "type": "0",
            # "status": "1",
            # "_": f'{int(time.time())}'
        }
        self.hospital_url = 'http://smh.cc/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            print("第{}页".format(index + 1))
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()['data']['list']

        for each in context:
            title = each['title']
            ori_url = "{}id={}".format(response.url,each['id'])
            release_date = each['time']
            mainbody = each['html']
            mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
            # annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
            # annex_title = response.xpath('//a[@class="ke-insertfile"]/text()')
            item = self.save
            item['annex_link'] = ''
            item['annex_title'] = ''
            # if (len(annex_url) != 0) and (len(annex_title) != 0):
            #     annex_link = self.hospital_url + response.xpath('//a[@class="ke-insertfile"]/@href').extract()[0]
            #     item['annex_link'] = annex_link
            #     item['annex_title'] = annex_title.extract()[0]
            item['title'] = title
            item['ori_url'] = ori_url
            item['release_date'] = release_date
            item['mainbody'] = mainbody
            item['col'] = self.name
            item['hospital_name'] = self.hospital_name

            self.client = pymongo.MongoClient(host=settings.MONGO_HOST, port=int(settings.MONGO_PORT))
            self.db = self.client[settings.MONGO_DB]
            self.col = self.db[item['col']]
            item['crawl_time'] = item['crawl_time'].format("YYYY-MM-DD HH:mm:ss")
            filter = {"ori_url": item["ori_url"]}
            self.col.update_one(filter, {'$setOnInsert': item}, upsert=True)
        return

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@class="tt"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="remark"]/text()').extract()[0]
        release_date = release_date.split("：")[3][0:10]
        mainbody = response.xpath('//div[@id="main"]').extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        annex_title = response.xpath('//a[@class="ke-insertfile"]/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        if (len(annex_url) != 0) and (len(annex_title) != 0):
            annex_link = self.hospital_url + response.xpath('//a[@class="ke-insertfile"]/@href').extract()[0]
            item['annex_link'] = annex_link
            item['annex_title'] = annex_title.extract()[0]
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
