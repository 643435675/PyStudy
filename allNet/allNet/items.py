# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllnetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LongXunDaoHang(scrapy.Item):
    # 分类名称
    category = scrapy.Field()
    # 分类link
    categoryLink = scrapy.Field()

