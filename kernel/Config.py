#Description system config file
import json
import os
class Config():
    config_dict=None
    def __init__(self):
        path=os.path.dirname(os.path.dirname(__file__))
        self.config_dict=json.loads(open(path+"/Config.json",'r',encoding='utf-8-sig').read())
    def get_data(self,data,key):
        return data[key]
    def Get(self,args):
        result=self.config_dict
        for key in args.split("."):
            result=self.get_data(result,key)
        return result