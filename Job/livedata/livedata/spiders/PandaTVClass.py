# encoding=utf8
import requests
import json



url = "https://www.panda.tv/live_lists?status=2&order=person_num&token=&pageno=%d&pagenum=120&_=%d".format(a=range(0,35),b=range(1501946526480,1501946526880))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    ,
    'Cookie': '__guid=96554777.3243119502220345300.1500627276199.6702; smid=608e0bde-ffe2-4251-90ca-2938cabdc074; monitor_count=18'
    ,
}


def getHtml(url):
    print('##'*30)
    req = requests.get(url, headers=headers)
    print(req.text)
    return req.text


data = getHtml(url)

def printInfos(data):
    jsondata = json.loads(data, "utf-8")
    print(jsondata)
    itemsinfo = jsondata['data']['items']
    for pinfo in itemsinfo:
        name = pinfo['name']
        person_num = pinfo['person_num']
        nickName = pinfo['userinfo']['nickName']
        lelvel = pinfo['host_level_info']
        lable = pinfo['label']
        print(lable)
        cname = pinfo['classification']
        print(cname)
        print(name)
        print(person_num)
        print(nickName)
        print(lelvel)

def mainStart():

    for n in range(0, 50):
        pageindex = 1 + n
        pagetime = int(1501946526480 + n)
        url = "https://www.panda.tv/live_lists?status=2&order=person_num&token=&pageno=%d&pagenum=120&_=%d"%(pageindex,pagetime)
        data = getHtml(url)
        printInfos(data)


mainStart()