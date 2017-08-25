# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ChuanzhibokemyfendouPipeline(object):
    def process_item(self, item, spider):
        return item

# 写入json文件类
class JsonWritePipeline(object):
    def __init__(self):
        self.file = open('传智我的奋斗我的路最新投稿.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
