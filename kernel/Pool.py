import hashlib
import time
import random
from Spider.Handler.channel.Channel import Channel
from inspect import isfunction
import threading
import time
class pool():
    __pool_name=None
    __channel=None
    __init_pool_fun=None
    def __init__(self,pool_name=None):
        if pool_name==None:
            pool_name=hashlib.md5(str(str(time.time())+str(self.__rand(0,9,5))).encode("utf-8")).hexdigest()
        self.pool_name=pool_name
        self.channel=Channel(pool_name)
    def __rand(self, min, max, num):
        str1 = ""
        for i in range(0, num):
            str1 = str1 + str(random.randint(min, max))
        return str
    def get_pool_len(self):
        return self.channel.get_channel_len()
    def init_pool(self,pool_init_fun):
        self.init_pool_fun=pool_init_fun
        lock=threading.Lock()
        lock.acquire()
        if self.channel.get_channel_len()==0:
            self.__create_pool()
        lock.release()
        return self
    def __create_pool(self):
        if isfunction(self.init_pool_fun) == False:
            raise Exception("params init_pool_fun should be a fun but " + str(type(self.init_pool_fun)) + " given")
        data = self.init_pool_fun()
        if isinstance(data, list)==False:
            raise Exception("return pool_list_fun should be a list but " + str(type(data)) + " given")
        for i in data:
            self.channel.push(i)
    def reset_pool(self):
        self.channel.reset_channel()
        print("channel【{}】has been reset".format(self.pool_name))
    def Consumer(self,fun):
        if isfunction(fun)==False:
            raise Exception("params fun should be a method but "+str(type(fun))+" given")
        is_repush=True
        try:
            gLock = threading.Lock()  # 创建一把锁
            gLock.acquire()  # 上锁
            data=self.channel.unblock_pop()
            while data==None:
                data = self.channel.unblock_pop()
                time.sleep(0.1)
                self.__create_pool()
            gLock.release()
            if fun(data)==False:
                is_repush=False
        except Exception as e:
            print(e)
            is_repush=False
        finally:
            if is_repush==True:
                self.channel.push(data)




