from DaemonTask import RunningCheck

import datetime
import os


def main():
    # 启动设备
    start_device = ['5LM0216902001108', '5LM0216910000994', '5LM0216B03001264', 'APU0216408028484', 'DLQ0216630004610', 'E4J4C17405011422']
    for deviceNum in start_device:
        print(deviceNum)
        try:
            os.popen('python3.7 ' + deviceNum + '.py  >> /root/airtest/log/Device/Runniglog' + datetime.datetime.now().strftime("%Y%m%d") + '.log')
        except:
            print(
                '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 重启设备[' + deviceNum + ']异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            pass


if __name__ == '__main__':
    main()
    # 检查设备是否运行
    while True:
        RunningCheck()