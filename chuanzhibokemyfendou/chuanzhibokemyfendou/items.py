# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChuanzhibokemyfendouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 挑战到详情页用的aid
    titleAid = scrapy.Field()
    # 作者
    nickname = scrapy.Field()
    # 文章名称
    title = scrapy.Field()
    # 票数
    vote = scrapy.Field()
    # 发表时间戳
    adddate = scrapy.Field()
    # 是否点过赞（暂且这样考虑）
    stau = scrapy.Field()
    # pass

class BokeFighting(scrapy.Item):
    # 挑战到详情页用的aid
    titleAid = scrapy.Field()
    # 作者
    nickname = scrapy.Field()
    # 文章名称
    title = scrapy.Field()
    # 票数
    vote = scrapy.Field()
    # 发表时间戳
    adddate = scrapy.Field()
    # 是否点过赞（暂且这样考虑）
    stau = scrapy.Field()