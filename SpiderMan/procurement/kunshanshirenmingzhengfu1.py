import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement1(ProcurementBaseSpider):
    name = "Kunshanshirenmingzhengfu_1"
    base_link = ''
    hospital_name = '昆山市人民政府'

    def start_requests(self):
        # 初始页
        urls = []
        keywords = '医院'
        for i in range(232):
            list_url = 'http://www.ks.gov.cn/search4/s?searchWord={}&column=%25E5%2585%25A8%25E9%2583%25A8&pageSize=10&pageNum={}&siteCode=3205830040&sonSiteCode=&checkHandle=1&searchSource=1&govWorkBean=%257B%257D&areaSearchFlag=0&secondSearchWords=&topical=&docName=&label=&countKey=0&uc=0&left_right_index=0&searchBoxSettingsIndex=&manualWord={}&orderBy=0&startTime=&endTime=&timeStamp=5&strFileType=&wordPlace=1'.format(keywords, i + 1, keywords)
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
        self.hospital_url = 'http://www.ks.gov.cn/'

        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//div[@class='bigTit clearfix']/a/@href")

        for each in context:
            article_url = each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//h1[@class='article-title']/ucaptitle/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath("//div[@class='layui-input-block']/text()").extract()[2]

        mainbody = response.xpath('//div[@class="article-content article-content-body"]').extract()[0]
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
