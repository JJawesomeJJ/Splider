#description it is filter to filter the data of source of html as the rule we write and you can write your filter the handler the data
import re
from Spider.Filter import UserFilter
import sys
from Spider.kernel import AutoLoad
import importlib
class Filter():
    # RuleExample=[{
    #     "name":"列表",#标签名
    #     "reg":"<div class=\"item\">([/s/S]*?)</div>",#标签正则
    #     #标签中的数据作为子数据
    #     "children":[
    #         {
    #             "name": "标题",
    #             "reg": "<div class=\"title\">([/s/S]*?)</div>",
    #         }
    #     ],
    #     #是否存储该数据
    #     "is_store":False
    # }]
    #迭代过滤器
    def filter(self,reg_list,content):
        if reg_list==None:
            return content
        result=[]
        for i in reg_list:
            item_result={}
            reg =i['reg']
            item_result['name']=i['name']
            result_list = re.findall(reg, content)
            #User write the filter by yourself
            if "filter" in dict(i).keys():
                for filter_params in i['filter']:
                    filter_params=str(filter_params).split("@")
                    for index in range(0,len(result_list)):
                        result_list[index]=AutoLoad.load_method("Spider.Filter",filter_params[0],filter_params[1],result_list[index])
            if "is_store" not in dict(i).keys():
                if 'length' in dict(i).keys():
                    item_result['result'] =self.list_split(result_list,i['length'])
                else:
                    item_result['result']=result_list
            else:
                if i['is_store']==True:
                    if 'length' in dict(i).keys():
                        item_result['result'] = self.list_split(result_list, i['length'])
                    else:
                        item_result['result'] = result_list
            if "children" in dict(i).keys():
                item_result['children']=[]
                for item in result_list:
                    children=self.filter(i['children'],item)
                    item_result['children'].append(children)
            result.append(item_result)
        return result
    def list_split(self,list1,len1):
        result=[]
        if len1==1:
            if len1<=len(list1):
                return list1[len1-1]
            else:
                return ""
        for i in range(0,len1-1):
            if i<=len(list1):
                result.append(list1[i])
        return result
    def easyimport(self,Moudule,class_name):
        return importlib.import_module(Moudule+"."+class_name)
    def load_user_filter(self,class_name):
        return getattr(self.easyimport("Filter","UserFilter"),class_name)



