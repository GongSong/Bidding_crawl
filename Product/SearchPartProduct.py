import time
from datetime import datetime
from Product.GetsData import get_drug, write_excel
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


def get_goods(poco, device, stName, shopid):
    global drug_list
    drug_list = []
    drugname_list = get_drug()  # 获取药品名称
    for Drugname in drugname_list:
        drugid = Drugname[0]
        GetPartProduct(poco, device, Drugname[1], stName, shopid, drugid)
    poco('android.widget.ImageView').click()  # 返回药店详情页
    isExists = write_excel(drug_list)
    if isExists == 0:
        for drug in drug_list:
            sql = 'insert into mt_drug_info (shop_name, Drugname, drug_price, drug_sale, sell_out, datetimes, flag)values (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (drug[0], drug[1], drug[2], drug[3], drug[4], drug[5], str(drug[6])))  # 将药品信息存到数据库
        conn.commit()
    else:
        for drug in drug_list:
            flag = drug[-1]
            sql = 'update mt_drug_info set shop_name={}, Drugname={}, drug_price={}, drug_sale={}, sell_out={}, datetimes={} where flag={}'.format('"'+drug[0]+'"',  '"'+drug[1]+'"',  '"'+drug[2]+'"',  '"'+drug[3]+'"',  '"'+drug[4]+'"',  '"'+drug[5]+'"', '"'+flag+'"')
            cursor.execute(sql)
            conn.commit()


# 查询部分药品的数据
def GetPartProduct(poco, device, Drugname, stName, shopid, drugid):
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
        a = is_exists(items, Drugname, stName, shopid, drugid)
        if a == 0:
            poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").click()
            poco('android.widget.EditText').click()
            device.text(text=Drugname)  # 输入要查询的药名
            time.sleep(1)
            items = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup")
            if items:
                a = is_exists(items, Drugname, stName, shopid, drugid)
                if a == 0:
                    print('提示：这家店' + Drugname + '药品不存在！')
                    not_exists(stName, Drugname, shopid, drugid)
            else:
                print('提示：这家店' + Drugname + '药品不存在！')
                not_exists(stName, Drugname, shopid, drugid)
    else:  # 第二次查找药品
        poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").wait().click()
        poco('android.widget.EditText').click()
        device.text(text=Drugname)  # 输入要查询的药名
        items = poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("android.widget.ScrollView").child("android.view.ViewGroup")
        if items:
            a = is_exists(items, Drugname, stName, shopid, drugid)
            if a == 0:
                print('提示：这家店' + Drugname + '药品不存在！')
                not_exists(stName, Drugname, shopid, drugid)
        else:
            if Drugname == Drugname == '[可丽蓝]早早孕测试笔(验孕棒)1支' or '[毓婷]左炔诺孕酮片0.75mg*2片' or Drugname == '[金毓婷]左炔诺孕酮片1.5mg*1片' or Drugname=='[金戈]枸橼酸西地那非片50mg*1片*1板'or Drugname=='[芬必得]布洛芬缓释胶囊0.3g*10粒*2板' or Drugname=='[丹媚]左炔诺孕酮肠溶片1.5mg*1片'or Drugname=='[杜蕾斯]天然胶乳橡胶避孕套(超薄装)隐feel52mm*3只'or Drugname=='[江中]健胃消食片(成人)0.8g*8片*4板'or Drugname=='[云南白药]蒲地蓝消炎片0.3g*48片'or Drugname=='[康恩贝]肠炎宁片0.42g*12片*2板' or Drugname=='[白云山]板蓝根颗粒10g*20袋':
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
                        a = is_exists(items, Drugname, stName, shopid, drugid)
                        if a != 0:
                            b += 1
                            break
                if b == 0:
                    print('提示：这家店' + Drugname + '药品不存在！')
                    not_exists(stName, Drugname, shopid, drugid)
            else:
                print('提示：这家店' + Drugname + '药品不存在！')
                not_exists(stName, Drugname, shopid, drugid)
    # 点击清除药名
    poco("android:id/content").offspring("com.sankuai.meituan.takeoutnew:id/fl_mrn_container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup")[0].child("android.view.ViewGroup")[1].child("android.widget.ImageView").click()


# 存储存在的药品
def is_exists(items, Drugname, stName, shopid, drugid):
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
                else:
                    sell_out = '已售罄'
                sale = month_sale.split('售')[1]
                print('月售' + sale, '价格' + price)
                a += 1
                global Exists
                Exists = [stName, Drugname, price, sale, sell_out, datetime_z, str(shopid)+'-'+str(drugid)]
                drug_list.append(Exists)
        except:
            pass
    return a


# 存储不存在的药品
def not_exists(stName, Drugname, shopid, drugid):
    datetime_z = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取日期，时间
    price = sale = '无售卖'
    sell_out = ''
    global NotExists
    NotExists = [stName, Drugname, price, sale, sell_out, datetime_z, str(shopid)+'-'+str(drugid)]
    drug_list.append(NotExists)

