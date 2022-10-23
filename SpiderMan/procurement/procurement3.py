import json
import re
import scrapy
from scrapy.http.response.html import HtmlResponse
from procurement.Base import ProcurementBaseSpider


class Procurement3(ProcurementBaseSpider):
    name = "procurement3"
    base_link = ''
    hospital_name = '苏州市立医院'
    def start_requests(self):
        # 初始页
        # 页数
        page_num = 26
        urls = []
        for i in range(page_num):
            list_url = 'http://smh.cc/api2020/api/news/getNewsInfo?hospital=1010&category=32&tag=&size=8&pageNum={}&type=0&status=1&_=1656661309811'.format(
                i + 1)
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
        self.hospital_url = 'http://smh.cc/'
        # 遍历、翻页
        for index, url in enumerate(urls):
            yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse, method='GET')

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        context = response.json()
        articles = context['data']['list']
        for each in articles:
            article_url = "http://smh.cc/api2020/api/news/getNewsInfo?hospital=1010&id={}&status=1&_=1656667548301".format(
                each['id'])
            yield scrapy.FormRequest(url=article_url, callback=self.articleparse,
                                     method='GET')

    def articleparse(self, response: HtmlResponse):
        article_context = response.json()['data']['list'][0]
        title = article_context['title']
        ori_url = response.url
        release_date = article_context['time']
        mainbody = article_context['html']
        mainbody = re.sub('<[^<]+?>', '', mainbody).replace('\n', '').strip()
        item = self.save
        item['annex_link'] = ''
        item['annex_title'] = ''
        if article_context.__contains__('fileUrl'):
            fileUrl = article_context['fileUrl']
            if len(fileUrl) != 0:
                try:
                    item['annex_link'] = json.loads(json.loads(fileUrl))['url']
                    item['annex_title'] = json.loads(json.loads(fileUrl))['name']
                except:
                    print(f'procurement3 error {fileUrl}')
        item['content'] = response.text
        item['title'] = title
        item['ori_url'] = ori_url
        item['release_date'] = release_date
        item['mainbody'] = mainbody
        item['col'] = self.name
        item['hospital_name'] = self.hospital_name
        return item
