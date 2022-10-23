import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider

request_param = {
    "__VIEWSTATE": "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",
    "__VIEWSTATEGENERATOR": "F38E029A",
    "__EVENTTARGET": "AspNetPager1",
    "__EVENTARGUMENT": "1"
}

class Procurement416(ProcurementBaseSpider):
    name = "procurement416"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.njszyy.cn/ywgc/ywgc1.aspx?mtt=SLTX9566',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="ny-r2"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "南京市中医院"
            save["title"] = data.xpath('./span[1]/a/text()').extract()[0]
            save["ori_url"] = "http://www.njszyy.cn/" + data.xpath("./span[1]/a/@href").extract()[0]
            save["release_date"] = data.xpath("./span[2]/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            request_param['__EVENTARGUMENT'] = str(next_page[0].split("'")[-2].split("'")[-1])
            yield scrapy.FormRequest(url="http://www.njszyy.cn/ywgc/ywgc1.aspx?mtt=SLTX9566", callback=self.parse,
                                     formdata=request_param, method='POST')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        save['mainbody'] = response.xpath('//div[@class="plainText_content"]//text()').extract()[0]
        save['content'] = response.text
        yield save
