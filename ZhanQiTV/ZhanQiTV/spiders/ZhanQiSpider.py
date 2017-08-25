# -*- coding: utf-8 -*-
# @Time    : 2017/8/15 23:31
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : ZhanQiSpider.py
import scrapy
import json
# from ZhanQiTV.items import ZhanqitvItem

class ZhanQi(scrapy.Spider):
    name = 'ZhanQi'

    start_urls = ['https://www.zhanqi.tv/api/static/v2.1/live/list/20/1.json']

    allowed_domains= ['www.zhanqi.tv']

    def parse(self, response):
        json_data = json.loads(response.body_as_unicode())
        for j_data in json_data:
            msg = j_data['message']
            print(msg)