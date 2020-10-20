# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from CommonPackage.GlobalParameter import waitTime
from DbHelper.DbHelper import DbHelper
from Product.GetsData import get_shopName
from Send_Message import send_text
from StoreInfo.StoreSellScore import GetStoreName
from Operate.SwitchingPosition import SwithPosition
from Operate.SearchDrug import SearchDrugPage
from Product import ProductInfo
import time
from Operate.BackHomePage import BackHomePage
from .SearchPartProduct import get_goods


def SearchCatchStore(storeName: str, poco, device, DeviceNum: str, DeviceType: int):
    # 查找到该门店的相关信息
    AllClassifyInputClickNum = 0  # 大类进入点击小类的次数
    IsAllClassifyInput = False  # 是否从大类搜索进入(默认不是)
    DbContext = DbHelper()

    # result = DbContext.GetStorePoint(storeId)
    result = DbContext.GetStorePointForName(storeName)
    if len(result) == 1:
        # address字段可能找不到这个店，用AnchorPoint才能找到这个店
        strs = str(result[0]['AnchorPoint']).split(';')
        StoreAddress = strs[0]
        StoreName = result[0]['shopName']
        StoreCity = result[0]['City']
        storeId = result[0]['mtWmPoiId']

        IsAddress = SwithPosition(poco, StoreAddress, StoreCity, storeName, 0)  # 切换定位
        isExists = getStore(IsAddress, poco, DeviceNum,
                            IsAllClassifyInput, StoreName, device)
        if(not isExists):
            BackHomePage(poco, DbContext, DeviceNum, device)  # 返回首页
            StoreAddress = result[0]['address']
            IsAddress = SwithPosition(poco, StoreAddress, StoreCity, storeName, 0)  # 切换定位
            isExists = getStore(IsAddress, poco, DeviceNum, IsAllClassifyInput, StoreName, device)
            if(not isExists):
                # DbContext.AddLog(DeviceNum, 2, '爬取['+StoreName+']失败，没找到店铺')
                print('该店铺不存在！')
    pass

def search_store(storeName, poco, device, DeviceNum, DeviceType, flag, spider_num):  # 从excel获取地址
    IsAllClassifyInput = False  # 是否从大类搜索进入(默认不是)
    DbContext = DbHelper()

    we_address = get_shopName()[2]
    other_address = get_shopName()[3]
    we_storeCity = get_shopName()[4]
    other_storeCity = get_shopName()[5]

    # if DeviceNum == '' or DeviceNum == '5LM0216B03001264':
    #     StoreAddress = we_address[flag]
    #     StoreCity = we_storeCity[flag][0:-1]
    #     IsAddress = SwithPosition(poco, StoreAddress, StoreCity, storeName, DeviceNum, 0)  # 切换定位
    #     getStore(IsAddress, poco, DeviceNum, IsAllClassifyInput, storeName, device, flag, spider_num)
    if DeviceNum == '5LM0216910000994'or DeviceNum == '5LM0216902001108' or DeviceNum == 'DLQ0216729004546' or DeviceNum == 'APU0216408028484' or DeviceNum == '5LM0216B03001264' or DeviceNum == 'QVM0215C03007968' or DeviceNum == 'DLQ0216630004610' or DeviceNum == 'E4J4C17405011422' or DeviceNum == 'APU0215C11003517' or DeviceNum == 'APU0216226004541':
        StoreAddress = other_address[flag]
        StoreCity = other_storeCity[flag][0:-1]
        IsAddress = SwithPosition(poco, StoreAddress, StoreCity, storeName, DeviceNum, 0)  # 切换定位
        getStore(IsAddress, poco, DeviceNum, IsAllClassifyInput, storeName, device, flag, spider_num)

#5LM0216902001108


def DealStoreName(shopName: str):
    symbolList = ['(', ')', '（', '）', ' ']
    for item in symbolList:
        shopName = shopName.replace(item, '')
    return shopName


