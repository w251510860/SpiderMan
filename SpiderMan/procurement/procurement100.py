import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement100(ProcurementBaseSpider):
    name = "Procurement_100"
    base_link = ''
    hospital_name = '苏州市相城区阳澄湖镇卫生院'

    def start_requests(self):
        # 初始页
        urls = 'https://czju.suzhou.gov.cn/zfcg/content/searchkey.action'
        print(urls)
        params = {
            'title': '苏州市相城区阳澄湖镇卫生院',
            'page': "1",
            'rows': "30",
        }

        self.hospital_url = 'https://czju.suzhou.gov.cn/'

        # 遍历、翻页
        for index in range(4):
            print("第{}页".format(index + 1))
            params['page'] = '{}'.format(index + 1)
            yield scrapy.FormRequest(url=urls, formdata=params, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()

        for each in context['rows']:
            print(each)
            if 'PROJECTID' in each:
                article_url = 'https://czju.suzhou.gov.cn/zfcg/html/project/{}.shtml'.format(each['PROJECTID'])
                yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                         method='GET')
            else:
                article_url = 'https://czju.suzhou.gov.cn/zfcg/html/content/{}.shtml'.format(each['CP_CONTENT_ID'])
                yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                         method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@class="M_title"][1]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//div[@class="date"][1]/span/text()').extract()[0]
        # release_date = release_date.split("：")[3][0:10]
        mainbody = response.xpath('//div[@class="main"]').extract()[0]
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
