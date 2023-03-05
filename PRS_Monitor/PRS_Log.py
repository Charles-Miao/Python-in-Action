import os
import time
import re
import datetime
import csv
from multiprocessing import Pool

def get_newest_PRS_data(source_folder,source_folder_length,csv_path):
    line_folder=re.split(r'[\\]',source_folder.strip())[source_folder_length]
    prs_data=[]
    for station_folder in os.listdir(source_folder):
        for date_folder in os.listdir(source_folder+"\\"+station_folder):
            if date_folder==max(os.listdir(source_folder+"\\"+station_folder)):
                for files in os.listdir(source_folder+"\\"+station_folder+"\\"+date_folder):
                    li=os.listdir(source_folder+"\\"+station_folder+"\\"+date_folder)
                    if 'Thumbs.db' in li:
                        li.remove('Thumbs.db')
                        if files==max(li):
                            prs_data.append([line_folder,station_folder,date_folder,files])
                    else:
                        if files==max(li):
                            prs_data.append([line_folder,station_folder,date_folder,files])
    write_csv=open(csv_path,'a+',newline='')
    writer_csv=csv.writer(write_csv)
    writer_csv.writerows(prs_data)
    write_csv.close()
                        
def get_CPU_NumberOfCores():
	conent=os.popen("wmic cpu get NumberOfCores").readlines()
	CPU_NumberOfCores=0
	for index in range(len(conent)):
		if conent[index].strip()=="":
			continue
		elif conent[index].strip()=="NumberOfCores":
			continue
		else:
			CPU_NumberOfCores=CPU_NumberOfCores+int(conent[index].strip())
	return(str(CPU_NumberOfCores))        

if __name__ == "__main__":
    today=datetime.date.today()
    source_folder=r"\\192.168.123.47\prs"
    csv_path=r'D:\python_script\PRS_Monitor\prs.csv'

    source_folder_length=len(re.split(r'[\\]',source_folder))
    core=int(get_CPU_NumberOfCores())
    source_dirs=os.listdir(source_folder)
    
    headers=['line','station','newest_date_folder','newest_files_name']
    write_csv=open(csv_path,'w',newline='')
    writer_csv=csv.writer(write_csv)
    writer_csv.writerow(headers)
    write_csv.close()
    
    # get_newest_PRS_data(source_folder+"\\"+source_dirs[4],source_folder_length,csv_path)
    p = Pool(core*5)
    for i in range(len(source_dirs)):
        p.apply_async(get_newest_PRS_data, args=(source_folder+"\\"+source_dirs[i],source_folder_length,csv_path))
    p.close()
    p.join()
    print('All subprocesses done.')