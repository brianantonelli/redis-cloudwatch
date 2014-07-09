#!/usr/bin/env python
'''
Send Redis usage metrics to Amazon CloudWatch

This is intended to run on an Amazon EC2 instance and requires a boto config 
(~/.boto) allowing to write CloudWatch metrics.
'''

import redis
from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata

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

    # TODO: agg'd command metrics (http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/CacheMetrics.Redis.html)

    send_multi_metrics(instance_id, region, count_metrics)
    send_multi_metrics(instance_id, region, byte_metrics, 'Bytes')
