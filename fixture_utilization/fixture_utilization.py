import os
import re
import csv

log_path=r'D:\Fixture_Log\0312'
log_csv=r'D:\Fixture_Log\0312.csv'

if os.path.exists(log_csv):
	os.remove(log_csv)
log_data=[]
	
for filename in os.listdir(log_path):
	file_path=log_path+'\%s' %filename
	read_log=open(file_path,mode='r')
	conent=read_log.readlines()
	try:
		conent_split=re.split(r'[,]',conent[0])
	except IndexError:
		print(filename)
	if len(conent_split[3].strip())==10 or len(conent_split[3].strip())==17:
		line=conent_split[0].strip()
		station=conent_split[1].strip()
		time=conent_split[2].strip()
		sn=conent_split[3].strip()
		log_data.append([line,station,time,sn])
	else:
		pass
	read_log.close()
	
headers=['line','station','time','sn']
write_csv=open(log_csv,'w',newline='')
writer_csv=csv.writer(write_csv)
writer_csv.writerow(headers)
writer_csv.writerows(log_data)
write_csv.close()