# Author jjawesome
# created_at 2020-03-15
# description it is a single thread to handle the data of website like store on your compute so it can avoid some problem of many thread
# we use redis to share data of "worker"(many spider to get the data of website) to handler like golang channel but we can't avoid the input-output cause waste time
import time
import random
import hashlib
from Spider.Handler.channel.Channel import Channel
import threading
import sys
from Spider.Handler.channel.push_channel import push_channel
class Handler():
    channel_name=None
    channel=None
    def __init__(self,channel_name="system"):
        if channel_name=="system":
            self.channel_name=self.__create_channel_name()
        else:
            self.channel_name=channel_name
        self.channel=Channel(self.channel_name)
    def __create_channel_name(self):
        return hashlib.md5(str(str(time.time())+str(self.__rand(0,9,5))).encode("utf-8")).hexdigest()
    def __rand(self,min,max,num):
        str1=""
        for i in range(0,num):
            str1=str1+str(random.randint(min,max))
        return str
    def __get_channel(self):
        return self.channel
    def handler(self,data):
        pass
    def target(self):
        data=self.channel.pop()
        while(data!='---STOP---'):
            try:
                self.handler(data)
            except Exception as e:
                print(e)
                print (sys._getframe().f_lineno)
            data=self.channel.pop()
        print("收到停止命令process has been killed by user")
        self.Onclose()
    def start(self):
        t1 = threading.Thread(target=self.target)
        t1.start()
        return push_channel(self.channel_name)
    def Onclose(self):
        pass