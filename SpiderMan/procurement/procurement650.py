import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement650(ProcurementBaseSpider):
    name = "procurement650"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.tzszyy.com/index.php?r=site/news-list&id=78',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="list-item clearf"]/a')
        for data in datas:
            save = {}
            save["hospital_name"] = "宿迁市中医院"
            save["title"] = data.xpath('./div[1]/h2/text()').extract()[0]
            save["ori_url"] = "http://www.tzszyy.com/" + data.xpath("./@href").extract()[0]
            save["release_date"] = data.xpath("./div/div/p[2]/em/text()").extract()[0].replace("时间：", "")
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            yield scrapy.FormRequest(url=f"http://www.tzszyy.com/{next_page[0]}", callback=self.parse, method='GET')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@id="detail-con"]/p//text()').extract())
        print(save)
        yield save
