from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LMparser.spiders.LM import LmSpider
from LMparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider, query='ламинат')

    process.start()