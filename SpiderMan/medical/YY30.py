import scrapy
from scrapy.http.response.html import HtmlResponse

from .Base import BaseSpider


class YY30(BaseSpider):
    name = "YY30"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'https://ggzyjy.gansu.gov.cn/common/search/8a70f165d09848c990365416ed945480?_isAgg=true&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1',
        ]
        headers = {
            'authority': 'ggzyjy.gansu.gov.cn',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://ggzyjy.gansu.gov.cn/ggzyjy/c112562/list.shtml',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'Hm_lvt_0541817a94969e32507f712ba2e9846d=1648548075; jeeplus.session.id=b891f28d89ab45d782af882f2770d533; Hm_lpvt_0541817a94969e32507f712ba2e9846d=1648563576',
            'if-none-match': 'W/"1fe48-tikzAontG8TvEzF/ScYqOolBRFg"',
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        datas = response.json()['data']['results']

        if not datas:
            return
        # 解析列表页
        for data in datas:
            save = {}
            save['title'] = data['title']
            save['release_date'] = data['publishedTimeStr']
            save['mainbody'] = data['content']
            save['mainbody_table'] = data['title']
            save['annex_link'] = [f"https://ggzyjy.gansu.gov.cn{info['filePath']}" for info in data['resList']]
            save['annex_title'] = [info['title'] for info in data['resList']]
            save['tag'] = int(self.name.replace('YY', ''))
            save['ori_url'] = 'https://ggzyjy.gansu.gov.cn' + data['url']
            yield save
        next_page = response.meta['page'] + 1
        yield scrapy.Request(url=f'https://ggzyjy.gansu.gov.cn/common/search/8a70f165d09848c990365416ed945480?_isAgg=true&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={next_page}',
                             callback=self.parse, meta={'page': next_page})
