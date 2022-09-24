import scrapy
from fake_useragent import UserAgent
import arrow


class ResumeBaseSpider(scrapy.Spider):
    name = 'ResumeBaseSpider'
    headers = {'User-Agent': UserAgent().random}
    count = 0
    save = {
        "crawl_time": "",
        "tag": "",
        "status": "",
        "ori_url": "",
        "name": "",
        "title": "领导简介",
        "resume": "",
        "division": "",
        "annex_link": "",
        "annex_title": "",
        "img_link": "",
        "others": ""
    }
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderMan.pipeline.resume_pipeline.ResumeSaveMongoPipeline': 200}
    }
    
    # @staticmethod
    # def save_html(content):
    #     with open('test.html', 'w') as f:
    #         f.write(content)
    #
    # @staticmethod
    # def get_html():
    #     with open('test.html', 'r') as f:
    #         return f.read()


    # def parse(self, response):
    #     pass
