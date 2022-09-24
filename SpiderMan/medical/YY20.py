import json

import scrapy
from scrapy.http.response.html import HtmlResponse
import xmltodict
from lxml import etree

from .Base import BaseSpider


class YY20(BaseSpider):
    name = "YY20"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://ggzyjyzx.shandong.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15&unitid=483526&webid=428&path=http://ggzyjyzx.shandong.gov.cn/&webname=%E5%B1%B1%E4%B8%9C%E7%9C%81%E5%85%AC%E5%85%B1%E8%B5%84%E6%BA%90%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&col=1&columnid=209501&sourceContentType=1&permissiontype=0',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 45})

    def parse(self, response: HtmlResponse):
        content = xmltodict.parse(response.text)
        content = json.loads(json.dumps(content, indent=1))
        # 解析列表页
        datas = content['datastore']['recordset']['record']
        total_record = int(content['datastore']['totalrecord'])
        # 解析列表页
        for data in datas:
            self.count += 1
            save = {}
            ret = etree.HTML(data)
            detail_url = ret.xpath('//a/@href')[0]
            save['title'] = ret.xpath('//a/@title')[0]
            save['release_date'] = ret.xpath('//span/text()')[0]
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'save': save})
        if self.count >= total_record:
            return
        next_start = response.meta['page'] + 1
        next_end = response.meta['page'] + 45
        yield scrapy.Request(url=f'http://ggzyjyzx.shandong.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={next_start}&endrecord={next_end}&perpage=15&unitid=483526&webid=428&path=http://ggzyjyzx.shandong.gov.cn/&webname=%E5%B1%B1%E4%B8%9C%E7%9C%81%E5%85%AC%E5%85%B1%E8%B5%84%E6%BA%90%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&col=1&columnid=209501&sourceContentType=1&permissiontype=0', callback=self.parse, meta={'page': next_end})

    def parse_detail(self, response: HtmlResponse):
        # 解析详情页
        response.meta['save']['ori_url'] = response.url
        response.meta['save']['mainbody'] = '\n'.join(
            [''.join([data.extract() for data in datas.xpath('.//text()')]) for datas in
             response.xpath('//div[@class="zhengwen"]/p')])
        response.meta['save']['mainbody_table'] = response.meta['save']['title']
        response.meta['save']['annex_link'] = ''
        response.meta['save']['annex_title'] = ''
        response.meta['save']['tag'] = int(self.name.replace('YY', ''))
        yield response.meta['save']
