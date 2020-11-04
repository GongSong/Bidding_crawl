# -*- encoding=utf8 -*-
import os
from DbHelper.DbHelper import DbHelper
import psutil
import datetime


# 设备运行情况检查
def RunningCheck():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 设备运行情况检测 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    RunDevice = []
    # 检查设备程序是否在运行
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['cmdline'])
            if type(pinfo['cmdline']).__name__ != 'NoneType':
                if len(pinfo['cmdline']) > 0:
                    # 格式['python','main.py']
                    if '/bin/sh' == pinfo['cmdline'][0] and pinfo['cmdline'][1] == '-c':
                        command = str(pinfo['cmdline'][2])
                        print(command)
                        command = command.replace(".py", "").replace("PyDaemon", "").replace('./', "").replace(" ", "").replace("-d", "")
                        if 'python3.7' in command:
                            deviceNum = command.replace("python3.7", "")[:16]
                            if deviceNum not in RunDevice:
                                RunDevice.append(deviceNum)
                    pass
        except psutil.NoSuchProcess as e:
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 检测设备状态异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(repr(e))
            continue

    # 这里会限制只能重启8台
    if len(RunDevice) < 9:
        # 获取没有运行的设备
        DbContext = DbHelper()
        DeviceDict = ['5LM0216902001108', '5LM0216910000994', '5LM0216B03001264', 'APU0216408028484', 'DLQ0216630004610', 'E4J4C17405011422', 'DLQ0216729004546']
        DeviceList = []
        for devicenum in DeviceDict:
            DeviceList.append(devicenum)
        NotRunningDevice = list(set(DeviceList).difference(set(RunDevice)))
        if len(NotRunningDevice) > 0:
            # 启动没有运行的设备的Daemon
            for deviceNum in NotRunningDevice:
                try:
                    os.popen(
                        'python3.7 ' + deviceNum + '.py >> /root/airtest/log/Device/Runniglog' + datetime.datetime.now().strftime(
                            "%Y%m%d") + '.log')
                    DbContext.AddLog(deviceNum, 1, '启动设备[' + deviceNum + ']执行任务')
                except Exception as e:
                    print(
                        '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 重启设备[' + deviceNum + ']异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    DbContext.AddLog(deviceNum, 3, '重启设备[' + deviceNum + ']异常 ' + repr(e).replace("'", ""))
                    pass

