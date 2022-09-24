import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY13(BaseSpider):
    name = "YY13"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxyxcg/yp/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        if response.status == 404:
            return
        # 解析列表页
        datas = response.xpath('//div[@class="content_r_main"]/ul/li')
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"http://www.ggzyzx.jl.gov.cn/jygg/cgzxyxcg/yp" + data.xpath('./a/@href').extract()[0][1:]
            save['title'] = data.xpath('./a/text()').extract()[0]
            save['release_date'] = data.xpath('./div/text()').extract()[0].replace('\n', '').replace(' ', '')
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://www.ggzyzx.jl.gov.cn/jygg/cgzxyxcg/yp/index_{next_page}.html', callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join([''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in response.xpath('//div[@class="neirong"]/div[2]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']

        annex = response.xpath('//div[@class="neirong"]/div[2]/p/a')
        if annex:
            response.meta['save']['annex_link'] = annex.xpath('./@href').extract()
            response.meta['save']['annex_title'] = annex.xpath('./@title').extract()
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
