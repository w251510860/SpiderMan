import scrapy
from scrapy.http.response.html import HtmlResponse

from .ResumeBaseSpider import ResumeBaseSpider


class Resume1786(ResumeBaseSpider):
    name = "Resume1786"
    base_link = ''

    def start_requests(self):
        # 初始页
        urls = [
            'http://tyj.lishui.gov.cn/col/col1229229467/index.html',
            'http://tyj.lishui.gov.cn/col/col1229229462/index.html',
            'http://tyj.lishui.gov.cn/col/col1229229460/index.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': 0})

    def parse(self, response: HtmlResponse):
        # 解析列表页
        save = {}
        save['ori_url'] = response.url
        save['tag'] = "浙江省_丽水市_市体育局"
        save['name'] = response.xpath('//a[@class="bt_link"]/text()').extract()[3].split(' ')[0]
        save['status'] = response.xpath('//a[@class="bt_link"]/text()').extract()[3].split(' ')[1]
        save['img_link'] = 'http://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web3712/site' + response.xpath("//p//img/@src").extract()[0]
        print(save)
        yield save