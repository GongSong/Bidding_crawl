import sys
import redis
from datetime import datetime,  timedelta
from DbHelper.DbHelper import DbHelper

class CacheData:
    __conn = ''    
    
    def __init__(self):
        self.__conn = redis.Redis(host="192.168.1.132", 
                                  port=6379,
                                  password='arkodata', 
                                  decode_responses=True)
        pass
    def __del__(self):        
        try:            
            self.__conn.close()
        except Exception as e:
            print('************************释放redis对象异常************************')
            print(repr(e).replace("'","").replace("\"",""))        
        pass

    def CurrentlyData(self,taskid,execid,mtWmPoiId) -> bool:        
        SetName = str(taskid) + str(execid)        
        Result = False
        if not self.__Exist(SetName,mtWmPoiId):
            self.__AddData(SetName,mtWmPoiId)
            Result = True        
        return Result         

    #添加数据
    def __AddData(self,Name,Value):
        self.__conn.sadd(Name,Value)        
        pass

    #判断数据是否存在
    def __Exist(self, name, value) -> bool:
        try:
            if self.__conn.sismember(str(name), str(value)) == 1:                
                return True            
            return False
        except Exception as e:            
            print(repr(e))
            return False    
    
    #清除已经回传的数据
    def ActiveClear(self,taskid,execid):
        try:
            sql = '''
                select count(*) as num
                from task
                where TaskTag = '%s' and Exec = '%s' and IsExcute < 3
            ''' % (str(taskid),str(execid))
            DbContext = DbHelper()
            result = DbContext.Query(sql)
            #等于1说明当前只剩下这个任务没有回传,因此可以清除
            if result[0]['num'] == 1:
                #清除这个set
                SetName = str(taskid) + str(execid)
                members = self.__conn.smembers(SetName)
                for mem in members:
                    self.__conn.srem(SetName,mem)                    
            del DbContext
        except Exception as e:
            print(repr(e))        
        pass