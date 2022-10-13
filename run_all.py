import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tqdm import tqdm
import random

settings = get_project_settings()
crawler = CrawlerProcess(settings)


def run():
    """
    分批次运行所有爬虫，每次运行三个爬虫，间隔10min
    :return:
    """
    names = get_all_spider()
    random.shuffle(names)
    for _ in tqdm(range(1, len(names) // 3)):
        for index in range(len(names))[::3]:
            start(names[index: index + 3])
            time.sleep(60 * 10)


def start(spider_names):
    for spider_name in spider_names:
        print(f'\n{spider_name} start')
        crawler.crawl(spider_name)
    crawler.start()


def get_all_spider():
    """
    获取所有爬虫名称
    :return:
    """
    spider_names = []
    for spider_name in crawler.spiders.list():
        no_work_module = ['example', 'resume', 'yy', 'base']
        state = 1
        for module in no_work_module:
            if module in spider_name.lower():
                state = 0
        if state == 1:
            spider_names.append(spider_name)
    return spider_names


if __name__ == '__main__':
    run()
