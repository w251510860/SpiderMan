import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY11(BaseSpider):
    name = "YY11"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.sxyxcg.com/Showbulletin.asp?artStyleID=0&page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1, 'save': {}})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="sub_list"]/ul/li')
        if not datas:
            return
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"http://www.sxyxcg.com/" + data.xpath('./a/@href').extract_first()
            save['title'] = data.xpath('./a/@title').extract_first()
            save['release_date'] = data.xpath('./span/text()').extract_first()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://www.sxyxcg.com/Showbulletin.asp?artStyleID=0&page={next_page}',
                             callback=self.parse, meta={'page': next_page, 'save': {}})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join([''.join([text.extract() for text in texts.xpath('.//text()')]) for texts in response.xpath('//div[@class="sub_text"]/div')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        annex = response.xpath('//div[@class="sub_text"]/div//a')
        if annex:
            response.meta['save']['annex_link'] = annex.xpath('./@href').extract()
            response.meta['save']['annex_title'] = annex.xpath('./text()').extract()
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
