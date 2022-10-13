import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement417(ProcurementBaseSpider):
    name = "procurement417"
    base_link = "http://www.c-nbh.com/ywgk/"

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.c-nbh.com/ywgk/ywgk.asp?classid=2',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//tr')
        for data in datas:
            if len(data.xpath('.//td')) != 3:
                continue
            save = {}
            save["hospital_name"] = "南京脑科医院"
            save["title"] = data.xpath('./td[2]/a/text()').extract()[0]
            save["ori_url"] = self.base_link + data.xpath("./td[2]/a/@href").extract()[0]
            save["release_date"] = data.xpath("./td[3]/div/text()").extract()[0].replace("[", "").replace("]", "")
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下页')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=self.base_link + next_page[0], callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        save['mainbody'] = '\n'.join(response.xpath('//tr/td/div//text()').extract())
        yield save
