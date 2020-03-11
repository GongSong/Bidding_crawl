# -*- encoding=utf8 -*-
import sys
import pika
import configparser

class BaseRabbitMQ:
    __host = ''
    __virtualhost = ''
    __port = 15672
    __user = ''
    __pwd = ''
    _conn = ''
    connStr = 'Rabbitserver'
    def __init__(self):
        config = configparser.RawConfigParser()
        config.readfp(open('./RabbitMQ/RabbitMQ.ini'))
        self.__host = config.get(self.connStr,"host")
        self.__virtualhost = config.get(self.connStr,"virtualhost")
        self.__port = config.get(self.connStr,"port")
        self.__user = config.get(self.connStr,"user")
        self.__pwd = config.get(self.connStr,"pwd")        
        try:                        
            creds_broker = pika.PlainCredentials(self.__user,self.__pwd)
            parameters = pika.ConnectionParameters(host = self.__host,port=self.__port,virtual_host=self.__virtualhost,credentials=creds_broker)
            self._conn = pika.BlockingConnection(parameters)            
        except Exception as e:
            print('队列服务连接异常：'+repr(e).replace("'","").replace("\"",""))

     #析构函数
    def __del__(self):        
        try:            
            self._conn.close()
        except Exception as e:
            print('************************释放队列对象异常************************')
            print(repr(e).replace("'","").replace("\"",""))
        pass
    #返回连接
    def _getConn(self):
        return self._conn