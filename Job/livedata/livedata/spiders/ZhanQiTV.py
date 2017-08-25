# -*- coding: utf-8 -*-
# @Time    : 2017/8/15 23:18
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : ZhanQiTV.py  战旗tv全部直播信息
import scrapy
import json

class ZhanQi(scrapy.Spider):
    name = 'ZhanQi'

    start_urls = ['https://www.zhanqi.tv/api/static/v2.1/live/list/20/{}.json'.format(n) for n in range(0,10)]

    allowed_domains= ['www.zhanqi.tv']

    def parse(self, response):
        print('sssssss')
        print(response.body)
