# ------------------------------
# Written by: Charles Miao
# Company: Wistron Corporation
# Date: 2024-10-25
# version:Python3.9
# ------------------------------
import os
from multiprocessing import Pool
from datetime import date, timedelta
import configparser

from empty_temp import empty_folder
from log_filt import get_CPU_NumberOfCores
from log_filt import filt
from py_test_modify_V03 import process_log_file

if __name__ == "__main__":
    config=configparser.ConfigParser()
    config_file=os.getcwd()+"\config.ini"
    config.read(config_file)
    source_folder=config.get("config","source_folder")
    temp_folder=config.get("config","temp_folder")
    target_folder=config.get("config","target_folder")
    
    yesterday=str(date.today()-timedelta(1))    
    core=int(get_CPU_NumberOfCores())
    
    #empty temp folder
    try:
        empty_folder(temp_folder)
    finally:
        if not os.listdir(temp_folder):
            print("temp folder is empty")
        else:
            print("temp folder is not empty")
	
    #filt log
    source_dirs=os.listdir(source_folder)
    p = Pool(core)
    for i in range(len(source_dirs)):
        if source_dirs[i]=="Zone" or source_dirs[i]=="NPE_Zone":
            source_folder_dirs=os.listdir(source_folder+"\\"+source_dirs[i])
            for j in range(len(source_folder_dirs)):
                p.apply_async(filt, args=(source_folder+"\\"+source_dirs[i]+"\\"+source_folder_dirs[j],temp_folder,"all"))
    p.close()
    p.join()
    print('filt log was done.')

    #log to xml
    file_list=os.listdir(temp_folder)
    p = Pool(core)
    for file in file_list:
        p.apply_async(process_log_file, args=(temp_folder+"\\"+file,target_folder))
    p.close()
    p.join()
    print('log to xml was done.')