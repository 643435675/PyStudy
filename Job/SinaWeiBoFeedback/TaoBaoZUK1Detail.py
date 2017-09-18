# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 23:16
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : TaoBaoZUK1Detail.py zuk z1 详情页内容

import time
from selenium import webdriver
from lxml import etree

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
browser = webdriver.Chrome(chromedriver)

def getcomments():
    html = gethtml()
    source = etree.HTML(html)
    commens = source.xpath("//*[@id='J_TabBar']/li[3]/a/em/text()")
    # 将评论转为int类型
    commens = (int(commens[0]) % 20) + 1
    # 获取到总评论
    print(commens)

    return  commens

def gethtml():
    url = "https://detail.tmall.com/item.htm?id=531993957001&skuId=3609796167425&user_id=268451883&cat_id=2&is_b=1&rn=71b9b0aeb233411c4f59fe8c610bc34b"
    browser.get(url)
    time.sleep(5)
    browser.execute_script('window.scrollBy(0,3000)')
    time.sleep(2)
    browser.execute_script('window.scrollBy(0,5000)')
    time.sleep(2)

    # 累计评价
    btnNext = browser.find_element_by_xpath('//*[@id="J_TabBar"]/li[3]/a')
    btnNext.click()
    html = browser.page_source
    return html

# print(html)
def parseHtml(html):
    html = etree.HTML(html)
    commentlist = html.xpath("//*[@class='rate-grid']/table/tbody")
    for comment in commentlist:
        # 评论
        vercomment = comment.xpath(
            "./tr/td[@class='tm-col-master']/div[@class='tm-rate-content']/div[@class='tm-rate-fulltxt']/text()")
        # 机器类型
        verphone = comment.xpath("./tr/td[@class='col-meta']/div[@class='rate-sku']/p[@title]/text()")
        print(vercomment)
        print(verphone)
        # 用户(头尾各一个字，中间用****代替)
        veruser = comment.xpath("./tr/td[@class='col-author']/div[@class='rate-user-info']/text()")
        print(veruser)
    print(len(commentlist))

# parseHtml(html)
# print('*'*20)

def nextbuttonwork(num):
    if num != 0 :
        browser.execute_script('window.scrollBy(0,3000)')
        time.sleep(2)
        browser.find_element_by_css_selector('#J_Reviews > div > div.rate-page > div > a:nth-child(6)').click()
        time.sleep(2)
        browser.execute_script('window.scrollBy(0,3000)')
        time.sleep(2)
        browser.execute_script('window.scrollBy(0,5000)')
        time.sleep(2)
        html = browser.page_source
        parseHtml(html)
        print('nextclick finish  ')


def selenuim_work(num):
    print('selenuim start ... ')
    html = gethtml()
    parseHtml(html)
    nextbuttonwork()
    print('selenuim  end....')
    pass


def gettotalpagecomments(comments):
    for i in range(0,comments):
        selenuim_work()


commens = getcomments()
gettotalpagecomments(commens)