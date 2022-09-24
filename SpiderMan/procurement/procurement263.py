import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement1(ProcurementBaseSpider):
    name = "Procurement_263"
    base_link = ''
    hospital_name = '涟水县人民医院'

    def start_requests(self):
        # 初始页
        url = 'http://lsrmyy.com.cn/ywgk/ywgk.aspx'
        params = {
            "__VIEWSTATE": "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",
            "__EVENTTARGET": "AspNetPager1",
            "__EVENTARGUMENT": "1",
            "belongId": ""
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        self.hospital_url = 'http://lsrmyy.com.cn/ywgk/'
        # 遍历、翻页
        for index in range(17):
            print("第{}页".format(index + 1))
            params['__EVENTARGUMENT'] = "{}".format(index+1)
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse,headers=headers)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//p[@class='b1']/a/@href")

        for each in context:
            article_url = self.hospital_url+each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@class="detail"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="detail-1"]/p[2]/text()').extract()[0]
        release_date = release_date.split(":")[1][0:10]
        mainbody = response.xpath('//div[@class="in_bg"]').extract()[0]
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
