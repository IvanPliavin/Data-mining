from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobscraper.jobscraper import settings
from jobscraper.jobscraper.spiders.sjru import SjruSpider
from jobscraper.jobscraper.spiders.hhru import HhruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()