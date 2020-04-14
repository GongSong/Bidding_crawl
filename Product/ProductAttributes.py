# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

#滑动步长
switchStep = 3

def GetProductName(product,poco) -> str:
    #名称
    _productName = '获取名称失败'
    try:
        if product.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_name').exists():
            _productName = product.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_name').get_text()
        elif product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_name').exists():
            _productName = product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_name').get_text()
       
        return _productName    
    except Exception as e:
        print('爬取商品名称信息异常：' + repr(e))
        return _productName


def GetPrice(product,poco) -> float:
    _productCurrentPrice = -1
    switchNum = 0
    # while True:
    try:
            _productPrice = product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/ll_price_layout')
            #售价
            if _productPrice.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_price_fix').exists():
                _productCurrentPrice = _productPrice.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_price_fix').get_text()       
                # break
            # else:
                # poco.swipe([0.5,0.7],[0.5,0.65],duration = 0.3)
                # switchNum += 1
                # if switchNum > switchStep: #超过三次还是不显示就放弃
                #     break
    except Exception as e:
            print('爬取商品价格信息异常：' + repr(e))
            return _productCurrentPrice
    return _productCurrentPrice


#原价
def GetOriginPrice(product,poco) -> float:
    _productBeforePrice = -1
    switchNum = 0
    # while True:
    try:
            _productPrice = product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/ll_price_layout')
            if _productPrice.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_original_price_fix').exists():
                _productBeforePriceText = _productPrice.child(name = 'com.sankuai.meituan.takeoutnew:id/txt_stickyfoodList_adapter_food_original_price_fix').get_text()
                _productBeforePrice = float(_productBeforePriceText.replace('¥',''))
            # break
            # else:
            #     # poco.swipe([0.5,0.7],[0.5,0.65],duration = 0.3)
            #     switchNum += 1
            #     if switchNum > switchStep: #超过三次还是不显示就放弃
            #         break
    except Exception as e:
            print('爬取商品原价信息异常：' + repr(e))
            return _productBeforePrice
    return _productBeforePrice    



#折扣
def GetDiscount(product,poco) -> str:
    _productDiscount = '无折扣信息'
    switchNum = 0
    # while True:
    try:
            if product.offspring("com.sankuai.meituan.takeoutnew:id/txt_promotion_info").exists():                                    
                _productDiscount = product.offspring("com.sankuai.meituan.takeoutnew:id/txt_promotion_info").get_text()
                # break
            # else:
                # poco.swipe([0.5,0.7],[0.5,0.65],duration = 0.3)
                # switchNum += 1
                # if switchNum > switchStep: #超过三次还是不显示就放弃
                #     break
    except Exception as e:
            print('爬取商品折扣信息异常：' + repr(e))
            return _productDiscount
    return _productDiscount 


#销量
def GetSale(product,poco) -> int:
    _productSalesVolume = -1
    switchNum = 0
    # while True:
    try:
            if product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/tv_stickyfood_sold_count').exists():
                _productSalesVolumeStr = product.offspring(name = 'com.sankuai.meituan.takeoutnew:id/tv_stickyfood_sold_count').get_text()
                _productSalesVolume = int(_productSalesVolumeStr.replace('月售',''))
            #     break
            # else:
                # poco.swipe([0.5,0.7],[0.5,0.65],duration = 0.3)
                # switchNum += 1
                # if switchNum > switchStep: #超过三次还是不显示就放弃
                #     break
    except Exception as e:
            print('爬取商品销量信息异常：' + repr(e))
            return _productSalesVolume
    return _productSalesVolume 


