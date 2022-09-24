import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider
from lxml import etree


class Resume253(ResumeBaseSpider):
    name = "Resume253"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.wxlx.gov.cn/intertidwebapp/department/departmentDetailJson',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.json()['departmentVO']['leaders']
        # 解析列表页
        for data in datas:
            save = {}
            save['ori_url'] = 'http://www.wxlx.gov.cn/qmqjdbsc/zfxxgk/bmxxgkml/zfgk/index.shtml'
            save['name'] = data['leaderName']
            save['tag'] = "江苏_无锡_梁溪区_清名桥街道办事处"
            save['status'] = data['leaderPost']
            save['division'] = data['leaderLabor']
            save['resume'] = data['leaderResume']
            print(save)
            yield save
