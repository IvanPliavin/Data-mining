import scrapy
from scrapy.http import HtmlResponse
from jobscraper.jobscraper.items import JobscraperItem
from urllib.parse import urlparse

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets='
                  'true&salary=&st=searchVacancy&text=Data+scientist&from=suggest_post']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath('//h1//text()').extract_first()
        vacancy_salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').extract()
        vacancy_employer = response.xpath('//span[@class="bloko-section-header-2 '
                                          'bloko-section-header-2_lite"]/text()').extract()
        vacancy_link = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        source_name = urlparse(vacancy_link).netloc
        yield JobscraperItem(source_name=source_name,
                             vacancy_name=vacancy_name,
                             vacancy_salary=vacancy_salary,
                             vacancy_link=vacancy_link,
                             vacancy_employer=vacancy_employer)


