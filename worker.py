import config
import redis, time, json

def Start(level):
    '''
    Manager -> 不同层次error的log -> 最低1分钟为粒度:如果日志导出时间<1分钟, 则wait1分钟-可用时间, >1分钟, 则直接开始消费下一轮. 使用配置文件来获得redis的路径和错误码对应的数据库索引
    '''
    # 打开日志redis
    logs_redis = redis.Redis().from_url(config.LOGS_REDIS + '/' + str(level))
    # 打开mqredis
    mq_redis = redis.Redis().from_url(config.MQ_REDIS + '/0')
    # 工作循环
    while 1:
        print('处理 ' + str(level) + ' 的日志')
        began = time.time()
        cur = 0
        while 1:
            # 循环读取所有的nodes
            nex, keys = logs_redis.scan(cur)
            for node in keys:
                processNode(node, level, logs_redis, mq_redis)
            if nex != 0:
                cur = nex
            else:
                end = time.time()
                if (end - began) > config.WORKER_MINTIME:
                    pass
                else:
                    print(str(level) + ' 日志处理过快，休眠一会')
                    time.sleep(config.WORKER_MINTIME - (end - began))
                break        

def processNode(node, level, logs_redis, mq_redis):
    print('处理类型 ' + str(level) + ' 节点 ' + str(node))
    try:
        res = logs_redis.lrange(node, 0, config.WORKER_BATCHSIZE - 1)
    except:        
        res = None
    if res == None:
        return
    count = 0
    while len(res):
        # 删除老的日志
        logs_redis.ltrim(node, config.WORKER_BATCHSIZE, -1)
        # print('发送节点 ' + str(node) + ' 的 ' + str(len(res)) + ' 条日志')        
        count += len(res)
        # 处理拿到的日志
        for log in res:
            try:
                msg = json.loads(str(log))
            except:
                msg = {'m': str(log)}
            msg['n'] = str(node)
            msg['l'] = level
            mq_redis.publish(bytes(config.MQ_CHANNEL, 'utf-8'), json.dumps(msg, separators=(',', ':')))
        # 获取下一批
        res = logs_redis.lrange(node, 0, config.WORKER_BATCHSIZE - 1)
    print('发送类型 ' + str(level) + ' 节点 ' + str(node) + ' 的 ' + str(count) + ' 条日志')

