redis-cloudwatch
================

## About
Provides custom metrics for [Redis](http://redis.io) in AWS CloudWatch similar to those provided by Redis in Elasticache.
## Pre-requsites
This requires that you have installed [Boto](https://github.com/boto/boto) and have created a [Boto configuration file](http://docs.pythonboto.org/en/latest/boto_config_tut.html) with your AWS credentials. You'll want to run this script as a cronjob every minute.
## Install
    curl https://raw.githubusercontent.com/brianantonelli/redis-cloudwatch/master/cw-redis-stats.py | sudo tee /usr/local/bin/cw-redis-stats.py
    sudo chmod +x /usr/local/bin/cw-redis-stats.py
    (crontab -l ; echo "* * * * * /usr/local/bin/cw-redis-stats.py")| crontab -


## Metrics Captured
| Metric   |  Description | Unit |
|----------|:-------------|:------|
|CurrConnections | The number of client connections, excluding connections from read replicas. | Count
|Evictions | The number of keys that have been evicted due to the maxmemory limit. | Count
|Reclaimed | The total number of key expiration events. | Count
|BytesUsedForCache | The total number of bytes allocated by Redis. | Bytes
|CacheHits | The number of successful key lookups. | Count
|CacheMisses | The number of unsuccessful key lookups. | Count
|CurrItems | The number of items in the cache. This is derived from the Redis keyspace statistic, summing all of the keys in the entire keyspace. | Count
##Aggregated Command Metrics Captured
| Metric   |  Description | Unit |
|----------|:-------------|:------|
|GetTypeCmds | The total number of get types of commands. This is derived from the Redis commandstats statistic by summing all of the get types of commands (get, mget, hget, etc.) | Count
|SetTypeCmds | The total number of set types of commands. This is derived from the Redis commandstats statistic by summing all of the set types of commands (set, hset, etc.) | Count
|KeyBasedCmds | The total number of commands that are key-based. This is derived from the Redis commandstats statistic by summing all of the commands that act upon one or more keys. | Count
|StringBasedCmds | The total number of commands that are string-based. This is derived from the Redis commandstats statistic by summing all of the commands that act upon one or more strings. | Count
|HashBasedCmds | The total number of commands that are hash-based. This is derived from the Redis commandstats statistic by summing all of the commands that act upon one or more hashes. | Count
|ListBasedCmds | The total number of commands that are list-based. This is derived from the Redis commandstats statistic by summing all of the commands that act upon one or more lists. | Count
|SetBasedCmds | The total number of commands that are set-based. This is derived from the Redis commandstats statistic by summing all of the commands that act upon one or more sets. | Count
|SortedSetBasedCmds | The total number of commands that are sorted set-based. This is derived from the Redis commandstats | Count
|HyperLogLogBasedCmds | The total number of commands that are hyperloglog-based. This is derived from the Redis commandstats | Count 
|ScriptBasedCmds | The total number of commands that are script-based. This is derived from the Redis commandstats | Count

