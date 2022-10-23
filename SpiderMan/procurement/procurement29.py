import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement29(ProcurementBaseSpider):
    name = "procurement29"
    base_link = ''
    hospital_name = '吴江市第二人民医院'
    def start_requests(self):
        # 初始页
        urls = []
        for i in range(34):
            list_url = "https://www.wjeryuan.com/info.yhtm?id=&twoid=&oneid={7761B9FE-F168-44D3-A54A-CD53658F6FA3}&zid={25C7084A-D9EC-4A2B-80AC-1575CE0536FA}&page="+"{}".format(i+1)
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
        self.hospital_url = 'https://www.wjeryuan.com/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.xpath("//div[@class='content list']/a/@href")

        for each in context:
            article_url = self.hospital_url + each.extract()
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        title = response.xpath("//div[@class='newsInfo']/h3/text()").extract()[0]
        ori_url = response.url
        release_date = response.xpath("//div[@class='source']/ul/li/text()").extract()[0]
        # release_date = release_date.split("：")[3][0:10]
        mainbody = response.xpath("//div[@class='container bodywrap']").extract()[0]
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        annex_url = response.xpath('//span[@class="s1"]/a/@href')
        annex_title = response.xpath('//span[@class="s1"]/a/font/text()')
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        if (len(annex_url) != 0) and (len(annex_title) != 0):
            annex_link = self.hospital_url + annex_url.extract()[0]
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
