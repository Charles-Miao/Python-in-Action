#python3
import sqlite3
import xlrd
import xlwt
import os
from datetime import date,datetime
#All_ESS Table，用于存储所有提案
def createDataBase(cn):
	ess=sqlite3.connect(cn)
	ess.execute('''CREATE TABLE IF NOT EXISTS ALL_ESS 
	(PLANT TEXT,
	ESS_NUMBER TEXT PRIMARY KEY,
	IMPROVEMENT_SUBJECT TEXT,
	PROPOSAL_DATE NUMERIC,
	PROPOSAL_DEPARTMENT TEXT,
	PROPOSER TEXT,
	PROPOSER_NUMBER TEXT,
	APPROVED TEXT,
	STATUS TEXT,
	ACCEPTED_DAYS INTEGER,
	ACCEPTANCE_TIME NUMERIC,
	OFFICER_ACCEPTANCE_TIME NUMERIC,
	EXECUTOR_NUMBER TEXT,
	EXECUTOR TEXT,
	ASSIGN_PIC_PLANT TEXT,
	COMPLETION_DATE NUMERIC,
	EXECUTOR_DEPARTMENT TEXT,
	ESTIMATED_MANPOWER INTEGER,
	ESTIMATED_BENEFIT INTEGER,
	ACTUAL_MANPOWER INTEGER,
	ACTUAL_BENEFIT INTEGER,
	ESTIMATED_STARTDAY NUMERIC,
	ESTIMATED_DUEDAY NUMERIC,
	WHETHER_PAYMENT TEXT,
	MODIFIED_TIME NUMERIC,
	SEND_MAIL_TO_APPROVER TEXT,
	COMPLETE_DATE NUMERIC,
	IMPROVE_APPROVER_NAME TEXT,
	SITE_ID TEXT,
	PADEPT_ID TEXT,
	VAR_ASSIGN_PICDEPT_ID TEXT,
	VAR_PADEPT_MANAGER_ID TEXT,
	MODIFIER TEXT,
	FLOW_STEP_START_DATE NUMERIC,
	YEAR TEXT,
	SIGN_STEP TEXT,
	FOUNDER TEXT,
	ITEM_TYPE TEXT,
	PATH TEXT,
	DATE NUMERIC);''')

	
#PROPOSAL_DEPARTMENT Table，用于存储提案部门为特定部门的提案
def createProposalTable(cn):
	ess=sqlite3.connect(cn)
	ess.execute('''CREATE TABLE IF NOT EXISTS PROPOSAL_DEPARTMENT 
	(PLANT TEXT,
	ESS_NUMBER TEXT PRIMARY KEY,
	IMPROVEMENT_SUBJECT TEXT,
	PROPOSAL_DATE NUMERIC,
	PROPOSAL_DEPARTMENT TEXT,
	PROPOSER TEXT,
	PROPOSER_NUMBER TEXT,
	APPROVED TEXT,
	STATUS TEXT,
	ACCEPTED_DAYS INTEGER,
	ACCEPTANCE_TIME NUMERIC,
	OFFICER_ACCEPTANCE_TIME NUMERIC,
	EXECUTOR_NUMBER TEXT,
	EXECUTOR TEXT,
	ASSIGN_PIC_PLANT TEXT,
	COMPLETION_DATE NUMERIC,
	EXECUTOR_DEPARTMENT TEXT,
	ESTIMATED_MANPOWER INTEGER,
	ESTIMATED_BENEFIT INTEGER,
	ACTUAL_MANPOWER INTEGER,
	ACTUAL_BENEFIT INTEGER,
	ESTIMATED_STARTDAY NUMERIC,
	ESTIMATED_DUEDAY NUMERIC,
	WHETHER_PAYMENT TEXT,
	MODIFIED_TIME NUMERIC,
	SEND_MAIL_TO_APPROVER TEXT,
	COMPLETE_DATE NUMERIC,
	IMPROVE_APPROVER_NAME TEXT,
	SITE_ID TEXT,
	PADEPT_ID TEXT,
	VAR_ASSIGN_PICDEPT_ID TEXT,
	VAR_PADEPT_MANAGER_ID TEXT,
	MODIFIER TEXT,
	FLOW_STEP_START_DATE NUMERIC,
	YEAR TEXT,
	SIGN_STEP TEXT,
	FOUNDER TEXT,
	ITEM_TYPE TEXT,
	PATH TEXT,
	DATE NUMERIC);''')	
	
	
