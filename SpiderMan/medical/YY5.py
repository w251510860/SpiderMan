import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY5(BaseSpider):
    name = "YY5"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://202.100.182.111:8090/ypcgpt/ggtz/1.htm',
            'http://202.100.182.111:8090/ypcgpt/ggtz.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        if response.status == 404:
            return
        # 解析列表页
        datas = response.xpath('.//div[@id="con_one_1"]/table//tr')
        # 解析列表页
        for data in datas[:-3]:
            save = {}
            detail_url = data.xpath('.//a/@href').extract()
            if not detail_url:
                continue
            detail_url = 'http://202.100.182.111:8090/' + detail_url[0].replace('../', '')
            save['title'] = data.xpath('.//a/@title').extract()[0]
            save['release_date'] = data.xpath('.//span[@class="timestyle18426"]/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        if response.url == 'http://202.100.182.111:8090/ypcgpt/ggtz.htm':
            return
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://202.100.182.111:8090/ypcgpt/ggtz/{next_page}.htm', callback=self.parse,
                             meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        datas = response.xpath('//div[@id="vsb_content"]//p')
        response.meta['save']['ori_url'] = response.url
        # 解析详情页
        response.meta['save']['mainbody'] = ''.join(
            [''.join([content.extract() for content in data.xpath('./span/text()')]) for data in datas])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        annex_link = response.xpath('//td[@align="left"]/span/span[1]/a/@href').extract()
        response.meta['save']['annex_link'] = 'http://202.100.182.111:8090/' + annex_link[0].replace('../../',
                                                                                                     '') if annex_link else []
        response.meta['save']['annex_title'] = response.xpath(
            '//td[@align="left"]/span/span[1]/a/span/text()').extract()
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
