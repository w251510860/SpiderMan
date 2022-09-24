import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement685(ProcurementBaseSpider):
    name = "procurement685"
    base_link = ''
    page = 1
    def start_requests(self):
        # 初始页
        urls = [
            'https://www.ntzyy.com/news/1/',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="e_box e_box-000 p_news"]/div[@class="e_box e_ListBox-001 p_articles"]')
        if not datas:
            return
        for data in datas:
            save = {}
            save["hospital_name"] = "南通市中医院"
            save["title"] = data.xpath('./div[1]/text()').extract()[0]
            save["ori_url"] = "https://www.ntzyy.com" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath('.//div[@class="font"]/text()').extract()[0].replace("时间：", "")
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        self.page += 1
        yield scrapy.FormRequest(url=f"https://www.ntzyy.com/comp/news/list.do?compId=news_list-15269909323056087&cid=1&pageSize=10&currentPage={self.page}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="resetHtmlCssStyle"]/p//text()').extract())
        print(save)
        yield save
