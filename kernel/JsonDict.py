class JsonDict():
    def dict_convert_key_value(self,dict_,key,value_key):
        result={}
        result[dict_[key]]=dict_[value_key]
        return result
    def dict_link(self,list1):
        result={}
        for i in list1:
            for key in i.keys():
                result[key]=i[key]
        return result
    def list_covert(self,list):
        result=[]
        for list1 in list:
            item=[]
            for dic in list1:
                item.append(self.dict_convert_key_value(dic,"name","result"))
            result.append(self.dict_link(item))
        return result

