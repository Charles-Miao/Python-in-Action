import os
import re
import time
import datetime

def TimeStampToTime(timestamp):
	timeStruct=time.localtime(timestamp)
	return(time.strftime('%Y-%m-%d %H:%M:%S',timeStruct))

def get_FileModifyTime(filePath):
	#filePath=unicode(filePath,'utf8')
	t=os.path.getmtime(filePath)
	return(TimeStampToTime(t))

if __name__ == "__main__":
	source_folder=r"\\192.168.123.48\AIS_Log"
	result_path=r'D:\python_script\AIS_Backup_Result\AIS_Backup_Result.txt'
	
	with open(result_path, 'w') as fw:
		for filename in os.listdir(source_folder):
			filepath = os.path.join(source_folder, filename)
			if os.path.isfile(filepath):
				with open(filepath,'r') as f:
					fw.write(f.read().splitlines()[0]+",	"+get_FileModifyTime(filepath)+",	"+filename+"\n")