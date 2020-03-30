#Description it is a
import redis
from Spider.kernel.Config import Config
import time
class Channel():
    __con=None
    __config=None
    __channel_name=None
    __record_channel="spider_record_list"#记录在redis申请的通道 可以在后期删除它
    __backup_channel="backup_channel"#备份队列
    def __init__(self,channel_name):
        self.channel_name=channel_name
        config=Config()
        self.con=redis.Redis(host=config.Get("redis.host"), port=config.Get("redis.port"))
        self.con.hset(self.__record_channel,self.channel_name,time.time())
    def push(self,data):
        self.con.rpush(self.channel_name,data)
    def pop(self):
        return str(self.con.brpop(self.channel_name)[1],encoding='utf-8')
    def get_channel_len(self):
        return self.con.llen(self.channel_name)
    def reset_channel(self):
        self.con.delete(self.channel_name)
    def unblock_pop(self):
        return self.con.lpop(self.channel_name)
    def add_back_channel(self,data):
        script="""
        local result=redis.call('hGet',KEYS[1],KEYS[2]);
        if result==nil or result==false then
           local list={ARGV[1]}
           return redis.call('hSet',KEYS[1],KEYS[2],cjson.encode(list))
        else
           result=cjson.decode(result)
           table.insert(result,ARGV[1])
           return redis.call('hSet',KEYS[1],KEYS[2],cjson.encode(result))
        end
        """
        return self.con.eval(script,[self.__backup_channel,self.channel_name,data],2)
    def get_back_and_del(self):
        script = """
                local result=redis.call('hGet',KEYS[1],KEYS[2]);
                if result==nil or result==false then
                   return nil
                else
                   result=cjson.decode(result)
                   redis.call('del',KEYS[1],KEYS[1])
                   return result
                end
                """
        return self.con.eval(script,[self.__backup_channel,self.channel_name],2)