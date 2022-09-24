import arrow
import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY7(BaseSpider):
    name = "YY7"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'https://www.tjmpc.cn/WebSite/Home/NewsListPage',
        ]
        data = {
            'PageIndex': '1',
            'ISGJHC': '',
        }
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, formdata=data, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        if not response.json().get('rows'):
            return
        # 解析列表页
        datas = response.json()['rows']
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = f"https://www.tjmpc.cn/website/home/infoPage?NEWSID={data['NEWSID']}&NEWSCOLUMNID={data['NEWSCOLUMNID']}"
            save['title'] = data['NEWSTITLE']
            save['release_date'] = arrow.get(int(data['PUBLISHTIME'].replace('/Date(', '').replace(')/', ''))).format('YYYY-MM-DD HH:mm:ss')
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        next_page = response.meta['page'] + 1
        formdata = {'PageIndex': str(next_page), 'ISGJHC': ''}
        yield scrapy.FormRequest(url='https://www.tjmpc.cn/WebSite/Home/NewsListPage', callback=self.parse,
                                 formdata=formdata, meta={'page': next_page})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = ''.join([''.join([content.extract() for content in data.xpath('./span//text()')]) for data in response.xpath('//div[@id="new_xx"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = response.xpath('//div[@class="ATTACHMENT"]/a/@href').extract()
        response.meta['save']['annex_title'] = response.xpath('//div[@class="ATTACHMENT"]/a/text()').extract()
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
