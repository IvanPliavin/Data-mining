# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_url(url):
    if url:
        url = url.replace('w_82,h_82', 'w_2000,h_2000')
    return url

def process_params(params):
    if params:
        params = params.replace(' ', '').replace('\n', '')
    return params

class LmparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_url))
    price = scrapy.Field()
    url = scrapy.Field()
    params = scrapy.Field(input_processor=MapCompose(process_params))
    _id = scrapy.Field()