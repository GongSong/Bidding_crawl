import pandas as pd
import pymysql
from Send_Message import send_email, send_text, send_T1, send_T2, send_T3T4, send_T5T6, send_s30p200, send_self,set_file, get_person
from openpyxl import Workbook
from openpyxl.styles import Font
import time
import random
from datetime import datetime
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


'''
从数据库获取竞争药店状态码为0的店，
若状态码为0和为1的店的数量为零，就将店家的状态吗更新为0
若状态码为3则为停掉的设备重新爬取的店
'''
def get_shopName():
    time.sleep(random.randint(1, 10))
    sql = 'select id, storename, store_addr, city from mt_com_drugstore where status_code=0'
    cursor.execute(sql)
    id_name_addr_city = cursor.fetchone()
    conn.commit()
    if id_name_addr_city == None:
        time.sleep(random.randint(1, 10))
        sql = 'select id, storename, store_addr, city from mt_com_drugstore where status_code=1'
        cursor.execute(sql)
        status_code1 = cursor.fetchone()
        conn.commit()
        if status_code1 == None:
            # 状态全修改为0
            crawl_status_update()
            # 返回数据库第一个为0的店
            sql = 'select id, storename, store_addr, city from mt_com_drugstore where status_code=0'
            cursor.execute(sql)
            id_name_addr_city = cursor.fetchone()
            conn.commit()
            return id_name_addr_city, 0
        else:
            # time.sleep(random.randint(110, 250))
            return status_code1, 3
    else:
        return id_name_addr_city, 1


# 更新任务状态
def crawl_status_code(storeName, status_code):
    sql = 'update mt_com_drugstore set status_code={} where storename={}'.format(status_code, '"'+storeName+'"')
    cursor.execute(sql)
    conn.commit()


# 更新任务为0
def crawl_status_update():
    sql = 'update mt_com_drugstore set status_code=0'
    cursor.execute(sql)
    conn.commit()


# 从数据库获取药品数据
def get_drug():
    sql = 'select id, drugname from mt_drugname'
    cursor.execute(sql)
    drugs = cursor.fetchall()
    conn.commit()
    return drugs


# 将我店竟店数据写入excel
def write_excel(drug_list):
    # 创建excel
    font = Font(name='微软雅黑', size=9)
    wb = Workbook(write_only=True)
    sheet = wb.create_sheet('竞价')
    sheet.font = font
    row = ['序号', '月份', '抓取日期', '上次抓取时间', '商品名称', '竟店店铺名称', '上次价格', '上次月销', '售罄情况', '本次抓取时间', '本次价格', '本次月销','售罄情况', '价差', '警报']
    sheet.append(row=row)
    a = 0
    for index, drug in enumerate(drug_list):
        shop_name = drug[0]
        flag = drug[-1]
        # 查询店名是不是已存在
        sql = 'select * from mt_drug_info where shop_name={}'.format('"' + shop_name + '"')
        cursor.execute(sql)
        pre_drug_list = cursor.fetchall()
        conn.commit()
        if len(pre_drug_list) == 0:
            return 0
        else:
            for pre_drug in pre_drug_list:
                pre_flag = pre_drug[-1]
                if flag == pre_flag:
                    # 售罄情况
                    pre_sellout = pre_drug[4]
                    sellout = drug[4]
                    # 时间日期
                    pre_datetime = pre_drug[5]
                    pre_times = pre_datetime.split()[1]  # 上次时间
                    datetime_z = drug[5]
                    date = datetime_z.split()[0]  # 日期
                    month = date.split('-')[1]  # 月份
                    times = datetime_z.split()[1]  # 时间
                    # pre_drug中的信息
                    Drugname = pre_drug[1]
                    pre_price = (pre_drug[2])
                    pre_sale = pre_drug[3]
                    # drug中的信息
                    shopname = drug[0]
                    price = drug[2]
                    sale = drug[3]
                    # 价格信息处理
                    if price == '无售卖' or pre_price == '无售卖':
                        spread = tips = ''
                        remarks = ''
                    elif pre_price == '无售卖' and price == '无售卖':
                        spread = tips = ''
                        remarks = '无售卖'
                    else:
                        spread = float(price) - float(pre_price)  # 价差，这次比上次
                        if spread > 0:
                            a += 1
                            tips = '比上次高' + str(abs(round(spread, 5))) + '元'
                            row = [index, month, date, pre_times, Drugname, shopname, pre_price, pre_sale, pre_sellout, times, price, sale, sellout, spread, tips]
                            sheet.append(row=row)
                        elif spread < 0:
                            a += 1
                            tips = '比上次低' + str(abs(round(spread, 5))) + '元'
                            row = [index, month, date, pre_times, Drugname, shopname, pre_price, pre_sale, pre_sellout, times, price, sale, sellout, spread, tips]
                            sheet.append(row=row)
    time_stamp = str(round(time.time() * 1000))
    file = 'D:\\spider\\Bidding_crawl\\bidding_excel\\' + time_stamp + '-' + str(shop_name) + '价格对比.xlsx'
    wb.save(file)
    print('表生成成功！')
    if a != 0:
        data_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = '竟店价格变动：' +data_now+ str(shop_name)
        # 获取链接
        link_url = set_file(file)
        # 发送链接
        get_person(shop_name, content, link_url)
    return 1


