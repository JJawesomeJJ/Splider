from Spider.Handler.Abstract.Handler import Handler
import json
from Spider.kernel.Store import Store
class UserHandler(Handler):
    def handler(self,data):
        store=Store()
        data=json.loads(data)
        store.json_to_file(data['result'], data['path'])