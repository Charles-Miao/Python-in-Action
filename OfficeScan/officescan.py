# -*- coding: utf-8 -*-
import xlrd
import xlwt

#打开Excel(所有联网电脑中命名为p5te的电脑信息)
p5te_workbook=xlrd.open_workbook(r'C:\Users\Administrator.Charles-PC\Desktop\OfficeScan\p5te_computer_logon_report.xls')
#获取p5te_computer_logon_report.xls的sheet1
p5te_sheet1=p5te_workbook.sheet_by_name(p5te_workbook.sheet_names()[0])
#获取p5te_computer_logon_report.xls中sheet1的行数
p5te_sheet1_rows=p5te_sheet1.nrows

#打开Excel(所有连接officescan服务器的电脑信息)
officescan_workbook=xlrd.open_workbook(r'C:\Users\Administrator.Charles-PC\Desktop\OfficeScan\officescan_client_listing.xls')
#获取p5te_computer_logon_report.xls的sheet1
officescan_sheet1=officescan_workbook.sheet_by_name(officescan_workbook.sheet_names()[0])
#获取p5te_computer_logon_report.xls中sheet1的行数
officescan_sheet1_rows=officescan_sheet1.nrows

#将p5te_computer_logon_report.xls中的第一行写入p5te_computer_no_officescan.xls
result_book=xlwt.Workbook(encoding='utf-8',style_compression=0)
result_sheet=result_book.add_sheet("p5te_computer_no_officescan",cell_overwrite_ok=True)
for i in range(0,len(p5te_sheet1.row_values(0))):
	result_sheet.write(0,i,p5te_sheet1.row_values(0)[i])

result_row=0

for i in range(1,p5te_sheet1_rows):
	flag=0 #此变量用于做标记
	for j in range(1,officescan_sheet1_rows):
		if p5te_sheet1.cell(i,5).value.encode('utf-8')==officescan_sheet1.cell(j,1).value.encode('utf-8'):
			flag=1 #p5te_workbook中的电脑若能在officescan_workbook中找到则标记为1			
	if flag==0:
		result_row=result_row+1
		for k in range(0,len(p5te_sheet1.row_values(0))):
			result_sheet.write(result_row,k,p5te_sheet1.row_values(i)[k])
#		print(p5te_sheet1.cell(i,5).value.encode('utf-8'))
#		print(p5te_sheet1.row_values(i))
		
result_book.save('p5te_computer_no_officescan.xls')	