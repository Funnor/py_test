#-*- cofing: utf_8 -*-

import redis
from settings import REDIS

def get_redis_client(conf=REDIS):
    print(f'redis run on %s' % conf['host'])
    return redis.StrictRedis(host=conf['host'], port=conf['port'])