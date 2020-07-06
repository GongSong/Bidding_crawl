# -*- encoding=utf8 -*-
import sys
import os
import psutil
import time
from DbHelper.DbHelper import DbHelper
from CommonPackage.GlobalParameter import DaemonHeartbeat
import datetime
import argparse


while True:
    # 判断程序是否是自己停掉，否则就要重启
    DbContext = DbHelper()
    lateTaskTime = DbContext.getLateTaskTime()
    if len(lateTaskTime) > 0:
        lateTime = lateTaskTime[0]["ExcuteTime"]
        newTime = datetime.datetime.now()
        # 每次任务执行完后检查一下是否有中断的任务，并重启中断的任务
        if(((newTime - lateTime).seconds)/60 > 60 or (newTime - lateTime).days > 0):
            print("最后执行的任务执行了"+str((newTime - lateTime).days) +
                  "天"+str(((newTime - lateTime).seconds)/60)+"分钟还没完成,重启任务")
            # 把意外中断的任务重启
            DbContext.rebootTask()
    time.sleep(DaemonHeartbeat)
pass
