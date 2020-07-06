#!/usr/bin/python3
import glob
import pymysql
from timeit import Timer
from DbHelper.DbHelper import DbHelper
import re
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
        addressNoNumer = re.sub('[0-9\零一二三四五六七八九十壹貳叁肆伍劉柒捌玖拾]','_',"慈利县-\六阳镇三阳中路（申鸿华都352—660号门面）")
        print(addressNoNumer)
        pass

dels =DelStore()
dels.test()

