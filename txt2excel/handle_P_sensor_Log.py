#coding=utf-8
#将P-sensor Log整理成EXCEL格式

import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import os
#初始化
log_path="D:\Wistron\PSensor" #设定待处理的Log目录
xls_path="D:\Wistron\PSensor.xls" #设定生成EXCEL路径
sheet_name="sheet1"


#创建EXCEL
def create_excel(sheetname,filename):
	book=xlwt.Workbook(encoding='utf-8',style_compression=0)
	sheet=book.add_sheet(sheetname,cell_overwrite_ok=True)
	book.save(filename)
#写入EXCEL
def write_xls(row,col,data,filename):  
    rb=open_workbook(filename)  
    wb=copy(rb)  
    ws=wb.get_sheet(0)  
    ws.write(row,col,data) 
    wb.save(filename)

if os.path.exists(xls_path):
	pass
else:
	create_excel(sheet_name,xls_path)

	
#列出所有Log文件名
file_list=os.listdir(log_path)
#文件个数
#file_number=len(file_list)
col_number=1 #记录写入的列数

write_xls(1,0,"15cm",xls_path)
write_xls(2,0,"5cm",xls_path)
write_xls(3,0,"4cm",xls_path)
write_xls(4,0,"3cm",xls_path)
write_xls(5,0,"2cm",xls_path)
write_xls(6,0,"1cm",xls_path)
write_xls(7,0,"0cm",xls_path)


for list in file_list:
	
	file=open(log_path+"\\"+list,encoding='UTF-8')
	lines=file.readlines()
	s={} #设定一个空字典
	for line in lines:
		if "15cm" in line:
			s[15]=line.split()[3]
		elif "5cm" in line:
			s[5]=line.split()[3]
		elif "4cm" in line:
			s[4]=line.split()[3]
		elif "3cm" in line:
			s[3]=line.split()[3]
		elif "2cm" in line:
			s[2]=line.split()[3]
		elif "1cm" in line:
			s[1]=line.split()[3]
		elif "0cm" in line:
			s[0]=line.split()[3]
	#print(s[15])
	#写入EXCEL
	write_xls(0,col_number,list.split('_')[0],xls_path)
	try:
		write_xls(1,col_number,s[15],xls_path)
	except Exception as KeyError:
		pass
	
	try:
		write_xls(2,col_number,s[5],xls_path)
	except Exception as KeyError:
		pass
	
	try:
		write_xls(3,col_number,s[4],xls_path)
	except Exception as KeyError:
		pass
	
	try:
		write_xls(4,col_number,s[3],xls_path)
	except Exception as KeyError:
		pass
	
	try:
		write_xls(5,col_number,s[2],xls_path)
	except Exception as KeyError:
		pass
	
	try:
		write_xls(6,col_number,s[1],xls_path)
	except Exception as KeyError:
		pass
	
	try:
		write_xls(7,col_number,s[0],xls_path)
	except Exception as KeyError:
		pass
	
	file.close()
	col_number=col_number+1

#print(file_list)
#create_excel("sheet1","d:\p_sensor.xls")
#write_xls(0,1,"fuck","d:\p_sensor.xls")
#write_xls(1,1,"fuck","d:\p_sensor.xls")
