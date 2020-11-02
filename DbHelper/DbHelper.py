# -*- encoding=utf8 -*-
import sys
import configparser
import pymysql as pm
sys.path.append(r'./CommonPackage')
#from GlobalParameter import FaileAddress
from CommonPackage.GlobalParameter import FaileAddress
from DbHelper.DbBase import DbBase
import datetime
import uuid
import re
sys.path.append(r'./Entity')
#from AllEntity import *
from Entity.AllEntity import * 
class DbHelper(DbBase):    
    #初始化连接字符串
    def __init__(self):
        super().__init__()        
        pass
    
    #===========================================业务特别操作===========================================#    
    #获取没有爬到的定位点
    def getlocation(self,targetCity):
        sql = "select RepresentativeAdress,Genhash from address where isCap = 2 and RepresentativeAdress is not null and priority is not null and city like '%" + targetCity + "%' order by priority asc"
        cursors = self._conn.cursor()
        cursors.execute(sql)
        result = cursors.fetchall()
        return result
    
    #新增店铺
    def InsertShop(self,shopName,wmPoiScore,address,SellNum,AnchorPoint,Genhash,city,cityCode):
        mtWmPoiId = '' #门店ID
        try:            
            
            addressNoNumer = re.sub('[0-9\零一二三四五六七八九十壹貳叁肆伍劉柒捌玖拾]','_',address)
            sql = "select count(*) as nums from shop where shopName = '"+shopName+"' and address like '%"+addressNoNumer +"%'"
            cursors = self._conn.cursor()
            cursors.execute(sql)
            result = cursors.fetchall()        
            nums = result[0]['nums']
            #爬到的地址不存在直接新增   
            if int(nums)==0:
                shopInfo = shop(shopname = shopName,
                            wmPoiScore = wmPoiScore,
                            SellNum = SellNum,
                            address = address,
                            CityCode = cityCode,
                            City = city,
                            AnchorPoint = AnchorPoint,
                            Genhash = Genhash)
                mtWmPoiId = shopInfo.mtWmPoiId
                super()._InsertByEntity(shopInfo) 
            else:
                sql = "select mtWmPoiId,shopName from shop where shopName = '"+shopName+"' and address like '%"+addressNoNumer +"%' order by InsertTime asc"
                cursors.execute(sql)
                result = cursors.fetchall()
                shopid=''
                for item in result:
                    if(self.getBrand(shopName)== self.getBrand(item['shopName'])):
                        shopid = item["mtWmPoiId"]
                        break
                #爬到的门店地址存在但不是同个品牌也新增
                if(shopid==''):
                    shopInfo = shop(shopname = shopName,
                            wmPoiScore = wmPoiScore,
                            SellNum = SellNum,
                            address = address,
                            CityCode = cityCode,
                            City = city,
                            AnchorPoint = AnchorPoint,
                            Genhash = Genhash)
                    mtWmPoiId = shopInfo.mtWmPoiId
                    print('+++++++++++++++++++++++爬到的门店地址存在但不是同个品牌也新增+++++++++++++++++++++++')
                    super()._InsertByEntity(shopInfo) 
                else:#爬到的店地址存在并且有这个品牌就认为是同一家店
                    sql = "update shop set wmPoiScore = '" + wmPoiScore + "',SellNum = " + SellNum +  ",AnchorPoint = '" + AnchorPoint + "'  where mtWmPoiId = '" + shopid+"'"         
                    try:
                        result = cursors.execute(sql)                
                        self._conn.commit()     
                        print('+++++++++++++++++++++++之前存在的店 更新[' + str(result) + ']家评价和销量+++++++++++++++++++++++')
                        mtWmPoiId = shopid
                    except Exception as e:
                        print('更新数据异常'+repr(e))
                        mtWmPoiId=''
                        self._conn.rollback()   
                   
        except Exception as e:            
            if 'Duplicate' in repr(e):
                #如果之前存在那就更新销量和评分
                sql = '''
                    update shop
                    set wmPoiScore = '%s',
                    SellNum = %d,
                    AnchorPoint = '%s' 
                    where shopName = '%s' and City = '%s' 
                '''
                sql = sql % (wmPoiScore,int(SellNum),AnchorPoint, shopName,city)
                cursors = self._conn.cursor()
                result = cursors.execute(sql)                
                self._conn.commit()   
                print('--------------------------存在['+ shopName +'] 更新评价和销量[' + str(result) + ']家--------------------------')
                sql = '''
                    select mtWmPoiId
                    from shop 
                    where shopName = '%s' and City = '%s' 
                '''
                sql = sql % (shopName,city)
                mtid = super().Query(sql)
                mtWmPoiId = mtid[0]['mtWmPoiId']
                pass
            else:
                print('新增数据异常'+repr(e))
                mtWmPoiId =''
                self._conn.rollback()   
        return mtWmPoiId          
    def getBrand(self,shopName):
        if str(shopName).find('（')==-1 and str(shopName).find('(')==-1:
            return shopName
        elif str(shopName).find('（')!=-1:
            return str(shopName).split('（')[0]
        elif str(shopName).find('(')!=-1:
            return str(shopName).split('(')[0]
        pass
    #根据门店名字和地理散列查找门店信息
    #v2根据门店名字和city查找门店信息
    # def GetStoreInfo(self,shopName,wmPoiScore,SellNum,Genhash,city):
    def GetStoreInfo(self,shopName,wmPoiScore,SellNum,Genhash,city,AnchorPoint):
        # sql = "select count(*) as nums from shop where shopName = '" + shopName + "' and Genhash like '%" + Genhash + "%' and address not like '%" + FaileAddress + "%'" 
        sql = "select count(*) as nums from shop where shopName = '" + shopName + "' and City = '" + city + "' and address not like '%" + FaileAddress + "%'" 
        cursors = self._conn.cursor()
        cursors.execute(sql)
        result = cursors.fetchall()        
        nums = result[0]['nums']        
        if int(nums) == 0:#不存在继续爬门店信息           
            return True,'',''
        else:#有说明之前爬过不需要爬地址，直接更新销量等信息
            sql = "update shop set wmPoiScore = '" + wmPoiScore + "',SellNum = " + SellNum +  ",AnchorPoint = '" + AnchorPoint + "' where shopName = '" + shopName + "' and City ='" + city + "'"            
            try:
                cursors = self._conn.cursor()
                result = cursors.execute(sql)                
                self._conn.commit()     
                print('+++++++++++++++++++++++之前存在的店 更新[' + str(result) + ']家评价和销量+++++++++++++++++++++++')
                #获取这家店的地址
                sql = "select mtWmPoiId,address from shop where shopName = '" + shopName + "' and City = '" + city + "' and address not like '%" + FaileAddress + "%'"        
                cursors.execute(sql)
                result = cursors.fetchall()
                address = result[0]['address']
                mtWmPoiId = result[0]['mtWmPoiId']
            except Exception as e:
                print('更新数据异常'+repr(e))
                self._conn.rollback()   
                return False,'',''
            return False,address,mtWmPoiId
        pass
    
    #更新地理散列值
    def UpdateGeoHash(self,shopname,CityCode,GeoHash):
        address = FaileAddress
        mtWmPoiId = ''
        try:
            sql = "select mtWmPoiId,address from shop where shopName = '" + shopname + "' and CityCode = '" + CityCode + "'"       
            cursors = self._conn.cursor()
            cursors.execute(sql)
            result = cursors.fetchall()                             
            if len(result) == 1:#一个城市下的同一门店名字,也添加对应的地理散列
                sql = "update shop set Genhash = Concat('"+ GeoHash +";',if(Genhash is null,'',Genhash))  where shopName = '" + shopname + "' and CityCode = '" + CityCode + "'"   
                self.Update(sql)                
                print('+++++++++++++++++++++++将当前地理散列更新到门店['+ shopname +']里去,地址：['+ result[0]['address'] +']+++++++++++++++++++++++')
                address = result[0]['address']
                mtWmPoiId = result[0]['mtWmPoiId']
            else:
                address = FaileAddress
                mtWmPoiId = ''
        except Exception as e:
            print(repr(e))   
        return address,mtWmPoiId    
    
    #更新爬过的点
    def updateAddressIsCap(self,address,StoreNum):
        sql = '''
            update address
            set IsCap = 1,
            StoreNum = %d
            where RepresentativeAdress = '%s'
        '''
        sql = sql % (StoreNum,address)
        try:
            self.Update(sql)            
        except Exception as e:
            print('更新地址状态异常：'+repr(e))
            self._conn.rollback()   
        pass
    
    #获取按照模式1的设备任务
    def GetDeviceTask(self,DeviceNum,table = 'task'):
        result = []
        sql = """
            select t.TaskId,t.CityCode,d.TargetCity,t.Address as RepresentativeAdress,t.Genhash
            from %s t
            left join devicetaskschedule d on t.CityCode = d.CityCode
            where IsExcute in (0,1) and d.DeviceNum = '%s'
            order by TaskId asc
        """
        sql = sql % (table,DeviceNum)
        try:
            cursors = self._conn.cursor()
            cursors.execute(sql)
            result = cursors.fetchall()              
        except Exception as e:
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 获取目标城市失败 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')   
            print(repr(e))            
        return result
    
    #按照模式2获取设备的任务    
    def GetDeviceTaskByMode2(self,table = 'task'):
        result = []
        #获取模式2集中运行的城市
        runsql = '''
            select RunCity
            from runcitybymode2
            where IsRun = 1
        '''
        runcity = ''
        try:
            cursors = self._conn.cursor()
            cursors.execute(runsql)
            RunCity = cursors.fetchall()    
            if len(RunCity) > 0:
                for city in RunCity:
                    if city['RunCity'] != '不限':
                        runcity += "'%s'," % city['RunCity']
                    else:
                        runcity = city['RunCity']
                        break
            else:
                return result
            pass
        except Exception as e:
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 获取目标城市失败 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')   
            print(repr(e))  
            return result        
        if runcity == '不限':
            sql = """
                select t.TaskId,t.CityCode,d.TargetCity,t.Address as RepresentativeAdress,t.Genhash
                from %s t
                left join devicetaskschedule d on t.CityCode = d.CityCode
                where IsExcute in (0) 
                order by rand()
                limit 0,1
            """ % table
        else:
            sql = """
                select t.TaskId,t.CityCode,d.TargetCity,t.Address as RepresentativeAdress,t.Genhash
                from %s t
                left join devicetaskschedule d on t.CityCode = d.CityCode
                where IsExcute in (0)  and d.TargetCity in (%s)
                order by rand()
                limit 0,1
            """ % (table,runcity[:-1])
        try:
            cursors = self._conn.cursor()
            cursors.execute(sql)
            result = cursors.fetchall()              
        except Exception as e:
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 获取目标城市失败 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')   
            print(repr(e))            
        return result

    #获取最近一条执行了但是没有回写队列的任务执行时间
    def getLateTaskTime(self):
        taskListTime =[]
        sql = """
        select t.ExcuteTime 
        from task t 
        where t.IsExcute = 1 OR t.IsExcute = 2 
        order by ExcuteTime desc limit 0,1;
        """
        taskListTime = self.Query(sql)
        return taskListTime
    
    #把所有task表里中断的任务重启(一个小时还没有爬完的任务)
    def rebootTask(self):
        sql = """
        UPDATE task t 
        SET 
        t.IsExcute = 0
        WHERE
        (t.IsExcute = 1 OR t.IsExcute = 2) and ExcuteTime<SUBDATE(now(),interval 60 minute); 
        """
        self.Update(sql)
        pass

    #按照模式3获取设备的任务(即按照基础库数据更新)
    def GetDeviceTaskByMode3(self):
        return self.GetDeviceTaskByMode2('TaskBase')        


    #模式6(爬取门店商品)
    def GetDeviceTaskByMode6(self):
        
        pass


    #获取有待执行任务的设备
    def GetHasTaskDevice(self):
        deviceList = []
        sql = """
            select DeviceNum
            from taskschedule
            where Status in (0,1)
            order by Status asc
        """
        deviceList = self.Query(sql)
        return deviceList

    def deleteStore(self,mwid):
        sql = " delete from shop where mtWmPoiId= '"+mwid+"'"
        relust = self.Delete(sql)
        return relust
        
    #更新任务状态
    def UpdateTaskStatus(self,taskId,status,StoreNum,mode:int):
        table = 'task'
        if mode == 3:
            table = 'taskbase'
        sql = '''
        update %s
        set IsExcute = %d '''
        if status == 2:
            finishtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            sql = sql + ",FinishTime = '%s',StoreNum = %d " % (finishtime,StoreNum)
        elif status == 1:
            excuteTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            sql = sql + ",ExcuteTime = '%s'" % (excuteTime)
        elif status == 3:
            WriteBackTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            sql = sql + ",WriteBackTime = '%s'" % (WriteBackTime)
        sql = sql + ' where TaskId = %d'         
        sql = sql % (table,int(status),int(taskId))
        try:
            self.Update(sql)           
        except Exception as e:
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 更新任务状态失败 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            self.AddLog(taskId,3,'更新任务状态失败：' +repr(e))            
            self._conn.rollback()           
        pass
    
    #添加日志
    def AddLog(self,deviceNum,Type,info):       
        try:
            logs = loginfo(DeviceNum = deviceNum,Type = Type,Info = info)
            super()._InsertByEntity(logs)
        except Exception as e:
            self._conn.rollback()
            print('执行sql语句出错：'+repr(e)+"[sql]="+logs)  
        pass

    
    
    #获取过滤关键词
    def GetFilterKeyword(self):
        sql = """
            select k.key from keywordfilter k where IsUse = 1
        """
        result = self.Query(sql)
        resultList = []
        for key in result:
            resultList.append(key['key'])
        return resultList
    
    #获取设备的运行模式
    def GetDeviceRunningMode(self,DeviceNum):
        mode = 0
        try:
            sql = """
                select DeviceRunningMode from deviceinfo where DeviceNum = '%s'
            """
            sql = sql % (DeviceNum)
            cursors = self._conn.cursor()
            cursors.execute(sql)
            result = cursors.fetchall()    
            mode = result[0]['DeviceRunningMode']
        except Exception as e:
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 获取设备运行模式失败 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(repr(e))
        return mode

    #新增任务(弃用可删除)
    def AddTask(self,Id,StoreId,TaskTag,Lng,Lat,Address,Province,CityCode,District,GenHash,Exec):
        sql = '''
                insert into task(Id,StoreId,TaskTag,Lng,Lat,Address,Province,CityCode,District,GenHash,GeoHash,Exec,ReceiveTime) 
                values
                (%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
            '''
        ReceiveTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        sql = sql % (int(Id),StoreId,str(TaskTag),str(Lng),str(Lat),Address,str(Province),str(CityCode),str(District),str(GenHash)[:5],GenHash,str(Exec),ReceiveTime)
        cursors = self._conn.cursor()
        cursors.execute(sql)
        self._conn.commit() 
        pass
    
    #更新之前没有回写队列的任务
    def UpdateTask(self):
        sql = '''
            update task
            set StoreNum = NULL,    
                IsExcute = 0,
                ExcuteTime = NULL,
                FinishTime = NULL,
                WriteBackTime = NULL 
            where IsExcute in (1,2)
        '''
        self.Update(sql)
        pass

    #获取集群设备编号
    def GetAllDevice(self):
        sql = '''
            select DeviceNum
            from deviceinfo
            where DeviceNum != '0123456789ABCDEF'
        '''
        return self.Query(sql)    


