# -*- encoding=utf8 -*-
import sys
import datetime
from Entity.EntityBase import EntityBase
import uuid

#日志
class loginfo(EntityBase):
    Id :int
    DeviceNum : str
    Type : int
    Info : str
    CreateTime : str
    def __init__(self,DeviceNum : str,
                    Type : int,
                    Info : str):  
        self.DeviceNum = DeviceNum
        self.Type = Type
        self.Info = Info
        self.CreateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pass

#门店类
class shop(EntityBase):
    mtWmPoiId : str
    shopName : str
    Brand : str
    wmPoiScore : str
    SellNum : int
    address : str
    CityCode : str
    City : str
    Lng : str
    Lat : str
    AddressGeohash : str
    AnchorPoint : str
    Genhash : str
    InsertTime : str
    UpdateTime : str    
    def __init__(self,mtWmPoiId:str = None,
                    shopname:str = None,
                    wmPoiScore:str = None,
                    SellNum:int = None,
                    address:str = None,
                    CityCode:str = None,
                    City:str = None,
                    Lng:str = None,
                    Lat:str = None,                
                    AnchorPoint:str = None,
                    Genhash:str = None):        
        self.mtWmPoiId = str(uuid.uuid1()).replace("-","")
        self.shopName = shopname
        self.wmPoiScore = wmPoiScore
        self.SellNum = SellNum
        self.address = address
        self.CityCode = CityCode
        self.City = City
        self.Lng = Lng
        self.Lat = Lat
        self.AnchorPoint = AnchorPoint
        self.Genhash = Genhash        
        self.InsertTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pass

class task(EntityBase):
    Id : int
    StoreId : str
    TaskTag : str
    Lng : str
    Lat : str
    Address : str
    Province : str
    CityCode : str
    District : str
    GenHash : str
    GeoHash : str
    StoreNum : int
    IsExcute : int
    Exec : str
    ReceiveTime : str
    ExcuteTime : str
    FinishTime : str
    WriteBackTime : str
    def __init__(self,Id : int,
                    StoreId : str,
                    TaskTag : str,
                    Lng : str,
                    Lat : str,
                    Address : str,
                    Province : str,
                    CityCode : str,
                    District : str,
                    GenHash : str,
                    GeoHash : str,                    
                    Exec : str):
        self.Id = Id
        self.StoreId = StoreId
        self.TaskTag = TaskTag
        self.Lng = Lng
        self.Lat = Lat
        self.Address = Address
        self.Province = Province
        self.CityCode = CityCode
        self.District = District
        self.GenHash = GenHash
        self.GeoHash = GeoHash
        self.IsExcute = 0                     
        self.Exec = Exec
        self.ReceiveTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        pass