# -*- encoding=utf8 -*-
import json
import requests as rq
import json
from DbHelper.DbHelper import DbHelper


#用于更新没有地址的经纬度
def UpdateAddress(lng,lat,address,priority,DbContext):    
    sql = "update address set RepresentativeAdress = " +repr(str(address))+ ",priority = "+ str(priority) +"  where Lng = "+ str(lng) +" and Lat = " + str(lat) + " and city = '重庆' "        
    DbContext.Update(sql)
    pass 
#根据经纬度拿到地址信息
def getAddressFromGaoDe():
    DbContext = DbHelper()
    sql = """
        select Lng,Lat
        from address
        where city like '%重庆%' and Lng is not null and Lat is not null and RepresentativeAdress is null
        limit 5500
    """
    allLngLat = DbContext.Query(sql)    
    key = '929d86bb3c93b6895554459ab7893171'    
    print(str(len(allLngLat)))
    for item in allLngLat:        
        try:            
            #print(str(float(item["Lng"])),str(float(item["Lat"])))
            #url = url % (key,float(),float(item["Lat"]))    
            url = 'https://restapi.amap.com/v3/geocode/regeo?key=' + key + '&location=' + str(item["Lng"]) + ',' + str(item["Lat"]) + '&poitype=&radius=1000&extensions=base&batch=false&roadlevel=1'
            
            req = rq.get(url)
            dataDic = json.loads(req.text)            

            address = ''
            businessaddress = ''
            priority = 3
            if int(dataDic['status']) == 1:        
                baseaddress = str(dataDic['regeocode']['formatted_address'])  #基础地址
                if 'addressComponent' in dataDic['regeocode']:                    
                    if 'businessAreas' in dataDic['regeocode']['addressComponent']:                        
                        if len(dataDic['regeocode']['addressComponent']['businessAreas']) > 0:                                               
                            result = dataDic['regeocode']['addressComponent']['businessAreas'][0]                                                        
                            print(dataDic['regeocode']['addressComponent']['businessAreas'])
                            if len(result) > 0:                                    
                                if 'name' in result:
                                    print(222)
                                    businessaddress = ' ' + result["name"]                        
                                    priority = 1
                address = baseaddress + businessaddress
            else:
                address =  ''
                continue
            if address != '' and address != '[]':     
                address = address.replace("'","")                                      
                UpdateAddress(float(item["Lng"]),float(item["Lat"]),str(address),priority,DbContext)
                print(address)                
        except Exception as e:
            if 'not all arguments converted during string formatting' in  repr(e):                
                continue
            else:
                print('出错：'+ repr(e))
                break
        pass
    pass

#根据地址获取经纬度(shop)
def getLngLatByAddress():
    key = '929d86bb3c93b6895554459ab7893171'    
    sql = '''
        select shopName,city,address
        from shop s
        where s.Genhash is null
    '''
    try:
        DbContext = DbHelper()
        Alladdress = DbContext.Query(sql)  
        for address in Alladdress:
            _shopname = address['shopName']
            _city = address['city']
            _address = address['address']
            url = 'https://restapi.amap.com/v3/geocode/geo?key='+ key +'&address=' + _address +'&city=' + _city
            req = rq.get(url)
            dataDic = json.loads(req.text)      
            if int(dataDic['status']) == 1:      
                geocodes = dataDic['geocodes']    
                if len(geocodes) > 0:
                    location = geocodes[0]['location'].split(",")
                    if len(location) > 0:
                        Lng = location[0]
                        Lat = location[1]
                        sql = '''
                            update shop
                            set Lng = '%s',
                            Lat = '%s'
                            where shopName = '%s' and address = '%s'
                        '''
                        sql = sql % (str(Lng),str(Lat),_shopname,_address)
                        DbContext.Update(sql)
                        print('已更新【'+ _shopname +'】')
            pass 
    except Exception as e:
        print(repr(e))
    pass

