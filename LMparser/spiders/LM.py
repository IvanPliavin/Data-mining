import scrapy
from scrapy.http import HtmlResponse
from LMparser.items import LmparserItem
from scrapy.loader import ItemLoader

class LmSpider(scrapy.Spider):
    name = 'LM'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super(LmSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath('//div[contains(@class, "phytpj4_plp")]/a/@href')
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница:')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('params', "//div[@class='def-list__group']/dt/text()" + ' : '
                         + "//div[@class='def-list__group']/dd/text()")
        #loader.add_xpath('values', "//div[@class='def-list__group']/dd/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span/text()")
        yield loader.load_item()

