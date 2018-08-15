#-*- coding:utf-8 -*-
from settings import A_MINUTE, REDIS
from cashe_redis import get_redis_client

class RedisTest(object):

    def __init__(self):
        self.rs = get_redis_client()
    
    def get_test_key(self):
        return 'test_key'
    
    def get_test__key_value(self):
        key = self.get_test_key()
        value = self.rs.get(key)
        if value:
            return value.decode()
        # get from db
        value = 'test'
        self.rs.set(key, value,A_MINUTE)
        return value

    def get_test_dict_value(self):
        key = 'test_dict_key'
        v = self.rs.get(key)
        if v:
            return v.decode()
        v = REDIS
        self.rs.set(key, v)
        return v
    
    # list 
    def get_list_value(self):
        key = 'list_test'
        v = self.rs.lrange(key, 0, -1)
        if v:
            v = [eval(l.decode()) for l in v]
            return v
        v = [3, 4, 5]
        self.rs.lpush(key, v)
        return v
    # 管道
    # def get_list_by_pl(self):
    #     key = 'list_test'
    #     pl = self.rs.pipeline(transaction=False)
    #     v, total = pl.lrange(key, 0, -1).llen(key).execute()
    #     return v, total

    def get_list_by_pl(self):
        key = 'list_test'
        with self.rs.pipeline(transaction=False) as pl:
            pl = pl.lrange(key, 0, -1).llen(key)
            v, total = pl.execute()
        return v, total

    # set
    def get_set_value(self):
        key = 'myset'
        v = self.rs.smembers(key)
        if v:
            return v
        self.rs.sadd(key, 'set6', 'set9')
        return v

if __name__ == '__main__':
    rt = RedisTest()
    value = rt.get_test__key_value()
    print("value: %s, type: %s" %(value, type(value)))
    value = rt.get_test_dict_value()
    print("value: %s, type: %s" %(value, type(value)))

    value = rt.get_list_value()
    print("value: %s, type: %s" %(value, type(value)))

    value = rt.get_set_value()
    value = set(v.decode() for v in value)
    print("value: %s, type: %s" %(value, type(value)))
    
    value, total = rt.get_list_by_pl()
    print("value: %s,total: %s, type: %s" %(value, total, type(value)))