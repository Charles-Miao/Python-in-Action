#python3
import os
import sqlite3
import xlwt
import xlrd
from xlutils.copy import copy
from datetime import date,datetime
#创建EXCEL
def createExcel(filename):
	book=xlwt.Workbook(encoding='utf-8',style_compression=0)
	sheet=book.add_sheet("sheet1",cell_overwrite_ok=True)
	book.save(filename)	


#将筛选数据库的结果，塞入进EXCEL（插入表头）
def insertExcel(cursor,excel):
	row_number=0
	for row in cursor:
		#print(row)
		rb=xlrd.open_workbook(excel)  
		wb=copy(rb)  
		ws=wb.get_sheet(0)  
		for i in range(40):
			ws.write(row_number,i,row[i]) 
		wb.save(excel)
		row_number=row_number+1
	
	
if __name__=='__main__':
	#初始化
	cn="ess.db"
	ess=sqlite3.connect("ess.db")	
	
	excel1="01本月提案.xls"
	excel2="02本月省人提案.xls"
	excel3="03正在进行中提案.xls"
	excel4="04结案嘉奖提案.xls"
	excel5="05提案嘉奖提案.xls"
	
	if os.path.exists(excel1):
		os.remove(excel1)
		
	if os.path.exists(excel2):
		os.remove(excel2)
	
	if os.path.exists(excel3):
		os.remove(excel3)
	
	if os.path.exists(excel4):
		os.remove(excel4)
	
	if os.path.exists(excel5):
		os.remove(excel5)
	
	#创建5个EXCEL
	createExcel(excel1)
	createExcel(excel2)
	createExcel(excel3)
	createExcel(excel4)
	createExcel(excel5)
	
	
	#获取今天日期，并转换为（年-月）格式
	now=date.today()
	nowmonth=now.strftime('%Y-%m')
	'''
	功能0：插入表头
	'''
	cursor=ess.execute("select * from ALL_ESS where PLANT='廠別'")
	insertExcel(cursor,excel1)
	cursor=ess.execute("select * from ALL_ESS where PLANT='廠別'")
	insertExcel(cursor,excel2)
	cursor=ess.execute("select * from ALL_ESS where PLANT='廠別'")
	insertExcel(cursor,excel3)
	cursor=ess.execute("select * from ALL_ESS where PLANT='廠別'")
	insertExcel(cursor,excel4)
	cursor=ess.execute("select * from ALL_ESS where PLANT='廠別'")
	insertExcel(cursor,excel5)
	
	'''
	功能1：本月提案，并被厂长Approve
	'''
	#datetemp=datetime.strptime('2017-03-21','%Y-%m-%d')
	#lastmonth=datetemp.strftime('%Y-%m')
	#striptime：将Str转换为Date格式
	cursor=ess.execute("select * from PROPOSAL_DEPARTMENT where STATUS='Close' or STATUS='Implement'")
	#row[3]：提案日期
	row_number=1
	for row in cursor:
		#print(row)
		try:
			datetmp=datetime.strptime(row[3],'%Y-%m-%d')
		except:
			datetmp=datetime.strptime('1900-12-21','%Y-%m-%d')
		if datetmp.strftime('%Y-%m')==nowmonth:
			rb=xlrd.open_workbook(excel1)  
			wb=copy(rb)  
			ws=wb.get_sheet(0)  
			for i in range(40):
				ws.write(row_number,i,row[i]) 
			wb.save(excel1)
		row_number=row_number+1
	
	
	'''
	功能2：本月有节省人力的提案
	'''
	#datetemp=datetime.strptime('2017-03-21','%Y-%m-%d')
	#lastmonth=datetemp.strftime('%Y-%m')
	cursor=ess.execute("select * from EXECUTOR_DEPARTMENT where STATUS='Close' and ACTUAL_MANPOWER IS NOT NULL and ACTUAL_MANPOWER!=0")
	#row[15]:完成日期
	row_number=1
	for row in cursor:
		#print(row)
		try:
			datetmp=datetime.strptime(row[15],'%Y-%m-%d')
		except:
			datetmp=datetime.strptime('1900-12-21','%Y-%m-%d')
		if datetmp.strftime('%Y-%m')==nowmonth:
			rb=xlrd.open_workbook(excel2)  
			wb=copy(rb)  
			ws=wb.get_sheet(0)  
			for i in range(40):
				ws.write(row_number,i,row[i]) 
			wb.save(excel2)
		row_number=row_number+1
	
	
	'''
	功能3：正在进行中的提案
	'''
	#ASC，升序
	#DESC，降序
	cursor=ess.execute("select * from EXECUTOR_DEPARTMENT where STATUS='Issue' or STATUS='Implement' order by STATUS DESC, ESTIMATED_DUEDAY ASC")
	row_number=1
	for row in cursor:
		#print(row)
		rb=xlrd.open_workbook(excel3)  
		wb=copy(rb)  
		ws=wb.get_sheet(0)  
		for i in range(40):
			ws.write(row_number,i,row[i]) 
		wb.save(excel3)
		row_number=row_number+1
	
	
	'''
	功能4：结案嘉奖提案
	'''
	cursor=ess.execute("select * from EXECUTOR_DEPARTMENT where STATUS='Close' and ACTUAL_BENEFIT>=2000 order by COMPLETION_DATE DESC")
	row_number=1
	for row in cursor:
		#print(row)
		rb=xlrd.open_workbook(excel4)  
		wb=copy(rb)  
		ws=wb.get_sheet(0)  
		for i in range(40):
			ws.write(row_number,i,row[i]) 
		wb.save(excel4)
		row_number=row_number+1
	
	'''
	功能5：提案嘉奖提案
	'''
	cursor=ess.execute("select * from PROPOSAL_DEPARTMENT where STATUS='Close' or STATUS='Implement' order by PROPOSAL_DATE DESC")
	row_number=1
	for row in cursor:
		#print(row)
		rb=xlrd.open_workbook(excel5)  
		wb=copy(rb)  
		ws=wb.get_sheet(0)  
		for i in range(40):
			ws.write(row_number,i,row[i]) 
		wb.save(excel5)
		row_number=row_number+1