import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YYX(BaseSpider):
    name = "YYX"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            '',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0, 'save': {}})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('')
        # 解析列表页
        for data in datas:
            detail_url = f""
            response.meta['save']['title'] = data.xpath('').extratc()
            response.meta['save']['release_date'] = data.xpath('').extratc()
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': {}})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        self.count += 1
        print(self.count)
        response.meta['save']['mainbody'] = ''
        response.meta['save']['mainbody_table'] = ''
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        yield response.meta['save']
