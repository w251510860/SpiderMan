import json

import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY18(BaseSpider):
    name = "YY18"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://ybj.fujian.gov.cn/was5/web/search?channelid=294271&templet=advsch.jsp&sortfield=-docorderpri%2C-docreltime&classsql=chnlid%3D35207&prepage=150&page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = json.loads(response.text.replace('\n', '').replace('\r', '').replace(' ', ''))

        if datas['docs'][0]['title'] == '文章标题':
            return

        # 解析列表页
        for data in datas['docs']:
            if data['title'] == '文章标题':
                continue
            self.count += 1
            print(self.count)
            save = {}
            save['title'] = data['title']
            save['release_date'] = data['pubtime']
            save['mainbody'] = data['content']
            save['mainbody_table'] = data['title']
            save['annex_link'] = f'http://ybj.fujian.gov.cn/ztzl/yxcg/ggtz/{data["file"]}'
            save['annex_title'] = data['filedesc']
            save['tag'] = int(self.name.replace('YY', ''))
            save['ori_url'] = data['url']
            yield save
        next_page = response.meta['page'] + 1
        yield scrapy.Request(
            url=f'http://ybj.fujian.gov.cn/was5/web/search?channelid=294271&templet=advsch.jsp&sortfield=-docorderpri%2C-docreltime&classsql=chnlid%3D35207&prepage=150&page={next_page}',
            callback=self.parse, meta={'page': next_page})
