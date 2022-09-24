import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1785(ResumeBaseSpider):
    name = "Resume1785"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://czj.lishui.gov.cn/col/col1229261717/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//td[@class="content14"]//tr')
        # 解析列表页
        for data in datas:
            save = {}
            name = data.xpath('./td[2]/a/@title').extract()
            if not name: continue
            save['name'] = name[0]
            save['ori_url'] = data.xpath('./td[2]/a/@href').extract()[0]
            save['tag'] = "浙江省_丽水市_市财政局"
            yield scrapy.Request(url=save["ori_url"], callback=self.parse_detail, meta={'save': save})

    def parse_detail(self, response: HtmlResponse):
        data = response.xpath('//div[@class="zoom"]')
        save = response.meta['save']
        save['img_link'] = 'http://www.lishui.gov.cn' + data.xpath('.//img/@src').extract()[0]
        save['resume'] = ''.join([text.extract() for text in response.xpath('.//table[@class="leader_box2"]//tr[1]//text()')]).replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '')
        save['division'] = ''.join([text.extract() for text in response.xpath('.//table[@class="leader_box2"]//tr[2]//text()')]).replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '')
        print(save)
        yield save
