import re

import requests
import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1817(ResumeBaseSpider):
    name = "Resume1817"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            "http://sthj.xz.gov.cn/govxxgk/01405165st/2019-08-07/f5d032b2-2b26-482c-8af9-b4b6abd8b110.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//p/text()')
        for data in datas:
            save = {}
            content = ''.join(data.extract()).replace('\u2002', '')
            save['name'] = content.split('，')[0]
            save['ori_url'] = 'http://sthj.xz.gov.cn/govxxgk/01405165st/2019-08-07/f5d032b2-2b26-482c-8af9-b4b6abd8b110.html'
            save['tag'] = "徐州市生态环境局"
            save['status'] = content.split('。')[0].split('，')[-1]
            save['division'] = ''.join(content.split('。')[1:])
            print(save)
            yield save
