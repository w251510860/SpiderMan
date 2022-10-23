from os import getenv
from dotenv import load_dotenv

load_dotenv()

# 基础配置
BOT_NAME = 'SpiderMan'
SPIDER_MODULES = ['SpiderMan.medical', 'SpiderMan.resume', 'SpiderMan.procurement']
NEWSPIDER_MODULE = 'SpiderMan.procurement'

# 本地开发使用local, 生产环境使用prod
ENVIRONMENT = getenv('ENVIRONMENT')

# 遵守Robot协议
ROBOTSTXT_OBEY = False

# 请求失败后,最大重试次数
CONCURRENT_REQUESTS = 3

# 默认请求头
DEFAULT_REQUEST_HEADERS = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# 管道
ITEM_PIPELINES = {'SpiderMan.pipeline.pipelines.SaveMongoPipeline': 100} \
    if ENVIRONMENT == 'prod' else {'SpiderMan.pipeline.pipelines.TestPipeline': 200}

# 日志等级
LOG_LEVEL: str = getenv("LOG_LEVEL", 'WARNING')

# 数据库配置
MONGO_HOST: str = getenv('MONGO_HOST', '127.0.0.1')
MONGO_PORT: str = getenv('MONGO_PORT', 27017)
MONGO_DB: str = getenv('MONGO_DB', 'Spider')
MONGO_COLL: str = getenv('MONGO_COLL', 'treasure')
MONGO_USER: str = getenv('MONGO_USER', 'admin')
MONGO_PSW: str = getenv('MONGO_PSW', '123456')

# 下载间隔
DOWNLOAD_DELAY = 0.2

# 命令行启动多个爬虫
# todo: 暂时不可用,待修复
# COMMANDS_MODULE = 'SpiderMan.commands'


# DOWNLOAD_FAIL_ON_DATALOSS = False


# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False



# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'crawlers.middlewares.CrawlersSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'crawlers.middlewares.CrawlersDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
