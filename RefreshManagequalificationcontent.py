import sys
import pymysql as pm
import datetime

def UpdateCustomer(conn,QualificateID,reseltList):
	cursors = conn.cursor()
	sql = '''
		select m.CustomID,count(q.ID) as ContentCount
		from  qualificationcontent q
		LEFT JOIN managequalificationcontent m on m.QualificationContentID = q.ID
		where m.QualificationID = %d and  CustomID != 0 and CustomID is not null and q.IsShow = 1
		GROUP BY m.CustomID
	''' % (QualificateID)
	cursors.execute(sql)
	customQualificationID = cursors.fetchall()
	for custmer in customQualificationID:
		if custmer['ContentCount'] < len(reseltList):
			custom_id = custmer['CustomID']
			sql = '''
				select q.ID
				from  qualificationcontent q
				LEFT JOIN managequalificationcontent m on m.QualificationContentID = q.ID
				where m.QualificationID = %d and  CustomID = %d
			''' % (QualificateID,custom_id)
			cursors.execute(sql)
			HasQualification = cursors.fetchall()
			HasQualificationList = []
			for item in HasQualification:
				HasQualificationList.append(item['ID'])
			#找到差集
			instersaction = list(set(reseltList).difference(set(HasQualificationList)))
			print(instersaction)
			for QualificationContentID in instersaction:				
				try:
					sql = '''
						insert into managequalificationcontent(QualificationID,QualificationContentID,Content,CustomID,Crator,CrateTime)
						values (%d,%d,null,%d,'%s','%s')
					''' 
					currentime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					sql = sql % (QualificateID,int(QualificationContentID),custom_id,'c92277a7177d4915bda39f0e7f3c2851',currentime)				
					cursors.execute(sql)
					addrows = conn.commit()     
				except Exception as e:
					print(repr(e)) 
		print('客户['+ str(custmer['CustomID']) +']资质['+ str(QualificateID) +']内容刷新完毕！')
	pass

def UpdateStore(conn,QualificateID,reseltList):
	cursors = conn.cursor()
	sql = '''
		select m.StoreID,count(q.ID) as ContentCount
		from  qualificationcontent q
		LEFT JOIN managequalificationcontent m on m.QualificationContentID = q.ID
		where m.QualificationID = %d and  StoreID != 0 and StoreID is not null and q.IsShow = 1
		GROUP BY m.StoreID
	''' % (QualificateID)
	cursors.execute(sql)
	storeQualificationID = cursors.fetchall()
	for store in storeQualificationID:
		if store['ContentCount'] < len(reseltList):
			store_id = store['StoreID']
			sql = '''
				select q.ID
				from  qualificationcontent q
				LEFT JOIN managequalificationcontent m on m.QualificationContentID = q.ID
				where m.QualificationID = %d and  StoreID = %d
			''' % (QualificateID,store_id)
			cursors.execute(sql)
			HasQualification = cursors.fetchall()
			HasQualificationList = []
			for item in HasQualification:
				HasQualificationList.append(item['ID'])
			#找到差集
			instersaction = list(set(reseltList).difference(set(HasQualificationList)))
			for QualificationContentID in instersaction:
				sql = '''
					insert into managequalificationcontent(QualificationID,QualificationContentID,Content,StoreID,Crator,CrateTime)
					values (%d,%d,null,%d,'%s','%s')
				''' 
				currentime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				sql = sql % (QualificateID,int(QualificationContentID),store_id,'c92277a7177d4915bda39f0e7f3c2851',currentime)				
				cursors.execute(sql)
				addrows = conn.commit()      
		print('门店['+ str(store['StoreID']) +']资质['+ str(QualificateID) +']内容刷新完毕！')
	pass

def UpdateByQualificateID(conn,QualificateID):
	cursors = conn.cursor()
	sql = '''
		select Level
		from managequalification m
		where  m.Id = %d 
	''' % (int(QualificateID))
	cursors.execute(sql)
	resultLevel = cursors.fetchall()
	mode = resultLevel[0]['Level']
	sql = '''
		select ID
		from qualificationcontent q
		where q.QualificationID = %d and IsShow = 1
	''' % (int(QualificateID))
	
	cursors.execute(sql)
	result = cursors.fetchall()
	reseltList = []
	ShowId = '('
	for item in result:
		ShowId += str(item['ID']) + ','
		reseltList.append(item['ID'])
	if len(ShowId) > 1:
		ShowId = ShowId[:-1] + ')'		
	else:
		ShowId = ''
	#将已经不显示的内容删除
	if ShowId != '':
		sql = '''
			delete from managequalificationcontent
			where QualificationID = %d and QualificationContentID not in %s
		''' % (int(QualificateID),str(ShowId))	
		cursors.execute(sql)		
		deleterows = conn.commit()
		#将后来缺的补上
		#先刷客户
		if mode == 1:
			UpdateCustomer(conn,QualificateID,reseltList)	
		elif mode == 2:
			#刷新门店
			UpdateStore(conn,QualificateID,reseltList)
		pass

def main(QualificateID):
	try:
		conn = pm.connect(host='10.1.0.201',
						  port=3306,
						  user='sellcrmuser',
						  password='YiIE7vOLnfG2tpTq6EN8o7jIYQYAL9gZ',
						  db='sellcrmtest',
						  cursorclass=pm.cursors.DictCursor,
						  charset='utf8')
	except Exception as e:
		print('连接数据库异常' + repr(e))
	else:
		cursors = conn.cursor()
		#刷新指定资质
		if QualificateID != 0:
			UpdateByQualificateID(conn,QualificateID)
			pass
		else:
			sql = '''
				select Id
				from managequalification
				where IsActive = 1
			'''
			cursors.execute(sql)
			result = cursors.fetchall()			
			for QualificateID in result:
				pass
				UpdateByQualificateID(conn,QualificateID['Id'])
		pass


if __name__ == '__main__':
	main(0)
