# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
import time
from CommonPackage.GlobalParameter import waitTime
from Operate.CloseUpdate import CloseUpDateInfo

#从大类跳转到搜索用药界面
def SearchDrugPage(poco,device,DeviceNum):
    CloseUpDateInfo(poco)    
    if poco(text="全部分类").exists():                
        poco(text="全部分类").wait(waitTime).click([0,0])
    switchNum = 0
    HasDrugClassify = False
    while True:
        try:
            if poco(text="买药").exists():
                poco(text="买药").wait(waitTime).click()
                HasDrugClassify = True
                break
            switchNum += 1            
            if switchNum > 4:
                break
            poco.swipe([0,0.95],[0,0.55],duration = 0.3) 
        except PocoNoSuchNodeException:
            continue
        except Exception as e:
            print('搜索买药页面异常')
    if HasDrugClassify:
        if poco(text="常用药品").exists():
            poco(text="常用药品").wait(waitTime).click()
            return True
        elif poco(text="夜间送药").exists():
            poco(text="夜间送药").wait(waitTime).click()
            return True
        else:            
            if poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].offspring("android.widget.Button")[0].offspring("android.widget.ImageView").exists():
                print('不存在药类相关的商家--返回上一页1')
                poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].offspring("android.widget.Button")[0].offspring("android.widget.ImageView").click()
            else:
                print('不存在药类相关的商家--返回上一页2')
                device.keyevent("4")   
            return False
        pass
    else:
        try:
            if poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].offspring("android.widget.Button")[0].offspring("android.widget.ImageView").exists():
                print('不存在送药上门--返回上一页1')
                poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].offspring("android.widget.Button")[0].offspring("android.widget.ImageView").click()
            else:
                print('不存在送药上门--返回上一页2')
                device.keyevent("4")           
        except Exception as e:            
            device.keyevent("4")   
        return HasDrugClassify
    