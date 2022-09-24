import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1813(ResumeBaseSpider):
    name = "Resume1813"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.shuyang.gov.cn/syslj/jgszhrsrm/202112/a621e61e61d243d3a283391d91899250.shtml',
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
            if '服务乡镇' in content or '（单位）' in content or not content:
                continue
            save['name'] = content.split('：')[0].split('（')[0]
            save['ori_url'] = 'http://www.shuyang.gov.cn/syslj/jgszhrsrm/202112/a621e61e61d243d3a283391d91899250.shtml'
            save['tag'] = "宿豫区水利局"
            save['status'] = content.split('：')[0].split('（')[1].replace('）', '')
            save['division'] = content.split('：')[1]
            print(save)
            yield save
