import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1801(ResumeBaseSpider):
    name = "Resume1801"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://wsjsw.lishui.gov.cn/col/col1229231187/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="TRS_Editor"]/../../..//tr')
        leader_names = []
        # 解析列表页
        for data in datas[1:]:
            save = {}
            save['name'] = data.xpath('.//td[2]/a/@title').extract()[0]
            save['ori_url'] = data.xpath('.//td[2]/a/@href').extract()[0]
            save['tag'] = "浙江省_丽水市_市卫生健康委员会"
            yield scrapy.Request(url=save['ori_url'], callback=self.parse_detail, meta={'save': save})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        save = response.meta['save']
        data = response.xpath("//p/text()").extract()
        save['status'] = data[0]
        save['division'] = data[1] if len(data) > 1 else None
        print(save)
        yield save

