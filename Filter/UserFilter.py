#DESCRIPTION 用户动态自定义的过滤器：对数据进行过滤
import re
class UserFilter():
    def trim(self,input):
        if isinstance(input,str):
            return input.strip()
        if isinstance(input,list):
            result=[]
            for i in input:
                result.append(i.strip())
            return result
    def filter_goods(self,input):
        input=str(input)
        return input.replace('\\r\\n','').replace("&nbsp","").replace(" ","")
    def money(self,input):
        input=str(input).replace("万","")
        if(int(input)<10):
            return int(input)*10000
    def clear_number(self,input):
        return re.sub("【(.*?)类】","",input)
    def test(self,input):
        return input