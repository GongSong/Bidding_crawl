# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from CommonPackage.GlobalParameter import waitTime
from DbHelper.DbHelper import DbHelper
from StoreInfo.StoreSellScore import GetStoreName
from Operate.SwitchingPosition import SwithPosition
from Operate.SearchDrug import SearchDrugPage
from Product import ProductInfo
import time

def SearchCatchStore(storeId:str,poco,device,DeviceNum:str,DeviceType:int):
    #查找到该门店的相关信息
    AllClassifyInputClickNum = 0#大类进入点击小类的次数
    IsAllClassifyInput = False #是否从大类搜索进入(默认不是)
    DbContext = DbHelper()

    result = DbContext.GetStorePoint(storeId)
    if len(result) == 1:
        #address字段可能找不到这个店，用AnchorPoint才能找到这个店
        strs =str(result[0]['AnchorPoint']).split(';')
        StoreAddress =strs[0]
        StoreName = result[0]['shopName']
        StoreCity = result[0]['City']
       
        IsAddress = SwithPosition(poco,StoreAddress,StoreCity,0)#切换定位
        if not IsAddress:
            return False
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
        poco("com.sankuai.meituan.takeoutnew:id/action_search").click()
        time.sleep(1) #睡眠一段时间等待页面加载
        poco("com.sankuai.meituan.takeoutnew:id/txt_search_keyword").click()
        poco("com.sankuai.meituan.takeoutnew:id/txt_search_keyword").set_text(StoreName)
        poco("com.sankuai.meituan.takeoutnew:id/search_tv").click() 
        time.sleep(3) #睡眠一段时间等待页面加载
        storeNames = poco("com.sankuai.meituan.takeoutnew:id/list_poiSearch_poiList").child("android.widget.LinearLayout")
        for sName in storeNames:
            if DealStoreName(sName.offspring("com.sankuai.meituan.takeoutnew:id/textview_poi_name").get_text())==DealStoreName(StoreName):
                #找到要爬取的门店,继续商品信息
                sName.wait(waitTime).click()                            
                CatchProductResult = ProductInfo.GetProduct(poco,device,storeId)

        return 
        swipeNume= 0
        #第一次大幅度滑动
        if DeviceType == 1:            
            poco.swipe([0.2,0.9],[0.2,0.45],duration = 0.3)  
        else:
            poco.swipe([0.4,0.9],[0.4,0.75],duration = 0.3) 
        backPage = poco("com.sankuai.meituan.takeoutnew:id/iv_back")    
        bottomElement = poco("com.sankuai.meituan.takeoutnew:id/noMoreView")
        if IsAllClassifyInput:
            if poco(text="常用药品").exists():
                poco(text="常用药品").click()
                AllClassifyInputClickNum += 1
        IsSearch = False
        storelenNum = 0
        while True:
            AllStore = poco("com.sankuai.meituan.takeoutnew:id/fl_fragment_container").offspring("com.sankuai.meituan.takeoutnew:id/pull_to_refresh_view").offspring("com.sankuai.meituan.takeoutnew:id/viewpager_content").offspring("com.sankuai.meituan.takeoutnew:id/wm_st_poi_channel_list").child("android.widget.FrameLayout").wait(waitTime)
            i = 0
            if len(AllStore) > 0:               
                try:                   
                    for store in AllStore:
                        if i == 0:
                            i += 1 #第一个是顶部筛选
                            continue
                        storeNameResult =  GetStoreName(store)                        
                        if not storeNameResult[0]:                            
                            continue                        
                        storeName = storeNameResult[2]                        
                        if DealStoreName(StoreName) == DealStoreName(storeName):
                            #找到要爬取的门店,继续商品信息
                            IsSearch = True
                            store.wait(waitTime).click()                            
                            CatchProductResult = ProductInfo.GetProduct(poco,device,storeId)
                            break
                    if IsSearch:
                        break
                except Exception as e:
                    DbContext.AddLog(DeviceNum,3,'设备['+ DeviceNum +']爬取门店列表异常：' + repr(e).replace("'","").replace("\"",""))
                if IsSearch:
                    if AllStore.exists():
                        device.keyevent("4")
                    break
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
                        if len(AllStore) < 4:                            
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

def DealStoreName(shopName:str):
    symbolList = ['(',')','（','）',' ']
    for item in symbolList:
        shopName = shopName.replace(item,'')    
    return shopName    


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