# -*- coding: utf-8 -*-
# @Time    : 2017/8/9 23:17
# @Author  : 蛇崽
# @Email   : 17193337679@163.com
# @File    : JDPhone.py
import requests
import json
from urllib.parse import quote
from bs4 import BeautifulSoup
import os
import re
import time
import datetime
from random import choice
import traceback
import csv

"""
京东爬虫：抓取京东手机类别下的所有型号的产品信息（基本信息+相对属性+绝对属性+图片）、评论信息

productId 和 skuId:

字段：
基本信息：所属分类名称，分类ID，店铺链接，productId，小标题，价格，

相对属性：


图片：保存到：分类名称/商品id/  目录下


@API:
1. 产品介绍的富文本：https://cd.jd.com/description/channel?skuId=3564140&mainSkuId=3564140&cdn=2&callback=showdesc
2. 产品配件： https://c.3.cn/recommend?callback=handleComboCallback&methods=accessories&p=103003&sku=3564140&cat=9987%2C653%2C655&lid=1&uuid=484377010&pin=&ck=pin%2CipLocation%2Catw%2Caview&lim=5&cuuid=484377010&csid=122270672.70.484377010%7C21.1500617159&_=1500621893531
3. 优惠套装：https://c.3.cn/recommend?callback=jQuery8538482&sku=3564140&cat=9987%2C653%2C655&area=1_72_2799_0&methods=suitv2&count=6&_=1500621893408
4. 产品评价统计数据：https://club.jd.com/comment/productCommentSummaries.action?referenceIds=3564140&callback=jQuery8710223&_=1500621893394
5. 产品价格：https://p.3.cn/prices/mgets?callback=jQuery366476&type=1&area=1_72_2799_0&pdtk=&pduid=484377010&pdpin=&pin=null&pdbp=0&skuIds=J_3564140&ext=11000000&source=item-pc
6. 增值服务及配送方式：https://c0.3.cn/stock?skuId=3564140&area=1_72_2799_0&venderId=1000000904&cat=9987,653,655&buyNum=1&choseSuitSkuIds=&extraParam={%22originid%22:%221%22}&ch=1&fqsp=0&pduid=484377010&pdpin=&callback=jQuery3612846
7. 当前产品评论：https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv84200&productId=3846673&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
"""


