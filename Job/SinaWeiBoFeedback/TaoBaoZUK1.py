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
# os.environ["webriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

url = "https://www.tmall.com/"
browser.get(url)
time.sleep(5)
#手机号登录
phoneLogin = browser.find_element_by_xpath('//*[@id="mq"]')
phoneLogin.send_keys('ZUK Z2手机')

time.sleep(3)
# 搜索
btnNext = browser.find_element_by_xpath('//*[@id="mallSearch"]/form/fieldset/div/button')
btnNext.click()

# 找到手机一栏
time.sleep(3)
btnPhone = browser.find_element_by_xpath('//*[@id="J_NavAttrsForm"]/div/div[2]/div/div[2]/ul/li[4]/a')
btnPhone.click()
page = browser.page_source
html = etree.HTML(page)

links = html.xpath("//*[@id='J_ItemList']/div[@data-atp='a!,,1512,,,,,,,,']")
for link in links:
    price = link.xpath("./div[@class='product-iWrap']/p[@class='productPrice']/em/text()")

    detaillink = link.xpath("./div[@class='product-iWrap']/div[@class='productImg-wrap']/a/@href")
    abslink = 'https:'+str(detaillink)
    print(price,abslink)
    currentlink = 'https://detail.tmall.com/item.htm?id=531993957001&skuId=3609796167425&user_id=268451883&cat_id=2&is_b=1&rn=71b9b0aeb233411c4f59fe8c610bc34b'

print(len(links))
