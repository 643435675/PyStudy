# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 23:16
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : TaoBaoZUK1Detail.py zuk z1 详情页内容

import time
from telnetlib import EC

from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
from wheel.signatures.djbec import By

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
browser = webdriver.Chrome(chromedriver)

# 获取第一页的数据
def gethtml():
    url = 'https://item.jd.com/3077252.html'
    browser.get(url)
    time.sleep(5)
    browser.execute_script('window.scrollBy(0,3000)')
    time.sleep(2)
    browser.execute_script('window.scrollBy(0,5000)')
    time.sleep(2)

    # 累计评价
    btnNext = browser.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[5]')
    btnNext.click()
    time.sleep(3)
    html = browser.page_source
    return html



def getcomments(html):
    source = etree.HTML(html)
    commens = source.xpath("//*[@id='detail']/div[1]/ul/li[5]/s/text()")
    print('评论数一：',commens)
    commens = str(commens[0]).replace('(','').replace('+)','')
    # 将评论转为int类型
    commens = (int(commens) / 10) + 1
    # 获取到总评论
    print('评论数：',int(commens))
    return  int(commens)



# print(html)
def parseHtml(html):
    html = etree.HTML(html)
    commentlist = html.xpath("//*[@id='comment-0']")
    for comment in commentlist:
        # 评论
        vercomment = comment.xpath("./div[@class='comment-item']/div[@class='comment-column J-comment-column']/p[@class='comment-con']/text()")
        print('vercomment',vercomment)
    print(len(commentlist))

# parseHtml(html)
# print('*'*20)

def nextbuttonwork(num):

    if num != 0 :
        browser.execute_script('window.scrollBy(0,1000)')
        time.sleep(2)
        # browser.find_element_by_css_selector('#J_Reviews > div > div.rate-page > div > a:nth-child(6)').click()
        browser.find_element_by_css_selector('#comment-0 > div.com-table-footer > div > div > a.ui-pager-next').click()

        time.sleep(2)
        browser.execute_script('window.scrollBy(0,3000)')
        time.sleep(2)
        # browser.execute_script('window.scrollBy(0,5000)')
        # time.sleep(2)
        html = browser.page_source
        parseHtml(html)
        print('nextclick finish  ')


def selenuim_work(html):
    print('selenuim start ... ')
    parseHtml(html)
    nextbuttonwork(1)
    print('selenuim  end....')
    pass


def gettotalpagecomments(comments):
    html = gethtml()
    for i in range(0,comments):
        selenuim_work(html)

data = gethtml()
# 得到评论
commens = getcomments(data)
# 根据评论内容进行遍历
gettotalpagecomments(commens)