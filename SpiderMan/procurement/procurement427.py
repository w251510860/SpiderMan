import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement427(ProcurementBaseSpider):
    name = "procurement427"
    base_link = ''
    data = {
        "__VIEWSTATE": "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",
        "__VIEWSTATEGENERATOR": "E4EF4CD1",
        "__EVENTTARGET": "AspNetPager1",
        "__EVENTARGUMENT": "3"
    }

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.njsech.net/news/news.aspx?mtt=39',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="ab-xi"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "南京市第二医院"
            save["title"] = data.xpath('./a/text()').extract()[0]
            save["ori_url"] = "http://www.njsech.net/news/" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath("./span/text()").extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '>')]/@href").extract()
        if next_page:
            self.data['__EVENTARGUMENT'] = next_page[0].replace("javascript:__doPostBack('AspNetPager1','", "").\
                replace("')", "")
            yield scrapy.FormRequest(url="http://www.njsech.net/news/news.aspx?mtt=39", callback=self.parse,
                                     formdata=self.data, method='POST')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="ne-new-xi"]/p//text()').extract())
        annex = response.xpath('//div[@class="ne-new-xi"]/p/a')
        if annex:
            save['annex_link'] = 'http://www.njsech.net' + annex.xpath('./@href').extract()[0]
            save['annex_title'] = annex.xpath('./text()').extract()[0]
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        save['content'] = response.text
        yield save
