import os
import configparser

def check_logging(log_path,key_world):
	count=0
	read_log=open(log_path,mode='r',encoding='UTF-8')
	conent=read_log.readlines()
	for index in range(len(conent)):
		if key_world in conent[index].strip():
			count=count+1	
	read_log.close()
	return(count)	

if __name__ == "__main__":
	config=configparser.ConfigParser()
	config_file=os.getcwd()+"\config.ini"
	config.read(config_file)
	check_folder_empty_log=config.get("config","check_folder_empty_log")
	log_path=config.get("config","log_path")
	result_path=config.get("config","result_path")
	temp_folder=config.get("config","temp_folder")
	
	temp_folder_length=len(os.listdir(temp_folder))
	check_folder_empty_result=check_logging(check_folder_empty_log,"TEMP folder is empty")
	copy_script_result=check_logging(log_path,"copy log OK")
	copy_command_result=check_logging(log_path,"1 file(s) copied.")
	copy_script_error_result=check_logging(log_path,"copy log has error")
	compress_result=check_logging(log_path,"Everything is Ok")
	filt_log_done=check_logging(log_path,"filt log was done.")
	compress_log_done=check_logging(log_path,"compress log was done.")
	
	print(temp_folder_length)
	print(copy_script_result)
	print(copy_command_result)
	print(copy_script_error_result)
	print(compress_result)
	print(filt_log_done)
	print(compress_log_done)
	print(check_folder_empty_result)
	
	if copy_script_result==copy_command_result and copy_script_error_result==0 and compress_result==temp_folder_length and filt_log_done+compress_log_done+check_folder_empty_result==3:
		with open(result_path,"w") as file:
			file.write("PASS")
	else:
		with open(result_path,"w") as file:
			file.write("FAIL")