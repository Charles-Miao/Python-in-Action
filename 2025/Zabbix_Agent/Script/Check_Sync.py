import os
import re
import time
import datetime
import configparser


def check_sync(path,string):
	check_sync_result=0
	read_log=open(path,mode='r',encoding='UTF-8')
	conent=read_log.readlines()
	for index in range(len(conent)):
		if string in conent[index]:
			check_sync_result=1
	read_log.close()
	return(check_sync_result)
	
def get_sync_date(path):
	info = os.stat(path)
	time_local=time.localtime(info.st_mtime)
	file_change_date=time.strftime("%Y-%m-%d",time_local)
	return(file_change_date)

def check_sync_result(path):
	config=configparser.ConfigParser()
	config.read(path)
	items=config.items("Sync_Path")
	
	sync=[]
	for index in range(len(items)):
		path_list=re.split(r'[,]',items[index][1])
		#skip empty path
		if str(items[index][1])=="":
			pass
		#if not exist sync result log, sync result is 0
		elif os.path.exists(path_list[0].strip())==False:
			sync.append(0)
		#if sync log is not today, sync result is 0
		elif str(get_sync_date(path_list[0].strip()))!=str(datetime.date.today()):
			sync.append(0)
		#if sync log not contains pass result, sync result is 0
		elif check_sync(path_list[0].strip(),path_list[1].strip())==0:
			sync.append(0)
		else:
			sync.append(1)
	return(sync)
	
if __name__ == '__main__':
	#check sync result
	ini_path=r"C:\Program Files\Zabbix Agent\Script\Check_Sync.ini"
	sync=check_sync_result(ini_path)
	sync_total=0
	for index in range(len(sync)):
		sync_total=sync_total+sync[index]
	if sync_total<len(sync):
		sync_result=0
	else:
		sync_result=1
	#print sync result
	print(sync_result)
	

	