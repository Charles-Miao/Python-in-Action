import xlrd
import xlwt

def readExcel(filename,cn):
	#读取
	workbook = xlrd.open_workbook(filename)
	#获取sheet
	sheet_name = workbook.sheet_names()[0]
	sheet = workbook.sheet_by_name(sheet_name)

	for i in range(0,sheet.nrows):
		temp = []
		for j in range(0,sheet.ncols):
			try:
				temp.append(sheet.cell(i,j).value.encode('utf-8'))
			except (AttributeError):
				temp.append(None)
			cn.execute("insert into ALL_ESS (PLANT,ESS_NUMBER,IMPROVEMENT_SUBJECT,PROPOSAL_DATE,PROPOSAL_DEPARTMENT,\
			PROPOSER,PROPOSER_NUMBER,APPROVED,STATUS,ACCEPTED_DAYS,\
			ACCEPTANCE_TIME,OFFICER_ACCEPTANCE_TIME,EXECUTOR_NUMBER,EXECUTOR,ASSIGN_PIC_PLANT,\
			COMPLETION_DATA,EXECUTOR_DEPARTMENT,ESTIMATED_MANPOWER,ESTIMATED_BENEFIT,ACTUAL_MANPOWER,\
			ACTUAL_BENEFIT,ESTIMATED_STARTDAY,ESTIMATED_DUEDAY,WHETHER_PAYMENT,MODIFIED_TIME,\
			SEND_MAIL_TO_APPROVER,COMPLETE_DATE,IMPROVE_APPROVER_NAME,SITE_ID,PADEPT_ID,\
			VAR_ASSIGN_PICDEPT_ID,VAR_PADEPT_MANAGER_ID,MODIFIER,FLOW_STEP_START_DATE,YEAR,\
			SIGN_STEP,FOUNDER,ITEM_TYPE,PATH,DATA) \
			values (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[9],temp[10],temp[11],temp[12],temp[13],temp[14],temp[15],temp[16],temp[17],temp[18],temp[19],temp[20],temp[21],temp[22],temp[23],temp[24],temp[25],temp[26],temp[27],temp[28],temp[29],temp[30],temp[31],temp[32],temp[33],temp[34],temp[35],temp[36],temp[37],temp[38],temp[39])")
	
	cn.commit()