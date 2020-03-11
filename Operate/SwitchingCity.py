# -*- encoding=utf8 -*-
from poco.exceptions import PocoNoSuchNodeException
from poco.proxy import UIObjectProxy
from CommonPackage.GlobalParameter import waitTime
import time
from Operate.CloseUpdate import CloseUpDateInfo

#切换定位城市
#切换失败返回False
def SwitchingCity(poco,targetcity):
    CloseUpDateInfo(poco)
    if poco("com.sankuai.meituan.takeoutnew:id/wm_address_city_location_text").exists():
        #当前定位城市   
        CloseUpDateInfo(poco)
        print('目标城市：'+targetcity)                         
        CurrentlocateCity = poco("com.sankuai.meituan.takeoutnew:id/wm_address_city_location_text").wait(waitTime).get_text()
        if targetcity not in CurrentlocateCity :
            #跳转到切换城市页面            
            poco("com.sankuai.meituan.takeoutnew:id/wm_address_city_location_arrow").wait(waitTime).click()                        
            try:
                time.sleep(3)
                locate = poco(text = "输入城市名进行搜索").wait(waitTime)
                if locate.exists():                    
                    #搜索
                    locate.wait(waitTime).click()                    
                    locate.wait(waitTime).set_text(targetcity)      
                    time.sleep(3)           
                    #选定                                                          
                    if poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[1].child("android.widget.TextView").exists():
                        poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup").child("android.view.ViewGroup")[1].child("android.widget.TextView").click()                        
                        return True
                    elif poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup").exists():                        
                        poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup").click()                        
                        return True
                    else:
                        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 没有搜索到指定城市 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        return False                                                     
                else:
                    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 定位输入框没找到 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    return False
            except PocoNoSuchNodeException as e:                
                print('设置定位城市异常:' + repr(e))
                return False
            
        else:
            #当前定位为目标城市
            return True        
    else:
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o(╥﹏╥)o 获取当前定位城市失败 o(╥﹏╥)o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return False
    pass