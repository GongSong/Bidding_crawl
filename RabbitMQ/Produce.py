# -*- encoding=utf8 -*-
import sys
import pika
import time
import configparser
import json
from RabbitMQ.RabbitMqBase import BaseRabbitMQ
from CommonPackage.CommonFunc import EncodeText,DecodeText
from DbHelper.DbHelper import DbHelper
from RedisManage.Cache import CacheData
import datetime
#生产者
class SendMessage(BaseRabbitMQ):
    __QueueName = 'result_mt'
    def __init__(self):
        BaseRabbitMQ.__init__(self)        
    
    #去重同一任务多次上传门店
    def __GoHeavy(self,taskid,execid,sendMessageList):
        try:
            r = CacheData()
            for msg in sendMessageList:
                if not r.CurrentlyData(taskid,execid,msg['Id']):
                    #去掉重复的
                    sendMessageList.remove(msg)
            #判断是否要清除缓存
            r.ActiveClear(taskid,execid)
        except Exception as e:
            DbContext = DbHelper()
            DbContext.AddLog('',4,'redis去重异常异常：' + repr(e).replace("'","").replace("\"",""))
            del DbContext
        return sendMessageList        
    
    def __DealSendMessage(self,taskId,sendMessageList):
        Result = str(sendMessageList)
        Data = {}
        Data['State'] = 1        
        DbContext = DbHelper()
        sql = '''
            select Id,StoreId,Lng,Lat,GeoHash,Province,CityCode,District,TaskTag,Exec
            from task 
            where TaskId = %d
        ''' % (int(taskId))
        receiveMsgList = DbContext.Query(sql)
        receiveMsgDict = receiveMsgList[0]
        Data['Id'] = receiveMsgDict['Id']
        Data['StoreId'] = receiveMsgDict['StoreId']
        Data['Lng'] = receiveMsgDict['Lng']
        Data['Lat'] = receiveMsgDict['Lat']
        Data['GeoHash'] = receiveMsgDict['GeoHash']        
        Data['Platform'] = 'mt'
        Data['Province'] = receiveMsgDict['Province']
        Data['City'] = receiveMsgDict['CityCode']
        Data['District'] = receiveMsgDict['District']
        Data['Task'] = receiveMsgDict['TaskTag']
        Data['Exec'] = receiveMsgDict['Exec']
        Data['Type'] = 'StoreGet'
        if len(sendMessageList) > 0:
            Data['Exists'] = 1      
            sendMessageList = self.__GoHeavy(Data['Task'],Data['Exec'],sendMessageList)
            if len(sendMessageList) > 0:   
                Data['Exists'] = 1 
            else:
                Data['Exists'] = 0
            Result = str(sendMessageList)
        else:
            Data['Exists'] = 0
        Data['Result'] = Result
        return str(Data)
    #发送错误数据
    def sendErrorMessage(self,message):
        try:
            #创建通道
            channel = self._conn.channel()
            
            # channel.queue_declare(queue=self.__QueueName)
            channel.basic_publish(exchange='', 
                                  routing_key=self.__QueueName,
                                  body = message,
                                  properties=pika.BasicProperties(delivery_mode=2,))
        except Exception as e:
            DbContext = DbHelper()
            DbContext.AddLog('',4,'发送队列出错数据异常：' + repr(e).replace("'","").replace("\"",""))
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print('发送队列出错数据异常：' + repr(e).replace("'","").replace("\"",""))
            del DbContext    
    #执行完当前任务就回写到队列
    def sendMessage(self,taskId,messageList):
        try:
            message = self.__DealSendMessage(taskId,messageList)
            #创建通道
            channel = self._conn.channel()                        
            #channel.queue_declare(queue=self.__QueueName,durable=True)
            EncodeTextMsg = EncodeText(message)            
            channel.basic_publish(exchange='', 
                                  routing_key=self.__QueueName,
                                  body = EncodeTextMsg,
                                  properties=pika.BasicProperties(delivery_mode=2,))                      
        except Exception as e:
            DbContext = DbHelper()
            DbContext.AddLog('',4,'发送数据异常：' + repr(e).replace("'","").replace("\"",""))
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print('发送队列出错数据异常：' + repr(e).replace("'","").replace("\"",""))
            del DbContext                        
            return False    
        else:        
            return True

    #执行回写失败的任务
    def BatchSendMessage(self):
        sql = '''
            update task
            set IsExcute = 1
            where IsExcute = 2
        '''
        DbContext = DbHelper()
        DbContext.Update(sql)
        pass
    