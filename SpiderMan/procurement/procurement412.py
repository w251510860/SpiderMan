import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement412(ProcurementBaseSpider):
    name = "procurement412"
    base_link = ''
    data = {
        "__EVENTTARGET": "AspNetPager1",
        "__EVENTARGUMENT": "1",
        "__VIEWSTATE": "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",
        "__VIEWSTATEGENERATOR": "0ECB3CD9",
        "__EVENTVALIDATION": "RAFLsXiALOy5z+srkfbfHrY8WZsJZ9dSsBpITCELqaz9GkHtU1I2ZGE65uvYnYEh2EWU5fjZMLNvfCXV91Lg8HC9aBkraB0ZpI0kU3TUHAM2qqnJyMHiu7CCKxd7WSTeAYoUOF0saTNmQz/+Y6tWfNjBUdssQY8H7YslgA==",
        "top%24txtSo": ""
    }
    url = 'https://www.njglyy.com/cggl/xxgs.aspx?mtt=24#box'
    def start_requests(self):
        # 初始页
        for _ in [1]:
            yield scrapy.FormRequest(url=self.url, formdata=self.data, callback=self.parse, method='POST')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="mtbd-list"]/dl')
        for data in datas:
            save = {}
            save["hospital_name"] = "南京市鼓楼医院"
            save["title"] = data.xpath("./a/dt/text()").extract()[0]
            save["ori_url"] = "https://www.njglyy.com/cggl/" + \
                              data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath("./a/dd/text()").extract()[0].replace("[", '').replace("]", '')
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '>')]/@href").extract()
        if next_page:
            next_page = next_page[0].replace("javascript:__doPostBack('AspNetPager1','", "").replace("')", "")
            self.data['__EVENTARGUMENT'] = str(next_page)
            yield scrapy.FormRequest(url=self.url, formdata=self.data, callback=self.parse, method='POST')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = response.xpath('//div[@class="detail2"]//text()').extract()
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        yield save

