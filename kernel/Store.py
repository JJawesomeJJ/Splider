#description it is a file operate class to fast store the json format data in yoour computer
import json
import os
import hashlib
class Store():
    def json_to_file(self,json_object,file_name):
        text=json.dumps(json_object)
        self.store_file(text,file_name)
    def store_file(self,text,file_name):
        path=os.path.dirname(file_name)
        if os.path.isdir(path)==False:
            try:
                os.makedirs(path)
            except Exception as e:
                print(e)
        # if os.path.isfile(file_name):
        #     print("File is Already exist "+file_name+"!!!")
        #     return
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(text)
            file.close()
    def file_walk(self,path):
        result=[]
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                result.append((dirpath + "\\" + i).replace("~$", ""))
        return result
    def file_extension_filter(self,path,extension_list):
        result=[]
        file_name_list=self.file_walk(path)
        for i in file_name_list:
            if os.path.splitext(i)[1].replace(".","") in extension_list:
                result.append(i)
        return result
    def file_name(self,path):
        name=os.path.splitext(path)[0]
        name_info=name.split("\\")
        return name_info[len(name_info)-1]

    def getmd5(self,file):
        m = hashlib.md5()
        with open(file, 'rb') as f:
            for line in f:
                m.update(line)
        md5code = m.hexdigest()
        return md5code
    def file_to_json(self,path,encoding="utf8"):
        if os.path.isfile(path)==False:
            raise Exception("Splider failed find your file may it is not exist --"+path)
        try:
            ccontent = json.loads(open(path, encoding=encoding).read())
            return ccontent
        except Exception as e:
            raise Exception("Splider failed convert content of file to json")