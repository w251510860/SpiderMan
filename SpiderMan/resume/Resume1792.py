import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1792(ResumeBaseSpider):
    name = "Resume1792"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://kjj.lishui.gov.cn/col/col1229219753/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = re.findall(r'(<li>.*</li>)', response.text)
        leader_names = []
        # 解析列表页
        for data in datas:
            save = {}
            data = etree.HTML(data)
            name = data.xpath('.//@title')
            if not name or name[0] in leader_names:
                continue
            leader_names.append(name[0])
            save['name'] = name[0]
            save['ori_url'] = data.xpath('.//@href')[0]
            save['tag'] = "浙江省_丽水市_市科技局"
            yield scrapy.Request(url=save["ori_url"], callback=self.parse_detail, meta={'save': save})

    def parse_detail(self, response: HtmlResponse):
        data = response.xpath('//table[@class="bk1"]//td[@valign="top"]')
        save = response.meta['save']
        save['status'] = ''.join(data[1].xpath('.//tr[1]//text()').extract())
        save['img_link'] = 'http://kjj.lishui.gov.cn/' + data[0].xpath('.//img/@src').extract()[0]
        save['division'] = ''.join([text.extract() for text in data[1].xpath('..//tr[5]//text()')])
        print(save)
        # yield save
