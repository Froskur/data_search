# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient("mongodb://dbUser:Froskur1234@cluster0-shard-00-00-llgb1.gcp.mongodb.net:27017,cluster0-shard-00-01-llgb1.gcp.mongodb.net:27017,cluster0-shard-00-02-llgb1.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

class SpyPipeline(object):
    def process_item(self, item, spider):
        db = client[spider.name]
        coll = db[type(item).__name__]

        #print(1)
        if item.get('salary'):
            coll.insert(item)

        return item
