import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY14(BaseSpider):
    name = "YY14"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.hljypcg.org.cn/xw/queryGd',
        ]
        data = {
            'pageNo': '1',
            'pageSize': '50',
            'pageCount': '26',
            'XWLB': '2',
            'XWID': '',
        }
        for url in urls:
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse, meta={'page': 1, 'data': data})

    def parse(self, response: HtmlResponse):
        print(response.url)
        # 解析列表页
        datas = response.xpath('//ul[@class="news_list"]/li')
        if not datas:
            return
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = 'http://www.hljypcg.org.cn/xw/queryXwnrForYl?XWID=' + \
                         data.xpath('./span/a/@onclick').extract()[0].replace("queryXwnr('", ''). \
                             replace("');return false;", '')
            save['title'] = data.xpath('./span/a/@title').extract()[0]
            save['release_date'] = data.xpath('./span[2]/text()').extract()[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        data = response.meta['data']
        data['pageNo'] = str(next_page)
        yield scrapy.FormRequest(url='http://www.hljypcg.org.cn/xw/queryGd', formdata=data, callback=self.parse, meta={'page': next_page, 'data': data})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join([''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in response.xpath('//div[@class="detail"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']

        annexs = response.xpath('//div[@class="zcfg_pd"]//a')
        if annexs:
            base_url = 'http://www.hljypcg.org.cn/upload/downFile?fjbh='
            annex_link = []
            annex_title = []
            for annex in annexs:
                if annex.xpath('./@href'):
                    annex_link.append(base_url + annex.xpath('./@href').extract()[0].replace("javascript:xiazai('", '').replace("')", ''))
                elif annex.xpath('./text()'):
                    annex_title.append(annex.xpath('./text()').extract()[0])
                else:
                    continue
            response.meta['save']['annex_link'] = annex_link
            response.meta['save']['annex_title'] = annex_title
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
