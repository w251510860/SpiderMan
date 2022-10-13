import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement429(ProcurementBaseSpider):
    name = "procurement429"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.jsdental.cn/Notice/cate.html',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@id="cat_list"]//tr')
        for data in datas:
            save = {}
            save["hospital_name"] = "江苏省口腔医院"
            save["title"] = data.xpath('./td[2]/a/@title').extract()[0]
            save["ori_url"] = "http://www.jsdental.cn" + data.xpath("./td[2]/a/@href").extract()[0]
            save["release_date"] = data.xpath("./td[3]/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '>>')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"http://www.jsdental.cn{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        content = []
        for data in response.xpath('//div[@id="detail_content"]/p'):
            content.append(''.join(data.xpath('./span/text()').extract()))
        save['mainbody'] = '\n'.join(content)
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        yield save
