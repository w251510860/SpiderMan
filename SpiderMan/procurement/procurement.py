import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement2(ProcurementBaseSpider):
    name = "Procurement2"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://fyy.sdfyy.cn/Article/lists/category/65.html',
        ]
        # 遍历、翻页
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        print(response.text)
        # 解析网页
        datas = response.xpath("//tr")
        print(datas)
        for data in datas:
            # 按table解析
            print(data)
