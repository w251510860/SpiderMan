import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY2(BaseSpider):
    name = "YY2"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'https://ylbzj.nmg.gov.cn/xwzx/tzgg/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'save': self.save, 'page': 0})

    def parse(self, response: HtmlResponse):
        if response.url == 'https://ylbzj.nmg.gov.cn/404/40x.html': return
        datas = response.xpath('//div[@class="bd"]/ul/li')
        for data in datas:
            # 解析列表页
            save = {}
            detail_url = f"https://ylbzj.nmg.gov.cn/xwzx/tzgg/{data.xpath('./a/@href').extract()[0][1:]}"
            save['title'] = data.xpath('./a/text()').extract()[0]
            save['ori_url'] = detail_url
            save['release_date'] = data.xpath('./span/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f"https://ylbzj.nmg.gov.cn/xwzx/tzgg/index_{next_page}.html", callback=self.parse,
                             meta={'save': self.save, 'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        response.meta['save']['ori_url'] = response.url
        # 解析详情页
        response.meta['save']['mainbody_table'] = response.xpath('//div[@class="TongXiLanCont"]/h1/text()').extract()[0]
        contents = response.xpath('//div[@class="content"]/div[1]/p')
        mainbody: list = []
        for content in contents:
            text = content.xpath('./text()').extract()
            mainbody.append(text[0] if text else '')
        response.meta['save']['mainbody'] = '\n'.join(mainbody)
        response.meta['save']['tag'] = 2
        print(response.meta['save'])
        yield response.meta['save']
