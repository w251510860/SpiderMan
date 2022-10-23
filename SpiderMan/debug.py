import time

from scrapy.cmdline import execute
import sys
import os


def run(crawler_name):
    """
    单步调试：将crawler_name换成自己的爬虫名称
    :return:
    """
    print(f'爬虫 {crawler_name} 启动 ...')
    start = time.time()
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', crawler_name])
    print(f"运行耗时: {time.time() - start}s")


if __name__ == '__main__':
    run('Huaianshigonggongjiaoyizhongxin')
    # run('JS2')

