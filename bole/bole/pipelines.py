# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class BolePipeline(object):
    def process_item(self, item, spider):
        client = MongoClient()
        client["jobbole"]["bl"].insert_one(dict(item))
