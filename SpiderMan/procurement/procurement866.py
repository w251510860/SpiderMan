import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement1(ProcurementBaseSpider):
    name = "Procurement866"
    base_link = ''
    hospital_name = '丹阳市妇幼保健院'

    def start_requests(self):
        # 初始页
        urls = []
        for i in range(7):
            list_url = 'http://www.dysfybjy.com/index.php?_m=article_list&_a=get_page&article_category=&layer_id=layer092694226DE6CF074DB90424D8548B9C&page={}&article_category_more=92'.format(i + 1)
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
        self.hospital_url = 'http://www.dysfybjy.com/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//a[@class='articleid  memberoff']/@href")

        for each in context:
            article_url = each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//div[@class="artdetail_title"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//span[@class="detail_head_title pub_txt_span"]/text()').extract()[0]
        # release_date = release_date.split("：")[3][0:10]
        mainbody = response.xpath('//div[@class="wp-article_detail_content"]').extract()[0]
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
