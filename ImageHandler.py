from Spider.Handler.Abstract.Handler import Handler
import json
from Spider.kernel.Store import Store
import os
class ImageHandler(Handler):
    all_data={}
    def handler(self,data):
        data=json.loads(data)
        self.all_data[data['key']]=data['img']
        path = os.path.dirname(os.path.realpath(__file__))
        store = Store()
        store.json_to_file(data, path + "/data/img/{}/{}.json".format(data['brand_type'],data['key']))
