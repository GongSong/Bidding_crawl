# -*- encoding=utf8 -*-
__author__ = "lwq"
from poco.proxy import UIObjectProxy
from airtest.core.android import Android
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Operate.BackHomePage import BackHomePage
from Operate.GetAddress import AddressList
from StoreInfo.StoreList import StartCapture
from DbHelper.DbHelper import DbHelper
from Operate.GetAddress import getAddressFromGaoDe
from RabbitMQ.Produce import SendMessage
from Operate.ClearMemcache import ClearMemory
from Product.SearchStore import SearchCatchStore
import datetime
import time


def main(DeviceNum):
    # 多设备连接时,可指定设备编号
    # python -m airtest run main.py --device Android://127.0.0.1:5037/0123456789ABCDEF
    # device = Android('GWY0216C16002906')
    # 设备类型 1 手机[720,1280][1080,1920] 2平板[1200,1920]
    # DeviceNum = 'c5bac654'
    NeedSwipe = ['CLB0218414001154', 'DLQ0216824000142', 'E4J4C17405011422',
                 'APU0216530000778', 'APU0216408028484', 'APU0216111008105']
    try:
        DbContext = DbHelper()
        DeviceType = 0
        device = Android(DeviceNum)
        # device.adb.start_shell("su")
        # device.adb.start_shell("wipe data")
        # device.adb.start_shell("wipe cache")
        # device.adb.start_cmd("adb reboot")

        if '0123456789ABCDEF' not in DeviceNum:
            device.wake()  # 唤醒页面
            poco = AndroidUiautomationPoco(device)
            # if DeviceNum in NeedSwipe:
            poco.swipe([0.4, 0.9], [0.4, 0.55], duration=0.1)
            time.sleep(2)
            # 复位一下,防止之前没有睡眠也滑动
            poco.swipe([0.4, 0.45], [0.4, 0.9], duration=0.1)
        else:
            poco = AndroidUiautomationPoco(
                use_airtest_input=True, screenshot_each_action=False)
        # ClearMemory(device,poco,'')
        # return
        device_screen = poco.get_screen_size()
        device_x = device_screen[0]
        device_y = device_screen[1]
        print(str(device_y), str(device_x))
        if device_y > 1600 and device_x > 1080:
            DeviceType = 2
        else:
            DeviceType = 1
        if DeviceType == 0:
            print(
                '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 设备型号无法确定 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            DbContext.AddLog(DeviceNum, 3, '设备[' + DeviceNum + ']型号无法确定')
            return
        elif DeviceType == 1:
            print(
                '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 设备型号为手机 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        else:
            print(
                '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 设备型号为平板 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    except Exception as e:
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 设备连接异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        DbContext.AddLog(
            DeviceNum, 3, "设备[" + DeviceNum + "]连接异常：" + repr(e).replace("'", ""))
    else:
        BackHomeStatus = BackHomePage(
            poco, DbContext, DeviceNum, device)  # 返回首页
        if BackHomeStatus:
            mode = DbContext.GetDeviceRunningMode(DeviceNum)
            taskList = []
            # 获取当前设备要抓取的城市
            IsRunning = True
            if mode == 1:
                taskList = DbContext.GetDeviceTask(DeviceNum)
            elif mode == 2:
                taskList = DbContext.GetDeviceTaskByMode2()
            elif mode == 3:
                taskList = DbContext.GetDeviceTaskByMode3()
            elif mode == 5:
                IsRunning = False
            elif mode == 6:
                storeId = []
                if(DeviceNum == "0123456789ABCDEF"):
                    storeIds = []
                    # storeIds.append("e2c11bfe305b11ea8d92005056c00008")
                    # storeIds.append("0a06a048683a11eabb8500bb602e7439")
                    # storeIds.append("830d55d4c69c11ea81d100e04c81a0a3")
                    # storeIds.append("8b23a394c69d11ea895900e04c680875")
                    storeIds.append("a3323206a92f11eaa84700e04c680875")
                    # storeIds.append("4dc00ce6305a11ea89c6005056c00008")
                    for storeId in storeIds:
                        SearchCatchStore(storeId,
                                         poco, device, DeviceNum, DeviceType)
                        BackHomePage(
                            poco, DbContext, DeviceNum, device)  # 返回首页
                    BackHomePage(
                        poco, DbContext, DeviceNum, device)  # 返回首页
                elif(DeviceNum == "APU0215B25001477"):
                    storeIds = []
                    # storeIds.append("c6c3ad12305a11ea882a005056c00008")
                    # storeIds.append("dd386e06305911eaa34f005056c00008")
                    storeIds.append("99d93998305911ea8599005056c00008")

                    storeIds.append("7f3bd434305a11ea9d80005056c00008")
                    storeIds.append("d77bc6f83b2a11ea98ad00e04c680875")
                    storeIds.append("cffd8840305a11ea8ef2005056c00008")
                    storeIds.append("a65e8b00305a11eaaabc005056c00008")
                    storeIds.append("196f949e305911eab629005056c00008")
                    storeIds.append("8e45a038305911ea94b7005056c00008")


                    for storeId in storeIds:
                        SearchCatchStore(storeId,
                                         poco, device, DeviceNum, DeviceType)
                        BackHomePage(
                            poco, DbContext, DeviceNum, device)  # 返回首页

                elif(DeviceNum == "APU0216530000778"):
                    storeId = "d89e35ec845f11ea802b00e04c680875"
                elif(DeviceNum == 'APU0215C11003517'):
                    # [以岭]人参片100g
                    storeId = "96c26e8c305a11ea9505005056c00008"
                    SearchCatchStore(storeId,
                                     poco, device, DeviceNum, DeviceType)
                # if(storeId != ""):
                #     for idsd in storeId:
                #         SearchCatchStore(idsd,
                #                  poco, device, DeviceNum, DeviceType)
            if(len(taskList) == 1):
                # 更新任务为运行中
                DbContext.UpdateTaskStatus(
                    int(taskList[0]['TaskId']), 1, 0, mode)
            while IsRunning:
                BackHomeStatus = BackHomePage(
                    poco, DbContext, DeviceNum, device)  # 返回首页
                if BackHomeStatus:
                    for task in taskList:
                        # AddressList(task['TargetCity']) #获取未抓取的坐标点
                        AllPosition = [
                            {'RepresentativeAdress': task['RepresentativeAdress'], 'Genhash':task['Genhash']}]
                        taskId = task['TaskId']
                        cityCode = task['CityCode']
                        # 更新任务为运行中
                        DbContext.UpdateTaskStatus(int(taskId), 1, 0, mode)
                        # 计时
                        StartTime = datetime.datetime.now()
                        # 返回值需要写进队列
                        currentTaskResult, IsEmergencyStop = StartCapture(
                            poco, AllPosition, DeviceType, task['TargetCity'], DeviceNum, cityCode, device)  # 抓取数据
                        # 没有紧急置停的情况下才完成后续的更新
                        if not IsEmergencyStop:
                            EndTime = datetime.datetime.now()
                            DbContext = DbHelper()
                            DbContext.AddLog(DeviceNum, 2, '设备[' + DeviceNum + ']本次抓取[' + AllPosition[0]['RepresentativeAdress'] + '] [' + str(
                                len(currentTaskResult)) + '] 家店,耗时：' + str(((EndTime - StartTime).seconds)/60))
                            # 更新任务为完成
                            DbContext.UpdateTaskStatus(
                                int(taskId), 2, len(currentTaskResult), mode)
                            # 将任务的执行结果回写到队列
                            if mode != 3:
                                Produce = SendMessage()
                                result = Produce.sendMessage(
                                    taskId, currentTaskResult)
                                if result:
                                    # 将任务状态改为已回写队列
                                    DbContext.UpdateTaskStatus(
                                        int(taskId), 3, len(currentTaskResult), mode)
                        else:
                            break
                    mode = DbContext.GetDeviceRunningMode(DeviceNum)
                    if len(taskList) > 0:
                        taskList.clear()
                    if mode == 1:
                        taskList = DbContext.GetDeviceTask(DeviceNum)
                    elif mode == 2:
                        taskList = DbContext.GetDeviceTaskByMode2()
                    elif mode == 3:
                        taskList = DbContext.GetDeviceTaskByMode3()
                    elif mode == 5:
                        print(
                            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 紧急置停 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        break
                    if len(taskList) > 0:
                        print(
                            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 抽取一条任务 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    else:
                        print(
                            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 任务执行完毕 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

                        break
                else:
                    DbContext.AddLog(
                        DeviceNum, 3, '设备[' + DeviceNum + ']返回首页异常')
                    break
        else:
            DbContext.AddLog(DeviceNum, 3, '设备[' + DeviceNum + ']返回首页异常')
