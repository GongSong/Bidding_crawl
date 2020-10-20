import time
from datetime import datetime
from Product.GetsData import get_drug
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


def get_goods(poco, device, stName, DeviceNum, flag, spider_num):
    drugname_list = get_drug()  # 获取药品名称
    for Drugname in drugname_list:
        GetPartProduct(poco, device, Drugname, stName, DeviceNum, flag, spider_num)
    poco('android.widget.ImageView').click()  # 返回药店详情页
    if poco(text='您在购药过程中遇到了什么问题？').exists():
        poco('com.sankuai.meituan.takeoutnew:id/medical_new_user_dialog_button_negative').click()


# 查询部分药品的数据，并将数据写入数据库
def GetPartProduct(poco, device, Drugname, stName, DeviceNum, flag, spider_num):  # poco, device参数
    poco.swipe([0.5, 0.5], [0.5, 0.9], duration=0.3)
    time.sleep(5)
    try:
        poco('android.widget.EditText').click()
        if poco('com.sankuai.meituan.takeoutnew:id/txt_search_keyword').exists():
            poco('com.sankuai.meituan.takeoutnew:id/txt_search_keyword').click()
    except:
        poco('com.sankuai.meituan.takeoutnew:id/tv_search_hint').click()
    device.text(text=Drugname)  # 输入要查询的药名
    # 获取查询到的数据列表，以获得药的月售，价格信息
    items = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup")
    time.sleep(1)
    if items:
        a = search_name(items, Drugname, stName, DeviceNum, flag, spider_num)
        if a == 0:
            poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").click()
            poco('android.widget.EditText').click()
            device.text(text=Drugname)  # 输入要查询的药名
            time.sleep(1)
            items = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup")
            if items:
                a = search_name(items, Drugname, stName, DeviceNum, flag, spider_num)
                if a == 0:
                    print('提示：这家店' + Drugname + '药品不存在！')
                    not_exists(stName, Drugname, DeviceNum, flag, spider_num)
            else:
                print('提示：这家店' + Drugname + '药品不存在！')
                not_exists(stName, Drugname, DeviceNum, flag, spider_num)

    else:  # 第二次查找药品
        poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").wait().click()
        poco('android.widget.EditText').click()
        device.text(text=Drugname)  # 输入要查询的药名
        time.sleep(1)
        items = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup")
        if items:
            a = search_name(items, Drugname, stName, DeviceNum, flag, spider_num)
            if a == 0:
                print('提示：这家店' + Drugname + '药品不存在！')
                not_exists(stName, Drugname, DeviceNum, flag, spider_num)
        else:
            if Drugname == Drugname == '[可丽蓝]早早孕测试笔(验孕棒)1支'or '[毓婷]左炔诺孕酮片0.75mg*2片'or Drugname == '[金毓婷]左炔诺孕酮片1.5mg*1片'or Drugname=='[金戈]枸橼酸西地那非片50mg*1片*1板'or Drugname=='[芬必得]布洛芬缓释胶囊0.3g*10粒*2板' or Drugname=='[丹媚]左炔诺孕酮肠溶片1.5mg*1片'or Drugname=='[杜蕾斯]天然胶乳橡胶避孕套(超薄装)隐feel52mm*3只'or Drugname=='[江中]健胃消食片(成人)0.8g*8片*4板'or Drugname=='[云南白药]蒲地蓝消炎片0.3g*48片'or Drugname=='[康恩贝]肠炎宁片0.42g*12片*2板' or Drugname=='[白云山]板蓝根颗粒10g*20袋':
                b = 0
                for i in range(2):
                    time.sleep(1)
                    try:
                        poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").click()
                    except:
                        pass
                    poco('android.widget.EditText').click()
                    device.text(text=Drugname)

                    items = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup")
                    if items:
                        a = search_name(items, Drugname, stName, DeviceNum, flag, spider_num)
                        if a != 0:
                            b += 1
                            break
                if b == 0:
                    print('提示：这家店' + Drugname + '药品不存在！')
                    not_exists(stName, Drugname, DeviceNum, flag, spider_num)
            else:
                print('提示：这家店' + Drugname + '药品不存在！')
                not_exists(stName, Drugname, DeviceNum, flag, spider_num)
    conn.commit()
    # 点击清除药名
    try:
        poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").click()
    except:
        pass


