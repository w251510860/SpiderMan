import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY19(BaseSpider):
    name = "YY19"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.jxyycg.cn/list-7e2cc1851a05454e9ac408dc91e8d0a8.html?pageNo=1&pageSize=15',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        current_page = response.xpath('//li[@class="active"]/a/text()').extract()[0]
        if response.meta['page'] > int(current_page):
            return
        # 解析列表页
        datas = response.xpath('//div[@class="r w-900"]//div[@class="bd"]/ul/li')
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"http://www.jxyycg.cn" + data.xpath('./a/@href').extract()[0]
            save['title'] = data.xpath('./a/div[1]/text()').extract()[0]
            save['release_date'] = data.xpath('./a/div[2]/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        yield scrapy.Request(
            url=f'http://www.jxyycg.cn/list-7e2cc1851a05454e9ac408dc91e8d0a8.html?pageNo={next_page}&pageSize=15',
            callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="r-main details"]//div[@class="bd"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
