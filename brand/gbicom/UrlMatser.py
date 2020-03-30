from Spider.kernel.Worker import Woker
import os
import threading
import json
import os
import hashlib
from Spider.kernel.Store import Store
from Spider.Handler.AutoHandle import AutoHandle
#读取ip池
def get_ip_pool():
    result=[]
    if os.path.isfile("IpPool.txt")==False:
        get_ip_pool_file()
    data=open("IpPool.txt",encoding="utf-8").read().replace("\n\n","\n").split("\n")
    for i in data:
        print(i)
        info=i.replace("\ufeff","").split(":")
        if len(info)>1:
            result.append({"host":info[0],"port":info[1]})
    return result
#获取新的池
def get_ip_pool_file():
    data = Woker("http://http.tiqu.alicdns.com/getip3?num=10&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4").start()
    print("load")
    with open("IpPool.txt", "w") as f:
        print("ip pool has been reload")
        print(data)
        f.write(data)
    pass
def ip_parse_index():
    result={}
    for i in range(0,len(ip_pool)):
        key=ip_pool[i]['host']+"-"+ip_pool[i]["port"]
        result[key]=i
    return result
#获取当前最少使用的ip分配给线程使用 ip负载均衡调模块儿
def get_min_request():
    file_name = Store.getmd5("IpPool.txt") + ".json"
    ip_use_record={}
    if os.path.isfile(file_name):
        try:
            ip_use_record = json.loads(open(file_name, encoding="UTF-8").read())  ##加载记录ip每个ip访问次数
        except Exception as e:
            ip_use_record={}
    if len(ip_use_record.keys()) == 0:
        for i in ip_pool_index:
            value = ip_pool_index[i]
            ip_use_record[i] = 0
    if len(ip_use_record.keys())==1:
        print("ip pool has been reload")
        get_ip_pool_file()
        init_pool()
        print(ip_use_record)
        exit()
    key=min(ip_use_record, key=ip_use_record.get)
    ip_use_record[key]=ip_use_record[key]+1
    with open(file_name,"w") as f:
        f.write(json.dumps(ip_use_record))
    return ip_pool[ip_pool_index[key]]
#抓取程序
def splider(url,proxies,reg,page,ip_port):
    UrlWorker = Woker(url,reg)
    UrlWorker.spliers.set_proxies(proxies)
    try:
        result=UrlWorker.start("GET",{},headers)
        if len(result[0]['children'])==0:
            print(UrlWorker.content)
        # # if len(result[0]['children'])==0:
        # print(UrlWorker.content)
        channel.push(json.dumps({"page": page, 'result': result[0]['children'], "ip_port": ip_port}))
    except Exception as e:
        print(e)
        result=[]
        channel.push(json.dumps({"page": page, 'result': [], "ip_port": ip_port}))
##初始化ip池
def init_pool():
    global ip_pool # ip pool like is {}
    global ip_pool_index #ip池对象的index as this
    global ip_use_record
    global file_name
    global fail_recored
    ip_pool=get_ip_pool()
    file_name=Store.getmd5("IpPool.txt") + ".json"
    ip_pool_index=ip_parse_index()
    if os.path.isfile(file_name):
        try:
            ip_use_record = json.loads(open(file_name, encoding="UTF-8").read())  ##加载记录ip每个ip访问次数
        except Exception as e:
            pass
    if len(ip_use_record.keys()) == 0:
        for i in ip_pool_index:
            value = ip_pool_index[i]
            ip_use_record[i] = 0
#删除失败的ip
def del_ip(ip_port):
    file_name = Store.getmd5("IpPool.txt") + ".json"
    ip_use_record = json.loads(open(file_name, encoding="UTF-8").read())
    del ip_use_record[ip_port]
    Store.json_to_file(ip_use_record,Store.getmd5("IpPool.txt") + ".json")
#初始化ip池的访问记录
def init_recored():
    if len(ip_use_record.keys())==0:
        for i in ip_pool_index:
            value=ip_pool_index[i]
            ip_use_record[i]=0
if __name__ == '__main__':
    ip_use_record={}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
    }
    max_process=8
    Store=Store()
    init_pool()
    #---初始化ip池
    #---初始化ip池
    #创建一个抓取数据后的函数处理块儿
    path = os.path.dirname(__file__)
    def handler(data):
        print(data)
        data=json.loads(data)
        page=data['page']
        result=data['result']
        if(len(result)==0):
            del_ip(data['ip_port'])
            print("ip has been limit system has been remove it")
            return
        Store.json_to_file(result,path+"/data/"+str(page)+".json")
        # print(data)
    #创建一个管道 多线程将数据都插如这个单线程进行处理 参照 golang 的 chan
    channel=AutoHandle().handle_closure(handler).start()
    # 代理服务器
    proxyHost = "ip"
    proxyPort = "port"
    #页面提取的规则
    rules=[
        {
            "name":"item",
            "reg":'<dl style="position: relative;" class="search-list-trademarks"([\s\S]*?)</dl>',
            "children":[
                {
                    "name":"name",
                    "reg":'brandname = "(.*?)"',
                    "length":1
                },
                {
                    "name":"register_number",
                    "reg":'bh = "(.*?)"',
                    "length":1
                },
                {
                    "name":"img",
                    "reg":'data-url="(.*?)"',
                    'length': 1
                },
                {
                    "name":"number",
                    "reg":'【(.*?)类】',
                    'length':1
                },
                {
                    "name":"groups",
                    "reg":'<p title="([\s\S]*?)" class="list-introduction">',
                    "filter":["UserFilter@clear_number"],
                    'length': 1
                }
            ],
            'is_store':False
        }
    ]
    for i in range(1,23441):
        if os.path.isfile(os.path.dirname(__file__)+"/data/"+str(i)+".json"):
            # print("data of page-{} has been read".format(i))
            continue
        url="http://www.gbicom.cn/search/0/2/all/1/desc/{},,,,,1,0/1/all".format(i)
        ip=get_min_request()
        proxyMeta = "http://%(host)s:%(port)s" % {
            "host": ip['host'],
            "port": ip['port'],
        }
        proxies = {
            "http": proxyMeta,
        }
        while max_process<len(threading.enumerate()):
            pass
        t=threading.Thread(target=splider,args=[url,proxies,rules,i,ip["host"]+"-"+ip['port']])
        t.start()
        print("当前页码【{}/23441】 当前线程数【{}】".format(i,len(threading.enumerate())))
        # print(requests.get("http://www.gbicom.cn/search/0/2/all/1/desc/{},,,,,1,0/1/all".format(i)).text)