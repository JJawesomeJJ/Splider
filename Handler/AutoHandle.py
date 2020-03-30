#description it is simple handler program you can make a single instance of this and the
from Spider.Handler.Abstract.Handler import Handler
class AutoHandle(Handler):
    __closure=None
    def handler(self,data):
        self.closure(data)
    def handle_closure(self,closure):
        # if closure.__closure__==None:
        #     raise Exception("params closure should be a closure but "+str(type(closure))+" given")
        self.closure=closure
        return self

