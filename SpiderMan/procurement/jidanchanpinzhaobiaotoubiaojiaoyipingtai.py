import json
import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider
from lxml import etree

class Jidanchanpinzhaobiaotoubiaojiaoyipingtai(ProcurementBaseSpider):
    name = "Jidanchanpinzhaobiaotoubiaojiaoyipingtai"
    base_link = ''
    hospital_name = '机电产品招标投标交易平台'

    def start_requests(self):
        # 初始页
        urls = 'https://www.chinabidding.com/search/proj.htm'
        keywords = ['医院', '卫生院', '保健院']
        pages = [100, 100, 100]
        params = {
            'fullText': '医院',
            'infoClassCodes': '0105',
            'poClass': 'BidNotice',
            'currentPage': '1'
        }
        self.hospital_url = 'https://www.chinabidding.com/'

        # 遍历、翻页
        for index, url in enumerate(keywords):
            params['fullText'] = keywords[index]
            for i in range(pages[index]):
                params['currentPage'] = '{}'.format(i+1)
                yield scrapy.FormRequest(url=urls, body=json.dumps(params), callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath('//a[@class="as-pager-item"]/@href')
        for each in context:
            article_url = each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        # with open("index.html",'wb+') as f:
        #     f.write(response.body)
        #     f.close()
        title = response.xpath("//active[@class='title']/h1/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath("//active[@class='title']/em/text()").extract()[0]
        release_date = release_date.split(" ")[0][0:10]
        mainbody = response.xpath("//section[@class='text']").extract()[0]
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
