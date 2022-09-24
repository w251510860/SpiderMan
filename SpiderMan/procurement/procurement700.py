import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement700(ProcurementBaseSpider):
    name = "procurement700"
    base_link = ''
    data = {
        "__EVENTTARGET": "ctl00$ContentPlaceHolder2$lbtnIndex",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "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",
        "__VIEWSTATEGENERATOR": "77BE98E0",
        "__EVENTVALIDATION": "/wEWAwL87O32CAKxw5ijDQK2tc/wDoicGhp6BM0tnm15PNjXVOaWJWYc"
    }
    url = "http://www.rgzyy.com/ListNews.aspx?UrlOneClass=8"
    def start_requests(self):
        # 初始页
        for _ in [1]:
            yield scrapy.FormRequest(url=self.url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@id="DivNewsList"]/div')
        for data in datas:
            save = {}
            save["hospital_name"] = "如皋市中医院"
            save["title"] = data.xpath('./a/text()').extract()[0]
            save["ori_url"] = "http://www.rgzyy.com/" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath('./span/text()').extract()[0].replace("时间：", "")
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={'save': save})
        self.data['__VIEWSTATEGENERATOR'] = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract()[0]
        self.data['__EVENTVALIDATION'] = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract()[0]
        viewstate = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract()
        self.data['__VIEWSTATE'] = viewstate if viewstate else ''
        self.data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder2$lbtnNext'
        yield scrapy.FormRequest(url=self.url, formdata=self.data, callback=self.parse, method='POST')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="DivNewsContent"]//text()').extract())
        yield save

