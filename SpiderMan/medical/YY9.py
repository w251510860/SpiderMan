import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY9(BaseSpider):
    name = "YY9"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.yjsds.com/dailitongzhi/list/p/1.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1, 'save': {}})

    def parse(self, response: HtmlResponse):
        datas = response.xpath('//ul[@class="news_hd_list"]/li')
        if not datas:
            return
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = data.xpath('./a/@href').extract_first()
            save['title'] = data.xpath('./a/text()').extract_first()
            save['release_date'] = data.xpath('./span/text()').extract_first()
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'http://www.yjsds.com/dailitongzhi/list/p/{next_page}.html',
                             callback=self.parse, meta={'page': next_page, 'save': {}})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        texts = response.xpath('//div[@class="news_text_cont"]//p[@class="MsoNormal"]')
        if texts:
            response.meta['save']['mainbody'] = ''.join([''.join([info.extract() for info in text.xpath('.//text()')]) for text in texts])
            response.meta['save']['mainbody_table'] = response.meta['save']['title']

        annex = response.xpath('//a[@class="ke-insertfile"]')
        if annex:
            response.meta['save']['annex_link'] = 'http://www.yjsds.com/' + annex.xpath('./@href')[0].extract()
            response.meta['save']['annex_title'] = annex.xpath('./text()').extract_first()

        img = response.xpath('//div[@class="news_text_cont"]/p/img/@src')
        if img:
            response.meta['save']["img_link"] = img[0].extract()
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
