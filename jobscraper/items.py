# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscraperItem(scrapy.Item):
    # define the fields for your item here like:
    vacancy_name = scrapy.Field()
    vacancy_salary = scrapy.Field()
    vacancy_employer = scrapy.Field()
    vacancy_link = scrapy.Field()
    source_name = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency = scrapy.Field()
    _id = scrapy.Field()
    pass
