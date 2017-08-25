# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AichengxuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class androidItem(scrapy.Item):
    # 阅读量
    count = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 链接
    titleLink = scrapy.Field()
    # 描述
    desc = scrapy.Field()
    # 时间
    time = scrapy.Field()
