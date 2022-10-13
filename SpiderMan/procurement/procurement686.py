import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement686(ProcurementBaseSpider):
    name = "procurement686"
    base_link = ''
    def start_requests(self):
        # 初始页
        urls = [
            'http://www.nt2191.com/news.html?cid=39',
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.xpath('//div[@class="p_news new-lists"]/div[@class="new-list"]/div')
        if not datas:
            return
        for data in datas:
            save = {}
            save["hospital_name"] = "南通市第一人民医院"
            save["title"] = data.xpath('./a/text()').extract()[0]
            save["ori_url"] = "http://www.nt2191.com" + data.xpath("./a/@href").extract()[0]
            save["release_date"] = data.xpath('./span/text()').extract()[0].replace("[", "").replace("]", "")
            yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
        next_page = response.xpath('//div[@class="pageNum active"]/text()').extract()
        if next_page:
            next_page = int(next_page[0]) + 1
            params = {
                "compId": "portalResNews_list-15706208352073504",
                "currentPage": str(next_page),
                "pageSize": "15",
                "cid": "39"
            }
            yield scrapy.FormRequest(url=f"http://www.nt2191.com/comp/portalResNews/list.do", formdata=params, callback=self.parse, method='POST')

    def detail(self, response: HtmlResponse):
        save = response.meta['save']
        img = response.xpath('.//div[@class="newsarticles"]//img/@src').extract()
        content = response.xpath('.//div[@class="newsarticles"]//text()').extract()
        if img:
            save['img_link'] = 'http://www.nt2191.com' + response.xpath('.//div[@class="newsarticles"]//img/@src').extract()[0]
        if content:
            save['mainbody'] = '\n'.join(content)
        mainbody_table = response.xpath('//table').extract()
        save['mainbody_table'] = mainbody_table if mainbody_table else []
        yield save
