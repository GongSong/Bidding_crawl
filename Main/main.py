# -*- encoding=utf8 -*-
from Product.GetsData import get_shopName, write_excel

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
from Product.SearchStore import SearchCatchStore, search_store
import datetime
import time
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler

conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()

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
            elif mode == 6:  # 根据店名爬取
                sched = BlockingScheduler()
                while True:
                    @sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=0, end_date='2020-10-10')
                    def job():
                        device.wake()
                        # 1, 存到1表
                        if(DeviceNum == "DLQ0216630004610"):  # 爬取我方的72家
                            res = get_shopName()
                            count = len(res[1])  # 取出返回元组的药店名
                            other_shop = res[1]
                            sql = 'select shop_index, spider_num from shopindex where device_num="DLQ0216630004610"'
                            cursor.execute(sql)
                            shopindex = cursor.fetchone()
                            flag = int(shopindex[0])
                            spider_num = int(shopindex[1])
                            for i in range(flag, 31):
                                storeName = other_shop[i]
                                print(storeName, '第' + str(i) + '家店')
                                search_store(storeName, poco, device, DeviceNum, DeviceType, i, spider_num)
                                f = i + 1
                                sql1 = 'update shopindex set shop_index=%s where device_num="DLQ0216630004610"'%str(f)
                                cursor.execute(sql1)
                                conn.commit()
                                BackHomePage(poco, DbContext, DeviceNum, device)
                                write_excel(str(spider_num)+'-'+str(i))
                            spider_num += 1
                            sql1 = 'update shopindex set shop_index=0, spider_num=%s where device_num="DLQ0216630004610"'%(spider_num)
                            cursor.execute(sql1)
                            conn.commit()
                        # 2，
                        elif DeviceNum == 'DLQ0216729004546':  # E4J4C17405011422， 5LM0216B03001264
                            res = get_shopName()
                            other_shop = res[1]  # 取出返回元组的药店名
                            sql = 'select shop_index, spider_num from shopindex where device_num="DLQ0216729004546"'
                            cursor.execute(sql)
                            shopindex2 = cursor.fetchone()
                            flag = int(shopindex2[0])
                            spider_num = int(shopindex2[1])
                            for k in range(flag, 62):
                                storeName = other_shop[k]
                                print(storeName, '第' + str(k) + '家店')
                                search_store(storeName, poco, device, DeviceNum, DeviceType, k, spider_num)
                                f = k + 1
                                sql1 = 'update shopindex set shop_index=%s where device_num="DLQ0216729004546"' % str(f)
                                cursor.execute(sql1)
                                conn.commit()
                                BackHomePage(poco, DbContext, DeviceNum, device)
                                write_excel(str(spider_num)+'-'+str(k))
                            spider_num += 1
                            sql1 = 'update shopindex set shop_index=31, spider_num=%s where device_num="DLQ0216729004546"'%(spider_num)
                            cursor.execute(sql1)
                            conn.commit()
                        # 3 ; 存到1表
                        elif DeviceNum == 'E4J4C17405011422':
                            res = get_shopName()
                            other_shop = res[1]  # 取出返回元组的药店名
                            sql = 'select shop_index, spider_num from shopindex where device_num="E4J4C17405011422"'
                            cursor.execute(sql)
                            shopindex3 = cursor.fetchone()
                            flag = int(shopindex3[0])
                            spider_num = int(shopindex3[1])
                            for j in range(flag, 93):
                                storeName = other_shop[j]
                                print(storeName, '第' + str(j) + '家店')
                                search_store(storeName, poco, device, DeviceNum, DeviceType, j, spider_num)
                                f = j + 1
                                sql1 = 'update shopindex set shop_index=%s where device_num="E4J4C17405011422"' % str(f)
                                cursor.execute(sql1)
                                conn.commit()
                                BackHomePage(poco, DbContext, DeviceNum, device)
                                write_excel(str(spider_num)+'-'+str(j))
                            spider_num += 1
                            sql1 = 'update shopindex set shop_index=62, spider_num=%s where device_num="E4J4C17405011422"'%(spider_num)
                            cursor.execute(sql1)
                            conn.commit()
                        # 4，
                        elif DeviceNum == '5LM0216910000994':
                            res = get_shopName()
                            other_shop = res[1]  # 取出返回元组的药店名
                            sql = 'select shop_index, spider_num from shopindex where device_num="5LM0216910000994"'
                            cursor.execute(sql)
                            shopindex4 = cursor.fetchone()
                            flag = int(shopindex4[0])
                            spider_num = int(shopindex4[1])
                            count = len(res[1])
                            for l in range(flag, 124):
                                storeName = other_shop[l]
                                print(storeName, '第' + str(l) + '家店')
                                search_store(storeName, poco, device, DeviceNum, DeviceType, l, spider_num)
                                f = l + 1
                                sql1 = 'update shopindex set shop_index=%s where device_num="5LM0216910000994"' % str(f)
                                cursor.execute(sql1)
                                conn.commit()
                                BackHomePage(poco, DbContext, DeviceNum, device)
                                write_excel(str(spider_num)+'-'+str(l))
                            spider_num += 1
                            sql1 = 'update shopindex set shop_index=93, spider_num=%s where device_num="5LM0216910000994"'%(spider_num)
                            cursor.execute(sql1)
                            conn.commit()
                        # 5,
                        elif (DeviceNum == "5LM0216B03001264"):
                            res = get_shopName()
                            other_shop = res[1]
                            sql = 'select shop_index, spider_num from shopindex where device_num="5LM0216B03001264"'
                            cursor.execute(sql)
                            shopindex = cursor.fetchone()
                            flag = int(shopindex[0])
                            spider_num = int(shopindex[1])
                            for i in range(flag, 155):
                                storeName = other_shop[i]
                                print(storeName, '第' + str(i) + '家店')
                                search_store(storeName, poco, device, DeviceNum, DeviceType, i, spider_num)
                                f = i + 1
                                sql1 = 'update shopindex set shop_index=%s where device_num="5LM0216B03001264"' % str(f)
                                cursor.execute(sql1)
                                conn.commit()
                                BackHomePage(poco, DbContext, DeviceNum, device)
                                write_excel(str(spider_num)+'-'+str(i))
                            spider_num += 1
                            sql1 = 'update shopindex set shop_index=124, spider_num=%s where device_num="5LM0216B03001264"' % (
                                spider_num)
                            cursor.execute(sql1)
                            conn.commit()
                        # 6,
                        elif (DeviceNum == "APU0216408028484"):
                            res = get_shopName()
                            count = len(res[1])  # 取出返回元组的药店名
                            other_shop = res[1]
                            sql = 'select shop_index, spider_num from shopindex where device_num="APU0216408028484"'
                            cursor.execute(sql)
                            shopindex = cursor.fetchone()
                            flag = int(shopindex[0])
                            spider_num = int(shopindex[1])
                            for i in range(flag, 191):
                                storeName = other_shop[i]
                                print(storeName, '第' + str(i) + '家店')
                                search_store(storeName, poco, device, DeviceNum, DeviceType, i, spider_num)
                                f = i + 1
                                sql1 = 'update shopindex set shop_index=%s where device_num="APU0216408028484"' % str(f)
                                cursor.execute(sql1)
                                conn.commit()
                                BackHomePage(poco, DbContext, DeviceNum, device)
                                write_excel(str(spider_num)+'-'+str(i))
                            spider_num += 1
                            sql1 = 'update shopindex set shop_index=155, spider_num=%s where device_num="APU0216408028484"' % (
                                spider_num)
                            cursor.execute(sql1)
                            conn.commit()
                    sched.start()

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
