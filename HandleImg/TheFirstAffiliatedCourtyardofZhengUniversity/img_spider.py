import json
import random
import datetime
import time
import requests
from lxml import etree
# from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Screenshot import Screenshot
import os

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
}
cookies = {
    ".AspNetCore.Antiforgery.v7RqO6G7mpk": "CfDJ8Irqz2GeS1VHkuGnAUMNAca92QD_Ju0GiLJgHEPq044kibUOnOxy5xgSCQxJKNvZikbn4eqMngAfegEGAJUIq8_VLrrbA4fSeMaz3gw31d30tcLe4qRaGQ8xX1XyQ0gxizWK2V8FkmAeA0PO8iD8-EQ",
    "SECKEY_ABVK": "N8hgzbPwiV00cGE7GDd2yzBQxHDezRAjb2IiU93l0nU%3D",
    "BMAP_SECKEY": "N8hgzbPwiV00cGE7GDd2y5WOFawpWjkt7ysFAExhvQfsEv739809cFHy3t2KEeoQpnLlnkjbyBNc2bTNixb0QCkhr6CmT5uFTcMR7SbbKRbHBi0RDwxg7xkF6wouNFMMMro6vAJI58nhRR7o1HRQ9zynHI2YqSCZkHVyS-4k0dzMN0g1M2Nh0ubSRc_mttDz",
    "Power_SiteUniqueVisitorKey": "%2F1%2F"
}
# 1> 获取chrome参数对象
chrome_options = Options()
# 2> 添加无头参数r,一定要使用无头模式，不然截不了全页面，只能截到你电脑的高度
# chrome_options.add_argument('--headless')
# 3> 为了解决一些莫名其妙的问题关闭 GPU 计算
chrome_options.add_argument('--disable-gpu')
# 4> 为了解决一些莫名其妙的问题浏览器不动
chrome_options.add_argument('--no-sandbox')
ob = Screenshot.Screenshot()
driver = webdriver.Chrome(executable_path='../../ChromeDriver/chromedriver', chrome_options=chrome_options)

def get_url(url):
    response = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = etree.HTML(response.text)
    datas = response.xpath('//ul[@class="newslist-con2c"]/li')
    saves = []
    for data in datas:
        save = dict()
        save["title"] = data.xpath('.//div[@class="newslist-con2c2"]/span/text()')[0]
        save["ori_url"] = "https://www.zdyfy.com" + data.xpath("./a/@href")[0]
        saves.append(save)
    next_page = response.xpath("//a[contains(text(), '下一页')]/@href")
    if next_page and 'java' not in next_page[0]:
        next_url = f"https://www.zdyfy.com{next_page[0]}"
    else:
        next_url = None
    return saves, next_url


def run():
    count = 0
    url = "https://www.zdyfy.com/zbcg_1"
    datas = []
    while url:
        count += 1
        saves, url = get_url(url)
        print(url)
        datas.extend(saves)
        if count % 30 == 0:
            st = random.random() * 10 + 10
            print(f'休息{st}s')
            print(datetime.datetime.now())
            time.sleep(st)
            print('开始')
            print(datetime.datetime.now())
    with open("./datasests/menu.json", 'a') as f:
        f.write(json.dumps(datas))


def run1():
    with open("./datasests/menu.json", 'r') as f:
        data = f.read()
        datas = json.loads(data)
    for content in datas[250:]:
        ret = False
        while not ret:
            try:
                ret = screenshot(content['ori_url'], content['title'])
            except Exception as f:
                time.sleep(30)
        time.sleep(1)

def screenshot(url, title):
    driver.get(url)
    driver.maximize_window()
    # driver.execute_script("document.body.style.zoom='0.5'")
    # time.sleep(5)
    title = title.replace('.', '')
    img_url = ob.full_Screenshot(driver, save_path=f"./screenshots/", image_name=f'{title}.png', load_wait_time=10, multi_images=True)
    print(img_url)
    print(f'url -> {url} title -> {title}')
    return True


if __name__ == '__main__':
    run1()

# class zzu(ProcurementBaseSpider):
#     name = "zzu"
#     count = 0
#     repeat_count = 0
#     base_urls = [
#         'https://www.zdyfy.com/zbcg_41',
#     ]
#
#     def start_requests(self):
#         self.driver = webdriver.Chrome(executable_path='../../ChromeDriver/chromedriver')
#         # 初始页
#         urls = [
#             'https://www.zdyfy.com/zbcg_41',
#         ]
#         for url in urls:
#             yield scrapy.FormRequest(url=url, callback=self.parse, method='GET')
#
#     def parse(self, response: HtmlResponse):
#         # 测试请求是否成功
#         datas = response.xpath('//ul[@class="newslist-con2c"]/li')
#         if not datas:
#             return
#         for data in datas:
#             save = {}
#             save["hospital_name"] = "郑州大学第一附属医院"
#             save["title"] = data.xpath('.//div[@class="newslist-con2c2"]/span/text()').extract()[0]
#             save["ori_url"] = "https://www.zdyfy.com" + data.xpath("./a/@href").extract()[0]
#             save["release_date"] = data.xpath('./a/span[@class="newslist-con2c1"]/text()').extract()[0].replace("时间：",
#                                                                                                                 "")
#             yield scrapy.FormRequest(url=save["ori_url"], callback=self.detail, method='GET', meta={"save": save})
#         next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract()
#         if next_page:
#             print('休息30s')
#             print(datetime.datetime.now())
#             st = random.random() * 20 + 20
#             time.sleep(st)
#             print('开始')
#             print(datetime.datetime.now())
#
#             yield scrapy.FormRequest(url=f"https://www.zdyfy.com{next_page[0]}", callback=self.parse, method='GET')
#
#     def detail(self, response: HtmlResponse):
#         save = response.meta['save']
#         save['mainbody'] = '\n'.join(response.xpath('//div[@class="news-detail2"]/p//text()').extract())
#         mainbody_table = response.xpath('//table').extract()
#         save['mainbody_table'] = mainbody_table if mainbody_table else []
#         save['content'] = response.text
#         self.count += 1
#         self.driver.get(response.url)
#         self.driver.maximize_window()
#         self.driver.save_screenshot('../../screenshots/' + save['title'] + '.png')
#         self.driver.quit()
#         yield save
