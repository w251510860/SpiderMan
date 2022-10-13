import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement411(ProcurementBaseSpider):
    name = "procurement411"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = 'http://zhaobiao.jsph.org.cn/supplier/release/cgInfoList'
        yield scrapy.FormRequest(url=urls, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//dl[@class="llist"]/dd')
        for data in datas[1:]:
            save = {}
            save["hospital_name"] = "江苏省人民医院"
            save["title"] = data.xpath("./a/text()").extract()[0]
            save["ori_url"] = "http://zhaobiao.jsph.org.cn/supplier/release/releaseCgInfoDetail?id=" + \
                              data.xpath("./a/@href").extract()[0].split("'")[1].split("'")[0]
            save["release_date"] = data.xpath("./span/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@onclick").extract()
        if next_page:
            page = next_page[0].split("'")[1].split("'")[0]
            yield scrapy.FormRequest(url=f"http://zhaobiao.jsph.org.cn/supplier/release/cgInfoList?pageNo={page}&pageSize=10", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="contentStyle"]//text()').extract())
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        if response.xpath('//a[contains(text(), "附件")]/@href').extract():
            save['annex_link'] = 'http://zhaobiao.jsph.org.cn' + response.xpath('//a[contains(text(), "附件")]/@href').extract()[0]
            save['annex_title'] = response.xpath('//a[contains(text(), "附件")]/text()').extract()[0]
        yield save

