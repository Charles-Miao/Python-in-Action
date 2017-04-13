import sqlite3
from datetime import date,datetime

if __name__=='__main__':
	#初始化
	cn="ess.db"
	ess=sqlite3.connect("ess.db")	
	
	#获取今天日期，并转换为（年-月）格式
	now=date.today()
	nowmonth=now.strftime('%Y-%m')
	
	'''
	功能1：本月提案，并被厂长Approve
	'''
	#datetemp=datetime.strptime('2017-03-21','%Y-%m-%d')
	#lastmonth=datetemp.strftime('%Y-%m')
	#striptime：将Str转换为Date格式
	cursor=ess.execute("select * from PROPOSAL_DEPARTMENT where STATUS='Close' or STATUS='Implement'")
	#row[3]：提案日期
	for row in cursor:
		#print(row)
		try:
			datetmp=datetime.strptime(row[3],'%Y-%m-%d')
		except:
			datetmp=datetime.strptime('1900-12-21','%Y-%m-%d')
		if datetmp.strftime('%Y-%m')==nowmonth:
			print(row)
	
	
	'''
	功能2：本月有节省人力的提案
	'''
	#datetemp=datetime.strptime('2017-03-21','%Y-%m-%d')
	#lastmonth=datetemp.strftime('%Y-%m')
	cursor=ess.execute("select * from EXECUTOR_DEPARTMENT where STATUS='Close' and ACTUAL_MANPOWER IS NOT NULL and ACTUAL_MANPOWER!=0.0")
	#row[15]:完成日期
	for row in cursor:
		#print(row)
		try:
			datetmp=datetime.strptime(row[15],'%Y-%m-%d')
		except:
			datetmp=datetime.strptime('1900-12-21','%Y-%m-%d')
		if datetmp.strftime('%Y-%m')==nowmonth:
			print(row)
	
	
	'''
	功能3：正在进行中的提案
	'''
	#ASC，升序
	#DESC，降序
	cursor=ess.execute("select * from EXECUTOR_DEPARTMENT where STATUS='Issue' or STATUS='Implement' order by STATUS DESC, ESTIMATED_DUEDAY ASC")
	#for row in cursor:
	#	print(row)
		
	
	'''
	功能4：结案嘉奖提案
	'''
	cursor=ess.execute("select * from EXECUTOR_DEPARTMENT where STATUS='Close' and ACTUAL_BENEFIT>=2000 order by COMPLETION_DATE DESC")
	#for row in cursor:
	#	print(row)
	
	
	'''
	功能5：提案嘉奖提案
	'''
	cursor=ess.execute("select * from PROPOSAL_DEPARTMENT where STATUS='Close' or STATUS='Implement' order by PROPOSAL_DATE DESC")
	#for row in cursor:
	#	print(row)
	