import pandas as pd
import pymysql
from Send_Message import send_email, send_text, send_T1, send_T2, send_T3T4, send_T5T6, send_s30p200, send_self, \
    set_file
from openpyxl import Workbook
from openpyxl.styles import Font
import time


conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


# 从excel获取两方药店的名称, 地址
def get_shopName():
    xl = pd.read_excel(r"D:\工作文件\mt\191家目标店&竞品店铺信息清单 20200908.xlsx", sheet_name='赋能')
    we_shop = list(xl.iloc[0:191, 5])  # 我店
    other_shop = list(xl.iloc[0:191, 12])  # 竞店
    we_address = list(xl.iloc[0:191, 7])
    other_address = list(xl.iloc[0:191, 13])
    we_storeCity = list(xl.iloc[0:191, 10])
    other_storeCity = list(xl.iloc[0:191, 15])
    return we_shop, other_shop, we_address, other_address, we_storeCity, other_storeCity


# 从excel获取药品数据
def get_drug():
    df = pd.read_excel(r'D:\工作文件\mt\30个竞价商品清单（直营&赋能）.xlsx')
    drug_name = list(df.iloc[0:31, 1])  # 切片操作获取药品名
    drug_code = list(df.iloc[0:31, 3])
    drug_Allname = list(df.iloc[0:31, 4])
    return drug_name


# 将我店竟店数据写入excel
def write_excel(flag):
    spider_num = int(flag.split('-')[0])
    drug_index = flag.split('-')[1]
    pre_flag = str(spider_num - 1) + '-' + drug_index
    # 连接数据库获取竟方店铺信息
    other_storeCity = get_shopName()[5]
    other_city = other_storeCity[int(drug_index)]
    sql = 'select * from drug_info where flag={}'.format('"'+flag+'"')
    cursor.execute(sql)
    others = cursor.fetchall()   # 30个药品， 查询标记为flag的商店药品数据
    conn.commit()
    sql1 = 'select * from drug_info where flag={}'.format('"'+pre_flag+'"')
    cursor.execute(sql1)
    pre_others = cursor.fetchall()
    conn.commit()
    print(len(others), len(pre_others), flag, pre_flag)
    if len(others) == 30 and len(pre_others) == 30:  # 一方下标为flag的数据不存在就不做比较
        # 创建excel
        font = Font(name='微软雅黑', size=9)
        wb = Workbook(write_only=True)
        sheet = wb.create_sheet(flag)
        sheet.font = font
        row = ['序号', '爬取次数', '月份', '抓取日期', '上次抓取时间', '商品名称', '竟店店铺名称', '上次价格', '上次月销', '售罄情况', '本次抓取时间', '本次价格', '本次月销',
               '售罄情况', '价差', '警报']
        sheet.append(row=row)
        a = 0
        for i in range(30):
            # 售罄情况
            pre_sellout = pre_others[i][4]
            other_sellout = others[i][4]
            # 时间日期
            pre_datetime = pre_others[i][5]
            pre_times = pre_datetime.split()[1]  # 上次时间
            datetime_z = others[i][5]
            date = datetime_z.split()[0]  # 日期
            month = date.split('-')[1]  # 月份
            times = datetime_z.split()[1]  # 时间
            # 价格
            pre_shopname = (pre_others[i])[0]
            Drugname = pre_others[i][1]
            pre_price = (pre_others[i][2])
            pre_sale = pre_others[i][3]
            # # 竟店信息
            other_shopname = others[i][0]
            other_price = others[i][2]
            other_sale = others[i][3]
            # 价格信息处理
            if other_price == '无售卖' or pre_price == '无售卖':
                spread = tips = ''
                remarks = ''
            elif pre_price == '无售卖' and other_price == '无售卖':
                spread = tips = ''
                remarks = '无售卖'
            else:
                spread = float(other_price) - float(pre_price)  # 价差，这次比上次
                if spread > 0:
                    a += 1
                    tips = '比昨天高' + str(abs(round(spread, 5))) + '元'
                    row = [i, spider_num, month, date, pre_times, Drugname, other_shopname, pre_price, pre_sale, pre_sellout, times, other_price, other_sale, other_sellout, spread, tips]
                    sheet.append(row=row)
                elif spread < 0:
                    a += 1
                    tips = '比昨天低' + str(abs(round(spread, 5))) + '元'
                    row = [i, spider_num, month, date, pre_times, Drugname, other_shopname, pre_price, pre_sale, pre_sellout, times, other_price, other_sale, other_sellout, spread, tips]
                    sheet.append(row=row)
                else:
                    tips = '价格相等！'
        print('表生成成功！')
        file = 'D:\\工作文件\\价格比较\\' + date + '-' + str(drug_index) + '价格对比.xlsx'
        wb.save(file)
        link_url = set_file(file)  # 获取链接
        content = '竟店价格变动：' + date + ' ' + times + ' ' + other_shopname
        if a != 0:
            get_person(other_shopname, content, link_url)
    else:
        print('有一方数据不全无法比较！')


# 获取人员信息，发送消息到各人员的群中
def get_person(other_shopname, content, link_url):
    xl = pd.read_excel(r"D:\工作文件\mt\store list 202009071624.xlsx")
    shop_names = list(xl.iloc[0:191, 5])  # 店名
    head_person = list(xl.iloc[0:191, 11])  # 负责人
    a = 0
    for index, shop_name in enumerate(shop_names):
        if shop_name == other_shopname:
            a += 1
            person = head_person[index]
            if person == '杨晓明&丁俊':
                send_T1(other_shopname, content, link_url)
                print('发送成功！1')
            elif person == '范文超':
                send_T2(other_shopname, content, link_url)
                print('发送成功！2')
            elif person == '笑寒':
                send_T3T4(other_shopname, content, link_url)
                print('发送成功！3')
            elif person == '郭燕':
                send_T5T6(other_shopname, content, link_url)
                print('发送成功！4')
            elif person == '朱沙沙&谢威盛':
                send_s30p200(other_shopname, content, link_url)
                print('发送成功！5')
            elif person == '蔡培桂，赵嘉雄，谭群红，范文超':
                send_self(other_shopname, content, link_url)
                print('发送成功！6')
            else:
                print('没有找到这个人, 发送失败！')
    if a == 0:
        content1 = '监控到：'+other_shopname+'在storeList表中没有找到对应的店名'
        print(content1)


# write_excel('19-185')
