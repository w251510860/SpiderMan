import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY17(BaseSpider):
    name = "YY17"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.ahyycg.cn/index/notice.html?id=15&pageIndex=1',
            'http://www.ahyycg.cn/index/notice.html?id=16&pageIndex=1',
            'http://www.ahyycg.cn/index/notice.html?id=17&pageIndex=1',
            'http://www.ahyycg.cn/index/notice.html?id=18&pageIndex=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1, 'save': {}})

    def parse(self, response: HtmlResponse):
        current_page = response.xpath('//li[@class="number active"]/text()').extract()[0]
        if int(current_page) < response.meta['page']:
            return

        # 解析列表页
        datas = response.xpath('//div[@class="message-conten activet"]/div')
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = 'http://www.ahyycg.cn' + data.xpath('./@onclick').extract()[0].replace("window.open('", '').replace("')", '')
            save['title'] = data.xpath('./div[1]/div[2]/@title').extract()[0]
            save['release_date'] = data.xpath('./div[2]/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://www.ahyycg.cn/index/notice.html?id=15&pageIndex={next_page}',
                             callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="db-content"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = []
        response.meta['save']['annex_title'] = []
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
