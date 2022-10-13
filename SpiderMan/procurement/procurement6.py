import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement6(ProcurementBaseSpider):
    name = "procurement6"
    base_link = ''
    hospital_name = '苏州大学附属第二医院'
    def start_requests(self):
        # 初始页
        url = "http://www.sdfey.com/indexAction_initNews.action?menuId=99C4B9FA-61B5-4373-93D3-3C550FD9334A" \
              "&parentMenuId=BED3FE47-FE96-4B4D-BD2A-70F25475E3A4 "
        params = {
            "page.curPage": "",
            "page.sortValue": "",
            "page.hasAscing": "false",
            "page.pageSize": "30"
        }
        self.hospital_url = 'http://www.sdfey.com/'
        # 遍历、翻页
        for i in range(36):
            params["page.curPage"] = "{}".format(i+1)
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath('//div[@class="t"]/a/@href')
        for each in context:
            article_url = self.hospital_url + each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@id="Par_title"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@id="Par_title2"]/text()').extract()[0]
        release_date = release_date[release_date.find("2"):release_date.find("2")+10]
        mainbody = response.xpath('//div[@id="Par_content"]').extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        # annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        # annex_title = response.xpath('//a[@class="ke-insertfile"]/span/text()')
        item = self.save
        # item['annex_link'] = ''
        # item['annex_title'] = ''
        # if (len(annex_url) != 0) and (len(annex_title) != 0):
        #     annex_link = self.hospital_url + response.xpath('//a[@class="ke-insertfile"]/@href').extract()[0]
        #     item['annex_link'] = annex_link
        #     item['annex_title'] = annex_title.extract()[0]
        mainbody_table = response.xpath('//table').extract()
        item['mainbody_table'] = mainbody_table if mainbody_table else []
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
