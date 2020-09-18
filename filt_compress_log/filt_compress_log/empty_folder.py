import shutil
import os
import configparser
import time

def empty_folder(folder):
	try:
		shutil.rmtree(folder)
	finally:
		time.sleep(2.1)
		os.mkdir(folder)

if __name__ == '__main__':
	config=configparser.ConfigParser()
	config_file=os.getcwd()+"\config.ini"
	config.read(config_file)
	temp_folder=config.get("config","temp_folder")
	check_folder_empty_log=config.get("config","check_folder_empty_log")
	
	
	try:
		empty_folder(temp_folder)
	finally:
		if not os.listdir(temp_folder):
			with open(check_folder_empty_log,"w") as file:
				file.write("TEMP folder is empty")
		else:
			with open(check_folder_empty_log,"w") as file:
				file.write("TEMP folder is not empty")