import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement7(ProcurementBaseSpider):
    name = "procurement7"
    base_link = ''
    hospital_name = '苏州大学附属儿童医院'
    def start_requests(self):
        # 初始页
        urls = []
        for i in range(110):
            list_url = 'http://www.sdfey.cn/zhao-biao.html?page={}'.format(i + 1)
            urls.append(list_url)
        params = {
            # "hospital": "1010",
            # "category": "32",
            # "tag": "",
            # "size": "8",
            # "pageNum": "1",
            # "type": "0",
            # "status": "1",
            # "_": f'{int(time.time())}'
        }
        self.hospital_url = 'http://www.sdfey.cn/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//li[@class='wow animated fadeInUp']/a/@href")

        for each in context:
            article_url = self.hospital_url + each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//div[@class='single-top']/h3/text()").extract()[0]
        ori_url = response.url
        release_index = response.xpath("//div[@class='single-top']/p/text()").extract()[0].index('2')
        release_date = response.xpath("//div[@class='single-top']/p/text()").extract()[0]
        release_date = release_date[release_index:release_index+11]
        mainbody = response.xpath("//div[@class='con']").extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        # annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        # annex_title = response.xpath('//a[@class="ke-insertfile"]/span/text()')
        item = self.save
        mainbody_table = response.xpath('//table').extract()
        item['mainbody_table'] = mainbody_table if mainbody_table else []
        item['annex_link'] = ''
        item['annex_title'] = ''
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
