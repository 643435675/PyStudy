# encoding=utf8
import requests
import json
import re
import time

startUrl = 'https://m.weibo.cn/api/container/getIndex?uid=5650743478&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&featurecode=20000320&type=uid&value=5650743478&containerid=1076035650743478'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    ,
    'Cookie': 'ALF=1504709445; SCF=Ag0epa_4tyFCglnCwHJiaRDznUy645wpqEhg-dG3Sv0cbfGX1wNmqXPnHQroard1FW2nn3RdCnmux4VZ7bFRuMo.; SUHB=0ebt4qVvtKU1d7; _T_WM=22bb4d80315608a0e9bd3bf92b3c1dac; SUB=_2A250jA4VDeRhGeBN6FsT8i7MyTyIHXVXjpJdrDV6PUJbktBeLXjBkW1oTOqmqg0rff3UmekP4TzhMFYtsw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFNrBkhSeVrfPGckwnaFCcy5JpX5o2p5NHD95Qce0e4eoz7ehz7Ws4DqcjBIcHVdr.peoepeoefeK5Ee5tt; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%2540%25E4%25BA%25AC%25E4%25B8%259C%25E5%25AE%25A2%25E6%259C%258D%26featurecode%3D20000320%26fid%3D1076035650743478%26uicode%3D10000011'
    ,
    'Host':'m.weibo.cn'
    ,
'Accept':'application/json, text/plain, */*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate, br',
    'X-Requested-With':'XMLHttpRequest',
    'Referer':'https://m.weibo.cn/u/5650743478?uid=5650743478&luicode=10000011&lfid=100103type%3D1%26q%3D%40%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&featurecode=20000320',

}

# 详情页list
detaiList = []
# 说说
textList = []
# 说说跟详情页
textAnddetailList = []
# 评论数，详情页返回的是每一页10个
commentsList = []

numSizeList  = []

detaiLinks = []
def getJsonData(url):
    req = requests.get(url, headers=headers)
    # print(req.text)
    return req.text


jsonData = getJsonData(startUrl)


def parseDetailListdata(listdata):
    for detailData in listdata:
        text = detailData['text'] if 'text' in detailData else ""
        reply_text = detailData['reply_text'] if 'reply_text' in detailData else ""
        f.write(text+'\r\n')
        print(text)
        print(reply_text)
        f.write(reply_text + '\r\n')
    # pass


def parseJsonData(jsonData):
    global pagedetail
    jsondata = json.loads(jsonData, 'utf-8')
    print(jsondata)
    listdata = jsondata['cards']if 'cards' in jsondata else ""
    print(listdata)

    for datainfo in listdata:
        # print(datainfo)
        mblog = datainfo['mblog'] if 'mblog' in datainfo else ""

        # print(mblog)
        if len(mblog)> 0 :  # 有数据，继续执行
            descText = mblog['text']
            # print(descText)
            descText = getTextInfo(descText)
            dex = '发表的说说开始：\r\n'
            f.write(dex)
            dex2 = '发表的说说内容：'+descText+'\r\n'
            f.write(dex2)
            print("发表的说说开始：")
            print('发表的说说内容：'+descText)
            textList.append(descText)

            comments = mblog['comments_count']  # 评论数
            numSizeList.append(comments)
            # print(comments)
            # if comments > 1:  # 有评论，获取到评论链接上的数据
            #     detailLine = datainfo['scheme']
            #     print(detailLine)
            #     detaiList.append(detailLine)

            idstr = mblog['idstr']
            detaiLinks = getpageSize(comments,idstr)
            pagedetail = 1
            for detaillink in detaiLinks:
                jsonData2 = getJsonData(detaillink)
                str11 = '评论详情页条目：'+str(pagedetail)+'      .......\r\n'
                f.write(str11)
                print('评论详情页条目：'+str(pagedetail)+'      .......')
                print(jsonData2)
                pagedetail = pagedetail +1
                jsonDatadetail = json.loads(jsonData2, 'utf-8')
                listdata = jsonDatadetail['data'] if 'data' in jsonDatadetail else ''
                # print(listdata)
                parseDetailListdata(listdata)
            pagedetail = 1
            print('主页条目结束...')
            f.write('主页条目结束...\r\n')
            # detailJsonStr = 'https://m.weibo.cn/api/comments/show?id=' + str(idstr) + '&page=' + str(comments)
            # print(detailJsonStr)
            # commentsList.append(detailJsonStr)
        else:
            # 在里面的话，直接跳出方法
            return
    print('爬取结束......')


def getTextInfo(textStr):
    # 得到文本内容
    # for textStr in textList:
    # print('***********')
    regx = '<span(.*?)</span>'
    strregx = re.compile(regx)
    strregx = re.findall(strregx, str(textStr))
    replacestr = str(textStr).replace('<span' + ''.join(strregx) + '</span>', '')
    str1 = '<span'

    sstr1 = str(textStr)[0:str(textStr).find(str1)]
    # print(sstr1)
    return sstr1
        # print(textStr)
        # print(replacestr)


# 得到文本详情页链接
def getpageSize(comments,idstr):
    for i in range(1,int((comments / 10))+2):
        # 评论也的link
        detaiLink = 'https://m.weibo.cn/api/comments/show?id=' + str(idstr) + '&page=' +str(i)
        detaiLinks.append(detaiLink)
        # print(detaiLink)
        return detaiLinks

# parseJsonData(jsonData)


# print(str(textList))  page = 7
# print(str(detaiList))
f = open('微博京东说说跟评论.txt', 'a',encoding='utf-8')
def main_start():
    for inde in range(11,50):
        # startUrl = 'https://m.weibo.cn/api/container/getIndex?uid=5650743478&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&featurecode=20000320&type=uid&value=5650743478&containerid=1005055650743478&page='+str(inde)

        startUrl = 'https://m.weibo.cn/api/container/getIndex?uid=5650743478&luicode=10000011&lfid=100103type%3D1%26q%3D@%E4%BA%AC%E4%B8%9C%E5%AE%A2%E6%9C%8D&featurecode=20000320&type=uid&value=5650743478&containerid=1076035650743478&page={}'+str(inde)
        pageindex = '页数：'+str(inde)+'\r\n'
        print('startUrl   '+'index '+str(inde)+'     '+startUrl)
        f.write(pageindex)
        data = getJsonData(startUrl)
        parseJsonData(data)
        time.sleep(2)
    f.close()

main_start()
