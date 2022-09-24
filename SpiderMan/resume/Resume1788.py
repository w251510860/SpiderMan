import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1788(ResumeBaseSpider):
    name = "Resume1788"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://yjj.lishui.gov.cn/col/col1229282937/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = re.findall(r'(<a style=.*</a>)', response.text)
        # 解析列表页
        for data in datas:
            save = {"tag": "浙江省_丽水市_市应急管理局"}
            h5 = etree.HTML(data)
            save['ori_url'] = h5.xpath('.//@href')[0]
            save['name'] = h5.xpath('.//text()')[0]
            yield scrapy.Request(url=save['ori_url'], callback=self.parse_detail, meta={'save': save})
        return None

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        rets = response.xpath('//div[@class="TRS_Editor"]//text()')
        data = set([ret.extract() for ret in rets])
        response.meta['save']['division'] = '\n'.join(data)
        print(response.meta['save'])
        yield response.meta['save']