def getStore(IsAddress, poco, DeviceNum, IsAllClassifyInput, StoreName, device, flag, spider_num):
    if not IsAddress:
        return False

    try:
        time.sleep(3)
        if DeviceNum == '0123456789ABCDEF':
            if poco(text="买药").exists():
                poco(text="买药").wait(waitTime).click([0, 0])
        else:
            poco.swipe([0.5, 0.6], [0.5, 0.5], duration=0.3)
            if poco(text="买药").exists():
                poco(text="买药").wait(waitTime).click([0, 0])

        if poco(text='医药新人礼包').exists():
            poco("android.widget.FrameLayout").offspring("android:id/content").child(
                "android.widget.FrameLayout").child(
                "android.widget.FrameLayout").child("android.widget.FrameLayout").child(
                "android.widget.FrameLayout").child(
                "android.widget.FrameLayout").child("android.widget.FrameLayout")[2].child(
                "android.widget.ImageView").click()
        # elif poco(text='会员卡包').exists():
        #     poco('')
        # result = SearchDrugPage(poco, device, DeviceNum)
        # if not result:
        #     print(DeviceNum)
        #     print(
        #         '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 第一个定位点无买药 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        #     IsAddress = False
        # else:
        #     IsAllClassifyInput = True
    except PocoNoSuchNodeException:
        print(DeviceNum)
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 第一个定位点无买药 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        IsAddress = False
        pass
    if poco(text='会员卡包').exists():
        poco('com.sankuai.meituan.takeoutnew:id/tv_medicine_more_entrance').click()
    poco.swipe([0.5, 0.5], [0.5, 0.9], duration=0.3)
    time.sleep(5)
    poco('com.sankuai.meituan.takeoutnew:id/tv_header_search_view').wait(10).click()
    time.sleep(3)  # 睡眠一段时间等待页面加载
    poco("com.sankuai.meituan.takeoutnew:id/txt_search_keyword").click()
    poco("com.sankuai.meituan.takeoutnew:id/txt_search_keyword").set_text(StoreName)
    time.sleep(1)  # 睡眠一段时间等待页面加载
    poco("com.sankuai.meituan.takeoutnew:id/search_tv").click()
    time.sleep(3)  # 睡眠一段时间等待页面加载

    storeNames = poco("com.sankuai.meituan.takeoutnew:id/list_poiSearch_poiList").child("android.widget.LinearLayout").wait(5)
    # isExists = False
    a = 0
    poco.swipe([0.5, 0.5], [0.5, 0.9], duration=3)
    time.sleep(5)
    for sName in storeNames:
        if sName.offspring("com.sankuai.meituan.takeoutnew:id/textview_poi_name").exists():
            # 找到要爬取的门店,继续商品信息
            stName = DealStoreName(sName.offspring(
                "com.sankuai.meituan.takeoutnew:id/textview_poi_name").get_text())
            # print("店名："+stName)
            if stName == DealStoreName(StoreName):
                a += 1
                if poco('com.sankuai.meituan.takeoutnew:id/imageview_mt_delivery').exists():  # 出现全城送
                    sName.wait(waitTime).click()
                    if poco(text='本店休息啦').exists():
                        poco.swipe([0.5, 0.9], [0.5, 0.8], duration=0.3)
                    time.sleep(5)
                else:
                    sName.wait(waitTime).click()
                    time.sleep(1)
                    if poco(text='本店休息啦').exists():
                        poco.swipe([0.5, 0.9], [0.5, 0.8], duration=0.3)
                    # CatchProductResult = ProductInfo.GetProduct(poco, device, storeId)

                poco('com.sankuai.meituan.takeoutnew:id/search_background').click()  # 点击搜索框
                get_goods(poco, device, stName, DeviceNum, flag, spider_num)
                time.sleep(1)
                try:
                    poco('com.sankuai.meituan.takeoutnew:id/img_back_gray').click()  # 从药品列表页再返回
                except:
                    poco('com.sankuai.meituan.takeoutnew:id/img_back_light').click()
    if a == 0:
        content = '监控到：' + str(flag)+'--' + StoreName + '--根据地址没有找到店名！'
        send_text(content)
        print(content)



    # return isExists
    pass

# 是否点击夜间送药
def ClickClassify(poco, AllClassifyInputClickNum):
    if AllClassifyInputClickNum == 1:
        if poco(text="夜间送药").exists():
            poco(text="夜间送药").wait(waitTime).click()
            return True
        else:
            return False
    else:
        return False
