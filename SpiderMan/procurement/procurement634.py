import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement634(ProcurementBaseSpider):
    name = "procurement634"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.sqszyy.com/yygg/',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="mar_10"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "宿迁市中医院"
            save["title"] = data.xpath('./a/text()').extract()[0]
            save["ori_url"] = "http://www.sqszyy.com/" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath("./span/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"http://www.sqszyy.com/{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = response.xpath('//div[@id="endtext"]//text()').extract()
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        yield save
