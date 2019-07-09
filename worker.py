import config
import redis, time

def Start(level):
    '''
    Manager -> 不同层次error的log -> 最低1分钟为粒度:如果日志导出时间<1分钟, 则wait1分钟-可用时间, >1分钟, 则直接开始消费下一轮. 使用配置文件来获得redis的路径和错误码对应的数据库索引
    '''
    # 打开日志redis
    logs_redis = redis.Redis().from_url(config.LOGS_REDIS + '/' + level)
    # 打开mqredis
    mq_redis = redis.Redis().from_url(config.MQ_REDIS + '/0')
    # 工作循环
    while 1:
        began = time.time()
        # 循环读取所有的nodes
        cur = 0
        nex, keys = logs_redis.scan(cur)
        if cur != nex:
            cur = nex
            for node in keys:
                processNode(node, logs_redis, mq_redis)
        else:
            end = time.time()
            if end - began > config.WORKER_MINTIME:
                continue
            else:
                time.sleep(config.WORKER_MINTIME - (end - began))

def processNode(node, logs_redis, mq_redis):
    pass
