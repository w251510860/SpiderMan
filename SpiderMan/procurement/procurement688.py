import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement688(ProcurementBaseSpider):
    name = "procurement688"
    base_link = ''
    def start_requests(self):
        # 初始页
        urls = [
            'http://www.ahnmc.com/news2.asp',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//tr[2]//tr')
        if not datas:
            return
        for data in datas:
            if len(data.xpath("./td")) != 3:
                continue
            save = {}
            save["hospital_name"] = "南通大学附属医院"
            save["title"] = data.xpath('./td[2]/a/text()').extract()[0]
            save["ori_url"] = "http://www.ahnmc.com/" + data.xpath("./td[2]/a/@href").extract()[0]
            save["release_date"] = data.xpath('./td[3]/font/text()').extract()[0].replace("(", "").replace(")", "")
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"http://www.ahnmc.com/news2.asp{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        content = response.xpath('.//font[@face="Verdana"]//text()').extract()
        save['mainbody'] = '\n'.join(content)
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        yield save
