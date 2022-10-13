import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Wuxishirenmingzhengfu2(ProcurementBaseSpider):
    name = "wuxishirenmingzhengfu2"
    base_link = ''
    hospital_name = '无锡市市人民政府_卫生院'

    def start_requests(self):
        # 初始页
        urls = 'https://www.wuxi.gov.cn/search/index.html?siteId=4&siteName=江阴市人民政府'
        params = {
            'searchType': 'fullSearch',
            'kind': '5',
            'keyword': '卫生院',
            'isLocalWebSite': 'true',
            'siteId': '4',
            'queryFilter': '',
            'channel': '市公共资源交易中心',
            'timeCondition': 'unlimitedTime',
            'dateRange': '',
            'page': '1',
            'sortType': 'timeSort'
        }
        self.hospital_url = 'https://www.wuxi.gov.cn/search/'

        # 遍历、翻页
        for i in range(98):
            params['page'] = '{}'.format(i+1)
            yield scrapy.FormRequest(url=urls, formdata=params, callback=self.parse)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath('//div[@class="result "]/a/@href')

        for each in context:
            article_url = self.hospital_url + each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//div[@class='ind36 lw_title']/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath("//span[@class='content-time']/text()").extract()[0]
        release_date = release_date[0:10]
        mainbody = response.xpath("//div[@class='content-body lw_content']").extract()[0]
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
