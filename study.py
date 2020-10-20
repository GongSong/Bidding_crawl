#!/usr/bin/python3
import glob
import pymysql
from timeit import Timer
from DbHelper.DbHelper import DbHelper
import re
import json
from CommonPackage.CommonFunc import DecodeText, EncodeText


from airtest.core.android import Android
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
class DelStore():

    def delStore(self):
        DbContext = DbHelper()
        storelist = open("log.txt", mode='r')
        for index in range(16901):
            line = next(storelist)
            delline = str(line).split(',')[0]
            relust = DbContext.deleteStore(delline)
            print("删除第%d行 - %s" % (index, delline)+str(relust))

        pass

    def test(self):
        DeviceNum = 'APU0215B25001477'
        device = Android(DeviceNum)
        poco = AndroidUiautomationPoco(device)
        
        poco.swipe([0.4, 0.8], [0.4, 0.5], duration=0.3)
        pass


dels = DelStore()
dels.test()
