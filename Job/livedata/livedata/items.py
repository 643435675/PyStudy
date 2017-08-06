# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LivedataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 房间大标题
    roomName = scrapy.Field()
    # 房间小标题（房主）
    roomHost = scrapy.Field()
    # 房间等级
    roomLevel = scrapy.Field()
    # 房间观看人数
    roomAudience = scrapy.Field()

    # 房间类型
    roomType = scrapy.Field()
    # 房间第一页截图
    roomScreen = scrapy.Field()

    # 房间链接地址
    roomLink = scrapy.Field()

