#!/usr/bin/python3
import glob
import pymysql
from timeit import Timer
from DbHelper.DbHelper import DbHelper
import re
import json
from CommonPackage.CommonFunc import DecodeText,EncodeText

class DelStore():

    def delStore(self):
        DbContext = DbHelper()
        storelist = open("log.txt",mode='r')
        for index in range(16901):
            line = next(storelist)
            delline =str(line).split(',')[0]
            relust=DbContext.deleteStore(delline)
            print("删除第%d行 - %s" % (index,delline)+str(relust))
            
           

        pass
    def test(self):
        # addressNoNumer = re.sub('[0-9\零一二三四五六七八九十壹貳叁肆伍劉柒捌玖拾]','_',"慈利县-\六阳镇三阳中路（申鸿华都352—660号门面）")
        # print(addressNoNumer)
        receiveMsg = "H4sIAAAAAAAAC6tW8kxRsjK2MDI0N9JRCi7JL0oFCeSV5uToKPnkpStZGRqY6RmYmpiZGAMFEkuAig30zM2NLU1MdZTcU/M9EoszlKyUynPNi7LMTCoyigyzlXSUHFNSilKLi4EST2d0vmja9GL7ekNDs6f925/v63u6rv1Z07Knu9Y+bV3zdP3k52vWPNnV82xB98uZLU92NADVqAP5QApoTEBOYklaflEu0JzcEhC/KL8sMy85VcnK1NAACHSUnDNLKkE8Q2MQzyWzuKQoMxnoSLCIiY5SSGJxtpKVhYkRkO1akZoMZFuYAFUGFGXmF4H1GgIVVRYAjTSoBQCGr/33DQEAAA=="
        receiveMsgDict = json.loads(DecodeText(receiveMsg))   
        pass

dels =DelStore()
dels.test()

