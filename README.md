redis-cloudwatch
================

## About
Provides custom metrics for Redis in AWS CloudWatch similar to those provided by Redis in Elasticache.
## Pre-requsites
This requires that you have installed Boto and have created a [Boto configuration file](http://docs.pythonboto.org/en/latest/boto_config_tut.html) with your AWS credentials.

You'll want to run this script as a cronjob every minute:

    (crontab -l ; echo "* * * * * /<path_to_file>/cw-redis-stats.py")| crontab -
## Metrics Captured
| Metric   |  Description | Unit |
|----------|:-------------:|------:|
|CurrConnections | The number of client connections, excluding connections from read replicas. | Count
|Evictions | The number of keys that have been evicted due to the maxmemory limit. | Count
|Reclaimed | The total number of key expiration events. | Count
|BytesUsedForCache | The total number of bytes allocated by Redis. | Bytes
|CacheHits | The number of successful key lookups. | Count
|CacheMisses | The number of unsuccessful key lookups. | Count
|CurrItems | The number of items in the cache. This is derived from the Redis keyspace statistic, summing all of the keys in the entire keyspace. | Count
