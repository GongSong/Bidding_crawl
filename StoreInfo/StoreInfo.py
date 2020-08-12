# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import time
from airtest.core.android import Android
from CommonPackage.GlobalParameter import waitTime,FaileAddress,FaileAddresstagList

def GetStoreInfo(poco,DbContext,DeviceNum):  
    storeAddress = FaileAddress
    NoShopInfoNum = 0
    notAddressList = DbContext.GetFilterKeyword()
    # device = Android(DeviceNum) 

    while True:            
        try:
            if poco(text = "重新加载").exists():
                print('~~~~~~~~~~~~~~~本店暂无在售商品，稍后再来吧~~~~~~~~~~~~~~~')
                poco("com.sankuai.meituan.takeoutnew:id/img_back_gray").wait(waitTime).click()
                return storeAddress               
            poco("com.sankuai.meituan.takeoutnew:id/btn_more_poi_dark").wait(waitTime).click()
            
            if poco(text="商家详情").exists():        
                poco(text="商家详情").click()                        
                ExceptionNum = 0
                time.sleep(1)
                while True:
                    try:                        
                        #view = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.support.v4.view.ViewPager").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup").wait(waitTime)                        
                        #view = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.support.v4.view.ViewPager").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup").wait(waitTime)
                        #重试5次后还是无法获取到地址就代表着这个界面的标签是另一种
                        if ExceptionNum<3:
                            #老版
                            view = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.support.v4.view.ViewPager").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup").wait(waitTime)
                        elif ExceptionNum>=7:
                            #新版 有品牌故事
                            view = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[4].child("android.widget.HorizontalScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup").wait(waitTime)
                        else:
                            #新版 无品牌故事
                            view = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.widget.HorizontalScrollView")[0].child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup").wait(waitTime)

                       
                        if view.exists():
                            if len(view) > 1:
                                item = view[1].child(name = 'android.widget.TextView')
                                if item.exists():        
                                    storeAddress = item.get_text().replace('\'','|')
                                    #判断是否是正确的地址
                                    for item in notAddressList:
                                        if item in storeAddress:
                                            storeAddress = FaileAddress
                                            break
                                else:
                                    print('~~~~~~~~~~~~~~~获取地址信息失败~~~~~~~~~~~~~~~')
                                break
                            else:
                                print('~~~~~~~~~~~获取界面定位为空_1~~~~~~~~~~~')
                        else:
                            print('~~~~~~~~~~~获取界面定位为空_2~~~~~~~~~~~')
                    except PocoNoSuchNodeException:                        
                        ExceptionNum += 1
                        if ExceptionNum <=10:
                            time.sleep(1)
                            continue
                        else:
                            # device.adb.start_cmd("adb shell")
                            # device.adb.start_cmd("su")
                            # device.adb.start_cmd("wipe cache")
                            # device.adb.start_cmd("exit")
                            # device.adb.start_cmd("exit")
                            # device.adb.start_cmd("adb reboot")
                            print('~~~~~~~~~~~~~~~~~~~~~~~~超过10次没有获取到地址信息 自动返回~~~~~~~~~~~~~~~~~~~~~~~~')
                            break #超过五次不在重试
                pass                
            pass               
            poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[0].offspring("android.widget.ImageView").wait(waitTime).click()
            poco("com.sankuai.meituan.takeoutnew:id/img_back_light").wait(waitTime).click()
            break
        except PocoNoSuchNodeException:
            if poco("com.sankuai.meituan.takeoutnew:id/txt_tips").exists(): #已经打烊的店铺            
                print('~~~~~~~~~~~~~~店铺打烊 继续抓取~~~~~~~~~~~~~~')
                NoShopInfoNum += 1
                if NoShopInfoNum >= 3:
                    print('~~~~~~~~~~~~~~店铺打烊 抓取不到~~~~~~~~~~~~~~')
                    poco("com.sankuai.meituan.takeoutnew:id/img_back_gray").click()
                    break
                #滑动一下
                poco.swipe([0.5,0.9],[0.5,0.8],duration = 0.1)                 
                pass     
            else:      
                NoShopInfoNum += 1                      
                if NoShopInfoNum >= 3:
                    print('~~~~~~~~~~~~~~~本店暂无在售商品，稍后再来吧~~~~~~~~~~~~~~~')
                    poco("com.sankuai.meituan.takeoutnew:id/img_back_gray").click()
                    break                   
        except Exception as e:
            DbContext.AddLog(DeviceNum,3,'设备['+ DeviceNum +']爬取门店地址异常：' + repr(e))
            break
    pass
    return storeAddress
    
