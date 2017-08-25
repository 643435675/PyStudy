# -*- coding: utf-8 -*-
# @Time    : 2017/8/10 22:19
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : BokeFightingMain.py  传智博客主页最新投稿文章
import scrapy
import json
# from chuanzhibokemyfendou.chuanzhibokemyfendou.items import BokeFighting
f = open('传智排行.txt', 'a',encoding='utf-8')

class BokeFightingMain(scrapy.Spider):

    name = 'bokemain'

    allowed_domains = ['fendou.itcast.cn']

    start_urls = ['http://fendou.itcast.cn/Article/newpaihang.html?offset={}'.format(n) for n in range(1,20)]

    def parse(self, response):
        root_list = json.loads(response.body_as_unicode())
        for info in root_list:
            # Boke = BokeFighting()
            Boke = []
            print(info)
            # 挑战到详情页用的aid
            # Boke['titleAid'] = info['aid']  if 'aid' in info else ''
            titleAid= info['aid']  if 'aid' in info else ''
            f.write(str(titleAid))
            # 作者
            # Boke['nickname'] = info['nickname']  if 'nickname' in info else ''
            nickname= info['nickname']  if 'nickname' in info else ''
            # 文章名称
            # Boke['title'] = info['title']  if 'title' in info else ''
            title = info['title']  if 'title' in info else ''
            # 票数
            # Boke['vote'] = info['vote']  if 'vote' in info else ''
            vote = info['vote']  if 'vote' in info else ''
            # 发表时间戳
            # Boke['adddate'] = info['adddate']  if 'adddate' in info else ''
            adddate = info['adddate']  if 'adddate' in info else ''
            # 是否点过赞（暂且这样考虑）
            # Boke['stau'] = info['stau']  if 'stau' in info else ''
            stau = info['stau']  if 'stau' in info else ''
            print('*'*20)
            print(str(adddate))
            # yield
    f.close()