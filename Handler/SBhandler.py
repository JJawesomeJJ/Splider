#商标网站的存储程序
from Spider.Handler.Abstract.Handler import Handler
import json
from Spider.kernel.Store import Store
class SBhandler(Handler):
    all_data={}
    def handler(self,data):
        data=json.loads(data)
        print(data)
        self.all_data[data['key']]=data['value']
    def Onclose(self):
        store=Store()
        store.json_to_file(self.all_data,r"D:\Program Files\JetBrains\PyCharm Community Edition 2019.2.4\jbr\bin\python\Spider\brand\86sb.com\data\page.json")
