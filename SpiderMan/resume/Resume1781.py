import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider
from lxml import etree


class Resume1781(ResumeBaseSpider):
    name = "Resume1781"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://sjgswj.lishui.gov.cn/col/col1229286422/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0, 'save': {}})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = re.findall(r'(<tr>.*</tr>)', response.text)
        # 解析列表页
        for data in datas:
            save = {"tag": "浙江省_丽水市_市机关事务服务中心"}
            h5 = etree.HTML(data)
            save['ori_url'] = h5.xpath('.//a/@href')[0]
            save['name'] = h5.xpath('.//a/text()')[0]
            yield scrapy.Request(url=save['ori_url'], callback=self.parse_detail, meta={'save': save})
        yield None

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        rets = response.xpath('.//div[@id="zoom"]/p/span/text()')
        data = set([ret.extract() for ret in rets])
        response.meta['save']['resume'] = '\n'.join(data)
        img = response.xpath('.//div[@id="zoom"]//@src').extract()
        response.meta['save']['img_link'] = f'http://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web3663/site{img[0]}' if img else ''
        print(response.meta['save'])
        yield response.meta['save']

