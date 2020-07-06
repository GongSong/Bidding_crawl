# -*- encoding=utf8 -*-
import sys
import configparser
import pymysql as pm
from Entity.EntityBase import EntityBase


class DbBase:
    _conn = pm.Connection  # 数据库连接对象
    # 初始化连接字符串

    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open('./DbHelper/Client.ini'))
        try:
            conn = pm.connect(host=config.get("db", "ip_addr"),
                              port=int(config.get("db", "port")),
                              user=config.get("db", "user"),
                              password=config.get("db", "password"),
                              db=config.get("db", "dbname"),
                              cursorclass=pm.cursors.DictCursor,
                              charset='utf8')
            self._conn = conn
        except Exception as e:
            print('数据库连接异常：' + repr(e))
        pass
    # 析构函数

    def __del__(self):
        try:
            self._conn.close()
        except Exception as e:
            print('释放数据库对象异常：' + repr(e))
        pass

    #===========================================数据库通用操作===========================================#
    # 执行指定的查询语句
    def Query(self, sql: str):
        result = []
        try:
            cursors = self._conn.cursor()
            cursors.execute(sql)
            result = cursors.fetchall()
        except Exception as e:
            print(repr(e))
        return result

    # 判断指定的记录是否存在
    def keyIsExist(self, keyName: str, KeyValue, tablename) -> bool:
        sql = """
        select count(1) as Keycount
        from %s
        where %s = %s
        """
        sql = sql % (tablename, keyName, KeyValue)
        cursors = self._conn.cursor()
        cursors.execute(sql)
        result = cursors.fetchall()
        if result[0]['Keycount'] > 0:
            return True
        else:
            return False
        pass

    # 执行指定的插入语句
    def Insert(self, sqlstr: str):
        # 执行sql语句
        cursors = self._conn.cursor()
        cursors.execute(sqlstr)
        # 提交到数据库执行
        return self._conn.commit()

 # 执行指定的删除语句
    def Delete(self, sqlstr: str):
        try:
            # 执行sql语句
            cursors = self._conn.cursor()
            cursors.execute(sqlstr)
            # 提交到数据库执行
            return self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print('执行sql语句出错：' + sqlstr+" "+repr(e))
    # 执行指定的更新语句

    def Update(self, sqlstr: str):
        try:
            # 执行sql语句
            cursors = self._conn.cursor()
            cursors.execute(sqlstr)
            # 提交到数据库执行
            return self._conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            print('更新出错：' + repr(e))
            self._conn.rollback()
        pass

    #===========================================基于面向对象的一些通用操作===========================================#
    # 根据实体有值的部分新增
    # 返回受影响行数
    def _InsertByEntity(self, entity: EntityBase) -> int:
        keyvalue = entity.__dict__
        field = ''
        values = ''
        tablename = type(entity).__name__
        for key, value in keyvalue.items():
            field += key + ','
            if type(value).__name__ == 'int':
                values += str(value) + ','
            elif type(value).__name__ == 'str':
                values += "'" + str(value) + "',"
            elif value == None:
                values += 'null,'
        if len(field) > 0:
            field = field[:-1]
        if len(values) > 0:
            values = values[:-1]
        sql = '''
            insert into %s (%s)
            values (%s)
        ''' % (tablename, field, values)
        return self.Insert(sql)

    # 根据ID字段更新实体有值部分
    def _UpdateByEntity(self, entity: EntityBase, condition: list) -> int:
        keyvalue = entity.__dict__
        tablename = type(entity).__name__
        whereCondition = ' where 1 = 1 '
        updateFiled = ''
        for key, value in keyvalue.items():
            if key in condition:
                if type(value).__name__ == 'int':
                    whereCondition += ' and ' + key + '=' + str(value)
                elif type(value).__name__ == 'str':
                    whereCondition += " and " + key + "='" + value + "'"
                elif value == None:
                    continue
            else:
                if type(value).__name__ == 'int':
                    updateFiled += key + '=' + str(value) + ','
                elif type(value).__name__ == 'str':
                    updateFiled += key + "='" + value + "',"
        if len(updateFiled) > 0:
            updateFiled = updateFiled[:-1]
        sql = '''
            update %s 
            set %s
            %s
        ''' % (tablename, updateFiled, whereCondition)
        print(sql)
        return 1
        # return self.Update(sql)
