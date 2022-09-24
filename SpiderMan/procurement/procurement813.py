import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement813(ProcurementBaseSpider):
    name = "Procurement_813"
    base_link = ''
    hospital_name = '江苏省苏北人民医院'
    def start_requests(self):
        # 初始页
        urls = []
        for i in range(33):
            list_url = 'https://www.yzsbh.com/Html/News/Columns/7/{}.html'.format(i + 1)
            urls.append(list_url)
        print(urls)
        params = {

        }

        self.hospital_url = 'https://www.yzsbh.com/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            print("第{}页".format(index + 1))
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        print("123")
        context = response.xpath("//ul[@class='column_list']/li/a/@href")

        for each in context:
            article_url = self.hospital_url + each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//h1[@class="article_title"]/font/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="sub_tit"]/span[@class="fbsj"]/text()').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath('//div[@id="zoom"]').extract()[0]
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
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
