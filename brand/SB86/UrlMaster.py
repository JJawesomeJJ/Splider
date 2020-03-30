from Spider.kernel.Worker import Woker
import os
import requests
from Spider.kernel.Store import Store
from Spider.Handler.SBhandler import SBhandler
import json
import threading
import time
def get_data(url,i):
    print(url)
    num = (Woker(url, rules).set_diver("webdriver").start('GET', headers))[0]['result'][0]
    SBhandler.push(json.dumps({'key': i, "value": num}))
if __name__ == '__main__':
    all_data={}
    store = Store()
    SBhandler=SBhandler("86sb").start()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    for i in range(1,46):
        url="http://www.86sb.com/products/list?tt=0&bt=&bigclassid={}&orderby=sort%7Cdesc&is_index=1&cg=1#listfirst".format(i)
        rules=[
            {
                "name":"page",
                "reg":"共(.*?)页"
            }
        ]
        while(len(threading.enumerate())>8):
            pass
        t1 = threading.Thread(target=get_data,args=[url,i])
        t1.start()
        time.sleep(2)
    time.sleep(60)
    SBhandler.stop()
    # store.json_to_file(all_data,os.path.dirname(os.path.realpath(__file__))+"/data/page_info.json")