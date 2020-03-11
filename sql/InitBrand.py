import sys
import uuid
import pymysql as pm

def UpdateBrand(DbContext):
    sql = '''
        select Name
        from brands 
        
    '''
    
    allBrand = DbContext.Query(sql)
    i = 0
    for brand in allBrand:
        brandName = brand['Name']
        sql = "update shop set Brand = '"+ brandName +"',UpdateTime = UpdateTime where shopName like '%" + brandName + "%' "
        DbContext.Update(sql)
        i += 1
        print(str(i) + brandName +'更新完毕')
    print('更新完毕!')

def UpdateO2OBrand():
    try:
        conn = pm.connect(host='10.1.0.202',
                        port=10042,
                        user='linwenqiang',
                        password='ZXJ8RuCgaRHQmUN277g0r0l3UW5fN5N3',
                        db='o2o',
                        cursorclass=pm.cursors.DictCursor,
                        charset='utf8')
        sql = '''
            select Name 
            from brands
        '''
        cursors = conn.cursor()
        cursors.execute(sql)
        allBrand = cursors.fetchall()
        i = 0
        for brand in allBrand:
            brandName = brand['Name']
            sqlstr = "update stores set Brand = '"+ brandName +"' where Name like '%" + brandName + "%' and Platform = 'mt'"
            try:            
                # 执行sql语句
                cursors = conn.cursor()
                cursors.execute(sqlstr)
                # 提交到数据库执行
                rows = conn.commit()                 
                i += 1
                print(str(i) + brandName +'更新完毕,更新门店[' + str(rows) + ']家')
            except Exception as e:
                # Rollback in case there is any error            
                print('更新出错：' + repr(e))
                conn.rollback()
        cursors.close()
        conn.close()  
    except Exception as e:
        print('数据库连接异常：' + repr(e))
    


def UpdatemtWmPoiId(DbContext):
    sql = '''
        select shopName,address
        from shop
        where mtWmPoiId is null
    '''
    allshop = DbContext.Query(sql)
    for shop in allshop:
        mtWmPoiId = uuid.uuid1()
        updatasql = '''
            update shop
            set mtWmPoiId = '%s'
            where shopName = '%s' and address = '%s'
        ''' % (str(mtWmPoiId).replace("-",""),shop['shopName'],shop['address'])
        DbContext.Update(updatasql)
        print(shop['shopName'] + '更新完')
