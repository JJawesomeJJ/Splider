from Spider.kernel.Worker import Woker
import os
from Spider.kernel.Store import Store
import threading
import time
import json
from Spider.Handler.UserHandler import UserHandler
def get_data(store_path,url):
    url="https://r.yuzhua.com"+url
    result=Woker(url,rules).start()
    channel.push(json.dumps({"path":store_path,"result":result}))
if __name__ == '__main__':
    list=[]
    path=os.path.dirname(__file__)+"/data"
    channel=UserHandler("the_data_has").start()
    Store=Store()
    max_processs=8
    rules = [
        {
            "name": "name",
            "reg": """<p class="head_detail_show_title"><span>([\s\S]*?)</span></p>""",
            "length": 1,
            'filter': ["UserFilter@trim"]
        },
        {
            "name": "price",
            "reg": """<span class="price">(.*)</span>""",
            "length": 1,
        },
        {
            "name": "goods",
            "reg": """<span class="dotd">([\s\S]*?)</span>""",
            "length": 1,
            'filter': ["UserFilter@filter_goods", "UserFilter@trim"]
        },
        {
            "name": "groups",
            "reg": """<p class="head_detail_show_similar">类似群组：<span>([\s\S]*?)</span></p>""",
            "length": 1
        },
        {
            "name": "img",
            "reg": "<img src=\"(.*?)\" alt=\"鱼爪商标转让网",
            "length": 1
        },
        {
            'name':"type",
            'reg':'组合类型：<span>(.*?)</span>',
            'length':1
        },
        {
            'name':'numbers',
            'reg':'第(.*?)类',
            'length':1
        },
        {
            'name':'time',
            'reg':'<p class="head_detail_show_expiry">有效期限：(.*?)</p>',
            'length':1
        }
    ]
    for i in Store.file_walk(path):
        pass
    worker=Woker("https://r.yuzhua.com/goods/8164226228.html",rules)
    worker.start("GET")
    for i in range(1,10):
        for json_path in Store.file_walk(path):
            numbers=os.path.basename(json_path).replace(".json","")
            brand_item=data=json.loads(open(json_path).read())
            for key in dict(brand_item).keys():
                    for url in brand_item[key]:
                        file_path=path + "/" + numbers + "/" + key + "/"+os.path.basename(url).split('.')[0]+".json"
                        if os.path.isfile(file_path):
                            print("Url {} has been read".format(url))
                            continue
                        while (len(threading.enumerate()) > max_processs):
                            pass
                        t1 = threading.Thread(target=get_data,args=[file_path,url])
                        t1.start()
                    print("当前线程数[{}]".format(len(threading.enumerate())))
                    print("正在抓取第[{}]类第[{}/{}]页".format(numbers,key,len(dict(brand_item).keys())))