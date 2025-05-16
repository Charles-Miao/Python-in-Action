import os
import re
import csv

class filt_logs():
	def __init__(self,source,destination):
		self.source=source
		self.destination=destination

	def move(self):
		for filename in os.listdir(self.source):
			file_path=self.source+'\%s' %filename
			SN = re.split(r'[._]', filename.strip())[0]
			SN_pattern = r'^(P.{20}|N.{13})$'
			
			if re.match(SN_pattern, SN):
				# print(SN)
				try:
					os.system('move "%s" "%s"' % (file_path,self.destination))
				except Exception as e:
					print(f"while moving {file_path} to {self.destination}: {e}")
					return

if __name__=="__main__":
	source_folder=r'C:\Users\Administrator\Desktop\XML_Log'
	destination_folder=r'C:\Users\Administrator\Desktop\Temp'
	
	filt_log=filt_logs(source_folder,destination_folder)
	filt_log.move()