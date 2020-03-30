from Spider.kernel.JsonDict import JsonDict
from Tool.File import File
from Spider.kernel.Store import Store
import time
if __name__ == '__main__':
    start=float(time.time())
    file=File()
    store=Store()
    jsondict=JsonDict()
    num=0
    register_list=store.file_to_json("../brand.json")
    # print(register_list)
    index=1
    source="SB86"
    if "fsf" in register_list:
        pass
    print(start)
    print(float(time.time())-start)
    print()
    for i in file.file_walk(r"D:\Program Files\JetBrains\PyCharm Community Edition 2019.2.4\jbr\bin\python\Spider\brand\gbicom\data"):
        index=index+1
        print(index)
        data=store.file_to_json(i)
        store.json_to_file(jsondict.list_covert(data),i)
        # print(i)
    #     brand_list=store.file_to_json(i)
    #     for brand in range(0,len(brand_list)):
    #         if brand_list[brand]['register_number'] not in register_list:
    #             num = num + 1
    #             brand_list[brand]['is_insert']=True
    #         else:
    #             brand_list[brand]['is_insert'] = False
    #         brand_list[brand]['source']=source
    #     # for brand in range(0,len(brand_list)):
    #     #     if brand_list[brand]['is_insert']==True:
    #     #         num = num + 1
    #     #         register_list.append(brand_list[brand]['register_number'])
    #     #     brand_list[brand]['source']=source
    #     store.json_to_file(brand_list,i)
    #     print(i)
    # # store.json_to_file(register_list,"../brand.json")
    # print(num)




