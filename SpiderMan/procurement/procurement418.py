import re
import time

import scrapy
from scrapy.http.response.html import HtmlResponse

from lxml import etree

from procurement.Base import ProcurementBaseSpider


class Procurement418(ProcurementBaseSpider):
    name = "procurement418"
    base_link = ''
    data = {
        "t_": "0.29215714086261735",
        "window_": "json",
        "start": "1",
        "limit": "25",
        "filter": "",
        "sort": "begin_time desc",
        "type": "FBGG",
        "isEnd": "",
        "catalog": "",
        "categoryId": "",
        "notShopType": "ZGBA",
        "request_method_": "ajax",
        "browser_": "notmsie",
        "page": "cms.psms.publish.query"
    }
    data_1 = {
        "t_": "0.5080822286300299",
        "window_": "json",
        "start": "1",
        "limit": "25",
        "filter": "",
        "sort": "begin_time desc",
        "type": "ZCGG",
        "isEnd": "",
        "catalog": "",
        "categoryId": "",
        "notShopType": "ZGBA",
        "request_method_": "ajax",
        "browser_": "notmsie",
        "page": "cms.psms.publish.query"
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ztbxt.njzdyy.com:3345",
        "Referer": "https://ztbxt.njzdyy.com:3345/sfw_cms/e?page=cms.psms.gglist&type=xq",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\""
    }
    cookies = {
        "JSESSIONID": "E47E8C0F21F8D8D4F685D4446D203393"
    }

    def start_requests(self):
        # 初始页
        urls = [
            ('https://ztbxt.njzdyy.com:3345/sfw_cms/e', self.data),
            ('https://ztbxt.njzdyy.com:3345/sfw_cms/e', self.data_1),
        ]

        for url, data in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse, formdata=data, method='POST',
                                     meta={"start": 1, "url": url, "data": data}, headers=self.headers, cookies=self.cookies)

    def parse(self, response: HtmlResponse):
        # 解析列表页
        # 测试请求是否成功
        datas = response.json()["resultset"]
        for data in datas:
            save = {}
            save["hospital_name"] = "东南大学附属中大医院"
            save["title"] = data["subject"]
            save["ori_url"] = "https://ztbxt.njzdyy.com:3345/provider/#/publish/" + data["syncId"]
            save["release_date"] = data["syncTime"]
            if data["contentHtml"]:
                content = etree.HTML(data["contentHtml"])
                save['mainbody'] = '\n'.join(content.xpath("//text()"))
            print(save)
            yield save
        start = response.meta['start']
        if start >= int(response.json()["count"]):
            return None
        data = response.meta['data']
        data["start"] = str(start + 25)
        yield scrapy.FormRequest(url=response.meta['url'], callback=self.parse, formdata=self.data, method='POST',
                                 meta={"start": start + 25, "url": response.meta['url'], "data": self.data},
                                 headers=self.headers, cookies=self.cookies)