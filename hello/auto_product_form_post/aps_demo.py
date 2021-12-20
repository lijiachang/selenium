import time
from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
# 在每天22点，每隔 1分钟 运行一次 job 方法
scheduler.add_job(job, 'cron', hour=22, minute='*/1', args=['job1'])
# 在每天22和23点的25分，运行一次 job 方法
scheduler.add_job(job, 'cron', hour='22-23', minute='25', args=['job2'])

scheduler.start()
