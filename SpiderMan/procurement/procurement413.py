import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement413(ProcurementBaseSpider):
    name = "procurement413"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = 'https://www.jszlyy.com.cn/Major/news/index2/id/498/tid/354/fid/316'
        yield scrapy.FormRequest(url=urls, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="connewslist"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "江苏省肿瘤医院"
            save["title"] = data.xpath('.//div[@class="newscontent1"]/h3/text()').extract()[0]
            save["ori_url"] = "https://www.jszlyy.com.cn" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = f'{data.xpath("./a/span/h6/text()").extract()[0]}-{data.xpath("./a/span/h5/text()").extract()[0]}'
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '>')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"https://www.jszlyy.com.cn/{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = response.xpath('//div[@class="jscontent"]//text()').extract()
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        if response.xpath('//a[contains(@href, "upload")]/@href').extract():
            save['annex_link'] = 'https://www.jszlyy.com.cn/' + response.xpath('//a[contains(@href, "upload")]/@href').extract()[0]
            save['annex_title'] = response.xpath('//a[contains(@href, "upload")]//text()').extract()[0]
        save['content'] = response.text
        yield save

