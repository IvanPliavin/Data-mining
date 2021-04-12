# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import hashlib
from scrapy.utils.python import to_bytes

def list_to_dict(params):
    params_dict = {}
    for i in range(len(params) // 2):
        i *= 2
        params_dict[params[i]] = params[i + 1]
    return params_dict

class LmparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['params'] = list_to_dict(item['params'])
        item['price'] = item['price'][0] + '.' + item['price'][2] + ' ' + item['price'][2]
        collection.incert_one(item)
        return item

class LmphotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        file_dir = item['name'][0]
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{file_dir}/{image_guid}.jpg'

    def thumb_path(self, request, thumb_id, response=None, info=None):
        thumb_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'thumbs/{thumb_id}/{file_dir}/{thumb_guid}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

