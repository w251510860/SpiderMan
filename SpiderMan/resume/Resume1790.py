import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1790(ResumeBaseSpider):
    name = "Resume1790"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://slj.lishui.gov.cn/col/col1229248018/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//div[@class="mainlm_l fl"]/ul[1]/li')
        # 解析列表页
        for data in datas:
            save = {}
            name = data.xpath('./a/@title').extract()
            if not name: continue
            name = name[0].split(' ')
            save['name'] = name[0]
            save['status'] = ''.join(name[1:])
            save['ori_url'] = 'http://slj.lishui.gov.cn' + data.xpath('./a/@href').extract()[0]
            save['tag'] = "浙江省_丽水市_市水利局"
            yield scrapy.Request(url=save["ori_url"], callback=self.parse_detail, meta={'save': save})

    def parse_detail(self, response: HtmlResponse):
        data = response.xpath('//div[@class="mainlm_r fr"]/table[1]/tbody/tr[2]')
        save = response.meta['save']
        save['img_link'] = 'http://slj.lishui.gov.cn' + data.xpath('.//img/@src').extract()[0]
        save['division'] = ''.join([text.extract() for text in data.xpath('.//p//text()')])
        print(save)
        yield save
