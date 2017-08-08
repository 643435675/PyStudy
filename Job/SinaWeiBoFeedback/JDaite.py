# -*- coding: utf-8 -*-
# @Time    : 2017/8/7 23:50
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : JDaite.py.py  @京东客服的微博

import requests
import json
import re
import time

headers = {
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cookie':'_T_WM=1d462fed9671c44a3db52e0ccd9d3e3d; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E4%25BA%25AC%25E4%25B8%259C%25E5%25AE%25A2%25E6%259C%258D%26fid%3D100103type%253D1%2526q%253D%2540%25E4%25BA%25AC%25E4%25B8%259C%25E5%25AE%25A2%25E6%259C%258D%26uicode%3D10000011',
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/p/100103type%3D1%26q%3D%40%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D?type=all&queryVal=%40%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&title=%40%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D',
    'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}
# 详情页内容
detail_list = []

def getJsonData(url):
    time.sleep(20)
    req = requests.get(url, headers=headers)
    # print(req.text)
    return req.text


def parseDetailJsonData(detailjson):
    detail_jsondata = json.loads(detailjson, 'utf-8')
    detail_data = detail_jsondata['data'] if 'data' in detail_jsondata else ''
    for detail in detail_data:
        detail_text = detail['text']
        print('detail_text'+str(detail_text))
        f.write('detailLink  ' + str(detail_text) + '\r\n')
        # detail_replytext = detail['reply_text'] if 'reply_text' in detail else ''
        # print('replytext'+str(detail_replytext))



def getPageDetailComment(comments_count, idstr):

    for index  in range(1,int((comments_count / 10))+2):
        # 评论的详情列表
        detailLink = "https://m.weibo.cn/api/comments/show?id={}&page={}".format(str(idstr),str(index))
        print('detailLink  '+str(detailLink))
        f.write('detailLink  '+str(detailLink)+'\r\n')
        time.sleep(10)
        detailjson = getJsonData(detailLink)
        parseDetailJsonData(detailjson)

def parseJsonData(tempjson):
    jsondata = json.loads(tempjson, 'utf-8')

    print(jsondata)
    listdata = jsondata['cards']if 'cards' in jsondata else ''
    print(listdata)
    for datainfo in listdata:
        group_list = datainfo['card_group'] if 'card_group' in datainfo else ''

        if len(group_list) > 0 :
            for group_item in group_list:
                print(group_item)

                mblgs  = group_item['mblog'] if 'mblog' in group_item else ''
                # @文本
                text  = mblgs['text'] if 'text' in mblgs else ""
                print('text : '+str(text))
                # 发布时间
                created_at = mblgs['created_at'] if 'created_at'in mblgs else ''
                print('created_time '+str(created_at))
                comments_count = mblgs['comments_count'] if 'comments_count' in mblgs else 0
                print("="*20)
                print(comments_count)
                idstr = mblgs['idstr'] if 'idstr' in mblgs else ''
                time.sleep(10)
                dex = '发表的说说开始：\r\n'
                f.write(dex)
                dex2 = '发表的说说内容：' + str(text) + '\r\n'
                dex3 = '发布时间：' + str(created_at) + '\r\n'
                f.write(dex2)
                f.write(dex3)
                if int(comments_count) > 1:
                    getPageDetailComment(comments_count,idstr)
                else:
                    # 在里面的话，直接跳出方法
                    return
f = open('at微博京东说说跟评论.txt', 'a',encoding='utf-8')
def main_start():
    # page = 7
    for pageindex in range(3,100):
        time.sleep(10)
        starUrl = 'https://m.weibo.cn/api/container/getIndex?type=all&queryVal=@%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&title=@%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&containerid=100103type%3D1%26q%3D@%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&page={}'.format(str(pageindex))
        data = getJsonData(starUrl)
        pageindex = '页数：' + str(pageindex) + '\r\n'
        f.write(pageindex)
        parseJsonData(data)
    f.close()
main_start()