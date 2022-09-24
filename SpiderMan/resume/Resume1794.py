import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1794(ResumeBaseSpider):
    name = "Resume1794"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.lishui.gov.cn/col/col1229430239/index.html?key',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = re.findall(r'(<li><a.*</li>)', response.text)
        leader_names = []
        # 解析列表页
        for data in datas:
            save = {}
            data = etree.HTML(data)

            save['name'] = data.xpath('.//a/@title')[0]
            save['ori_url'] = data.xpath('.//a/@href')[0]
            save['tag'] = "浙江省_丽水市_市市场监管局"
            yield scrapy.Request(url=save['ori_url'], callback=self.parse_detail, meta={'save': save})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        save = response.meta['save']
        content = response.xpath('//table[@class="leader_box2"]//td//p/text()').extract()
        save['img_link'] = 'lishui.gov.cn' + response.xpath('//td[@align="center"]/img/@src').extract()[0]
        save['status'] = response.xpath('//table[@class="leader_box2"]/tr[1]/td[2]//text()').extract()[0]
        save['division'] = content[1]
        print(save)
        yield save
