# -*- encoding=utf8 -*-
import sys
import pika
import configparser
import json
import os
from RabbitMQ.RabbitMqBase import BaseRabbitMQ
from RabbitMQ.Produce import SendMessage
from CommonPackage.CommonFunc import DecodeText,EncodeText
from DbHelper.DbHelper import DbHelper
from Entity.AllEntity import task
import psutil
import requests as rq
import datetime
#消费者
class ReceiveMessage(BaseRabbitMQ):  
    __receiveNum = 0     
    __QueueName = 'task_mt'    
    
    def __init__(self):
        BaseRabbitMQ.__init__(self)   

    #设备运行情况检查
    def __RunningCheck(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 设备运行情况检测 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        RunDevice = []    
        #检查设备程序是否在运行
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['cmdline'])            
                if type(pinfo['cmdline']).__name__ != 'NoneType':
                    if len(pinfo['cmdline']) > 0:
                        #格式['python','main.py']                        
                        if '/bin/sh' == pinfo['cmdline'][0] and pinfo['cmdline'][1] == '-c':
                            command = str(pinfo['cmdline'][2])       
                            command = command.replace(".py","").replace("PyDaemon","").replace('./',"").replace(" ","").replace("-d","")
                            if 'python3.7' in command:                            
                                deviceNum = command.replace("python3.7","")[:16]
                                if deviceNum not in RunDevice:
                                    RunDevice.append(deviceNum)
                        pass
            except psutil.NoSuchProcess as e:
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 检测设备状态异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print(repr(e))
                continue
                   
        if len(RunDevice) < 9:
            #获取没有运行的设备
            DbContext = DbHelper()
            DeviceDict = DbContext.GetAllDevice()
            DeviceList = []
            for devicenum in DeviceDict:
                DeviceList.append(devicenum['DeviceNum'])
            NotRunningDevice = list(set(DeviceList).difference(set(RunDevice)))
            if len(NotRunningDevice) > 0:                
                #启动没有运行的设备的Daemon
                for deviceNum in NotRunningDevice:                
                    try:                        
                        os.popen('python3.7 ./PyDaemon.py -d '+ deviceNum +' >> /root/airtest/log/Device/Runniglog'+ datetime.datetime.now().strftime("%Y%m%d") +'.log')
                        DbContext.AddLog(deviceNum,1,'启动设备[' + deviceNum + ']执行任务')
                    except Exception as e:
                        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 重启设备['+ deviceNum +']异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        DbContext.AddLog(deviceNum,3,'重启设备['+ deviceNum +']异常 ' + repr(e).replace("'",""))
                        pass  
            del DbContext

    #根据经纬度获取地址
    def __GetAddressByLngLat(self,Lng,Lat):
        key = '929d86bb3c93b6895554459ab7893171'    
        try:
            url = 'https://restapi.amap.com/v3/geocode/regeo?key=' + key + '&location=' + str(Lng) + ',' + str(Lat) + '&poitype=&radius=1000&extensions=base&batch=false&roadlevel=1'            
            req = rq.get(url)
            dataDic = json.loads(req.text)
            address = ''
            businessaddress = ''
            if int(dataDic['status']) == 1:
                baseaddress = str(dataDic['regeocode']['formatted_address'])  #基础地址
                if 'addressComponent' in dataDic['regeocode']:
                    if 'businessAreas' in dataDic['regeocode']['addressComponent']:                        
                        if len(dataDic['regeocode']['addressComponent']['businessAreas']) > 0:                                               
                            result = dataDic['regeocode']['addressComponent']['businessAreas'][0]                                                                                    
                            if len(result) > 0:                                    
                                if 'name' in result:                                    
                                    businessaddress = result["name"]                        
                               
                address = baseaddress + businessaddress            
        except Exception as e:
            #吞掉异常
            DbContext = DbHelper()
            DbContext.AddLog('',4,'地址转换异常：' + repr(e))
            del DbContext                     
        return address.replace('|','').replace(' ','').replace('·','')      

    #持久化消息出错时的回传信息
    def __ErrorReturn(self,receiveMsgDict):
        ErrorResult = {}
        ErrorResult['State'] = 0
        ErrorResult['Exists'] = 0
        ErrorResult['Result'] = str([])
        ErrorResult['Id'] = receiveMsgDict['Id']
        if receiveMsgDict['StoreId'] == None:
            ErrorResult['StoreId'] = ''
        else:
            ErrorResult['StoreId'] = receiveMsgDict['StoreId']
        ErrorResult['Lng'] = receiveMsgDict['Lng']
        ErrorResult['Lat'] = receiveMsgDict['Lat']
        ErrorResult['GeoHash'] = receiveMsgDict['GeoHash']
        ErrorResult['Platform'] = receiveMsgDict['Platform']
        ErrorResult['Province'] = receiveMsgDict['Province']
        ErrorResult['City'] = receiveMsgDict['City']
        ErrorResult['District'] = receiveMsgDict['District']
        ErrorResult['Task'] = receiveMsgDict['Task']
        ErrorResult['Exec'] = receiveMsgDict['Exec']
        ErrorResult['Type'] = receiveMsgDict['Type']
        return EncodeText(str(ErrorResult))
          
    def __callback(self,ch, method, properties, body):
        try:                        
            receiveMsg = str(body,encoding="utf-8")            
            receiveMsgDict = json.loads(DecodeText(receiveMsg))                       
            Id = receiveMsgDict['Id']
            if receiveMsgDict['StoreId'] == None:
                StoreId = ''
            else:
                StoreId = receiveMsgDict['StoreId']            
            Lng = receiveMsgDict['Lng']
            Lat = receiveMsgDict['Lat']
            GeoHash = str(receiveMsgDict['GeoHash'])
            Province = receiveMsgDict['Province']
            District = receiveMsgDict['District']
            City = receiveMsgDict['City']
            Task = receiveMsgDict['Task']       
            Exec = receiveMsgDict['Exec']     
            Address = ''
            if receiveMsgDict['Address'] != None and receiveMsgDict['Address'] != '':
                Address = str(receiveMsgDict['Address']).replace("|","")
            else:
                if '0.0' in str(Lng) or '0.0' in str(Lat):  
                    errorResult = self.__ErrorReturn(receiveMsgDict)
                    producer = SendMessage()
                    if ch.is_open:
                        ch.basic_ack(delivery_tag = method.delivery_tag)           
                        producer.sendErrorMessage(errorResult)
                        #记录一下异常的点
                        DbContext = DbHelper()                
                        DbContext.AddLog('',4,'持久化任务错误：当前任务的经纬度为0,不做处理！')
                        print('持久化任务错误：当前任务的经纬度为0,不做处理！')
                    return                 
                else:
                    print('没有包含地址,调用高德地图获取地址！')
                    Address = self.__GetAddressByLngLat(Lng,Lat)    
        except Exception as e:         
            errorResult = self.__ErrorReturn(receiveMsgDict)
            producer = SendMessage()
            producer.sendErrorMessage(errorResult)        
            DbContext.AddLog('',4,'回调方法处理消息异常' + repr(e).replace("'","").replace("\"","") + '[队列消息]：' + receiveMsg)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print('回调方法处理消息异常' + repr(e).replace("'","").replace("\"","") + '[队列消息]：' + receiveMsg)
            del producer
        else:
            try:            
                if ch.is_open:                  
                    tasks = task(Id = int(Id),
                                StoreId = StoreId,
                                TaskTag = str(Task),
                                Lng = str(Lng),
                                Lat = str(Lat),
                                Address = Address,
                                Province = str(Province),
                                CityCode = str(City),
                                District = str(District),
                                GenHash = GeoHash[:5],
                                GeoHash = GeoHash,
                                Exec = str(Exec))   
                    DbContext = DbHelper()
                    DbContext._InsertByEntity(tasks)            
                    #手动确认                        
                    ch.basic_ack(delivery_tag = method.delivery_tag)
            except Exception as e:
                #持久化任务异常时,将消息回写到队列
                errorResult = self.__ErrorReturn(receiveMsgDict)
                producer = SendMessage()
                producer.sendErrorMessage(errorResult)
                DbContext.AddLog('',4,'持久化任务异常' + repr(e).replace("'","").replace("\"","") + '[队列消息]：' + receiveMsg)
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print('持久化任务异常' + repr(e).replace("'","").replace("\"","") + '[队列消息]：' + receiveMsg)
                del producer
                pass
            else:                
                self.__receiveNum += 1
                if self.__receiveNum == 1 or self.__receiveNum % 100 == 0:                    
                    self.__receiveNum = 1
                    self.__RunningCheck()        
            pass
    
    def receiveMessage(self):
        try:
            #创建通道
            channel = self._conn.channel() 
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~O(∩_∩)O 消息接收中 O(∩_∩)O~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')           
            #channel.queue_declare(queue=self.__QueueName,durable=True)      
            self.__RunningCheck()                              
            channel.basic_qos(prefetch_count = 1)
            channel.basic_consume(on_message_callback = self.__callback,queue=self.__QueueName)                   
            channel.start_consuming()             
        except Exception as e:
            DbContext = DbHelper()
            DbContext.AddLog('',4,'接收数据异常：' + repr(e).replace("'","").replace("\"",""))
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print('接收数据异常：' + repr(e).replace("'","").replace("\"",""))
            del DbContext            
        pass    