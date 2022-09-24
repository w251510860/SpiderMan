import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY24(BaseSpider):
    name = "YY24"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'https://www.gdmede.com.cn/announcement/?page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="wrap"]/a')
        if not datas:
            return
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"https://www.gdmede.com.cn" + data.xpath('./@href').extract()[0]
            save['title'] = data.xpath('./div[1]/span/text()').extract()[0]
            save['release_date'] = data.xpath('./div[2]/div[@class="date"]/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'https://www.gdmede.com.cn/announcement/?page={next_page}',
                             callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="f-detail-content"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
