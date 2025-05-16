import os
import re
import csv

log_path=r'C:\Users\Administrator.Charles-PC\Desktop\Log\FCT'
log_csv=r'C:\Users\Administrator.Charles-PC\Desktop\log.csv'

if os.path.exists(log_csv):
	os.remove(log_csv)
log_data=[]
	
for filename in os.listdir(log_path):
	filename_split=re.split(r'[_.]',filename)
	test_time=filename_split[0][0:14]
	test_type=filename_split[2]
	test_plan=filename_split[3]
	if filename_split[4]=='log':
		sn="none sn"
	else:
		sn=filename_split[4]
	
	file_path=log_path+'\%s' %filename
	read_log=open(file_path,mode='r')
	conent=read_log.readlines()
	error_message="none"
	for index in range(len(conent)):
		if "INFO - Status" in conent[index]:
			test_result=re.split(r'[:]',conent[index])[3].strip()
		elif "INFO - Failure Message" in conent[index]:
			error_message=re.split(r'[,:]',conent[index])[4].strip()
		elif "INFO - Test Software" in conent[index]:
			test_software=re.split(r'[:]',conent[index])[3].strip()
	read_log.close()

	log_data.append([test_time,test_plan,test_type,test_software,sn,test_result,error_message])
	

	
headers=['test_time','test_plan','test_type','test_software','SN','test_result','error_message']
write_csv=open(log_csv,'w',newline='')
writer_csv=csv.writer(write_csv)
writer_csv.writerow(headers)
writer_csv.writerows(log_data)
write_csv.close()