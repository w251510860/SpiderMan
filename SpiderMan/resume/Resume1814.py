import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1814(ResumeBaseSpider):
    name = "Resume1814"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.siyang.gov.cn/siyslj/ldxx2/202112/3d0ff72ed7fe43f7b18a3f04f1f8f2dd.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath("//ucapcontent/p")
        # 解析列表页
        for data in datas:
            save = {}
            content = ''.join(data.xpath('.//text()').extract()).replace('\u2002', '')
            if ':' not in content:
                continue
            save['name'] = content.split(':')[0]
            save['ori_url'] = 'http://www.siyang.gov.cn/siyslj/ldxx2/202112/3d0ff72ed7fe43f7b18a3f04f1f8f2dd.shtml'
            save['tag'] = "宿豫区水利局"
            save['status'] = content.split(':')[1].split('。')[0].replace('）', '')
            save['division'] = content.split(':')[1]
            if not save['status']:
                continue
            print(save)
            yield save
