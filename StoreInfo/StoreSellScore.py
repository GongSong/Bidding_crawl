# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException

#获取门店名称
def GetStoreName(store):
    result = []
    try:
        if store.offspring("com.sankuai.meituan.takeoutnew:id/root_layout").child("android.widget.FrameLayout").child("android.widget.LinearLayout").child("android.widget.LinearLayout")[0].exists():
            storeUI = store.offspring("com.sankuai.meituan.takeoutnew:id/root_layout").child("android.widget.FrameLayout").child("android.widget.LinearLayout").child("android.widget.LinearLayout")[0]
            storeNameUI  = storeUI.offspring("android.widget.RelativeLayout")
            storeName = storeNameUI.child(name = "com.sankuai.meituan.takeoutnew:id/txt_poiList_adapter_name").get_text()                        
            result.append(True)
            result.append(storeUI)
            result.append(storeName)
            return result
        else:            
            result.append(False)      
            result.append('获取门店名称失败')        
            return result
    except PocoNoSuchNodeException:
        result.append(False)      
        result.append('获取门店名称异常')        
        return result        

#因为滑动幅度的问题,底部的肯定读取不到,直接向上滑动
#获取门店销量
def GetStoreSell(storeUI):
    result = []
    try:
        Sell_ScoreUI = storeUI.child("android.widget.LinearLayout")
        try:
            SellUI = Sell_ScoreUI.offspring("com.sankuai.meituan.takeoutnew:id/ll_poiList_poi_rating_sales")[0]
            Sell = SellUI.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_poiList_adapter_info_middle').get_text()    
        except PocoNoSuchNodeException:
            result.append(False)      
            result.append('获取SellUI异常')
            return result       
        result.append(True)
        result.append(Sell_ScoreUI)
        result.append(Sell)
        return result
    except PocoNoSuchNodeException:
        result.append(False)      
        result.append('获取门店销量异常')        
        return result
    pass

#获取门店评分
def GetStoreScore(Sell_ScoreUI):
    result = []
    try:
        ScoreUI = Sell_ScoreUI.offspring("com.sankuai.meituan.takeoutnew:id/txt_poiList_poi_rating_num")[0]
        Score = ScoreUI.get_text()
        result.append(True)
        result.append(Score)
        return result
    except PocoNoSuchNodeException:
        result.append(False)      
        result.append('获取门店评分异常')        
        return result
    pass