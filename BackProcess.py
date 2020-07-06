from RabbitMQ.Consumer import ReceiveMessage
from DbHelper.DbHelper import DbHelper
import datetime
import os

def main():
    os.popen('python3.7 DaemonTask.py  &>> /root/airtest/log/TaskRunniglog'+ datetime.datetime.now().strftime("%Y%m%d") +'.log')
    while True:
        try:
            consumer = ReceiveMessage()
            consumer.receiveMessage()
            pass
        except Exception as e:
            print('接收消息异常：' + repr(e))
            try:
                DbContext = DbHelper()
                DbContext.AddLog('',4,'接收消息异常：' + repr(e).replace("'","").replace("\"","").replace("\\",""))
                del DbContext
            except Exception as e:
                continue
            continue            
    pass

if __name__ == '__main__':
    main()
    pass