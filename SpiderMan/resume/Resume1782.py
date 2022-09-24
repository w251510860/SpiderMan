import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1782(ResumeBaseSpider):
    name = "Resume1782"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://xzsp.lishui.gov.cn/art/2021/3/23/art_1229215737_4566848.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//table[@border="1"]//tr')
        # 解析列表页
        for data in datas:
            name = data.xpath('./td[2]/p/span/text()').extract()
            if '姓名' in name:
                continue
            division = data.xpath('./td[3]/p/span/text()').extract()
            resume = data.xpath('./td[4]/p/span/text()').extract()
            if not name:
                continue
            save = {
                "tag": "浙江省_丽水市_市行政服务中心",
                "name": name[0] if name else "",
                "division": division[0] if division else "",
                "resume": ''.join(resume) if resume else "",
                "ori_url": "http://xzsp.lishui.gov.cn/art/2021/3/23/art_1229215737_4566848.html",
                "detail_url": "http://xzsp.lishui.gov.cn/art/2021/3/23/art_1229215737_4566848.html"
            }
            print(save)
            yield save