def search_name(items, Drugname, stName, DeviceNum, flag, spider_num):   # 存储存在的药品
    a = 0
    for item in items:
        datetime_z = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取日期，时间
        time.sleep(1)
        goods_list = item.child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").children()  # 获取一列内的所有信息，药品列表
        try:
            if Drugname == goods_list[0].get_text():  # 药名相等，获取数据
                month_sale = goods_list[1].get_text()  # 月售
                # print(month_sale, '----------------1')
                if month_sale == None:
                    month_sale = goods_list[2].get_text()
                    # print(month_sale, '---------------2')
                price = goods_list[3].get_text()  # 价格
                print(price, '----------------------3')
                if price == None or '券' in price or '折' in price or '第' in price:
                    price = goods_list[4].get_text()  # 折扣价格
                    sell_out = ''
                    print(price, '--------------4')
                    if price == None or '券' in price or '折' in price or '赠' in price or '第' in price:
                        price = goods_list[5].get_text()
                        print(price, '--------------5')
                        sell_out = ''  # 没有售罄的就为空
                        if price == None or '折' in price or '第' in price:
                            price = goods_list[6].get_text()
                            print(price, '---------------6')
                            sell_out = ''
                            if price == None:
                                price = goods_list[7].get_text()
                                print(price, '---------------7')
                                sell_out = ''
                        # try:
                        #     price6 = goods_list[6].get_text()
                        #     print(price6, '---------------6')
                        #     if float(price5[1:]) >= float(price6[1:]):  # 判断5和6的价格高低，来获取低的折扣价格
                        #         price = price6  # 取出折扣价格
                        #
                        #         sell_out = ''  # 没有售罄的就为空
                        #     else:
                        #         price = price5
                        #
                        #         sell_out = ''  # 没有售罄的就为空
                        # except:
                        #     if price5 == None:
                        #         price = goods_list[7].get_text()
                        #         print(price, '--------------------7')
                        #         sell_out = ''  # 没有售罄的就为空
                        #     else:
                        #         price = price5
                        #         print(price, '--------------5')
                        #         sell_out = ''  # 没有售罄的就为空
                else:
                    sell_out = '已售罄'
                sale = month_sale.split('售')[1]
                print('月售' + sale, '价格' + price)
                a += 1
                if DeviceNum == 'DLQ0216729004546'or DeviceNum == '5LM0216902001108' or DeviceNum == '5LM0216910000994' or DeviceNum == 'APU0216408028484' or DeviceNum == '5LM0216B03001264' or DeviceNum == 'QVM0215C03007968' or DeviceNum == 'DLQ0216630004610' or DeviceNum == 'E4J4C17405011422'or DeviceNum == 'APU0215C11003517' or DeviceNum == 'APU0216226004541':
                    sql = 'insert into drug_info (shop_name, Drugname, drug_price, drug_sale, sell_out, datetimes, flag)values (%s, %s, %s, %s, %s, %s, %s)'

                    cursor.execute(sql, (stName, Drugname, price, sale, sell_out, datetime_z, str(spider_num) + '-' + str(flag)))  # 将药品信息存到数据库

            else:
                pass
        except:
            pass
    return a


def not_exists(stName, Drugname, DeviceNum, flag, spider_num):  # 存储不存在的药品
    datetime_z = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取日期，时间
    price = sale = '无售卖'
    sell_out = ''
    if DeviceNum == 'DLQ0216729004546'or DeviceNum == '5LM0216902001108' or DeviceNum == '5LM0216910000994' or DeviceNum == 'APU0216408028484' or DeviceNum == '5LM0216B03001264' or DeviceNum == 'QVM0215C03007968' or DeviceNum == 'DLQ0216630004610' or DeviceNum == 'E4J4C17405011422'or DeviceNum == 'APU0215C11003517' or DeviceNum == 'APU0216226004541':
        sql = 'insert into drug_info (shop_name, Drugname, drug_price, drug_sale, sell_out, datetimes, flag)values (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (stName, Drugname, price, sale, sell_out, datetime_z, str(spider_num)+'-'+str(flag)))  # 将药品信息存到数据库
