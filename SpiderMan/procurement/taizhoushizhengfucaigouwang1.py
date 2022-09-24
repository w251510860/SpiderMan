import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Taizhoushizhengfucaigouwang1(ProcurementBaseSpider):
    name = "Taizhoushizhengfucaigouwang_1"
    base_link = ''
    hospital_name = '泰州市政府采购网'

    def start_requests(self):
        # 初始页
        urls = []
        keywords = ['医院', '卫生院', '保健']
        pages = [58, 6, 3]
        for index, page in enumerate(pages):
            keyword = keywords[index]
            for j in range(page):
                list_url = 'http://czj.taizhou.gov.cn/module/sitesearch/index.jsp?keyword=vc_title&columnid=0&keyvalue={}&webid=69&modalunitid=95103&currpage={}'.format(keyword, j + 1)
                urls.append(list_url)
        print(urls)
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
        self.hospital_url = 'http://czj.taizhou.gov.cn/'

        # 遍历、翻页
        for index, url in enumerate(urls):
            print("第{}页".format(index + 1))
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath('//a[@style="font-size:14px;color:#0066cc; text-decoration:none;line-height:18px;"]/@href')

        for each in context:
            article_url = each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//td[@align="center"]/text()[1]').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//table[@width="700"]/tr/td[2]').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath('//div[@id="container"]').extract()[0]
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
