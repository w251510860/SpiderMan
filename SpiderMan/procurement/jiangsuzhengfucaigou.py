import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider
from lxml import etree

class Jiangsuzhengfucaigou(ProcurementBaseSpider):
    name = "Jiangsuzhengfucaigou"
    base_link = ''
    hospital_name = '江苏政府采购'
    def start_requests(self):
        # 初始页
        urls = []
        keywords = ['医院', '卫生院', '保健']
        pages = [500, 50, 34]
        cookies = {
            'JSESSIONID': 'E2A4244771F087393EA10E5A3F0C7ECE'
        }
        for index, page in enumerate(pages):
            keyword = keywords[index]
            for j in range(page):
                list_url = 'http://search.changzhou.gov.cn/index.php?c=index&a=search&keyword={}&referer=&range=2&edit=0&lanmu=0&sitename=zfcg&sort=3&time=0&page={}&contype=0'.format(keyword, j + 1)
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
        self.hospital_url = 'http://zfcg.changzhou.gov.cn/'

        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        j = response.json()['result_html']
        parser = etree.HTMLParser(encoding="utf-8")
        html = etree.HTML(text=j, parser=parser)
        context = html.xpath('//div[@class="tit"]/a/@href')
        for each in context:
            article_url = each
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath('//td[@class="news_tit"]/text()').extract()[0]
        ori_url = response.url
        release_date = response.xpath('//td[@style="border-top:1px solid #CCC; font-size:13px;height: 30px;line-height: 30px;"]/text()[1]').extract()[0]
        release_date = release_date.split("：")[1][0:10]
        mainbody = response.xpath("//table[@style='margin-top:30px;']").extract()[0]
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
