# -*- coding: utf-8 -*-
# @Time    : 2017/8/25 21:54
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : aichengxuspider.py 爱程序网 www.aichengxu.com

import scrapy
from aichengxu.items import androidItem
import logging
class aiChengxu(scrapy.Spider):

    name = 'aichengxu'

    allowed_domains = ['www.aichengxu.com']

    start_urls = ["http://www.aichengxu.com/android/{}/".format(n) for n in range(1,10000)]

    def parse(self, response):
        node_list = response.xpath("//*[@class='item-box']")
        print('nodelist',node_list)
        for node in node_list:
            android_item = androidItem()
            count = node.xpath("./div[@class='views']/text()").extract()
            title_link = node.xpath("./div[@class='bd']/h3/a/@href").extract()
            title = node.xpath("./div[@class='bd']/h3/a/text()").extract()
            desc = node.xpath("./div[@class='bd']/div[@class='desc']/text()").extract()
            time = node.xpath("./div[@class='bd']/div[@class='item-source']/span[2]").extract()
            print(count,title,title_link,desc,time)
            android_item['title'] = title
            android_item['titleLink'] = title_link
            android_item['desc'] = desc
            android_item['count'] = count
            android_item['time'] = time
            yield android_item
