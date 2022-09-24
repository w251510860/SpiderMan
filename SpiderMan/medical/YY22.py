import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY22(BaseSpider):
    name = "YY22"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.hbyxjzcg.cn/drug/0-1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1, 'save': {}})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        disable = response.xpath('//span[@class="disabled"]/text()').extract()
        datas = response.xpath('//ul[@class="news_list"]/li')

        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"http://www.hbyxjzcg.cn" + data.xpath('./a/@href').extract()[0]
            save['title'] = data.xpath('./a/@title').extract()[0]
            save['release_date'] = data.xpath('./span/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        if disable and '下一页' in disable[0]:
            return

        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://www.hbyxjzcg.cn/drug/0-{next_page}.html',
                             callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="entry"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
