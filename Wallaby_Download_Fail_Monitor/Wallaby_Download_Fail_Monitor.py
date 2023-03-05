import os
import time
import re
import datetime
import csv
import shutil

from multiprocessing import Pool

from uni_UI_test_log import filt_logs
from empty_folder import empty_folder

if __name__ == "__main__":
    #generate UI csv file 
    today=datetime.date.today()
    yesterday=today - datetime.timedelta(days=1)
    two_days_ago=today - datetime.timedelta(days=2)

    today_v_source_folder=r"\\192.168.123.48\Test_Log\WALLABY_V"+'\\'+str(today).replace("-", "_")+'\\TV\\UI_Log'
    today_a_source_folder=r"\\192.168.123.48\Test_Log\WALLABY_A"+'\\'+str(today).replace("-", "_")+'\\TV\\UI_Log'
    yesterday_v_source_folder=r"\\192.168.123.48\Test_Log\WALLABY_V"+'\\'+str(yesterday).replace("-", "_")+'\\TV\\UI_Log'
    yesterday_a_source_folder=r"\\192.168.123.48\Test_Log\WALLABY_A"+'\\'+str(yesterday).replace("-", "_")+'\\TV\\UI_Log'
    two_days_ago_v_source_folder=r"\\192.168.123.48\Test_Log\WALLABY_V"+'\\'+str(two_days_ago).replace("-", "_")+'\\TV\\UI_Log'
    two_days_ago_a_source_folder=r"\\192.168.123.48\Test_Log\WALLABY_A"+'\\'+str(two_days_ago).replace("-", "_")+'\\TV\\UI_Log'
    

    today_target_folder=r"D:\python_script\Wallaby_Download_Fail_Monitor\UI_Log"+'\\'+str(today).replace("-", "_")
    yesterday_target_folder=r"D:\python_script\Wallaby_Download_Fail_Monitor\UI_Log"+'\\'+str(yesterday).replace("-", "_")
    two_days_ago_target_folder=r"D:\python_script\Wallaby_Download_Fail_Monitor\UI_Log"+'\\'+str(two_days_ago).replace("-", "_")

    log_path=r'D:\python_script\Wallaby_Download_Fail_Monitor\UI_Log'
    csv_path=r'D:\python_script\Wallaby_Download_Fail_Monitor\csv'

    empty_folder(log_path)
    empty_folder(csv_path)

    os.makedirs(today_target_folder)
    os.makedirs(yesterday_target_folder)
    os.makedirs(two_days_ago_target_folder)

    if os.path.exists(today_v_source_folder):
        os.system("copy "+today_v_source_folder+" "+today_target_folder)
    if os.path.exists(today_a_source_folder):
        os.system("copy "+today_a_source_folder+" "+today_target_folder)
    if os.path.exists(yesterday_v_source_folder):
        os.system("copy "+yesterday_v_source_folder+" "+yesterday_target_folder)
    if os.path.exists(yesterday_a_source_folder):
        os.system("copy "+yesterday_a_source_folder+" "+yesterday_target_folder)
    if os.path.exists(two_days_ago_v_source_folder):
        os.system("copy "+two_days_ago_v_source_folder+" "+two_days_ago_target_folder)
    if os.path.exists(two_days_ago_a_source_folder):
        os.system("copy "+two_days_ago_a_source_folder+" "+two_days_ago_target_folder)

    log_path=r'D:\python_script\Wallaby_Download_Fail_Monitor\UI_Log'
    csv_path=r'D:\python_script\Wallaby_Download_Fail_Monitor\csv'

    log_dirs=os.listdir(log_path)
    for i in range(len(log_dirs)):
    	log_dir=log_path+"\\"+log_dirs[i]
    	log_csv=csv_path+"\\"+log_dirs[i]+".csv"
    	filt_log=filt_logs(log_dir,log_csv)
    	filt_log.remove_log_file()
    	filt_log.filt()