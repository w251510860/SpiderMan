import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY29(BaseSpider):
    name = "YY29"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.sxsyxcg.com/Homepage/ShowListNew.aspx?CatalogId=3',
        ]
        data = {
            '__VIEWSTATE': 'R+Cjn9zmupcyz5Igu1nt+ItzPjsIk3dK3ACcZ6d/QuSP0Ch97gJKv4pmQtPN10pKAP2UNQb89qCxh03HZr6HV8X9o/AHlJ6yOZauKmIInmtuhPAB/vzp9jen+z6iGk9nm119rnS2LZT0P2VJ10vLPN2VEy22AgWhdaeuwPBCFygrzMwjf8lK4fmJTkw=',
            '__VIEWSTATEGENERATOR': '0CAF9199',
            '__EVENTTARGET': 'pager1',
            '__EVENTARGUMENT': '1',
            '__EVENTVALIDATION': 'SOC+/GMz6a3dic60bQATa3PW3raQiPIMLepl8CIFj8gCYujQX4gg4FVVZt2CuTYM5cOyujKF90Qtu7QTInN3lH9qEcDfWnSVWcl7Li+BrhJtcGweoIUYnIUPfTs=',
            'txtTitle': '',
        }
        self.headers = {
            'Proxy-Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Origin': 'http://www.sxsyxcg.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://www.sxsyxcg.com/Homepage/ShowListNew.aspx?CatalogId=3',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'ASP.NET_SessionId=rbwwuu55kvx0v545qalvorba; _gscu_1493419039=485480689km69f15; _gscbrs_1493419039=1; _gscs_1493419039=t48561152sv4vl915|pv:1',
        }
        for url in urls:
            yield scrapy.FormRequest(url=url, formdata=data, headers=self.headers, callback=self.parse,
                                     meta={'page': 1, 'data': data})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="els-messagelist els-box-body"]/ul/li/a')
        last_page = response.xpath('//select/option[last()]/text()').extract()[0]
        # 解析列表页
        for data in datas:
            save = {}
            detail_url = "http://www.sxsyxcg.com" + data.xpath('./@href').extract()[0]
            content = ''.join(data.xpath('.//text()').extract())
            _, save['title'], save['release_date'] = content.split('\xa0')
            save['release_date'] = save['release_date'].replace('[', '').replace(']', '')
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})

        next_page = response.meta['page'] + 1
        if next_page > int(last_page):
            return
        data = response.meta['data']
        data['__EVENTARGUMENT'] = str(next_page)
        yield scrapy.FormRequest(url='http://www.sxsyxcg.com/Homepage/ShowListNew.aspx?CatalogId=3',
                                 formdata=data, headers=self.headers, callback=self.parse,
                                 meta={'page': next_page, 'data': data})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="els-contentCon"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']