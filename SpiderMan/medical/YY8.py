import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY8(BaseSpider):
    name = "YY8"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.smpaa.cn/xxgk/gggs/index_zhaobiao.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        if response.status == 404:
            print(f'网站异常: {response.url}')
            return
        # 解析列表页
        datas = response.xpath('//div[@class="list_list_con"]/ul/li/a')
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = 'http://www.smpaa.cn' + data.xpath('./@href').extract()[0]
            save['title'] = data.xpath('./text()')[0].extract()
            save['release_date'] = data.xpath('./span/text()')[0].extract()
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://www.smpaa.cn/xxgk/gggs/index_zhaobiao{next_page}.shtml', callback=self.parse, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        datas = response.xpath('//div[@class="content_con_cen"]/p')
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        if not datas:
            return response.meta['save']
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join([''.join([content.extract() for content in data.xpath(".//text()")]) for data in datas])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        annex = datas.xpath('//div[@class="content_con_cen"]/div//a/@href')
        if annex:
            response.meta['save']['annex_link'] = 'http://www.smpaa.cn/' + annex[0].extract()
        annex_title = datas.xpath('//div[@class="content_con_cen"]/div//a/text()')
        if annex_title:
            response.meta['save']['annex_title'] = annex_title[0].extract()
        return response.meta['save']
