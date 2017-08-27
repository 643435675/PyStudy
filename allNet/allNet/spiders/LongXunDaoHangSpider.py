# -*- coding: utf-8 -*-
# @Time    : 2017/8/27 0:43
# @Author  : 蛇崽
# @Email   : 17193337679@163.com  （主要进行全站爬取的练习）
# @File    : LongXunDaoHangSpider.py

# crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口
from scrapy.spider import CrawlSpider,Rule,Request

# 配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor

# scrapy 中用作登陆使用的一个包
from scrapy import FormRequest
from allNet.items import LongXunDaoHang

class longxunDaoHang(CrawlSpider):

    name = 'longxun'

    allowed_domains = ['autohome.com.cn']

    start_urls = ['http://www.autohome.com.cn/shanghai/']

    rules = (
        Rule(LinkExtractor(allow=('\.html',)),callback='parse_item',follow=True),
    )



    def parse_item(self,response):
        print(response.url)
        daohang = LongXunDaoHang()
        daohang['categoryLink'] = response.url
        yield daohang