import requests
import json
import time
import random
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()

# 发送报警到钉钉群
def send_text(content):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=7be487f2f56efd147d41807b854d517f22402f51db2309ca8cfa064dcde5c3e8'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg ={
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    text_textMsg = json.dumps(text_textMsg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


def send_T1(other_shopname, content, link_url):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=546acb9eedd44334c1ee0a6aca73e753a31ec5957c69df291ea4739c7f0f829c'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    link_Msg = {
        "msgtype": "link",
        "link": {
            "text": content,
            "title": other_shopname,
            "picUrl": "",
            "messageUrl": link_url
        }
    }
    text_textMsg = json.dumps(link_Msg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


def send_T2(other_shopname, content, link_url):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=1620bf9887e40c7f4fcd95b7f9ab8fb3e95bd5cc0d2ebe5275e358f48c7a8a0d'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    link_Msg = {
        "msgtype": "link",
        "link": {
            "text": content,
            "title": other_shopname,
            "picUrl": "",
            "messageUrl": link_url
        }
    }
    text_textMsg = json.dumps(link_Msg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


def send_T3T4(other_shopname, content, link_url):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=710d2bebf5243b70a430ac952ea67f1fdf5b34167c22c704a3a122ce6f15fd8b'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    link_Msg = {
        "msgtype": "link",
        "link": {
            "text": content,
            "title": other_shopname,
            "picUrl": "",
            "messageUrl": link_url
        }
    }
    text_textMsg = json.dumps(link_Msg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


def send_T5T6(other_shopname, content, link_url):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=08a53ebcf9cbbeab7e2c0f0821db934d034afc99b2e9c3d63b7d21fdef1e6534'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    link_Msg = {
        "msgtype": "link",
        "link": {
            "text": content,
            "title": other_shopname,
            "picUrl": "",
            "messageUrl": link_url
        }
    }
    text_textMsg = json.dumps(link_Msg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


def send_s30p200(other_shopname, content, link_url):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=33306b09e0ee1ce921f26b8bcfcdc54aec3abb5512c0d16c74a5447f85624e2c'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    link_Msg = {
        "msgtype": "link",
        "link": {
            "text": content,
            "title": other_shopname,
            "picUrl": "",
            "messageUrl": link_url
        }
    }
    text_textMsg = json.dumps(link_Msg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


# 发送给自营
def send_self(other_shopname, content, link_url):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=45c641b2299d3b6ae521b8f23f922a1c1358ef765e7e52c79b7a2c86b67f0b08'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    text_textMsg = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {"atMobiles": [], "isAtAll": False}
    }
    link_Msg = {
        "msgtype": "link",
        "link": {
            "text": content,
            "title": other_shopname,
            "picUrl": "",
            "messageUrl": link_url
        }
    }
    text_textMsg = json.dumps(link_Msg)
    requests.post(url, data=text_textMsg, headers=HEADERS)


# 发送邮件提示
def send_email(date, flag,  we_shopname, other_shopname):
    import yagmail
    user = 'dandelionlee@foxmail.com'  # 帐号设置的是默认发信帐号
    password = 'cppnjzaopnksbhij'  # 授权码
    yag = yagmail.SMTP(user=user, password=password, host='smtp.qq.com', encoding='gbk')  # 创建SMTP连接
    body = date+'，'+we_shopname+'和'+other_shopname+'的价差比较表'
    to = ['luoyinglee@gmail.com', 'jiaxiong.zhao@qyt1902.com']
    cc = ['xiaoming.yang@qyt1902.com']
    yag.send(to=to, cc=cc, subject='美团竞价', contents=body, attachments='F:\工作文件\价差比较\\' + date + '-' + str(flag)+'价格对比.xlsx')  # 发送信息
    print('邮件发送成功！')


# 上传excel文件
def upload(filename):
    sql = 'select Token from mt_gettoken'
    cursor.execute(sql)
    token = cursor.fetchone()[0]
    conn.commit()
    url = "http://fileshare.arkodata.cn/upload"
    headers = {
        'authorization': "Bearer "+token
    }
    file_name = filename.split('\\')[-1]
    files = {'file': (file_name, open(filename, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    try:
        response = requests.post(url, files=files, headers=headers).text
        print(response)
        key = json.loads(response)['data']['key']
        return key
    except:
        pass


# 设置文件存储时长
def set_file(filename):
    key = upload(filename)
    sql = 'select Token from mt_gettoken'
    cursor.execute(sql)
    token = cursor.fetchone()[0]
    url = "http://fileshare.arkodata.cn/set"

    payload = {'key': key, 'days': '10', 'type': '1'}
    payload = json.dumps(payload)
    headers = {
        'authorization': "Bearer "+token,
        'content-type': "application/json",
    }
    try:
        response = requests.post(url, data=payload, headers=headers).text
        link_url = json.loads(response)['data']['url']
        print(link_url)
        return link_url
    except:
        pass
# set_file('D:\\spider\\Bidding_crawl\\bidding_excel\\1604555724588-张仲景大药房洛阳王城大道店.xlsx')
#

# 获取人员信息，发送消息到各人员的群中
def get_person(other_shopname, content, link_url):
    sql = 'select storename, director from mt_director'
    cursor.execute(sql)
    stores = cursor.fetchall()
    a = 0
    for store in stores:
        shop_name = store[0]
        if shop_name == other_shopname:
            a += 1
            person = store[1]
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

set_file('D:\\spider\\Bidding_crawl\\bidding_excel\\1604639467621-海王星辰广州新港西店.xlsx')


