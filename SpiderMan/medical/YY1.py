import sys

import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY1(BaseSpider):
    name = "YY1"
    base_link = 'http://gxyxcg.gxzf.gov.cn/gsgg'

    def start_requests(self):
        urls = [
            'http://gxyxcg.gxzf.gov.cn/gsgg/index.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        a_list = response.xpath('//div[@id="morelist"]/ul/li/a')
        for data in a_list:
            save = {}
            save['title'] = data.xpath('./text()').extract()[0]
            yield scrapy.Request(url=f"{self.base_link}{data.xpath('./@href').extract()[0][1:]}",
                                 meta={'save': save}, callback=self.parse_detail)
        next_page = response.meta["page"] + 1
        yield scrapy.Request(url=f'http://gxyxcg.gxzf.gov.cn/gsgg/index_{next_page}.shtml',
                             callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        response.meta['save']['ori_url'] = response.url
        self.count += 1
        body = response.xpath('//div[@class="article-con"]')
        main_body = body.xpath('./div[1]')
        response.meta['save']['content'] = '\n'.join(
            [''.join(content.xpath('.//text()').extract()) for content in main_body.xpath('./p')])
        response.meta['save']['annex_link'] = [url.extract() for url in main_body.xpath('.//a/@href')]
        response.meta['save']['annex_title'] = [url.extract() for url in main_body.xpath('.//a/text()')]
        response.meta['save']['tag'] = 1
        print(response.meta['save'])
        yield response.meta['save']
