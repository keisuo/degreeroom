# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo

class ExtractDataPipeline(object):
    # 剔除html代码
    def take_out_html(self,html):
        strHtml = str(html)
        strHtml = re.sub(r'</?\w+[^>]*>','', strHtml)
        strHtml = re.sub(r'\s+', '', strHtml)
        return strHtml

    def process_item(self, item, spider):
        print(">>> ExtractDataPipeline >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        self.extract_data(item, 'url')
        self.extract_data(item, 'title')
        self.extract_data(item, 'total_price')

        self.extract_data(item, 'hu_xin')
        self.extract_data(item, 'mian_ji')
        self.extract_data(item, 'unit_price')
        self.extract_data(item, 'chao_xiang')
        self.extract_data(item, 'lou_ceng')
        self.extract_data(item, 'zhuang_xiu')
        self.extract_data(item, 'hu_xin')

        self.extract_data(item, 'xiao_qu')
        self.extract_data(item, 'qu_yu')
        self.extract_data(item, 'xue_xiao')
        self.extract_data(item, 'jianzu_year')
        self.extract_data(item, 'id')
        self.extract_data(item, 'publish_date')
        self.extract_data(item, 'core_maidian')
        self.extract_data(item, 'imgs')
        return item
    # 剔除数据中的多余部分
    def extract_data(self, item, key):
        if self.check_key_exist(item, key):
            item[key] = self.take_out_html(item[key])
        else:
            item[key] = ""
        #self.print_itme_value(item, key_bread_positon)
    # 检查key是否存在
    def check_key_exist(self, item, key):
        return key in item.keys()
    # 输出数据
    def print_itme_value(self, item, key):
        print(key, item[key])

class SaveDataPipline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        print(">>> SaveDataPipline >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        collection_name = self.mongo_db
        # self.db[collection_name].update({'id': item['id']}, {'$setOnInsert': dict(item)}, upsert=True)
        self.db[collection_name].insert(dict(item))
        return item