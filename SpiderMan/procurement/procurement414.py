import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement414(ProcurementBaseSpider):
    name = "procurement414"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.jshtcm.com/list.php?fid=1191',
            'http://www.jshtcm.com/list.php?fid=947',
            'http://www.jshtcm.com/list.php?fid=997'
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="listContent"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "江苏省中医院"
            save["title"] = data.xpath('./a/text()').extract()[0]
            save["ori_url"] = "http://www.jshtcm.com/" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath("./a/span/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=next_page[0], callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        mainbody = response.xpath('//div[@class="plainText_content"]//text()').extract()
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        save['mainbody'] = mainbody[0] if mainbody else None
        save['content'] = response.text
        yield save

