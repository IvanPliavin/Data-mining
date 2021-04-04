import scrapy
from scrapy.http import HtmlResponse
from jobscraper.jobscraper.items import JobscraperItem
from urllib.parse import urlparse

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['www.superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Data%20Science&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="jNMYr GPKTZ _1tH7S"]//@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n f-test-button-dalshe'
                                   ' f-test-link-Dalshe"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath('//h1//text()').extract_first()
        vacancy_salary = response.xpath('//span[@class="_3mfro _2Wp8I PlM3e _2JVkc"]//text()').extract()
        vacancy_employer = response.xpath('//h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract_first()
        vacancy_link = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        source_name = urlparse(vacancy_link).netloc
        yield JobscraperItem(source_name=source_name,
                             vacancy_name=vacancy_name,
                             vacancy_salary=vacancy_salary,
                             vacancy_link=vacancy_link,
                             vacancy_employer=vacancy_employer)