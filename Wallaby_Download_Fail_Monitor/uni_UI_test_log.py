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
			file_path=self.log_dir+'\%s' %filename
			read_log=open(file_path,mode='r',encoding='UTF-8')
			conent=read_log.readlines()
			for index in range(len(conent)):
				if "PAT_TRACK" in conent[index]:
					SN=re.split(r'[,]',conent[index])[1].strip()
					test_time=re.split(r'[,]',conent[index])[2].strip()
					fixture_id=re.split(r'[,]',conent[index])[6].strip()
					model_name=re.split(r'[,]',conent[index])[8].strip()
					test_item=re.split(r'[,]',conent[index])[9].strip()
					test_result=re.split(r'[,]',conent[index])[11].strip()
					total_time=re.split(r'[,]',conent[index])[12].strip()
			read_log.close()
			log_data.append([SN,test_time,fixture_id,model_name,test_item,test_result,total_time])

		headers=['SN','test_time','fixture_id','model_name','test_item','test_result','total_time']
		write_csv=open(self.log_csv,'w',newline='')
		writer_csv=csv.writer(write_csv)
		writer_csv.writerow(headers)
		writer_csv.writerows(log_data)
		write_csv.close()

if __name__=="__main__":
	log_path=r'C:\Users\long\Desktop\UI_Log'
	csv_path=r'C:\Users\long\Desktop\csv'

	log_dirs=os.listdir(log_path)
	for i in range(len(log_dirs)):
		log_dir=log_path+"\\"+log_dirs[i]
		log_csv=csv_path+"\\"+log_dirs[i]+".csv"
		filt_log=filt_logs(log_dir,log_csv)
		filt_log.remove_log_file()
		filt_log.filt()