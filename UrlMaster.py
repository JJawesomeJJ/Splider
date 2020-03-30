from Spider.kernel.Worker import Woker
from Spider.kernel.Store import Store
import os
import threading
import json
import time
from Spider.ImageHandler import ImageHandler
from Spider.Handler.AutoHandle import AutoHandle
def to_dict(data):
    result={}
    for i in data:
        result[i['name']]=i['result']
    return result
def get_img(brand_type,url,i):
    result = Woker(url, total_rules).start()[0]['children'][0][0]['children']
    for brand_info in result:
        brand_info = to_dict(brand_info)
        file_path = path + "/" + str(brand_type) + "类/" + str(i) + "/" + brand_info['href'] + ".json"
        file_path=file_path.replace("/","\\")
        channel.push(json.dumps({"key":brand_info['href'],"img":brand_info['img'],'brand_type':brand_type}))
if __name__ == '__main__':
    total=0
    Store=Store()
    def hanndler(data):
        print(data)
    handler=AutoHandle().handle_closure(hanndler).start()
    handler.push("odada")
    handler.stop()
    print(os.name)
    exit()
    channel=ImageHandler("image_channel").start()
    for brand_type in range(5,46):
        print("以抓取"+str(brand_type)+"/"+"45")
        if brand_type<10:
            brand_type="0"+str(brand_type)
        print(brand_type)
        url="https://r.yuzhua.com/search/{0}--------------{1}-.html".format(str(brand_type),1)
        path = os.path.dirname(__file__) + "/data"
        rules=[{
            "name":"max_page",
            "reg":"共(.*?)页",
            "length":1
            }]
        #获取最大页数
        max_process=8
        max_page=Woker(url,rules).start()[0]['result']
        max_page=int(max_page)
        brand_list = {}
        file_name=os.path.dirname(__file__)+"/data/"+str(brand_type)+"类.json"
        # if os.path.isfile(file_name)==True:
        #     continue
        path_ = os.path.dirname(os.path.realpath(__file__))
        for i in range(1,max_page+1):
            print("已抓取小页"+str(i)+"/"+str(max_page))
            url = "https://r.yuzhua.com/search/{0}--------------{1}-.html".format(str(brand_type),i)
            total_rules=[
                {
                    "name":"ul_container",
                    "reg":'<ul class="listBox_card">([\s\S]*?)</ul>',
                    "length":1,
                    'children':[{
                        'name':'item',
                        'reg':'<a ([\s\S]*?)listBox_card_p1',
                        'children':[
                            {
                                "name":'href',
                                'reg':'href="/goods/(.*?).html"',
                                'length':1
                            },
                            {
                                "name": 'img',
                                'reg': 'src="(.*?)"',
                                'length': 1
                            }
                        ],
                        "is_store":False
                    }],
                    'is_store':False
                }
            ]
            while len(threading.enumerate())>max_process:
                pass
            # if int(brand_type)>10:
            # if os.path.isdir(path_ + "/data/img/{}".format(brand_type)):
            #     continue
            # result = Woker(url, total_rules).start()[0]['children'][0][0]['children']
            t = threading.Thread(target=get_img, args=[brand_type, url, i])
            t.start()
        print("进程数[{}]".format(len(threading.enumerate())))
    # time.sleep(10)
    # channel.stop()


