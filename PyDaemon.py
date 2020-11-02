# -*- encoding=utf8 -*-
import sys
import os
import psutil
import time
from DbHelper.DbHelper import DbHelper
from CommonPackage.GlobalParameter import DaemonHeartbeat
import datetime
import argparse

try:
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-d','--DeviceNum', default='')
    args = parser.parse_args()
    DeviceNum = args.DeviceNum
    RestartExcepNum = 0
    AllowRun = False
    if DeviceNum != '':
        AllowRun = True
except Exception as e:
    print('获取设备编号失败：' + repr(e))
    AllowRun = False
while AllowRun:    
    isRunning = False
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['cmdline'])            
            if type(pinfo['cmdline']).__name__ != 'NoneType':
                if len(pinfo['cmdline']) > 0:
                    for item in pinfo['cmdline']:
                        if item == 'python3.7':
                            continue
                        elif item == DeviceNum+'.py':
                            isRunning = True
                            break
                        else:
                            break
                    pass
                else:
                    continue
            if isRunning:
                
                break
        except psutil.NoSuchProcess:
            pass    
    if isRunning:    
        pass
    else:
        # 判断程序是否是自己停掉，否则就要重启
        DbContext = DbHelper()
        mode = DbContext.GetDeviceRunningMode(DeviceNum) 
        if mode == 1:
            taskList = DbContext.GetDeviceTask(DeviceNum)
        elif mode == 2:
            taskList = DbContext.GetDeviceTaskByMode2()   
        elif mode == 3:
            taskList = DbContext.GetDeviceTaskByMode3()    
        elif mode == 5:
            taskList = []   
        elif mode == 6:
            taskList = []

        if len(taskList) > 0:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Reatarting~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')                       
            try:
                path = '/root/airtest/log/Device/' + datetime.datetime.now().strftime("%Y%m%d") + '/'
                if not os.path.exists(path):
                    os.mkdir(path)
                if  os.path.exists('/root/airtest/'+DeviceNum+'.py'):  
                    os.popen('python3.7 '+ DeviceNum +'.py &>> '+ path + DeviceNum + '.log')
            except Exception as e:            
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 重启程序异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')                
                if RestartExcepNum > 20:
                    break        
    time.sleep(DaemonHeartbeat)
pass