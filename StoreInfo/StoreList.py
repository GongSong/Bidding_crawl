# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
import time
from CommonPackage.GlobalParameter import waitTime,FaileAddress
from Operate.SwitchingPosition import SwithPosition
from DbHelper.DbHelper import DbHelper
from StoreInfo.StoreInfo import GetStoreInfo
from StoreInfo.StoreSellScore import GetStoreScore,GetStoreSell,GetStoreName
from Operate.SearchDrug import SearchDrugPage
from Operate.CloseUpdate import CloseUpDateInfo
from Product import ProductInfo
import datetime

def StartCapture(poco,AllPosition,DeviceType,TargetCity,DeviceNum,cityCode,device):
    CloseUpDateInfo(poco)
    IsAllClassifyInput = False #是否从大类搜索进入(默认不是)
    AllClassifyInputClickNum = 0#大类进入点击小类的次数
    currentTaskResult = []#存放本次任务抓取的门店信息
    if poco(text = "美团外卖").exists():
        poco(text = "美团外卖").click()  
    if DeviceNum == 'E4J4C17405011422':
        poco.swipe([0.5,0.5],[0.5,0.6],duration = 0.3)        
    IsAddress = SwithPosition(poco,AllPosition[0]['RepresentativeAdress'],TargetCity,0)#第一次切换定位    
    if not IsAddress:
        return currentTaskResult,False
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        if poco(text="送药上门").exists():                
            poco(text="送药上门").wait(waitTime).click([0,0])      
        else:
            if DeviceNum == 'E4J4C17405011422':
                poco.swipe([0.5,0.6],[0.5,0.5],duration = 0.3)
            result = SearchDrugPage(poco,device,DeviceNum)
            if not result:
                print(DeviceNum)
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 第一个定位点无送药上门 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                IsAddress = False
            else:
                IsAllClassifyInput = True                
    except PocoNoSuchNodeException:
        print(DeviceNum)
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 第一个定位点无送药上门f o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        IsAddress = False
        pass    
    StoreList = []#只存储当前定位的门店名称
    SwitchNum = 0 #定位切换次数    
    DbContext = DbHelper()        
    for addressDic in AllPosition:#结构改了以后AllPosition只会有一条数据
        address = addressDic['RepresentativeAdress']#标志性坐标点
        addressGenhash = addressDic['Genhash'] #地理散列值        
        print('===========================【'+ DeviceNum +'】抓取【' + address + '】开始===========================')    
        #第一次进来不需要切换定位
        if SwitchNum > 0:
            StoreList.clear()#切换一次地址就将列表清空
            IsAddress = SwithPosition(poco,address,TargetCity,SwitchNum) #切换定位                        
            if not IsAddress:                
                print('===========================【'+ DeviceNum +'】抓取【' + address + '】完成 无店铺===========================\n')
                continue
            SongYaoNum = 0
            while True:
                if poco(text="送药上门").exists():                                            
                    poco(text="送药上门").wait(waitTime).click([0,0])
                    break
                SongYaoNum += 1
                time.sleep(1)
                if SongYaoNum >= 3:
                    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 该定位点无送药上门 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    IsAddress = False           
                    break
        SwitchNum += 1
        if not IsAddress:
            print('===========================【'+ DeviceNum +'】抓取【' + address + '】完成 无店铺===========================\n')            
            continue        
        storelenNum = 0
        swipeNume= 0
        #第一次大幅度滑动
        if DeviceType == 1:            
            poco.swipe([0.2,0.9],[0.2,0.45],duration = 0.3)  
        else:
            poco.swipe([0.4,0.9],[0.4,0.75],duration = 0.3) 
        if IsAllClassifyInput:
            if poco(text="常用药品").exists():
                poco(text="常用药品").click()
                AllClassifyInputClickNum += 1
        #按照销量排序
        if poco(text = '销量').exists():
           poco(text = '销量').wait(waitTime).click() 
        #当前循环是一个定位点的门店
        backPage = poco("com.sankuai.meituan.takeoutnew:id/iv_back")    
        bottomElement = poco("com.sankuai.meituan.takeoutnew:id/noMoreView")         
        while True:
            #判断程序是否被紧急置停
            mode = DbContext.GetDeviceRunningMode(DeviceNum)
            if mode == 5:
                device.keyevent("4")
                return currentTaskResult,True            
            AllStore = poco("com.sankuai.meituan.takeoutnew:id/fl_fragment_container").offspring("com.sankuai.meituan.takeoutnew:id/pull_to_refresh_view").offspring("com.sankuai.meituan.takeoutnew:id/viewpager_content").offspring("com.sankuai.meituan.takeoutnew:id/wm_st_poi_channel_list").child("android.widget.FrameLayout").wait(waitTime)                       
            i = 0
            if len(AllStore) > 0:
                #print('当前列表展示的门店数量：'+  str(len(AllStore)))
                circleIsFail = False
                for store in AllStore:                    
                    if i == 0:
                        i += 1 #第一个是顶部筛选
                        continue
                    storeInfo = {}    
                    try:                        
                        storeNameResult =  GetStoreName(store)
                        if not storeNameResult[0]:                            
                            continue                        
                        storeName = storeNameResult[2]       
                        
                        #销量、评分
                        Sell = '0'
                        Score = '评分未知'                      

                        storeSellResult = GetStoreSell(storeNameResult[1])
                        if not storeSellResult[0]:                            
                            continue
                        else:
                            Sell = storeSellResult[2]
                            storeScoreResult = GetStoreScore(storeSellResult[1])
                            if not storeScoreResult[0]:                                
                                continue
                            else:
                                Score = storeScoreResult[1]
                        
                        #该定位点存在且门店名称也存在,有且只有一个地址,那么就不需要继续爬门店地址,更新销量和评分数据即可
                        IsClickStore = False
                        if storeSellResult[0] and storeScoreResult[0]: #销量和评分全部获取到在判断
                            #同一定位地址,同店铺名字的不予考虑   
                            if storeName in StoreList:
                                continue 
                            else:
                                if '成人用品' in storeName or '情趣' in storeName:#成人用品店不抓取,干扰太大
                                    continue
                                StoreList.append(storeName)      
                                storeInfo['Name'] = storeName                          
                                if '暂无评分' in str(Score):
                                    storeInfo['Score'] = 0
                                else:
                                    storeInfo['Score'] = float(Score)   
                                Sell_Str = str(Sell).replace("月售","").replace("+","").replace("件","")            
                                storeInfo['Sales'] = float(Sell_Str)
                                storeInfo['Phone'] = ''
                                storeInfo['Brand'] = ''
                                storeInfo['Created'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                            IsClickStore,addressinfo,mtWmPoiId = DbContext.GetStoreInfo(storeName,str(Score),str(Sell).replace("月售","").replace("+","").replace("件",""),addressGenhash)
                        #继续爬取门店地址                           
                        if IsClickStore:            
                            #根据店名+城市找地址                  
                            storeAddress,mtWmPoiId = DbContext.UpdateGeoHash(storeName,cityCode,addressGenhash)    
                            storeInfo['OriginAddress'] = storeAddress          
                            storeInfo['Id'] = mtWmPoiId                                                      
                            if FaileAddress in storeAddress:
                                #根据店名+城市获取地址失败在继续单击查找
                                store.click()
                                storeAddress = GetStoreInfo(poco,DbContext,DeviceNum)
                                Sell = str(Sell).replace("月售","").replace("+","").replace("件","")
                                storeAddress = storeAddress.replace("地址","").replace("地址：","")
                                if FaileAddress not in storeAddress:
                                    mtWmPoiId = DbContext.InsertShop(storeName,Score,storeAddress,Sell,address,addressGenhash,TargetCity,cityCode)
                                    storeInfo['Id'] = mtWmPoiId                            
                                    storeInfo['OriginAddress'] = storeAddress
                        else:
                            storeAddress = '不需要爬取地址'
                            storeInfo['OriginAddress'] = addressinfo
                            storeInfo['Id'] = mtWmPoiId                                                                
                        print(storeName + '  【' +str(Sell) +'】  【评分】:' + str(Score) + ' 【地址】:' + storeAddress + '\n')
                        if FaileAddress not in storeInfo['OriginAddress'] and len(storeInfo['Id']) !=0:
                            storeInfo['OriginAddress'] = str(storeInfo['OriginAddress']).replace(u'\xa0', u' ')
                            currentTaskResult.append(storeInfo)
                        ''' 药品信息
                        CatchProductResult = ProductInfo.GetProduct(poco)
                        if CatchProductResult == 'error':
                            circleIsFail = True
                            break
                        '''
                    except PocoNoSuchNodeException:                              
                        continue 
                    except Exception as e:
                        DbContext.AddLog(DeviceNum,3,'设备['+ DeviceNum +']爬取门店列表异常：' + repr(e).replace("'","").replace("\"",""))
                pass         
                if circleIsFail:
                    print('获取门店列表失败！')
                    break
                #判断是否滑动到底部    
                Isbottom = bottomElement.exists()    
                if Isbottom: 
                    print('~~~~~~~~~~~~~~~本次定位的门店到底了~~~~~~~~~~~~~~~')                    
                    if not ClickClassify(poco,AllClassifyInputClickNum):
                        if backPage.exists():                                         
                            backPage.wait(waitTime).click()
                        else:
                            device.keyevent("4")   
                        print('【因为抓取门店到底而结束本次定位查询】')
                        if IsAllClassifyInput:
                            device.keyevent("4")
                        break
                    else:
                        AllClassifyInputClickNum += 1
                        continue
                else:
                    #当前页面展示的门店数量
                    if len(AllStore) > 4:  
                        if DeviceType == 1:
                            poco.swipe([0.5,0.8],[0.5,0.35],duration = 0.3) 
                        else:
                            poco.swipe([0.5,0.8],[0.5,0.5],duration = 0.3) 
                    else:                
                        #手机展示不会超过4 + 1个 P20展示5+1个
                        if DeviceType == 1:                            
                            poco.swipe([0.5,0.8],[0.5,0.45],duration = 0.3) 
                        else:                              
                            poco.swipe([0.5,0.8],[0.5,0.65],duration = 0.3) 
                    swipeNume += 1
                    #滑动了40次(至少是120家店) 且门店数量还是小于一页，那么认为这个也没滑动到底且没有门店滑动到底的提示
                    if swipeNume > 40:
                        if len(StoreList) < 6 or len(AllStore) < 4:                            
                            if not ClickClassify(poco,AllClassifyInputClickNum):
                                if backPage.exists():                                         
                                    backPage.wait(waitTime).click()
                                else:
                                    device.keyevent("4")   
                                #如果是大类进来的，还要在返回一次
                                if IsAllClassifyInput:
                                    device.keyevent("4")
                                print('认为这个也没滑动到底且没有门店滑动到底的提示而退出')
                                break
                            else:
                                AllClassifyInputClickNum += 1
                                continue
            else:
                #判断定位点附近是否有门店
                if poco(text = '该定位下暂无服务商家，请切换地址').exists():                    
                    print('~~~~~~~~~~~~~~~~该定位下暂无服务商家，请切换地址~~~~~~~~~~~~~~~~')                                        
                    if not ClickClassify(poco,AllClassifyInputClickNum):
                        if backPage.exists():                                         
                            backPage.wait(waitTime).click()
                        else:
                            device.keyevent("4")
                        if IsAllClassifyInput:
                            device.keyevent("4")            
                        break     
                    else:
                        AllClassifyInputClickNum += 1
                        continue                             
                storelenNum += 1
                if storelenNum > 5:
                    print('【因为获取门店列表长度为0而结束本次定位查询】')
                    if not ClickClassify(poco,AllClassifyInputClickNum):
                        if backPage.exists():                                         
                            backPage.wait(waitTime).click()
                        else:
                            device.keyevent("4")  
                        if IsAllClassifyInput:
                            device.keyevent("4")   
                        break    
                    else:
                        AllClassifyInputClickNum += 1
                        continue                
                else:
                    if DeviceType == 1:
                        poco.swipe([0.5,0.9],[0.5,0.7],duration = 0.3)
                    continue
        pass        
        print('===========================【'+ DeviceNum +'】抓取【' + address + '】完成===========================\n')    
    return currentTaskResult,False
    #有些情况没有滑动到底部就退出,因此要保证保证滑动到底部才更新定位点
    #改成在外面更新任务的状态
    #if IsBottomNum > 0:
    #    DbContext.updateAddressIsCap(address,len(StoreList))   
# 是否点击夜间送药
def ClickClassify(poco,AllClassifyInputClickNum):
    if AllClassifyInputClickNum == 1:
        if poco(text="夜间送药").exists():
            poco(text="夜间送药").wait(waitTime).click()
            return True
        else:
            return False
    else:
        return False
    