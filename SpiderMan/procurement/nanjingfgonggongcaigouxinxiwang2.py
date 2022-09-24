import json
import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Nanjinggonggongcaigouxinxiwang2(ProcurementBaseSpider):
    name = "Nanjinggonggongcaigouxinxiwang_2"
    base_link = ''
    hospital_name = '南京公共采购信息网_卫生院'

    def start_requests(self):
        # 初始页
        urls = 'https://njgc.jfh.com/app/search/keywords'
        print(urls)
        params = {
            "keywords": "医院",
            "page": "1",
            "rows": "10"
        }
        self.hospital_url = 'https://njgc.jfh.com'
        pages = 13
        # 遍历、翻页
        for i in range(pages):
            print("第{}页".format(i + 1))
            params['page'] = i+1
            j = json.dumps(params)
            yield scrapy.FormRequest(url=urls, body=j, headers={'Content-Type': 'application/json'}, callback=self.parse, method='POST')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()['data']['records']

        for each in context:
            article_url = self.hospital_url + each['detailUrl']
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//h1[@class="middle_content_title"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="middle_content_title_labels_item"]/text()').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath('//div[@class="body"]').extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        annex_title = response.xpath('//a[@class="ke-insertfile"]/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        if (len(annex_url) != 0) and (len(annex_title) != 0):
            annex_link = self.hospital_url + response.xpath('//a[@class="ke-insertfile"]/@href').extract()[0]
            item['annex_link'] = annex_link
            item['annex_title'] = annex_title.extract()[0]
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
