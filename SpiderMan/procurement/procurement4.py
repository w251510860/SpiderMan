import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement4(ProcurementBaseSpider):
    name = "Procurement4"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://smh.cc/api2020/api/news/getNewsInfo',
        ]
        params = {
            "hospital": "1010",
            "category": "32",
            "tag": "",
            "size": "8",
            "pageNum": "1",
            "type": "0",
            "status": "1",
            "_": f'{int(time.time())}'
        }
        # 遍历、翻页
        for url in urls:
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        print(response.json())
        return