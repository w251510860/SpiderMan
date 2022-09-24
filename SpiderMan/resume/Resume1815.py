import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1815(ResumeBaseSpider):
    name = "Resume1815"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.pz.gov.cn/002/002002/002002001/002002001001/leaderInfos.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//li[@class="em-leader-item"]/a')
        # 解析列表页
        for data in datas:
            save = {}
            save['name'] = data.xpath('./text()').extract()[0].replace('\u3000', '')
            save['ori_url'] = 'http://www.pz.gov.cn' + data.xpath('./@href').extract()[0]
            save['tag'] = "邳州市人民政府"
            save['status'] = data.xpath('../div[@class="em-leader-title"]/text()').extract()[0].replace(' ', '').\
                replace('\r', '').replace('\t', '').replace('\n', '').replace('：', '')
            yield scrapy.Request(url=save['ori_url'], callback=self.parse_detail, meta={'save': save})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        save = response.meta['save']
        data = response.xpath('//div[@class="em-leader-infos"]/div')
        save['img_link'] = 'http://www.pz.gov.cn' + data[0].xpath('//img[@class="em-leader-photo "]/@src').extract()[0]
        save['resume'] = ''.join(data[1].xpath('//div[@class="em-content"]//text()').extract()).replace(' ', '').\
                replace('\r', '').replace('\t', '').replace('：', '')
        save['division'] = ''.join(data[1].xpath('//div[@class="em-activity-list"]//text()').extract()).replace(' ', '').\
                replace('\r', '').replace('\t', '').replace('：', '')
        print(save)
        yield save


