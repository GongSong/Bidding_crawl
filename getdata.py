import pandas as pd
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


def read_data():
    xl = pd.read_excel(r"D:\项目\工作文件\191家目标店&竞品店铺信息清单 20200908.xlsx", sheet_name='赋能')
    shop = list(xl.iloc[0:191, 12])  # 竞店
    address = list(xl.iloc[0:191, 13])
    province = list(xl.iloc[0:191, 14])
    City = list(xl.iloc[0:191, 15])
    area = list(xl.iloc[0:191, 16])
    print(address)

read_data()