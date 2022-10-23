import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider



class Procurement420(ProcurementBaseSpider):
    name = "procurement420"
    base_link = 'http://www.njfybjy.com/ywgk/'
    data = {
        "__EVENTTARGET": "AspNetPager1",
        "__EVENTARGUMENT": "1",
        "__VIEWSTATE": "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",
        "__EVENTVALIDATION": "/wEdAANmam8sxIVte9hqQHWjuQ5xN5WJAUWWFbd52MiIX8UZDG0tI/XNTpJ7S3vo8J4A0kAwHEaZ+nmfperuK9X3eEc6olIy+A==",
        "top%24txtSo": ""
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://www.njfybjy.com",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.njfybjy.com/ywgk/ywgklist.aspx?mtt=73&typename=%u62db%u6807%u4fe1%u606f&m=15",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    page = 1

    def start_requests(self):
        # 初始页
        urls = [
            'http://www.njfybjy.com/ywgk/ywgklist.aspx?mtt=73&typename=%E6%8B%9B%E6%A0%87%E4%BF%A1%E6%81%AF&m=15',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='POST', formdata=self.data,
                                     headers=self.headers)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="n-list"]/ul/li')
        for data in datas:
            save = {}
            save["hospital_name"] = "南京市妇幼保健院"
            save["title"] = data.xpath('./a/text()').extract()[0]
            save["ori_url"] = self.base_link + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath("./span/text()").extract()[0].replace('[', '').replace(']', '')
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})

        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            self.data['__EVENTARGUMENT'] = str(next_page[0].replace("javascript:__doPostBack('AspNetPager1','", '').replace("')", ""))
            yield scrapy.FormRequest(url='http://www.njfybjy.com/ywgk/ywgklist.aspx?mtt=73&typename=%E6%8B%9B%E6%A0%87%E4%BF%A1%E6%81%AF&m=15',
                                     callback=self.parse, method='POST', formdata=self.data, headers=self.headers)

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        save['mainbody'] = '\n'.join(response.xpath('//div[@class="ri-txt"]/div[2]//text()').extract())
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        save['content'] = response.text
        yield save
