import os
import re
import csv

class filt_logs():
	def __init__(self,log_dir,log_csv):
		self.log_dir=log_dir
		self.log_csv=log_csv

	def remove_log_file(self):
		if os.path.exists(self.log_csv):
			os.remove(self.log_csv)

	def filt(self):
		log_data=[]
		for filename in os.listdir(self.log_dir):
			filename_split=re.split(r'[_.]',filename)
			SN=filename_split[0]
			test_time=filename_split[1]
			try:
				test_result=filename_split[2]
			except:
				test_result='None result'
			file_path=self.log_dir+'\%s' %filename
			read_log=open(file_path,mode='r',encoding='UTF-8')
			conent=read_log.readlines()
			for index in range(len(conent)):
				if "LINE=" in conent[index]:
					LINE=re.split(r'[=]',conent[index])[1].strip()
			for index in range(len(conent)):
				if "STAGE=" in conent[index]:
					STAGE=re.split(r'[=]',conent[index])[1].strip()
			start_day=re.split(r'[ ]',conent[0])[0].strip()
			start_time=re.split(r'[ ]',conent[0])[1].strip()
			end_day=re.split(r'[ ]',conent[len(conent)-1])[0].strip()
			end_time=re.split(r'[ ]',conent[len(conent)-1])[1].strip()
			start=start_day+' '+start_time
			end=end_day+' '+end_time
			read_log.close()
			log_data.append([SN,test_time,LINE,STAGE,test_result,start,end])

		headers=['SN','test_time','LINE','STAGE','test_result','start','end']
		write_csv=open(self.log_csv,'w',newline='')
		writer_csv=csv.writer(write_csv)
		writer_csv.writerow(headers)
		writer_csv.writerows(log_data)
		write_csv.close()

if __name__=="__main__":
	log_path=r'C:\Users\Charles\Desktop\log'
	csv_path=r'C:\Users\Charles\Desktop\csv'

	log_dirs=os.listdir(log_path)
	for i in range(len(log_dirs)):
		log_dir=log_path+"\\"+log_dirs[i]
		log_csv=csv_path+"\\"+log_dirs[i]+".csv"
		filt_log=filt_logs(log_dir,log_csv)
		filt_log.remove_log_file()
		filt_log.filt()