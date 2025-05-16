import os
import re
import csv
from multiprocessing import Pool

def filt_logs(file_path,destination_folder,search_content):
	search_result=0
	read_log=open(file_path,mode='r',encoding='UTF-8')
	conent=read_log.readlines()
	for index in range(len(conent)):
		if search_content in conent[index]:
			search_result=1
	read_log.close()
	if search_result==1:
		try:
			os.system('move "%s" "%s"' % (file_path,destination_folder))
		except Exception as e:
			print(f"while moving {file_path} to {destination_folder}: {e}")
			return

def get_CPU_NumberOfCores():
	conent=os.popen("wmic cpu get NumberOfCores").readlines()
	CPU_NumberOfCores=0
	for index in range(len(conent)):
		if conent[index].strip()=="":
			continue
		elif conent[index].strip()=="NumberOfCores":
			continue
		else:
			CPU_NumberOfCores=CPU_NumberOfCores+int(conent[index].strip())
	return(str(CPU_NumberOfCores))  

if __name__=="__main__":
	source_folder=r'C:\Users\Administrator\Desktop\EDA\XML_EDA_1'
	destination_folder=r'C:\Users\Administrator\Desktop\TEMP_1'
	search_content='&'
	
	core=int(get_CPU_NumberOfCores())
	source_dirs=os.listdir(source_folder)
	
	p = Pool(core*5)
	for i in range(len(source_dirs)):
		p.apply_async(filt_logs, args=(source_folder+"\\"+source_dirs[i],destination_folder,search_content))
	p.close()
	p.join()
	print('All subprocesses done.')