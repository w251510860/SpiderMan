import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class ResumeX(ResumeBaseSpider):
    name = "ResumeX"
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
            save = {"tag": ""}
            detail_url = ""
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': {}})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        yield response.meta['save']
