# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import datetime
import time
from CommonPackage.GlobalParameter import waitTime
from Product.ProductAttributes import GetProductName,GetPrice,GetOriginPrice,GetDiscount,GetSale
from DbHelper.DbHelper import DbHelper

#获取商品
def GetProduct(poco,device,storeId):
    if( poco("com.sankuai.meituan.takeoutnew:id/category_recycler_view").exists()):
        poco("com.sankuai.meituan.takeoutnew:id/category_recycler_view").swipe([-0.8,0],duration = 0.5)
    time.sleep(3) #睡眠一段时间等待页面加载
   

    ContainAll = poco(text="全部分类")
    IsContainAll = ContainAll.exists()
    AllProductInfoList = []
    ErrorMessage = 'success'
    DbContext = DbHelper()
    if IsContainAll:
        #找到父节点        
        parent = ContainAll.parent()
        parent.wait(waitTime).click() #全部分类界面
    StartTime = datetime.datetime.now()
    time.sleep(1) #睡眠一段时间等待页面加载
    SlideNum = 0 #滑动次数
    BottomNum = 0 #到达底部次数
    CategaryNum= 0 #爬取的大类数目（一般药店第一个是折扣商品会包含折扣、原价信息,之后的几个大类下的商品则不会包含）        
    #用于存储抓取的商品数量
    CurrentProductNum = 0
    maxNum = 0
    while True:       
        try:             
            # if SlideNum % 5 == 0:#滑动几次之后大概睡眠一会
            #     time.sleep(1) #睡眠一段时间等待页面加载
            # else:                    
                #poco.swipe([0.5,0.7],[0.5,0.4],duration = 0.3)
                #判断是否出现释放展示下一类按钮
            #     nextCategary = poco("com.sankuai.meituan.takeoutnew:id/tv_refresh").wait(waitTime).exists()
            #     if nextCategary:
            #         print('===================当前药品大类抓取完成===================')         
            #         CategaryNum += 1       
            #         pass
            # SlideNum += 1     
            #当前要抓取的大类所能看见的界面展示  
            '''
            if nextCategary:
                time.sleep(1)     
                nextCategary = False'''
            time.sleep(1)
            CurrentClassfiy = poco("com.sankuai.meituan.takeoutnew:id/layout_shop_root_scroll_container").offspring("com.sankuai.meituan.takeoutnew:id/priority_scrollview").offspring("com.sankuai.meituan.takeoutnew:id/poi_pinned_layout").child("android.support.v7.widget.RecyclerView").child("android.widget.FrameLayout")
            if(len(CurrentClassfiy)==0):
                CurrentClassfiy = poco("com.sankuai.meituan.takeoutnew:id/recycler").offspring("com.sankuai.meituan.takeoutnew:id/ll_stickyfoodList_adapter_food_food")
            if(len(CurrentClassfiy)==0):
                CurrentClassfiy = poco("com.sankuai.meituan.takeoutnew:id/recycler").offspring("com.sankuai.meituan.takeoutnew:id/ll_stickyfoodList_adapter_food_food")

            if len(CurrentClassfiy) > 0:                                    
                message = '【名称】：%s  【售价】:%s  【原价】：%s 【销量】：%s 【折扣】：%s'
                print("本批抓到"+str(len(CurrentClassfiy))+"个")
                for product in CurrentClassfiy:   
                    try:         
                        #商品信息                        
                        # if(product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/ll_stickyfoodList_adapter_food_food').exists()):
                        #     product =product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/ll_stickyfoodList_adapter_food_food')
                        # if len(product)== 0:  
                        #     print("当前为非商品标签")
                        #     continue
                        #名称
                        _productName = GetProductName(product,poco)
                        if _productName == '获取名称失败':
                            continue
                        if _productName in AllProductInfoList:
                            print("【"+_productName+"】商品已存在")
                            continue    #之前爬取过的就不做处理
                        else:                                
                            # _productPrice = product.child(name = 'com.sankuai.meituan.takeoutnew:id/ll_stickysold_count_unit_price_original_price_fix').child(name = 'com.sankuai.meituan.takeoutnew:id/ll_price_layout')
                            #销量
                            _productSalesVolume = GetSale(product,poco)      
                            #售价
                            _productCurrentPrice = GetPrice(product,poco)
                            if _productCurrentPrice != -1:
                                #只有拿到售价的才算爬到商品的信息
                                AllProductInfoList.append(_productName)
                            #原价
                            if CategaryNum < 2: 
                                _productBeforePrice = GetOriginPrice(product,poco)                                    
                            else:
                                _productBeforePrice = '暂不获取原价'                                                         
                            #折扣
                            if CategaryNum < 2:
                                _productDiscount = GetDiscount(product,poco)                                    
                            else:
                                _productDiscount = '暂不获取折扣'
                            print(message % (str(_productName),str(_productCurrentPrice),str(_productBeforePrice),str(_productSalesVolume),str(_productDiscount)))                
                            #入库
                            if _productCurrentPrice != -1:                                    
                                DbContext.SynchroProductInfo(storeId,_productName,int(_productSalesVolume),float(_productCurrentPrice),str(_productBeforePrice),str(_productDiscount))
                    except Exception as e:                    
                        if('UIObjectProxy' in repr(e)):                            
                            continue #不存在的元素就直接下一个
                        else:
                            print('获取商品信息异常：'+repr(e))
                            ErrorMessage = 'error'
                            continue                            
            #判断是否滑动到底部
            #爬完一页
            print("爬完一批")
            Isbottom = poco("com.sankuai.meituan.takeoutnew:id/noMoreView").exists()    
            if Isbottom:
                BottomNum += 1
                if BottomNum == 1:
                    print('~~~~~~~~~~~~~~~~~~~~到达底部~~~~~~~~~~~~~~~~~~~~')
                else:
                    print('~~~~~~~~~~~~~~~~~全部药品抓取完成~~~~~~~~~~~~~~~')
                    break    
            else:  
                productNum = len(AllProductInfoList)
                #统计每次这个数量出现的频率,因为有的时候滑动到底部不会有到底的提示,所以当商品数量多次滑动不再增加的时候
                #就认为商品抓取完毕
                if CurrentProductNum !=productNum:
                    CurrentProductNum = productNum
                    maxNum=0
                else:
                    maxNum+=1
                
                #滑动20次依旧没有商品新增,则认为到底了
                if maxNum > 20:
                    print('~~~~~~~~~~~~~~~~~程序判定滑动到了底部~~~~~~~~~~~~~~~')
                    break
                else:
                    device_screen = poco.get_screen_size()
                    device_x = device_screen[0]
                    device_y = device_screen[1]        
                    if device_y > 1600 and device_x > 1080:
                        DeviceType = 2
                    else:
                        DeviceType = 1   
                   
                    if DeviceType == 1: 
                        poco.swipe([0.5,0.8],[0.5,0.2],duration = 0.2)
                    else:            
                        poco.swipe([0.5,0.8],[0.5,0.3],duration = 0.4)
                    
            pass
        except PocoNoSuchNodeException:
            continue
        except Exception as e:
            print('爬取商品信息异常：' + repr(e))
            continue
    pass
    EndTime = datetime.datetime.now()
    print('本次抓取耗时：'+ str(((EndTime - StartTime).seconds)/60) + '  爬取药品数量：'+str(len(AllProductInfoList)))
    #连续返回两次上一页
    backPage = poco("com.sankuai.meituan.takeoutnew:id/img_back_light")
    if backPage.exists():
        print('返回上一页')
        backPage.wait(waitTime).click()
        backPage.wait(waitTime).click()
    else:
        device.keyevent("4")
        device.keyevent("4")   
    return ErrorMessage