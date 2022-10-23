import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement1(ProcurementBaseSpider):
    name = "Procurement431"
    base_link = ''
    hospital_name = '南京市胸科医院'

    def start_requests(self):
        # 初始页
        urls = 'http://www.njxkyy.net/ztb/ztb.asp'
        params = {
            "idCurrentPage": "",
            "idCommand":"10820",
            "idCurPageNum":"1",
            "idTypCod":"",
            "idInfCod":"",
            "idCurPage":""
        }
        self.hospital_url = 'http://www.njxkyy.net/'
        # 遍历、翻页
        for i in range(3):
            params["idCurPageNum"] = "{}".format(i+1)
            yield scrapy.FormRequest(url=urls, formdata=params, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath('//tr[@align="center"]/td/a/@href')

        for each in context:
            article_url = self.hospital_url + each.extract().split('..')[1]
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//td[@class='style17']/text()").extract()[0]
        ori_url = response.url
        # release_date = response.xpath("//p[@style='TEXT-ALIGN: center; MARGIN: 0pt']/span/font/text()").extract()[0]
        # release_date = release_date.split("：")[3][0:10]
        mainbody = response.xpath('//table[@class="style2"]/tr/td[@class="style15"]').extract()[0]
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
        item['release_date'] = ""
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
