import json

CFG = json.loads(''.join(open('./config.json').readlines()))

# nnt框架日志保存的redis
LOGS_REDIS = CFG['logsredis']
# 通知logstash时使用的mq设置
MQ_CHANNEL = CFG['channel']
MQ_REDIS = CFG['mqredis']
# worker消费日志的最小工作时间
WORKER_MINTIME = CFG['minworktime']
# worker消费日志的批量大小
WORKER_BATCHSIZE = CFG['batchsize']