#EXECUTOR_DEPARTMENT Table，用于存储执行部门为特定部门的提案
def createExecutorTable(cn):
	ess=sqlite3.connect(cn)
	ess.execute('''CREATE TABLE IF NOT EXISTS EXECUTOR_DEPARTMENT 
	(PLANT TEXT,
	ESS_NUMBER TEXT PRIMARY KEY,
	IMPROVEMENT_SUBJECT TEXT,
	PROPOSAL_DATE NUMERIC,
	PROPOSAL_DEPARTMENT TEXT,
	PROPOSER TEXT,
	PROPOSER_NUMBER TEXT,
	APPROVED TEXT,
	STATUS TEXT,
	ACCEPTED_DAYS INTEGER,
	ACCEPTANCE_TIME NUMERIC,
	OFFICER_ACCEPTANCE_TIME NUMERIC,
	EXECUTOR_NUMBER TEXT,
	EXECUTOR TEXT,
	ASSIGN_PIC_PLANT TEXT,
	COMPLETION_DATE NUMERIC,
	EXECUTOR_DEPARTMENT TEXT,
	ESTIMATED_MANPOWER INTEGER,
	ESTIMATED_BENEFIT INTEGER,
	ACTUAL_MANPOWER INTEGER,
	ACTUAL_BENEFIT INTEGER,
	ESTIMATED_STARTDAY NUMERIC,
	ESTIMATED_DUEDAY NUMERIC,
	WHETHER_PAYMENT TEXT,
	MODIFIED_TIME NUMERIC,
	SEND_MAIL_TO_APPROVER TEXT,
	COMPLETE_DATE NUMERIC,
	IMPROVE_APPROVER_NAME TEXT,
	SITE_ID TEXT,
	PADEPT_ID TEXT,
	VAR_ASSIGN_PICDEPT_ID TEXT,
	VAR_PADEPT_MANAGER_ID TEXT,
	MODIFIER TEXT,
	FLOW_STEP_START_DATE NUMERIC,
	YEAR TEXT,
	SIGN_STEP TEXT,
	FOUNDER TEXT,
	ITEM_TYPE TEXT,
	PATH TEXT,
	DATE NUMERIC);''')	

	
	
def readExcel(filename,cn):
	ess=sqlite3.connect(cn)
	
	workbook = xlrd.open_workbook(filename)
	sheet_name = workbook.sheet_names()[0]
	sheet = workbook.sheet_by_name(sheet_name)


	for i in range(0,sheet.nrows):
		temp = []
		for j in range(0,sheet.ncols):
			if sheet.cell(i,j).value=='':
				temp.append(None)
			elif sheet.cell(i,j).ctype==3:
				date_value = xlrd.xldate_as_tuple(sheet.cell_value(i,j),workbook.datemode)
				date_tmp = date(*date_value[:3]).strftime('%Y-%m-%d')
				temp.append(date_tmp)
			else:
				temp.append(sheet.cell(i,j).value)
		
		#写进数据库
		ess.execute("insert into ALL_ESS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],
		temp[6],temp[7],temp[8],temp[9],temp[10],
		temp[11],temp[12],temp[13],temp[14],temp[15],
		temp[16],temp[17],temp[18],temp[19],temp[20],
		temp[21],temp[22],temp[23],temp[24],temp[25],
		temp[26],temp[27],temp[28],temp[29],temp[30],
		temp[31],temp[32],temp[33],temp[34],temp[35],
		temp[36],temp[37],temp[38],temp[39]))
	ess.commit()


if __name__=='__main__':
	#初始化
	filename="活頁簿1.xlsx"
	cn="ess.db"
	#删除DB
	if os.path.exists(cn):
		os.remove(cn)

	#创建DB ALL_ESS Table
	createDataBase(cn)
	#创建PROPOSAL_DEPARTMENT Table
	createProposalTable(cn)
	#创建EXECUTOR_DEPARTMENT Table
	createExecutorTable(cn)

	#读取所有数据，并导入ALL_ESS
	readExcel(filename,cn)

	#连接ess.db
	ess=sqlite3.connect("ess.db")	
	#将提案部门为MEZ900的提案，插入PROPOSAL_DEPARTMENT Table
	ess.execute("insert into PROPOSAL_DEPARTMENT select * from ALL_ESS where PROPOSAL_DEPARTMENT='MEZ900' or PROPOSAL_DEPARTMENT='MEZ910' or PROPOSAL_DEPARTMENT='MEZ920' or PROPOSAL_DEPARTMENT='MEZ930'")
	#将被提案部门为MEZ900的提案，插入EXECUTOR_DEPARTMENT Table
	ess.execute("insert into EXECUTOR_DEPARTMENT select * from ALL_ESS where EXECUTOR_DEPARTMENT='MEZ900' or EXECUTOR_DEPARTMENT='MEZ910' or EXECUTOR_DEPARTMENT='MEZ920'")

	ess.commit()
	