class Jingdong():
    # url获取所有手机品牌id和名称json
    url = 'https://list.jd.com/list.html?cat=9987,653,655&sort=sort_rank_asc&trans=1&md=1&my=list_brand'
    brands = {}
    brands['url'] = {}  # 存储与品牌相关的信息
    items = []      # 存储所有手机的URL
    path = ''  # 当前图片存储路径
    item_path = ''

    itemIDS = {}  # 爬取过的产品的id作为键，值为1

    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 ',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 ',
        'Mozilla/5.0 (Linux; U; Android 3.2; ja-jp; F-01D Build/F0001) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13 ',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; ja-jp) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5 ',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/ Safari/530.9 ',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    ]
    def __init__(self):

        text = json.loads(requests.get(self.url,headers=self.get_user_hearder()).text)

        for brand in text['brands']:
            url = 'https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_' + str(brand['id'])+'&sort=sort_rank_asc&trans=1&JL=3_'+quote(brand['name'])
            self.brands['url'][brand['name']] = url  # 存储所有品牌的 {名称：URL} 字典

            # data = {}
            # data['id'] = brand['id']
            # data['name'] = brand['name']
            # data['pinyin'] = brand['pinyin']
            # data['logo'] = brand['logo']
            # data['url'] = url

            # requests.post('127.0.0.1:8000/jingdong/', data=data,headers=self.get_user_hearder())


    def get_user_hearder(self):
        headers = {}
        headers['User-Agent'] = choice(self.user_agents)
        return headers


    def parse_brand(self):
        """
        遍历所有的品牌的URL，分别爬取所有品牌下的所有型号的手机（加上分页），并存储图片到相应品牌命名的文件夹下
        """
        for name in self.brands['url']:
            print('当前类别：'+name)
            self.path = name      # brands['url']字典的键是品牌的名称，值是该品牌的URL
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            brand_url = self.brands['url'][name]


            # 爬取该品牌下所有手机的信息
            while True:
                soup = BeautifulSoup(requests.get(brand_url,headers=self.get_user_hearder()).text)
                lis = soup.find_all("li",attrs={"class":"gl-item"}) # 抓该分类下的所有产品

                self.items.clear()
                for li in lis:
                    self.items.append("http:"+str(li.find("a").get('href')))


                for item_url in self.items:
                    print("当前商品："+item_url)
                    try:
                        html = requests.get(item_url,headers=self.get_user_hearder())
                        soup = BeautifulSoup(html.text)
                        item_id = re.sub("\D", "", item_url)
                        try:
                            self.item_path = os.path.join(self.path,str(item_id))
                            if not os.path.exists(self.item_path):
                                os.mkdir(self.item_path)

                            params = self.getParams(soup,item_id) # 获取参数并保存,绝对属性
                            commentMetas = self.getCommMeta(item_id) # 获取评价的相对属性
                            comments = self.getComments(item_id) # 获取100页评价
                            images = self.getImages(soup,self.item_path, item_id) # 获取相片并保存，照片

                            with open('products.csv', 'a') as f:  #
                                f.write(name+','+str(item_id)+','+params['skuName']+','+ params['price']+','+commentMetas['goodRateShow']+','+commentMetas['poorRateShow']
                                    +','+commentMetas['commentCount']+','+commentMetas['goodCount']+","+commentMetas['generalCount']+','+commentMetas['poorCount'])

                                for hotTag in list(commentMetas['hotCommentTags']):
                                    f.write(','+hotTag['name']+":"+str(hotTag['count']))

                                f.write('\n')



                            with open(name+'/' + str(item_id)+'_propertys.csv','w') as f:
                                for key in params['paramsList'].keys():
                                    f.write(key+','+params['paramsList'][key]+'\n')


                            with open(name+'/' + str(item_id)+'_comments.csv','w') as f:
                                try:
                                    for comm in comments['goodComments']:

                                        f.write(str(comm['cmid'])+','+str(comm['guid'])+','+comm['nickname']+','+comm['score']+','+'good,'+comm['creationTime']+','+comm['content'])
                                        if 'commentTags' in comm.keys():
                                            for commentTag in comm['commentTags']:
                                                f.write(','+commentTag['name'])
                                        f.write('\n')

                                except:
                                    pass
                                try:
                                    for comm in comments['geneComments']:

                                        f.write(str(comm['cmid'])+','+str(comm['guid'])+','+comm['nickname']+','+comm['score']+','+'gene,'+comm['creationTime']+','+comm['content'])
                                        if 'commentTags' in comm.keys():
                                            for commentTag in comm['commentTags']:
                                                f.write(','+commentTag['name'])
                                        f.write('\n')
                                except:
                                    pass
                                try:
                                    for comm in comments['badComments']:

                                        f.write(str(comm['cmid'])+','+str(comm['guid'])+','+comm['nickname']+','+comm['score']+','+'bad,'+comm['creationTime']+','+comm['content'])
                                        if 'commentTags' in comm.keys():
                                            for commentTag in comm['commentTags']:
                                                f.write(','+commentTag['name'])
                                        f.write('\n')

                                except:
                                    pass

                        except Exception as e:
                            # 每个商品，解析错误的时候，记录日志
                            with open('item_exception.log','a') as f:
                                # 格式：当前时间，所属类别，产品id，错误原因
                                f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ","+self.path + ","+ str(item_id) + ","+str(e)+"\n")
                                print(str(e))

                        time.sleep(2)   # 休息2秒
                    except Exception as e:
                        with open('item_error.log','a') as f:
                            # 格式：当前时间，所属类别，产品id，错误原因
                            f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ","+item_url +str(e)+"\n")
                            print(str(e))


                href = soup.find("a",attrs={"class":"pn-next"}) # 下一页

                if href:
                    brand_url = 'https://list.jd.com'+href.get('href')
                else:
                    break

                print('下一页')

            # break


    def getCommJson(self,productId, page=0,score=0):
        """
        获取评论的Json数据:
        score=0为全部，1为差评，2为中评，3为好评
        sortType=6为按时间排序，5为推荐排序
        isShadowSku 是否不只显示当前商品的评论，默认是 0否， 1为是
        获取到json后，京东解析json的js的URL：https://static.360buyimg.com/item/default/1.0.32/components/comment/??comment.js
        """
        #productPageComments
        commUrl="http://sclub.jd.com/comment/skuProductPageComments.action?productId="+str(productId)+"&score="+ str(score)+ "&sortType=6&pageSize=10&isShadowSku=0&page=" + str(page)

        # &callback=fetchJSON_comment98vv83110
        html=requests.get(commUrl,headers=self.get_user_hearder()).text
        # lsize=html.find('{')
        # rsize=html.rfind('}')+1

        # commentJson=json.loads(html[lsize:rsize])
        try:
            json_content = None
            # json_content = json.loads(re.search(r'(?<=\().*(?=\);)',html).group(0))
            json_content = json.loads(html)
        except Exception as e:
            print(traceback.format_exc())
        time.sleep(0.01)
        return json_content


    def getParams(self,soup,productId):
        """
        保存基本参数
        """
        params = {}
        params['price']=self.getPrice(productId)    #获取商品价格
        # skuName=soup.find("div",attrs={"class":"sku-name"}).string    #获取手机的标题
        skuName=soup.find("div",attrs={"id":"name"})
        if skuName is None:
            skuName=soup.find("div",attrs={"class":"sku-name"}).get_text()
        else:
            skuName=skuName.h1.get_text()

        params['skuName'] = skuName.strip()

        paramsList={}
        #获取单反相机的参数
        table=soup.find("table",attrs={"class":"Ptable"})
        if table is not None:
            tds=table.find_all("td",attrs={"class":"tdTitle"})
            for td in tds :
                tdTitle = td.get_text()
                tdContent = td.next_sibling.get_text()
                #paramfile.write(tdTitle+","+tdContent+"\n") #保存绝对属性值
                paramsList[tdTitle]=tdContent
        else:
            #获取手机的参数：绝对属性
            divSoup=soup.find("div",attrs={"class":"Ptable"})
            divs=divSoup.find_all("div",attrs={"class":"Ptable-item"})
            for dls in divs :
                dts = dls.find_all('dt');
                dds = dls.find_all("dd")
                for dt,dd in zip(dts,dds):
                    # paramfile.write(dt.get_text()+","+dd.get_text()+"\n") #保存绝对属性值
                    paramsList[dt.get_text()]=dd.get_text()
        params['paramsList'] = paramsList
        return params


    def getPrice(self,productId):   #根据productId获取商品价格
        url="https://p.3.cn/prices/mgets?type=1&area=1_72_2799_0&pdtk=&pduid=484377010&pdpin=&pin=null&pdbp=0&skuIds=J_"+str(productId)+"&ext=11000000&source=item-pc"
        html=requests.get(url,headers=self.get_user_hearder()).text
        json2=json.loads(html)
        return json2[0]["p"]


    def getImages(self, soup, item_path, item_id):  #获取图片，并保存
        imgs=soup.find("div",attrs={"id":"spec-list"})
        images = []
        if not imgs:
            return images

        imgs = imgs.find_all("img")

        i=1
        for img in imgs:
            try:
                imgUrl="http:"+str(img.get("src"))

                lsize=imgUrl.find("/n5/")       #手机的imageUrl变化
                rsize=imgUrl.find("_jfs")
                imgUrl=imgUrl[:lsize]+"/n1/s450x450"+imgUrl[rsize:] #修改图片的URL，获取高清的图片而不是缩略图

                # lsize=imgUrl.find("/n5/")     #单反相机的imageUrl变化
                # imgUrl=imgUrl[:lsize]+"/n1/"+imgUrl[lsize+4:] #修改图片的URL，获取高清的图片而不是缩略图

                images.append(imgUrl)

                image=requests.get(imgUrl, stream=True,headers=self.get_user_hearder())
                with open(item_path+"/" + str(item_id) + "_" + str(i)+".jpg","wb")  as jpg:#保存图片
                    for chunk in image:
                        jpg.write(chunk)
                i=i+1
            except:
                traceback.print_exc()

        return images


    def getCommMeta(self,item_id):
        """
        获取相对属性，买家印象，评论总结
        """
        commentJson = self.getCommJson(item_id)
        # https://club.jd.com/comment/skuProductPageComments.action
        # ?callback=fetchJSON_comment98vv40836&productId=4669576&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
        # &callback=jQuery3649390&_=1500941065939
        # https://club.jd.com/comment/productCommentSummaries.action?referenceIds=3564110

        commentMetas = {}

        commentMetas['goodRateShow'] = str(commentJson["productCommentSummary"]["goodRateShow"]) # 好评率
        commentMetas['poorRateShow'] = str(commentJson["productCommentSummary"]["poorRateShow"]) # 差评率
        commentMetas['commentCount'] = str(commentJson["productCommentSummary"]["commentCount"])    #评论数
        commentMetas['goodCount'] = str(commentJson["productCommentSummary"]["goodCount"])      #好评数
        commentMetas['generalCount'] = str(commentJson["productCommentSummary"]["generalCount"])    #中评数
        commentMetas['poorCount'] = str(commentJson["productCommentSummary"]["poorCount"])      #差评数

        # 买家印象
        commentMetas['hotCommentTags'] = commentJson["hotCommentTagStatistics"]

        return commentMetas

    def getComments(self,item_id):
        """
        获取该产品的好评，中评，差评各100页评论数据
        """
        comments = {}
        comments['goodComments'] = []
        comments['geneComments'] = []
        comments['badComments'] = []

        # 好评
        for i in range(100):
            commentJson = self.getCommJson(item_id, i,score=3)
            if commentJson == None:
                continue
            if len(commentJson['comments']) == 0:
                break
            comments['goodComments'].extend(self.splitComments(commentJson))

        time.sleep(1)
        # 中评
        for i in range(100):
            commentJson = self.getCommJson(item_id, i,score=2)
            if commentJson == None:
                continue
            if len(commentJson['comments']) == 0:
                break
            comments['geneComments'].extend(self.splitComments(commentJson))
        time.sleep(1)
        # 差评
        for i in range(100):
            commentJson = self.getCommJson(item_id, i,score=1)
            if commentJson == None:
                continue
            if len(commentJson['comments']) == 0:
                break
            comments['badComments'].extend(self.splitComments(commentJson))
        time.sleep(1)
        return comments


    def splitComments(self,commentJson):
        comments = []
        for comm in commentJson['comments']:
            comment = {}

            comment["cmid"] = str(comm.get('id',""))    # 该评论的id
            comment["guid"] = str(comm.get('guid',"")) # guid是啥？
            comment["content"] = str(comm.get('content',"")).replace(",","，").replace(' ',"").replace('\n',"").strip()
            comment["creationTime"] = str(comm.get('creationTime',""))
            comment["referenceId"] = str(comm.get('referenceId',""))  # 该评论所属的商品
            comment["replyCount"] = str(comm.get('replyCount',""))
            comment["score"] = str(comm.get('score',""))
            comment["nickname"] = str(comm.get('nickname',""))
            comment["productColor"] = str(comm.get('productColor',""))
            comment["productSize"] = str(comm.get('productSize',""))
            comments.append(comment)

        return comments


    def parseProducts(self, product_list):
        """
        product_list是形如 [[p1_sku1_id,p1_sku2_id,p1_sku3_id],[p2_sku1_id,p2_sku2_id,p2_sku3_id,p2_sku4_id]...] 的列表
        其中列表中的一个元素[p1_sku1_id,p1_sku2_id,p1_sku3_id]又是一个列表，表示一个product的 相同配置，不同颜色的sku
        @param product_list：自己手动构建一个满足条件的60个产品的sku的id列表，然后传进来让程序解析
        """
        for products in product_list:
            parent_product_id = products[0]     # 同一个列表里边默认第一个为父
            for item_id in products:
                try:
                    url = "https://item.jd.com/" + str(item_id) + ".html"   # 产品的url
                    print(url)
                    html = requests.get(url,headers=self.get_user_hearder())
                    soup = BeautifulSoup(html.text)

                    name = soup.find("div",attrs={"class":"J-crumb-br"}).find("div",attrs={"class":"head"}).find('a').text # 品牌
                    self.path = name
                    if not os.path.exists(self.path):
                        os.mkdir(self.path)

                    if not os.path.exists(self.path + "/propertys"):    # 用来放propertys
                        os.mkdir(self.path + "/propertys")

                    try:
                        self.item_path = os.path.join(self.path,str(parent_product_id)) # 同一个父的子产品的图片存在同一个文件夹下
                        if not os.path.exists(self.item_path):
                            os.mkdir(self.item_path)


                        params = self.getParams(soup,item_id) # 获取参数并保存,绝对属性
                        commentMetas = self.getCommMeta(item_id) # 获取评价的相对属性
                        comments = self.getComments(item_id) # 获取100页评价
                        images = self.getImages(soup,self.item_path,item_id) # 获取相片并保存，照片

                        if parent_product_id == item_id:    # 父sku的信息，作为主要的信息，其他的作为备份
                            with open('products.csv', 'a') as f:  #
                                f.write(name+','+str(item_id)+','+params['skuName']+','+ params['price']+','+commentMetas['goodRateShow']+','+commentMetas['poorRateShow']
                                    +','+commentMetas['commentCount']+','+commentMetas['goodCount']+","+commentMetas['generalCount']+','+commentMetas['poorCount'])

                                for hotTag in list(commentMetas['hotCommentTags']):
                                    f.write(','+hotTag['name']+":"+str(hotTag['count']))

                                f.write('\n')


                        # 不是父sku则存到其他文件作为备份
                        with open('products_backup.csv', 'a') as f:  #
                            f.write(name+','+str(item_id)+','+params['skuName']+','+ params['price']+','+commentMetas['goodRateShow']+','+commentMetas['poorRateShow']
                                +','+commentMetas['commentCount']+','+commentMetas['goodCount']+","+commentMetas['generalCount']+','+commentMetas['poorCount'])

                            for hotTag in list(commentMetas['hotCommentTags']):
                                f.write(','+hotTag['name']+":"+str(hotTag['count']))
                            f.write('\n')

                        with open(name+'/propertys/' + str(item_id)+'_propertys.csv','w') as f:
                            for key in params['paramsList'].keys():
                                f.write(key+','+params['paramsList'][key]+'\n')

                        with open(name+'/' + str(parent_product_id)+'_comments.csv','a') as f:
                            try:
                                # 存好评
                                for comm in comments['goodComments']:
                                    try:
                                        f.write(str(comm['cmid'])+','+str(comm['guid'])+','+comm['nickname']+','+comm['score']+','+'good,'+comm['creationTime']+','+comm['content'])
                                    except Exception as e:
                                        print("exception: " + str(e))
                                    if 'commentTags' in comm.keys():
                                        for commentTag in comm['commentTags']:
                                            f.write(','+commentTag['name'])
                                    f.write('\n')

                            except:
                                print('comment error save good comm' + str(item_id))
                                traceback.print_exc()
                            try:
                                # 存中评
                                for comm in comments['geneComments']:
                                    try:
                                        f.write(str(comm['cmid'])+','+str(comm['guid'])+','+comm['nickname']+','+comm['score']+','+'gene,'+comm['creationTime']+','+comm['content'])
                                    except Exception as e:
                                        print("exception: " + str(e))
                                    if 'commentTags' in comm.keys():
                                        for commentTag in comm['commentTags']:
                                            f.write(','+commentTag['name'])
                                    f.write('\n')
                            except:
                                print('comment error save gene comm' + str(item_id))
                            try:
                                # 存差评
                                for comm in comments['badComments']:
                                    try:
                                        f.write(str(comm['cmid'])+','+str(comm['guid'])+','+comm['nickname']+','+comm['score']+','+'bad,'+comm['creationTime']+','+comm['content'])
                                    except Exception as e:
                                        print("exception: " + str(e))
                                    if 'commentTags' in comm.keys():
                                        for commentTag in comm['commentTags']:
                                            f.write(','+commentTag['name'])
                                    f.write('\n')

                            except:
                                print('comment error save bad comm' + str(item_id))
                    except Exception as e:
                        # 每个商品，解析错误的时候，记录日志
                        with open('item_exception.log','a') as f:
                            # 格式：当前时间，所属类别，产品id，错误原因
                            log = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ","+self.path + ","+ str(item_id) + ","+str(e)+"\n"
                            f.write(log)
                        traceback.print_exc()

                    time.sleep(2)   # 休息2秒
                except Exception as e:
                    with open('item_error.log','a') as f:
                        # 格式：当前时间，所属类别，产品id，错误原因
                        log = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ","+ str(item_id) +str(e)+"\n"
                        f.write(log)
                        print(log)

            # break


    def split_comment_csv(self):
        """
        遍历所有评论文件，（即以_comments.csv结尾的文件），根据标点符号分句
        """
        file_list = []
        dirs = os.listdir(".")
        for dir_name in dirs:
            if os.path.isdir(dir_name):
                for name in os.listdir(dir_name):
                    if os.path.isfile(dir_name+"/"+name):
                        item = {}
                        item["filePath"] = dir_name+"/"+name
                        item['fileName'] = name
                        item['dirName'] = dir_name
                        file_list.append(item)

        if not os.path.exists('comment_clause'):
            os.mkdir('comment_clause')

        for item in file_list:
            reader = csv.reader(open(item['filePath']))
            csv_writer_name = 'comment_clause/' + item['dirName'] +"_" + item['fileName']

            with open(csv_writer_name, 'w', newline='\n') as csvfile:
                for row in reader:
                    if len(row) >= 7:
                        clauses = re.split('，|。|？|！|；|;|、|\?|!|·|）|（',row[6])

                        for clause in clauses:
                            clause.replace('&hellip','')
                            clause = clause.strip()
                            if len(clause) != 0:
                                csvfile.write(clause+"\n")


    def count_origin_comments(self):
        """
        对原始的未断句之前的评论统计数量
        """
        file_list = []
        dirs = os.listdir(".")
        for dir_name in dirs:
            if os.path.isdir(dir_name):
                for name in os.listdir(dir_name):
                    if os.path.isfile(dir_name+"/"+name):
                        item = {}
                        item["filePath"] = dir_name+"/"+name
                        item['fileName'] = name
                        item['dirName'] = dir_name
                        file_list.append(item)

        countData = []
        totalRowNum = 0 # 评论总条数
        totalClauseNum = 0  # 断句后的句子总数
        for item in file_list:
            reader = csv.reader(open(item['filePath']))
            rowNum = 0  # 该文件中的行数
            clauseNum = 0
            for row in reader:
                if len(row) >= 7:
                    rowNum = rowNum + 1
                    clauses = re.split('，|。|？|！|；|;|、|\?|!|·|）|（',row[6])

                    for clause in clauses:
                        clause.replace('&hellip','')
                        clause = clause.strip()
                        if len(clause) != 0:
                            clauseNum = clauseNum + 1

            totalClauseNum = totalClauseNum + clauseNum
            totalRowNum = totalRowNum + rowNum
            data_item = {}
            data_item['fileName'] = item['fileName']
            data_item['clauseNum'] = str(clauseNum)
            data_item['rowNum'] = str(rowNum)
            countData.append(data_item)

        with open('countData.csv', 'w') as f:
            f.write('文件名,原始评论条数,断句条数\n')
            for item in countData:
                f.write(item['fileName']+","+item['rowNum']+","+item['clauseNum']+'\n')
            f.write('评论总数,'+ str(totalRowNum)+"\n")
            f.write('句子总数,'+ str(totalClauseNum)+"\n")


