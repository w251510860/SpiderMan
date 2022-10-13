from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.cmdline import execute

settings = get_project_settings()

crawler = CrawlerProcess(settings)

crawler.crawl('procurement686')
crawler.crawl('procurement690')

crawler.start()