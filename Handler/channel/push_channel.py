from Spider.Handler.channel.Channel import Channel
from Spider.kernel.Config import Config
import redis
class push_channel():
    con = None
    config = None
    channel_name = None
    def __init__(self, channel_name):
        self.channel_name = channel_name
        config = Config()
        self.con = redis.Redis(host=config.Get("redis.host"), port=config.Get("redis.port"))
    def push(self,data):
        self.con.rpush(self.channel_name,data)
    def stop(self):
        self.push("---STOP---")