# -*- encoding=utf8 -*-
from poco.exceptions import PocoNoSuchNodeException
from poco.proxy import UIObjectProxy
from CommonPackage.GlobalParameter import waitTime
from airtest.core.android import Android
from Operate.CloseUpdate import CloseUpDateInfo

#从任意位置返回首页
def BackHomePage(poco,DbContext,DeviceNum,device):
    BackExceptionNum = 0
    BackNum = 0
    BackHomeStatus = False
    while True:
        try:      
            CloseUpDateInfo(poco)
            #新人领红包（关闭）
            if poco("com.sankuai.meituan.takeoutnew:id/close").exists():
                poco("com.sankuai.meituan.takeoutnew:id/close").click()
                print('新人领红包')
                continue
            #已经位于首页
            if poco("com.sankuai.meituan.takeoutnew:id/img_location_arrow").exists() or poco("com.sankuai.meituan.takeoutnew:id/layout_location_box").exists():
                BackHomeStatus = True
                break
            #单击美团外卖
            if poco(text = "美团外卖").exists():
                poco(text = "美团外卖").click() 
                continue
            #切换地址页面               
            if poco("com.sankuai.meituan.takeoutnew:id/left_action_view").exists():
                poco("com.sankuai.meituan.takeoutnew:id/left_action_view").wait(waitTime).click()
                print('切换地址页面返回')
                continue
            #已知未处理的1种情况应用无响应状态重启应用
            #手机有更新时取消更新,第一步
            if poco("android:id/button3").exists():
                poco("android:id/button3").click()
                continue
            #手机有更新时取消更新,第二步
            if poco("android:id/button2").exists():
                button2= poco("android:id/button2")
                if(button2.get_text() == "取消"):
                    button2.click()
                    continue
            #切换城市页面
            if poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.widget.ImageView").exists():
                poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.widget.ImageView").wait(waitTime).click()                
                print('切换城市页面返回')
                continue                    
            #送药上门页面                
            if poco("com.sankuai.meituan.takeoutnew:id/iv_back").exists():
                poco("com.sankuai.meituan.takeoutnew:id/iv_back").wait(waitTime).click()
                print('送药上门页面返回')
                continue
            #商家门店页面
            elif poco("com.sankuai.meituan.takeoutnew:id/img_back_light").exists():
                poco("com.sankuai.meituan.takeoutnew:id/img_back_light").wait(waitTime).click()
                print('商家门店页面返回')
                continue
            #商家详情界面
            elif poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[0].offspring("android.widget.ImageView").exists():
                poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[0].offspring("android.widget.ImageView").wait(waitTime).click()
                print('商家详情界面返回')
                continue 
            #从大类进入返回
            elif poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].offspring("android.widget.Button")[0].offspring("android.widget.ImageView").exists():
                poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].offspring("android.widget.Button")[0].offspring("android.widget.ImageView").click()
                print('商家详情界面返回')
                continue 
            
        except PocoNoSuchNodeException as e:            
            BackNum += 1
            if BackNum > 10:                             
                device.keyevent("4")  
                print(e)       
            if BackNum > 50:
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 返回首页异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')        
                DbContext.AddLog(DeviceNum,3,'设备['+ DeviceNum +']返回首页异常')
                break
            continue
        except Exception as e:
            BackExceptionNum += 1
            if BackExceptionNum > 50:
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 返回首页异常 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                DbContext.AddLog(DeviceNum,3,'设备['+ DeviceNum +']返回首页异常：' + repr(e).replace("'","").replace("\"",""))
                break
            continue
        pass        
    pass
    return BackHomeStatus