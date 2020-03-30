from Spider.kernel.Worker import Woker
import os
import requests
from Spider.kernel.Store import Store
from Spider.Handler.SBhandler import SBhandler
import json
import threading
import time
from Spider.brand.SB86.ResultHandler import ResultHandler
def target(url,path):
    data=[]
    result=json.loads(requests.get(url).text)['result']['l']
    for i in result:
        info={}
        info['name']=i['sbname']
        info['groups']=i['sbgroupidarr']
        info['img']=i['sbpic']
        info['goods']=i['sbbetween']
        info['price']=i['sblowprice']
        info['numbers']=i['sbbigclassid']
        info['register_number']=i['sbid']
        info['starttime']=i['sbadddate']
        data.append(info)
    channel.push(json.dumps({
        "path":path,
        'result':data
    }))
if __name__ == '__main__':
    max_process=8
    path=os.path.dirname(__file__)+"/"
    channel=ResultHandler("SB86").start()
    page_data=json.loads(open(os.path.dirname(__file__)+"/data/page.json",encoding="utf-8").read())
    for brand_class in range(1,46):
        for i in range(1,int(page_data[str(brand_class)])+1):
            path1=path+"data/brand/"+str(brand_class)+"类"+"/"+str(i)+".json"
            if(os.path.isfile(path)):
                continue
            while(len(threading.enumerate())>max_process):
                pass
            url="http://www.86sb.com/products/listarr?tt=0&c={}&ts=&te=&ls=&le=&k=&kk=&s=&l=&y=&f=&p=&cg={}&ob=&bt=".format(brand_class,i)
            print("正在抓取[{}]类 第{}/{}".format(brand_class,i,page_data[str(brand_class)]))
            print("当前线程数{}".format(len(threading.enumerate())))
            t=threading.Thread(target=target,args=[url,path1])
            t.start()
    channel.stop()

