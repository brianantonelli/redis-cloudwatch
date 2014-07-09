#!/usr/bin/env python
'''
Send Redis usage metrics to Amazon CloudWatch

This is intended to run on an Amazon EC2 instance and requires a boto config 
(~/.boto) allowing to write CloudWatch metrics.
'''

import redis
from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata

command_groups = {
    'GetTypeCmds': ['get','getbit','getrange','getset','mget','hget','hgetall','hmget'],
    'SetTypeCmds': ['set','setbit','setex','setnx','setrange','mset','msetnx','psetnx',
                    'hmset','hset','hsetnx','lset'],
    'KeyBasedCmds': ['zdel','dump','exists','expire','expireat','keys','move','persist',
                     'pexpire','pexpireat','pttl','rename','renamenx','restore','ttl',
                     'type','append','bitcount','bitop','bitpos','decr','decrby','get',
                     'getbit','getrange','getset','incr','incrby','incrbyfloat','mget',
                     'mset','msetnx','psetnx','set','setbit','setex','setnx','setrange',
                     'strlen','hdel','hexists','hget','hgetall','hincrby','hincrbyfloat',
                     'hkeys','hlen','hmget','hmset','hset','hsetnx','hvals','blpop',
                     'brpop','lindex','linsert','llen','lpop','lpush','lpushx','lrange',
                     'lrem','lset','ltrim','rpop','rpush','rpushx','sadd','scard','sdiff',
                     'sdiffstore','sinter','sinterstore','sismember','smembers','spop',
                     'srandmember','srem','sunion','sunionstore', 'sscan','zadd','zcard',
                     'zcount','zincrby','zinterstore','zlexcount','zrange','zrangebylex',
                     'zrangebyscore','zrank','zrem','zremrangebylex','zremrangebyrank',
                     'zremrangebyscore','zrevrange','zrevrangebyscore','zrevrank','zscore',
                     'zunionstore','zscan','pfadd','pfcount','pfmerge','watch','eval',
                     'evalsha'],
    'StringBasedCmds': ['append','bitcount','bitop','bitpos','decr','decrby','get','getbit',
                        'getrange','getset','incr','incrby','incrbyfloat','mget','mset',
                        'msetnx','psetnx','set','setbit','setex','setnx','setrange','strlen'],
    'HashBasedCmds': ['hdel','hexists','hget','hgetall','hincrby','hincrbyfloat','hkeys',
                      'hlen','hmget','hmset','hset','hsetnx','hvals','hscan'],
    'ListBasedCmds': ['blpop','brpop','brpoplpush','lindex','linsert','llen','lpop','lpush',
                      'lpushx','lrange','lrem','lset','ltrim','rpop','rpoplpush','rpush',
                      'rpushx'],
    'SetBasedCmds': ['sadd','scard','sdiff','sdiffstore','sinter','sinterstore','sismember',
                     'smembers','smove','spop','srandmember','srem','sunion','sunionstore',
                     'sscan'],
    'SortedSetBasedCmds': ['zadd','zcard','zcount','zincrby','zinterstore','zlexcount',
                           'zrange','zrangebylex','zrangebyscore','zrank','zrem',
                           'zremrangebylex','zremrangebyrank','zremrangebyscore','zrevrange',
                           'zrevrangebyscore','zrevrank','zscore','zunionstore','zscan'],
    'HyperLogLogBasedCmds': ['pfadd','pfcount','pfmerge'],
    'ScriptBasedCmds': ['eval','evalsha']
}

def collect_redis_info():
    r = redis.StrictRedis('localhost', port=6379, db=0)
    info = r.info()
    cmd_info = r.info('commandstats')

    return dict(info.items() + cmd_info.items())

def send_multi_metrics(instance_id, region, metrics, unit='Count', namespace='EC2/Redis'):
    cw = cloudwatch.connect_to_region(region)
    cw.put_metric_data(namespace, metrics.keys(), metrics.values(),
        unit=unit, dimensions={"InstanceId": instance_id})

if __name__ == '__main__':
    metadata = get_instance_metadata()
    instance_id = metadata['instance-id']
    region = metadata['placement']['availability-zone'][0:-1]
    redis_data = collect_redis_info()

    count_metrics = {
        'CurrConnections': redis_data['connected_clients'],
        'Evictions': redis_data['evicted_keys'],
        'Reclaimed': redis_data['expired_keys'],
        'CacheHits': redis_data['keyspace_hits'],
        'CacheMisses': redis_data['keyspace_misses'],
        'CurrItems': redis_data['db0']['keys']
    }

    byte_metrics = {
        'BytesUsedForCache': redis_data['used_memory'],
    }

    for command_group, commands in command_groups.items():
        count_metrics[command_group] = 0
        for command in commands:
            key = 'cmdstat_' + command
            if key in redis_data:
                count_metrics[command_group] += redis_data[key]['calls']

    print count_metrics
    send_multi_metrics(instance_id, region, count_metrics)
    send_multi_metrics(instance_id, region, byte_metrics, 'Bytes')
