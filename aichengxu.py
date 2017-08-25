# -*- coding: utf-8 -*-
import scrapy


class AichengxuSpider(scrapy.Spider):
    name = 'aichengxu'
    allowed_domains = ['aichengxu.com']
    start_urls = ['http://aichengxu.com/']

    def parse(self, response):
        pass
