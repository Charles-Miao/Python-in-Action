import sqlite3

ess=sqlite3.connect("ess.db")
#cursor=ess.execute("select * from ALL_ESS where PROPOSAL_DEPARTMENT='MEZ910'")
#for row in cursor:
#	print(row)

from datetime import date,datetime
#获取今天日期，并转换为年月格式
now=date.today()
nowmonth=now.strftime('%Y-%m')
#striptime：将Str转换为Date格式
cursor=ess.execute("select PROPOSAL_DATE from ALL_ESS")
for row in cursor:
	
	try:
		datetmp=datetime.strptime(row[0],'%Y-%m-%d')
	except:
		datetmp=datetime.strptime('1900-12-21','%Y-%m-%d')
	if datetmp.strftime('%Y-%m')==nowmonth:
		print(row[0])


	
