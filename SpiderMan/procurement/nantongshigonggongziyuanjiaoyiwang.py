import json
import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Nantongshigonggongziyuanjiaoyiwang(ProcurementBaseSpider):
    name = "Nantongshigonggongziyuanjiaoyiwang"
    base_link = ''
    hospital_name = '南通市政府采购网'

    def start_requests(self):
        # 初始页
        urls = 'http://zfcg.nantong.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
        keywords = ['医院', '卫生院', '保健']
        pages = [400, 100, 50]
        print(urls)
        params = {"token": "", "pn": 0, "rn": 20, "sdt": "", "edt": "", "wd": "医院", "inc_wd": "", "exc_wd": "",
                  "fields": "title;content", "cnum": "001", "sort": "{\"webdate\":\"0\"}", "ssort": "title", "cl": 500,
                  "terminal": "", "condition": [], "time": None, "highlights": "title;content", "statistics": None,
                  "unionCondition": None, "accuracy": "", "noParticiple": "0", "searchRange": None}
        self.hospital_url = 'http://zfcg.nantong.gov.cn/'

        # 遍历、翻页
        for index, page in enumerate(pages):
            params['wd'] = keywords[index]
            for j in range(page):
                params['pn'] = j * params['rn']
                print("关键词：{}，第{}页".format(params['wd'], params['pn']/20 + 1))
                yield scrapy.FormRequest(url=urls, body=json.dumps(params), callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()['result']['records']
        for each in context:
            article_url = self.hospital_url + each['linkurl']
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@class="article-info"]/h1/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//p[@class="info-sources"]/span/text()').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath('//div[@class="ewb-trade-mid"]').extract()[0]
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
