# -*- encoding=utf8 -*-
from poco.exceptions import PocoNoSuchNodeException
from poco.proxy import UIObjectProxy
from CommonPackage.GlobalParameter import waitTime
from Operate.SwitchingCity import SwitchingCity
from Operate.CloseUpdate import CloseUpDateInfo
import time
import random

from Send_Message import send_text
from Send_Message import send_email
#切换定位


def SwithPosition(poco, address, targetCity, storeName,SwitchNum):
    sec = random.randint(190, 320)
    print('睡眠-'+str(sec)+'-秒')
    # time.sleep(sec)
    CloseUpDateInfo(poco)
    #单击定位点
    if poco("com.sankuai.meituan.takeoutnew:id/img_location_arrow").exists():
        poco("com.sankuai.meituan.takeoutnew:id/img_location_arrow").wait(waitTime).click()
    elif poco("com.sankuai.meituan.takeoutnew:id/layout_location_box").exists():
        poco("com.sankuai.meituan.takeoutnew:id/layout_location_box").wait(waitTime).click()
    # 判断当前定位城市是否是要爬取的城市
    if SwitchNum < 2:
        IsTarGetcity = SwitchingCity(poco, targetCity)
        pass
    else:
        IsTarGetcity = True
    
    if IsTarGetcity:
        CloseUpDateInfo(poco)
        #输入定位点
        poco(name="com.sankuai.meituan.takeoutnew:id/address_search_map_txt").click()
        poco(name="com.sankuai.meituan.takeoutnew:id/address_search_map_txt").set_text(address)

        #单击搜索
        Searchelem = poco("com.sankuai.meituan.takeoutnew:id/search_address_txt")    
        if Searchelem.exists():        
            Searchelem.wait(waitTime).click()#搜索
            returnelem = poco("com.sankuai.meituan.takeoutnew:id/left_action_view")
            try:
                if poco(text='没有找到相关地址').exists():
                    print('没有找到相关地址')
                    content = '监控到：' + storeName + '-' + targetCity + '-' + address + '相关地址没有找到！'
                    # send_text(content=content)
                    if returnelem.exists():
                        returnelem.wait(waitTime).click()
                    return False
                elif poco(text='啊哦，网络悄悄跑到外星球去了~').exists():
                    print('美团定位接口被封~')
                    # time.sleep(1)


                try:
                    searchList = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/root_view_fl").offspring("com.sankuai.meituan.takeoutnew:id/list_map_location_info").child("android.widget.LinearLayout")
                except PocoNoSuchNodeException:
                    searchList = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/root_view_fl").offspring("android.widget.ListView").child("android.view.ViewGroup")
                if len(searchList) > 0:                
                    try:
                        if poco("com.sankuai.meituan.takeoutnew:id/txt_map_adapter_name").exists():                            
                            poco("com.sankuai.meituan.takeoutnew:id/txt_map_adapter_name").click()#选定 地址(只有一个)
                            return True
                        searchList[0].wait(waitTime).click()  # 选定 地址(多个)
                    except PocoNoSuchNodeException:                        
                        returnelem.wait(waitTime).click()
                        if returnelem.exists():
                            returnelem.wait(waitTime).click()
                            return False
                        pass
                    return True
                else:                                    
                    returnelem.wait(waitTime).click()
                    returnelem.wait(waitTime).click()
                    return False
            except PocoNoSuchNodeException:            
                returnelem.wait(waitTime).click()
                if returnelem.exists():                
                    returnelem.wait(waitTime).click()
                return False   
        pass
    return False               