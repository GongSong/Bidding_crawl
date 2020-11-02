import pymysql
import json
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def get_token():
    conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
    cursor = conn.cursor()

    url = "https://ids.arkodata.cn/connect/token"
    payload = "grant_type=client_credentials&client_id=test&client_secret=b81dba38-b8cf-427d-99bd-b324caf569a4&scope=fileshare.full_access"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    token = json.loads(response.text)['access_token']
    print(token)
    sql = 'update mt_gettoken set Token=' +'"'+ token+'"'
    cursor.execute(sql)
    conn.commit()
    conn.close()

def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    get_token()

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', minute='*/45')   # 每隔45分种运行一次
scheduler.start()