#==================================门店商品爬虫相关==================================#
    def GetStorePoint(self,StoreId:str):
        sql = """
            select s.shopName,s.City,s.AnchorPoint,s.address,s.mtWmPoiId
            from shop s
            where s.mtWmPoiId = '%s'
        """ % (StoreId)
        return self.Query(sql)        
    def GetStorePointForName(self,StoreName:str):
        sql = """
            select s.shopName,s.City,s.AnchorPoint,s.address,s.mtWmPoiId
            from shop s
            where s.shopName = '%s'
        """ % (StoreName)
        return self.Query(sql)        
    
    #同步商品信息
    def SynchroProductInfo(self,StoreID:str,Name:str,Sale:int,Price:float,OriginPrice:str,Discount:str):
        if OriginPrice == '-1' or OriginPrice == '暂不获取原价':
            OriginPrice = ''
        if Discount == '无折扣信息' or Discount == '暂不获取折扣':
            Discount = ''
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = 0
        sql = '''
            select count(1) as num
            from product p
            where p.StoreID = '%s' and Name = '%s'
        ''' % (StoreID,Name)
        result = self.Query(sql)
        if result[0]['num'] > 0:            
            sql = '''
                update product
                set Sale = %d,
                Price = %f,
                OriginPrice = '%s',
                Discount = '%s',
                UpdateTime = '%s'     
                where StoreID = '%s' and Name = '%s'
            ''' % (Sale,Price,OriginPrice,Discount,time,StoreID,Name)
            rows = self.Update(sql)
        else:
            try:
                sql = '''
                    insert into product (StoreID,Name,Sale,Price,OriginPrice,Discount,CreateTime)
                    values('%s','%s',%d,%f,'%s','%s','%s')
                ''' % (StoreID,Name,Sale,Price,OriginPrice,Discount,time)
                rows = self.Insert(sql)
            except Exception as e:
                print('新增商品信息失败：'+repr(e)) 
        return rows        



















