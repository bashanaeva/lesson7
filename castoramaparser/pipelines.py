# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


from pymongo import MongoClient

class CastoramaparserPipeline:

    # def __init__(self):
    #     client = MongoClient('localhost', 27017)
    #     self.mongo_base = client.CastoramaDZ

    def process_item(self, item, spider):
        print()
        # collection = self.mongo_base[spider.name]
        # collection.insert_one(item)
        return item


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        # item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
