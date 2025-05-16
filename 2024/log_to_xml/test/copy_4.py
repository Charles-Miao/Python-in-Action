import os
import re
import csv
from multiprocessing import Pool
from lxml import etree
import shutil

def filt_logs(file_path,destination_folder):
	tree = etree.parse(file_path)
	root = tree.getroot()
	empty_elements = []

	for elem in root.iter():
		if elem.tag in ['ErrorCode', 'LogErrorMessage', 'ErrorTestName', 'ErrorFullTestName', 'ErrorDetails']:
			if elem.text is None or elem.text.strip() == '':
				empty_elements.append(elem.tag)

			
	if len(empty_elements)==5:
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
	source_folder=r'C:\Users\Administrator\Desktop\PASS'
	destination_folder=r'C:\Users\Administrator\Desktop\PASS1'
	
	core=int(get_CPU_NumberOfCores())
	source_dirs=os.listdir(source_folder)
	
	p = Pool(core*5)
	for i in range(len(source_dirs)):
		p.apply_async(filt_logs, args=(source_folder+"\\"+source_dirs[i],destination_folder))
	p.close()
	p.join()
	print('All subprocesses done.')