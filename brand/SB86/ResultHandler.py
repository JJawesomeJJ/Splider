from Spider.Handler.Abstract.Handler import Handler
import json
from Spider.kernel.Store import Store
class ResultHandler(Handler):
    def handler(self,data):
        data=json.loads(data)
        store=Store()
        store.json_to_file(data['result'],data['path'])
