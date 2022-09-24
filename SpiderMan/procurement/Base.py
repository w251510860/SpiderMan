import scrapy
from fake_useragent import UserAgent
import arrow


class ProcurementBaseSpider(scrapy.Spider):
    name = 'ProcurementBaseSpider'
    headers = {'User-Agent': UserAgent().random}
    count = 0
    save = {
        "crawl_time": arrow.now(),
        "hospital_name": "",  # 医院名称
        "title": "",  # 标题
        "ori_url": "",  # 源文连接
        "release_date": "",  # 发布时间
        "annex_link": "",  # 附件链接（正文包含附件时）
        "annex_title": "",  # 附件标题（正文包含附件时）
        "img_link": "",  # 图片链接（正文是一张图片时）
        "img_title": "",  # 图片标题（正文是一张图片时）
        "mainbody": "",  # 内容主题（正文时文本时）
        "mainbody_table": "",  # 内容标题（正文时文本时）
        "others": ""  #
    }
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderMan.pipeline.procurement_pipeline.ProcurementSaveMongoPipeline': 200}
    }