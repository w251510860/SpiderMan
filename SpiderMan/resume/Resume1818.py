import re

import requests
import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1818(ResumeBaseSpider):
    name = "Resume1818"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            "http://zrzy.jiangsu.gov.cn/gtapp/nrglIndex.action?type=2&messageID=2c9082b55acb3a5b015acb3c73030001",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.xpath("//span[contains(text(),'个人简历')]")
        for data in datas:
            save = {}
            name_content = data.xpath('../preceding-sibling::p[1]//text()')
            if not name_content.extract()[1].replace('\r\n', ''):
                name_content = data.xpath('../preceding-sibling::p[2]//text()')
            content = name_content.extract()[1]
            save['name'] = content.split('，')[0]
            save['ori_url'] = 'http://zrzy.jiangsu.gov.cn/gtapp/nrglIndex.action?type=2&messageID=2c9082b55acb3a5b015acb3c73030001'
            save['tag'] = "徐州市自然资源和规划局"
            save['status'] = content.split('。')[0].split('，')[-1]
            save['division'] = ''.join(content.split('。')[1:])
            save['resume'] = ''.join(data.xpath('../following-sibling::p[1]//text()').extract())
            print(save)
            yield save
