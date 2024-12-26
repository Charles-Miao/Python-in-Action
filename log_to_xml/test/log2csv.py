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
			test_date="'"+filename_split[1]
			# test_time="time:"+filename_split[2]
			file_path=self.log_dir+'\%s' %filename
			read_log=open(file_path,mode='r',encoding='UTF-8')
			conent=read_log.readlines()
			for index in range(len(conent)):
				if "StationId" in conent[index]:
					StationId=re.split(r'[<>]',conent[index])[2].strip()
				if "<Result>" in conent[index]:
					Result=re.split(r'[<>]',conent[index])[2].strip()
				if "ModelName" in conent[index]:
					ModelName=re.split(r'[<>]',conent[index])[2].strip()
				if "StationType" in conent[index]:
					StationType=re.split(r'[<>]',conent[index])[2].strip()
				
			read_log.close()
			log_data.append([SN,ModelName,StationType,test_date,Result,StationId])

		headers=['SN','ModelName','StationType','test_date','Result','StationId']
		write_csv=open(self.log_csv,'w',newline='')
		writer_csv=csv.writer(write_csv)
		writer_csv.writerow(headers)
		writer_csv.writerows(log_data)
		write_csv.close()

if __name__=="__main__":
	log_path=r'C:\Users\Administrator\Desktop\EDA\XML_EDA'
	csv_path=r'C:\Users\Administrator\Desktop\EDA\test\XML_EDA.csv'

	filt_log=filt_logs(log_path,csv_path)
	filt_log.remove_log_file()
	filt_log.filt()