import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY4(BaseSpider):
    name = "YY4"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'https://nxyp.nxggzyjy.org/cms/showListZCFG.html?catalogId=2&bigType=&type=&pageNow=59',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 59})

    def parse(self, response: HtmlResponse):
        datas = response.xpath('//ul[@id="zcfgId"]/li')
        not_end = response.xpath('//div[@id="pages"]/input[@id="pageSelect"]/following-sibling::a[1]/text()').extract()
        if not not_end:
            return
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"https://nxyp.nxggzyjy.org{data.xpath('./a/@href').extract()[0]}"
            save['title'] = data.xpath('./a/label/text()').extract()[0]
            save['release_date'] = data.xpath('./span/text()').extract()
            if not save['release_date']:
                continue
            save['release_date'] = save['release_date'][0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        next_page_num = response.meta["page"] + 1
        next_page = f'https://nxyp.nxggzyjy.org/cms/showListZCFG.html?catalogId=2&bigType=&type=&pageNow={next_page_num}'
        yield scrapy.Request(url=next_page, callback=self.parse, meta={'page': next_page_num})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['img_link'] = response.xpath('//div[@class="contentCon"]/p[1]/img/@src').extract()
        response.meta['save']['img_title'] = response.xpath('//div[@class="contentTitle"]/text()').extract()
        response.meta['save']['annex_link'] = response.xpath('//div[@class="contentCon"]/p[2]/a/@href').extract()
        response.meta['save']['annex_title'] = response.xpath('//div[@class="contentCon"]/p[2]/a/text()').extract()
        response.meta['save']['tag'] = 4
        yield response.meta['save']