# -----------------------测试---------------------------

    def test_get_all_brand_url(self):
        text = json.loads(requests.get(self.url,headers=self.get_user_hearder()).text)

        for brand in text['brands']:
            url = 'https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_' + str(brand['id'])+'&sort=sort_rank_asc&trans=1&JL=3_'+quote(brand['name'])
            print(url)


    def test_find_next_page(self,url):
        soup = BeautifulSoup(requests.get(url,headers=self.get_user_hearder()).text)
        href = soup.find("a",attrs={"class":"pn-next"}) # 下一页


        if href:
            print(href.get('href'))
            brand_url = 'https://list.jd.com'+href.get('href')
        else:
            brand_url = ''
            print('url is None')
        print(brand_url)


    def test_get_comment_json(self,productId):
        json_content = self.getCommJson(productId)
        print(json_content)
        for comm in json_content['comments']:
            print(comm['content'].replace('\n',''))


    def test_read_csv(self):
        reader = csv.reader(open('test.csv'))
        for row in reader:
            if len(row) >= 6:
                print(row[6] + '\n')

if __name__ == '__main__':
    jingdong = Jingdong()
    # 爬全部的品牌
    # jingdong.parse_brand()
    # 测试
    # jingdong.getCommJson(12280434216,0,0)
    # 测试
    # jingdong.test_get_all_brand_url()
    # jingdong.test_find_next_page('https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand%5F8557&page=3&sort=sort_rank_asc&trans=1&JL=6_0_0')
    # jingdong.test_get_comment_json(11083454031)

    # 爬需要的60个手机型号(现在只有33个型号)

    # product_list = [
    # [3857525,4669576],[4411638, 4316775,4431603],[3924115,3875973],[3398125],[5097448,4199965],
    #   [4502433,4199967],[4411628],[3857521],[1345368],[11375078958,11774045896,11546640578],
    #   [4461939],[10417752533,10417197477],
    #   [10827008669],[4869176],[4086221,4086223,3867555,3867557],
    #   [4432058,4432056,4432052,4086229,4086227],[3352172,3352168],[4222708,3763103],[4170768,4170788,4170784,4170782],
    #   [4978326,4978306,4978332,5247848],[3729301,3729311,3729315],[10399574837,10416687137,10437750952,11089374104,11089374105],
    #   [1816276356,1816276354,10256482570,1816276355],[10065260353,10065260354,10069410228,10069410229],
    #   [10654370492,11022002650,10654370493,10654370494],[12481158400,12481163501,13304714040],
    #   [2166504],[3548595,3548599,3979666,3979664],[4363831,4363833,4363805,4363811,4363847],
    #   [4230493,5158518,5158508],[2589814,2589808,2589818],[2972184,2972174,2972172,2972186],[10213303571,10213303572]
    # ]

    # 追加的酷派，努比亚，一加
    product_list = [
        [3397564,3075827,3785780],[3151585,3159473],[3159465],[3789933],[3697279],[2917215],
        [2214850],[4066471],[2401116],[5019352,4160791],[10072766014],[10717616871],
        [4345197],[4345173],[5014204,4229972,4161762,2943569],[4746242,4983290,4024777,4746262,4245285],
        [4899658,4996220,4100837,5239536],[4220709,4534743,4220711,4497841],[3139087,3569552],
        [11881030122,11881076398,11839878990,12627332950]
    ]


    jingdong.parseProducts(product_list)

    # jingdong.test_read_csv()

    # jingdong.split_comment_csv()


    # jingdong.count_origin_comments()