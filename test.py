from DbHelper.DbHelper import DbHelper
from RabbitMQ.Consumer import ReceiveMessage
from RabbitMQ.Produce import SendMessage
from CommonPackage.CommonFunc import *
import json
from DbHelper.DbHelper import DbHelper
from Operate.GetAddress import *
from sql.InitBrand import UpdateBrand,UpdatemtWmPoiId,UpdateO2OBrand
from RedisManage.Cache import CacheData
from datetime import datetime,  timedelta
from Entity.AllEntity import *
import psutil


def main():    

    '''
    send = SendMessage()    
    send.sendMessage()

    receive = ReceiveMessage()
    receive.receiveMessage()
    
    data = {"Id":841627,"StoreId":None,"Lng":111.905332,"Lat":31.317212,"GeoHash":"wmxd4mngzprq","Platform":"elm","Province":420000
,"City":420600,"District":420624,"Task":203,"Exec":305,"Type":0}
    encode = EncodeText(str(data))
    print(encode)
    print(DecodeText(encode))
    '''
    '''
    Dbcontext = DbHelper()
    shopname = '金象大药房（新茸芝店）'
    CityCode = '110100'
    result = Dbcontext.Query("select address  from shop where shopName = '" + shopname + "' and CityCode = '" + CityCode + "'"       )
    print(result)
    '''
    '''
    _base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    _encode_map = {}
    for i in range(len(_base32)):    
        _encode_map[i]=_base32[i]
    GetLngLatByGeohash(104.075674,30.652641,_encode_map)
    
    result = GetLngLatByGeohash('uxvzb')
    print(str(result))
    '''

    #UpdateO2OBrand()
    #updateGeohash()
    #DbContext = DbHelper()    
    #UpdatemtWmPoiId(DbContext)
    #UpdateBrand(DbContext)    
    #t = DecodeText('H4sIAAAAAAAACx2OywrCMBBF/2XWoeTRJjY7UVHBhWB/IKSpBttGkvgo4r877e6eM3DvfOHYgha0EkoQuOQQ3SzGZ98TOI1X0IzxomaUUoXCZNBcFEzWXHECexcOJt1AwztRZUXXWqskEFi3bXQp4QHh3JvchTggDXnmGF5+tA50WWIvJbDxeVpIzrT1KUdvcWoxuNuYdMdPBJUEdh9nMVcrzM30wBb6+wPpSJ79xgAAAA==')
    #strs = "{'State': 1, 'Id': 4519, 'StoreId': '', 'Lng': '117.121383', 'Lat': '40.140701', 'GeoHash': 'wx5k35mhw10b', 'Platform': 'mt', 'Province': '110000', 'City': '110100', 'District': '110117', 'Task': '450', 'Exec': '556', 'Type': 'StoreGet', 'Exists': 1, 'Result': '[{'Name': '戴明眼镜（服务中心楼店）', 'Score': 0, 'Sales': 7.0, 'Phone': '', 'Brand': '', 'Created': '2020-01-14 11:04:36', 'OriginAddress': '北京市平谷区平谷镇文化北街4号体育服务中心楼1至2层4-78 ', 'Id': '1c2e69b8306111ea8565005056c00008'}, {'Name': '戴明眼镜（平谷镇店）', 'Score': 0, 'Sales': 0.0, 'Phone': '', 'Brand': '', 'Created': '2020-01-14 11:04:37', 'OriginAddress': '北京市平谷区平谷镇府前西街2-4号 ', 'Id': '1c1dac02306111eaacc7005056c00008'}]'}"
    #t = EncodeText(strs)
    #print(t)
    #getLngLatByAddress_task()
    #updateGeohash_taskbase()
    pass


if __name__ == '__main__':
    main()


'''
select CityCode, count(1)  from stores 
where Platform = 'elm'
GROUP BY CityCode
ORDER BY 2 DESC;

select s.Lng,s.Lat,SUBSTR(s.GeoHash,1,5) as Genhash,s.CityCode,a.`Name`,s.OriginAddress
from stores s
LEFT JOIN areas a on s.CityCode = a.AdCode
where s.CityCode in ('310100','110100')
GROUP BY Genhash

select s.City,count(s.shopName) as storeNum
from shop s
group by s.City
order by storeNum desc;

select s.CityCode,a.`Name`,count(s.`Name`) as nums
from stores s
left JOIN areas a on s.CityCode = a.AdCode
where s.Platform = 'elm'  and s.CityCode is not NULL
GROUP BY s.CityCode
HAVING count(s.`Name`) >= 10
order by nums desc;

select count(s.PlatformStoreId)
from stores s
where s.Platform = 'elm'  and s.CityCode is not NULL

SELECT s.shopName,s.Brand,s.wmPoiScore,s.SellNum,s.address,s.InsertTime,s.UpdateTime
from shop s
where s.City in ('绵阳','眉山') and (s.UpdateTime > '2020-03-01 00:00:00' or s.InsertTime > '2020-03-01 00:00:00')
ORDER BY s.SellNum desc
'''