import os
import re
import csv

class filt_logs():
	def __init__(self,source,destination,filt):
		self.source=source
		self.destination=destination
		self.filt=filt

	def move(self):
		
		for filename in os.listdir(self.filt):
			test_time=re.split(r'[_.]',filename.strip())[1]
			for filenames in os.listdir(self.source):
				if test_time==re.split(r'[_.]',filenames.strip())[0]:
					file_path=self.source+'\%s' %filenames
					try:
						os.system('move "%s" "%s"' % (file_path,self.destination))
					except Exception as e:
						print(f"while moving {file_path} to {self.destination}: {e}")
						return

if __name__=="__main__":
	source_folder=r'C:\Users\Administrator\Desktop\EDA\Temp_Log'
	filt_folder=r'C:\Users\Administrator\Desktop\FAIL'
	destination_folder=r'C:\Users\Administrator\Desktop\FAIL1'
	

	filt_log=filt_logs(source_folder,destination_folder,filt_folder)
	filt_log.move()