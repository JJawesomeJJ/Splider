from Spider.kernel.Pool import pool
import threading
def test():
    def cus(data):
        print(data)
    pool_.Consumer(cus)
if __name__ == '__main__':
    def init_pool():
        print("pool has been reload")
        return ["fsd","fsdf","fsdf"]
    pool_=pool("test_pool").init_pool(init_pool)
    max_process=2
    while True:
        while (len(threading.enumerate()) > max_process):
            pass
        t = threading.Thread(target=test)
        t.start()