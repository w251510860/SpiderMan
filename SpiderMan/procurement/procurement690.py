import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement690(ProcurementBaseSpider):
    name = "procurement690"
    base_link = ''
    params = {
        "compId": "portalResNews_list-1600322132153",
        "cid": "13",
        "pageSize": "20"
    }

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.ntzlyy.cn/news/13/#c_portalResNews_list-1600322132153-1',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//ul[@class="p_news"]/li')
        if not datas:
            return
        for data in datas:
            save = {}
            save["hospital_name"] = "南通市肿瘤医院南院"
            save["title"] = data.xpath('.//div[@class="h3"]/a/text()').extract()[0]
            save["release_date"] = data.xpath('.//div[@class="h3"]/span[@class="time"]/text()').extract()[0]
            ori_url = data.xpath('.//div[@class="h3"]/a/@href').extract()[0]
            if 'http' in ori_url:
                continue
            save["ori_url"] = "http://www.ntzlyy.cn" + data.xpath('.//div[@class="h3"]/a/@href').extract()[0]
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath('//div[@class="pageNum active"]/text()').extract()
        if next_page:
            self.params["currentPage"] = str(int(next_page[0]) + 1)
            yield scrapy.FormRequest(url=f"http://www.ntzlyy.cn/comp/portalResNews/list.do", formdata=self.params,
                                     callback=self.parse, method='POST')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        content = response.xpath('.//article/p//text()').extract()
        save['mainbody'] = '\n'.join(content)
        print(save)
        yield save
