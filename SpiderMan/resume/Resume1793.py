import re

import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1793(ResumeBaseSpider):
    name = "Resume1793"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://qtb.lishui.gov.cn/col/col1229269067/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = re.findall(r'(<div style="overflow-x: hidden.*</div>)', response.text)
        leader_names = []
        # 解析列表页
        for data in datas:
            save = {}
            data = etree.HTML(data)
            save['img_link'] = 'http://qtb.lishui.gov.cn/' + data.xpath('.//@src')[0]
            save['name'] = ''.join(data.xpath('.//tr[2]//text()')).replace(' ', '').replace('\xa0', '').replace('姓名：', '')
            save['ori_url'] = 'http://qtb.lishui.gov.cn/col/col1229269067/index.html'
            save['status'] = ''.join(data.xpath('.//tr[1]//text()')).replace(' ', '').replace('\xa0', '').replace('职务：', '')
            save['division'] = ''.join(data.xpath('.//tr[4]//text()')).replace(' ', '').replace('\xa0', '').replace('工作分工：', '')
            save['tag'] = "浙江省_丽水市_市外事办"
            print(save)
            yield save
