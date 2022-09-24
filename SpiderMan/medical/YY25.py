import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY25(BaseSpider):
    name = "YY25"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://zw.hainan.gov.cn/hngpc/new/0-1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1, 'save': {}})

    def parse(self, response: HtmlResponse):
        disable = response.xpath('//span[@class="disabled"]/text()').extract()
        # 解析列表页
        datas = response.xpath('//div[@class="els-infoContent"][1]/ul/li/a')
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = "http://zw.hainan.gov.cn" + data.xpath('./@href').extract()[0]
            save['title'] = data.xpath('./@title').extract()[0]
            save['release_date'] = data.xpath('./span/text()').extract()[0].replace('[', '').replace(']', '')
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        if disable and '下一页' in disable[0]:
            return
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://zw.hainan.gov.cn/hngpc/new/0-{next_page}.html',
                             callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="contentCon"]//div | //div[@class="contentCon"]//p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
