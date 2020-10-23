import pandas as pd
import pymysql
from Send_Message import send_email, send_text, send_T1, send_T2, send_T3T4, send_T5T6, send_s30p200, send_self, \
    set_file, get_person
from openpyxl import Workbook
from openpyxl.styles import Font
import time
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()

'''
从数据库获取竞争药店状态码为0的店，
若状态码为0和为1的店的数量为零，就将店家的状态吗更新为0
'''
def get_shopName():
    global task
    task = []
    sql = 'select id, storename, store_addr, city from mt_com_drugstore where status_code=0'
    cursor.execute(sql)
    id_name_addr_city = cursor.fetchone()
    conn.commit()
    if len(id_name_addr_city) == 0:
        sql = 'select id, storename, store_addr, city from mt_com_drugstore where status_code=1'
        cursor.execute(sql)
        id_name_addr_city = cursor.fetchall()
        conn.commit()
        if len(id_name_addr_city) == 0:
            crawl_status_code()
        else:
            storename = id_name_addr_city[1]
            task.append(storename)
    else:
        return id_name_addr_city


# 获取最近一条执行了但是没有回写数据库的任务执行时间
def get_last_time():
    sql = 'select storename from mt_com_drugstore where status_code=1'
    cursor.execute(sql)
    storename = cursor.fetchone()
    conn.commit()
    if storename in task:
        sql = 'update mt_com_drugstore set status_code=0 where storename={}'.format('"'+storename+'"')
        cursor.execute(sql)
        conn.commit()
        task.remove(storename)
    else:
        pass


# 从数据库获取药品数据
def get_drug():
    sql = 'select id, drugname from mt_drugname'
    cursor.execute(sql)
    drugs = cursor.fetchall()
    conn.commit()
    return drugs


# 正在爬取的药店设为1
def crawling_status_code(storeName):
    sql = 'update mt_com_drugstore set status_code=1 where storename={}'.format('"'+storeName+'"')
    cursor.execute(sql)
    conn.commit()


# 爬取结束的药店设为2
def crawled_status_code(storeName):
    sql = 'update mt_com_drugstore set status_code=2 where storename={}'.format('"'+storeName+'"')
    cursor.execute(sql)
    conn.commit()


# 未爬取状态码设为0
def crawl_status_code():
    sql = 'update mt_com_drugstore set status_code=0'
    cursor.execute(sql)
    conn.commit()


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
        Drugname = drug[1]
        flag = drug[-1]
        # 查询店名相同的的商店药品数据
        sql = 'select * from mt_drug_info where Drugname={}'.format('"' + Drugname + '"')
        print(sql)
        cursor.execute(sql)
        pre_drug_list = cursor.fetchall()
        print(pre_drug_list)
        conn.commit()
        if len(pre_drug_list) != 0:
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
                            tips = '比昨天高' + str(abs(round(spread, 5))) + '元'
                            row = [index, month, date, pre_times, Drugname, shopname, pre_price, pre_sale, pre_sellout, times, price, sale, sellout, spread, tips]
                            sheet.append(row=row)
                        elif spread < 0:
                            a += 1
                            tips = '比昨天低' + str(abs(round(spread, 5))) + '元'
                            row = [index, month, date, pre_times, Drugname, shopname, pre_price, pre_sale, pre_sellout, times, price, sale, sellout, spread, tips]
                            sheet.append(row=row)
                        # else:
                        #     tips = '价格相等！'
                    content = '竟店价格变动：' + date + ' ' + times + ' ' + shopname
                    file = 'D:\\Bidding_crawl\\bidding_excel\\' + flag + '价格对比.xlsx'
                    wb.save(file)
                    print('表生成成功！')
                    if a != 0:
                        link_url = set_file(file)  # 获取链接
                        get_person(shopname, content, link_url)
                    break
        else:
            print(Drugname+'：上次的数据不存在！')
        break

