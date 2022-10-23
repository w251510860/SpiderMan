import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement8(ProcurementBaseSpider):
    name = "procurement8"
    base_link = ''
    hospital_name = '苏州市中医医院'

    def start_requests(self):
        # 初始页
        urls = []
        for i in range(19):
            list_url = 'http://zyy.project.weijin365.com/front/selNewsByCategoryName?name=%E6%8B%9B%E6%A0%87%E4%BF%A1' \
                       '%E6%81%AF&limit=10&page={}'.format(i + 1)
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
        self.hospital_url = 'http://fyy.sdfyy.cn/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()['data']

        for each in context:
            article_url = "http://zyy.project.weijin365.com/front/selNewsByTitle?id={}".format(each["id"])
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        res = response.json()['data']
        title = res['title']
        ori_url = response.url
        release_date = res['createTime']
        mainbody = res['content']
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        # annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        # annex_title = response.xpath('//a[@class="ke-insertfile"]/span/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        # if (len(annex_url) != 0) and (len(annex_title) != 0):
        #     annex_link = self.hospital_url + response.xpath('//a[@class="ke-insertfile"]/@href').extract()[0]
        #     item['annex_link'] = annex_link
        #     item['annex_title'] = annex_title.extract()[0]
        item['content'] = response.text
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
