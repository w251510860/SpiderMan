import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement263(ProcurementBaseSpider):
    name = "procurement263"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = 'http://www.czyy120.cn/a/gongshigonggao/shebeigonggao/index.html'
        yield scrapy.FormRequest(url=urls, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//ul[@class="news_list_bar"]/li')
        for data in datas[1:]:
            save = {}
            save["hospital_name"] = "淮安市楚州医院"
            save["title"] = data.xpath("./a/text()").extract()[0]
            save["ori_url"] = "http://www.czyy120.cn/" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath("./span/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"http://www.czyy120.cn/a/gongshigonggao/shebeigonggao/{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="news_detail"]/div[2]/span//text()').extract())
        print(save)
        # yield save

