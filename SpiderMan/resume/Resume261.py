
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider
from lxml import etree


class Resume261(ResumeBaseSpider):
    name = "Resume261"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.jsxishan.gov.cn/doc/2019/04/26/1984360.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="TRS_Editor"]/table/tbody')
        # 解析列表页
        for data in datas:
            data = data.xpath('./tr[2]')
            save = {}
            save['ori_url'] = 'http://www.jsxishan.gov.cn/doc/2019/04/26/1984360.shtml'
            detail_data = data.xpath('./td[2]/p[2]/text()').extract()
            if not detail_data:
                continue
            save['status'], save['name'] = detail_data[0].replace('\u3000', '').split(' ')
            save['img_link'] = 'http://www.jsxishan.gov.cn' + data.xpath('./td[1]//img/@src').extract()[0]
            save['tag'] = "江苏_无锡_梁溪区_清名桥街道办事处"
            save['division'] = data.xpath('./td[2]/p[contains(text(), "分工")]/text()').extract()[0].replace('\u3000', '')
            save['resume'] = '\n'.join(data.xpath('./td[2]//p/text()').extract()).replace('\xa0', '').\
                replace('\n', '').replace('\u3000', '').replace('【分工】', '')
            print(save)
            yield save

