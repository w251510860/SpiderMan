import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement54(ProcurementBaseSpider):
    name = "procurement54"
    base_link = ''
    hospital_name = '太仓市中医医院'

    def start_requests(self):
        # 初始页
        url = "http://www.tczyy.com/newslist.aspx?type=gggs"
        params = {
            "__EVENTTARGET": "lbnNextPage",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": "",
            "__EVENTVALIDATION": "epTsqaQC53tZBumfS6k3Z8Ue6NPiqLDnddcLLzlMXbnaVGdHLn8grMuDbly0uySqPCZXl59Z0sIjOAmVx6LAtfiWVZKFv8DvXOQJ6tygYk3mofM0LerGiOXgg8FpzigR7Fn6J6zWty15yc4Zggx6gCaMXqkTn6g7s2ItEWKAvb9EMbBWyIK4y5bmXkvZCgnL1WkLFw3gRJm4/SDAEu/LT5lA7rsQA7NTbfSukrEswvD3IFFf5kf0NuyBO4prswtAklDthc7/jdIYnDvDTzQOWQhqp8jbj3s0ZqZrjkU8NySM2dPPHDQW6yCTRkJYrwTtLVLnvA/STU1QodC6xq2xDvmAjhVN5ysYudcXN2eWeVQjOmUU16nuHmqBTJE+VcNeN0TJ7B00odQaeMYI3k8A2ORv/GjesIdHvpNy4yy/RM1zOMzV4b7/M/hbWIRRz/eRPvunOF7lz9fKajWP/GzmIv0nmv+CZxl9H0fDhNx6ZdIgIUeYIqbW1qiZISrFHh5nmSPFRw==",
            "Ddl_PageNumber": "1"
        }
        cookie = {
            "ASP.NET_SessionId": "2v0tn4gndjbtyxwhmamso4ij"
        }
        self.hospital_url = 'http://www.tczyy.com/'
        # 遍历、翻页
        for i in range(1):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, cookies=cookie)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//td[@width='590']/a/@href")

        for i in range(915):
            article_url = "http://www.tczyy.com/news.aspx?id={}".format(915-i)
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//span[@id="lbltitle"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//span[@id="lbltime"]/text()').extract()[0]
        mainbody = response.xpath('//form[@id="form1"]').extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        # annex_url = response.xpath('//a[@class="ke-insertfile"]/@href')
        # annex_title = response.xpath('//a[@class="ke-insertfile"]/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
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
