import requests
import scrapy
from scrapy.http.response.html import HtmlResponse
from lxml import etree

from .Base import BaseSpider


class YY31(BaseSpider):
    name = "YY31"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://223.220.250.135:8081/HomePage/ShowList.aspx?CatalogId=8',
        ]
        data, self.headers = self.get_params()
        for url in urls:
            yield scrapy.FormRequest(url=url, formdata=data, headers=self.headers, callback=self.parse,
                                     meta={'page': 1, 'data': data})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@id="rightcenter"]/ul/li/a')
        last_page = response.xpath('//select/option[last()]/text()').extract()[0]
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = "http://223.220.250.135:8081" + data.xpath('./@href').extract()[0]
            content = ''.join(data.xpath('.//text()').extract())
            _, save['title'], save['release_date'] = content.split('\xa0')
            save['release_date'] = save['release_date'].replace('[', '').replace(']', '')
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        if next_page > int(last_page):
            return
        data = response.meta['data']
        data['__EVENTARGUMENT'] = str(next_page)
        yield scrapy.FormRequest(url='http://223.220.250.135:8081/HomePage/ShowList.aspx?CatalogId=8',
                                 formdata=data, headers=self.headers, callback=self.parse,
                                 meta={'page': next_page, 'data': data})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@id="info-content"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']

    def get_params(self):
        data = {
            '__VIEWSTATE': '/wEPDwULLTExMjYxNjYzNzYPZBYCZg9kFgICAw9kFgICBQ9kFgICAg8PFgQeC1JlY29yZENvdW50ApkGHgtDdXJyZW50UGFnZQICZGRkVk+y696KXS9WBLXp74TeTBEXJfumAFnhVlqUFGmnlgE=',
            '__VIEWSTATEGENERATOR': '16058434',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$pager1',
            '__EVENTARGUMENT': '1',
            '__EVENTVALIDATION': '/wEdAAM0HMxRq22HLdJrkkO2OozpjT3aQAwqo3bF7+3142UovI5MW6XMaFjzT9nUdsIknosAu7ZTQljo2jPFt2ysbLcHMB66v2vdC84QQwm0U+1r9w==',
            'ctl00$ContentPlaceHolder1$txtTitle': '',
        }
        headers = {
            'Proxy-Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://223.220.250.135:8081',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://223.220.250.135:8081/HomePage/ShowList.aspx?CatalogId=8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'ASP.NET_SessionId=peytbweqvemy0rdvpvm1zetu; UM_distinctid=17fd51f7405a54-0a38ae8390f266-1c3d645d-13c680-17fd51f7406e24; CNZZDATA1278203983=1348774306-1648548083-%7C1648556760',
        }
        url = 'http://223.220.250.135:8081/HomePage/ShowList.aspx?CatalogId=8'
        ret = requests.post(url, headers=headers, json=data)
        ret = etree.HTML(ret.text)
        VIEWSTATE = ret.xpath('//input[@name="__VIEWSTATE"]/@value')[0]
        EVENTVALIDATION = ret.xpath('//input[@name="__EVENTVALIDATION"]/@value')[0]
        data['__VIEWSTATE'] = VIEWSTATE
        data['__EVENTVALIDATION'] = EVENTVALIDATION
        return data, headers
