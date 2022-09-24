import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1812(ResumeBaseSpider):
    name = "Resume1812"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.suyu.gov.cn/suyu/jgxx/202106/16506d0f8d854618b346e79cd294aa75.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath("//ucapcontent/p")
        # 解析列表页
        for data in datas:
            save = {}
            content = ''.join(data.xpath('.//text()').extract())
            save['name'] = content.split('：')[0].split('（')[0]
            save['ori_url'] = 'http://www.suyu.gov.cn/suyu/jgxx/202106/16506d0f8d854618b346e79cd294aa75.shtml'
            save['tag'] = "宿豫区水利局"
            save['status'] = content.split('：')[0].split('（')[1].replace('）', '')
            save['division'] = content.split('：')[1]
            print(save)
            yield save
