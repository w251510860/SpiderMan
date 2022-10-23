import json
import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Jiangsuziyuanjiaoyizhongxin(ProcurementBaseSpider):
    name = "Jiangsuziyuanjiaoyizhongxin"
    base_link = ''
    hospital_name = '江苏资源交易中心'

    def start_requests(self):
        # 初始页
        urls = 'http://jsggzy.jszwfw.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
        keywords = ['医院', '卫生院', '保健']
        pages = [6847, 3005, 745]
        params = {"token": "", "pn": 0, "rn": 10, "sdt": "", "edt": "",
                  "wd": "医院",
                  "inc_wd": "", "exc_wd": "", "fields": "title;content", "cnum": "", "sort": "{\"infodatepx\":\"0\"}",
                  "ssort": "title", "cl": 500, "terminal": "", "condition": [], "time": None,
                  "highlights": "title;content", "statistics": None, "unionCondition": None, "accuracy": "",
                  "noParticiple": "0", "searchRange": None}
        self.hospital_url = 'http://jsggzy.jszwfw.gov.cn/'
        # 遍历、翻页
        for index, keyword in enumerate(keywords):
            for i in range(pages[index]):
                params['pn'] = i * 10
                params['wd'] = keyword
                j = json.dumps(params)
                yield scrapy.FormRequest(url=urls, body=j, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()

        for each in context['result']['records']:
            if each['categorynum'][0:6] == '003010':
                article_url = self.hospital_url+'ypcghtml'+each['linkurl']
            else:
                article_url = self.hospital_url + each['linkurl']

            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//h2[@class='ewb-trade-h']/text() | //div[@class='article-info']/h1/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath("//div[@class='ewb-trade-info']/text() | //span[@style='font-size:14px;font-weight:bold;color:black;']/text()").extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath("//div[@class='ewb-trade-mid']").extract()[0]
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
        mainbody_table = response.xpath('//table').extract()
        item['content'] = response.text
        item['mainbody_table'] = mainbody_table if mainbody_table else []
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
