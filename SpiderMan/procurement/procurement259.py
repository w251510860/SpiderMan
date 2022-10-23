import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement1(ProcurementBaseSpider):
    name = "Procurement259"
    base_link = ''
    hospital_name = '淮安市第一人民医院'

    def start_requests(self):
        # 初始页
        url = 'https://www.hasyy.cn/content/getPage'
        params = {
            "page": "1",
            "pageSize": "10",
            "menuId": "38",
            "belongId": ""
        }
        self.hospital_url = 'https://www.hasyy.cn/'
        # 遍历、翻页
        for index in range(172):
            params['page'] = "{}".format(index+1)
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()['contentList']

        for each in context:
            article_url = "https://www.hasyy.cn/content/contentDetail?contentId={}&menuId=38".format(each['contentId'])
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@class="smallTitle"]/b/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="smallTitle"]/div').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath('//div[@class="container"]').extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        annex_url = response.xpath('//div[@class="col-md-12"]//img/@src')
        # annex_title = response.xpath('//a[@class="ke-insertfile"]/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        if len(annex_url) != 0:
            item['annex_link'] = annex_url
            item['annex_title'] = "公告图片"
        mainbody_table = response.xpath('//table').extract()
        item['mainbody_table'] = mainbody_table if mainbody_table else []
        item['content'] = response.text
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
