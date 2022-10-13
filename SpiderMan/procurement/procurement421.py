import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement421(ProcurementBaseSpider):
    name = "procurement421"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.jssdezyy.com/index/notice/cid/24.html',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="news_list"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "江苏省第二中医院"
            save["title"] = data.xpath('.//h3/a/text()').extract()[0]
            save["ori_url"] = "http://www.jssdezyy.com" + data.xpath(".//h3/a/@href").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '>>')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"http://www.jssdezyy.com{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save["release_date"] = response.xpath('//div[@class="center desc"]/span[2]/text()').extract()[0]
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="detail_content"]/p//text()').extract())
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        yield save
