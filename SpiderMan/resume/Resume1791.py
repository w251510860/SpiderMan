import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1791(ResumeBaseSpider):
    name = "Resume1791"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://sfj.lishui.gov.cn/art/2018/9/10/art_1229261053_40201.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="union"]//img')
        # 解析列表页
        for data in datas:

            save = {}
            name = data.xpath('../following-sibling::p[1]//text()').extract()
            name = ''.join(name).replace('\xa0', ' ').strip().split(' ')
            save['name'] = name[-1].replace(' ', '')
            save['img_link'] = 'http://sfj.lishui.gov.cn' + data.xpath('./@src').extract()[0]
            save['ori_url'] = 'http://sfj.lishui.gov.cn/art/2018/9/10/art_1229261053_40201.html'
            save['status'] = ''.join(name[:-1])
            save['tag'] = "浙江省_丽水市_市司法局"
            division = data.xpath('../following-sibling::p')
            content = ''
            for text in division[1:]:
                text = text.xpath('.//text()').extract()
                if '\xa0' in text:
                    break
                content = content + '\n' + ''.join(text)
            save['division'] = content.replace('\xa0', '')
            print(save)
            yield save
