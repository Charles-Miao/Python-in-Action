import xlrd
import xlwt
from datetime import date,datetime

def read_excel():
	#打开文件
	workbook=xlrd.open_workbook(r'活頁簿1.xlsx')
	#获取所有sheet
	sheet_name=workbook.sheet_names()[0]
	sheet = workbook.sheet_by_name(sheet_name)

	#获取一行的内容
	for i in range(0,sheet.nrows):
		for j in range(0,sheet.ncols):
			try:
				print(sheet.cell(i,j).value.encode('utf-8'))
			except (AttributeError):
				pass
			
if __name__=='__main__':
	read_excel()