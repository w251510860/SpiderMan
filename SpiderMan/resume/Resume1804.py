import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1804(ResumeBaseSpider):
    name = "Resume1804"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://sswj.lishui.gov.cn/col/col1229347506/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath('//table[@class="ldxx"]//tr')
        # 解析列表页
        for data in datas[1:]:
            save = {}
            save['name'] = data.xpath('./td[1]/text()').extract()[0]
            save['ori_url'] = 'http://sswj.lishui.gov.cn/col/col1229347506/index.html'
            save['tag'] = "浙江省_丽水市_市卫生健康委员会"
            save['status'] = data.xpath('./td[3]/text()').extract()[0]
            save['division'] = ''.join(data.xpath('./td[4]//text()').extract())
            save['resume'] = ''.join(data.xpath('./td[2]//text()').extract())
            save['img_link'] = 'http://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web3701/site' + data.xpath('./td[6]//img/@src').extract()[0]
            print(save)
            yield save
