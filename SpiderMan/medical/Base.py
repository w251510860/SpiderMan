import scrapy
from fake_useragent import UserAgent
import arrow


class BaseSpider(scrapy.Spider):
    name = 'BaseSpider'
    headers = {'User-Agent': UserAgent().random}
    count = 0
    save = {
        "crawl_time": arrow.now(),
        "tag": "",  # ?
        "status": "",  # ?
        "title": "",  # 标题
        "ori_url": "",  # 源文连接
        "release_date": "",  # 发布时间
        "annex_link": "",  # 附件链接
        "annex_title": "",  # 附件标题
        "img_link": "",  # 图片链接
        "img_title": "",  # 图片标题
        "mainbody": "",  # 内容主题
        "mainbody_table": "",  # 内容标题
        "mainbody_indexinfo": "",  # ？
        "others": ""  # ？
    }

    def parse(self, response):
        pass
