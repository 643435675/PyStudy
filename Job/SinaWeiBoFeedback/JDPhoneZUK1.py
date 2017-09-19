# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 19:52
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : TaoBaoZUK1.py  联想zuk z1 手机评论信息爬取

import re
import time
from selenium import webdriver
import os
from lxml import etree

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
browser = webdriver.Chrome(chromedriver)

url = "https://www.jd.com/"
browser.get(url)
time.sleep(5)
#手机号登录
phoneLogin = browser.find_element_by_xpath('//*[@id="key"]')
phoneLogin.send_keys('ZUK Z2手机')

time.sleep(3)
# 搜索
btnNext = browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
btnNext.click()

# 找到手机一栏
time.sleep(3)
btnPhone = browser.find_element_by_xpath('//*[@id="J_searchWrap"]/div[2]/a')
btnPhone.click()
page = browser.page_source
html = etree.HTML(page)

links = html.xpath("//*[@id='J_goodsList']/ul[@class='gl-warp clearfix']")
print('links',links)
for link in links:
    verlink = link.xpath("./li[@class='gl-item']/div[@class='gl-i-wrap']/div[@class='p-img']/a/@href")


    price = link.xpath("./li[@class='gl-item']/div[@class='gl-i-wrap']/div[@class='p-price']/strong/text()")
    print(price)
    print(verlink)

print(len(links))
