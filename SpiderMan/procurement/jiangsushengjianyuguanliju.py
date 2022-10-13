import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider
from lxml import etree

class Jiangsushengjianyuguanliju(ProcurementBaseSpider):
    name = "Jiangsushengjianyuguanliju"
    base_link = ''
    hospital_name = '江苏省监狱管理局'

    def start_requests(self):
        # 初始页
        urls = []
        keywords = ['医院', '卫生院', '保健']
        pages = [21, 0, 0]
        for index, page in enumerate(pages):
            keyword = keywords[index]
            for j in range(page):
                list_url = 'http://jssjyglj.jiangsu.gov.cn/module/xxgk/search.jsp?texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title={}&vc_number=&currpage={}&sortfield=&fields=&fieldConfigId=&hasNoPages=&infoCount='.format(keyword, j + 1)
                urls.append(list_url)
        params = {
            'infotypeId': '06',
            'jdid': '52',
            'area': '014000108',
            'divid': 'div49342'
        }
        self.hospital_url = 'http://zfcg.changzhou.gov.cn/'

        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//table[@style='margin-top: 10px;']/tbody/tr/td[2]/a/@href")
        for i, each in enumerate(context):
            if i < 10:
                article_url = each.extract()
                yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                         method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//font[@face='宋体']/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath('//td[@class="c2"]/text()').extract()[3]
        mainbody = response.xpath('//table[@style="margin: 0 auto;"]').extract()[0]
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
        item['mainbody_table'] = mainbody_table if mainbody_table else []
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
