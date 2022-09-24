import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1784(ResumeBaseSpider):
    name = "Resume1784"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://tjj.lishui.gov.cn/col/col1229215913/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@id="h"]')
        # 解析列表页
        for data in datas:
            name = data.xpath('./div[1]/text()').extract()
            ori_url = data.xpath('./div[2]/img/@src').extract()
            division = data.xpath('./div[3]/text()').extract()
            resume = '\n'.join([text.extract() for text in data.xpath('./div[4]//text()')])
            save = {
                "tag": "浙江省_丽水市_市行政服务中心",
                "name": name[0] if name else "",
                "division": division[0] if division else "",
                "resume": resume if resume else "",
                "img_link": ori_url[0] if ori_url else "",
                "ori_url": "http://tjj.lishui.gov.cn/col/col1229215913/index.html"
            }
            print(save)
            yield save
