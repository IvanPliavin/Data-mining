# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    parse_user = scrapy.Field()
    user_id = scrapy.Field()
    insta_id = scrapy.Field()
    insta_name = scrapy.Field()
    photo = scrapy.Field()
    status = scrapy.Field()
    insta_url = scrapy.Field()
    _id = scrapy.Field()
    #user_data = scrapy.Field()
    pass