#根据地址获取经纬度(taskbase)
def getLngLatByAddress_task():
    key = '929d86bb3c93b6895554459ab7893171'    
    sql = '''
        select TaskId,Address
        from taskbase t
        where t.IsExcute = 4
    '''
    try:
        DbContext = DbHelper()
        Alladdress = DbContext.Query(sql)  
        for address in Alladdress:
            _TaskId = address['TaskId']            
            _address = address['Address']
            url = 'https://restapi.amap.com/v3/geocode/geo?key='+ key +'&address=' + _address +'&city=福州'
            req = rq.get(url)
            dataDic = json.loads(req.text)      
            if int(dataDic['status']) == 1:      
                geocodes = dataDic['geocodes']    
                if len(geocodes) > 0:
                    location = geocodes[0]['location'].split(",")
                    if len(location) > 0:
                        Lng = location[0]
                        Lat = location[1]
                        sql = '''
                            update taskbase
                            set Lng = '%s',
                            Lat = '%s'
                            where TaskId = %d
                        '''
                        sql = sql % (str(Lng),str(Lat),_TaskId)
                        DbContext.Update(sql)
                        print('已更新【'+ _address +'】')
            pass 
    except Exception as e:
        print(repr(e))
    pass

def updateGeohash_taskbase():
    sql = '''
        select Lng,Lat,TaskId
        from taskbase
        where IsExcute = 4
    '''
    _base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    _encode_map = {}
    for i in range(len(_base32)):    
        _encode_map[i]=_base32[i]
    DbContext = DbHelper()
    result = DbContext.Query(sql)
    for item in result:
        Lng = item['Lng']
        Lat = item['Lat']
        TaskId = item['TaskId']
        geohash = getGeoHashByLngLat(float(Lat),float(Lng),_encode_map)
        sql = '''
            update taskbase
            set GenHash = '%s'
            where TaskId = %d
        '''
        sql = sql % (geohash,TaskId)
        DbContext.Update(sql)
        print(str(TaskId) + '更新完')
    pass

#更新定位点的geohash
def updateGeohash():
    sql = '''
        select Lng,Lat,shopName,address
        from shop
        where address = '上海市浦东新区万祥镇严木桥路96号1-2层'
    '''
    _base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    _encode_map = {}
    for i in range(len(_base32)):    
        _encode_map[i]=_base32[i]
    DbContext = DbHelper()
    result = DbContext.Query(sql)
    for item in result:
        Lng = item['Lng']
        Lat = item['Lat']
        shopname = item['shopName']
        address = item['address']
        geohash = getGeoHashByLngLat(float(Lat),float(Lng),_encode_map)
        sql = '''
            update shop
            set AddressGeohash = '%s'
            where shopName = '%s' and address = '%s'
        '''
        sql = sql % (geohash,shopname,address)
        DbContext.Update(sql)
    pass

#通过地理散列得到经纬度
def GetLngLatByGeohash(geohash):
    _base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    _decode_map = {}
    for i in range(len(_base32)):
        _decode_map[_base32[i]] = i
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    is_lon=True
    for letter in geohash:
        code=str(bin(_decode_map[letter]))[2:].rjust(5,'0')
        for bi in code:
            if is_lon and bi=='0':
                lon_range[1]=sum(lon_range)/2
            elif is_lon and bi=='1':
                lon_range[0]=sum(lon_range)/2
            elif (not is_lon) and bi=='0':
                lat_range[1]=sum(lat_range)/2
            elif (not is_lon) and bi=='1':
                lat_range[0]=sum(lat_range)/2
            is_lon=not is_lon
    return sum(lat_range)/2,sum(lon_range)/2

#根据经纬度计算geohash
def getGeoHashByLngLat(lat,lon,_encode_map,precision=5):        
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    geohash=[]
    code=[]
    j=0
    while len(geohash)<precision:        
        j+=1
        lat_mid=sum(lat_range)/2
        lon_mid=sum(lon_range)/2
        #经度
        if lon<=lon_mid:
            code.append(0)
            lon_range[1]=lon_mid
        else:
            code.append(1)
            lon_range[0]=lon_mid
        #纬度
        if lat<=lat_mid:
            code.append(0)
            lat_range[1]=lat_mid
        else:
            code.append(1)
            lat_range[0]=lat_mid
        ##encode
        if len(code)>=5:
            geohash.append(_encode_map[int(''.join(map(str,code[:5])),2)])
            code=code[5:]
    result = ''.join(geohash)
    return result

#获取要抓取的地址列表
def AddressList(targetCity):    
    addressList = readCsv(targetCity)
    returnList = []    
    for item in addressList:    
        address = item['RepresentativeAdress']        
        if not returnList.__contains__(address):
            returnList.append(item) #将定位点和地理散列值都带出去
    pass                    
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~已获取目标城市【' + str(targetCity) + '】所有定位点~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    return returnList

def readCsv(targetCity):
    myCon = DbHelper()
    result = myCon.getlocation(targetCity)
    return result
    