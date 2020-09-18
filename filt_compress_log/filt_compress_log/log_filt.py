import os
import time
import re
from multiprocessing import Pool

def filt(source_folder,target_folder,source_folder_length,date="all"):
    for files in os.walk(source_folder):
        with os.scandir(files[0]) as entries:
            for entry in entries:
                if os.path.isfile(entry):
                    # 获取文件修改日期
                    info = entry.stat()
                    time_local=time.localtime(info.st_mtime)
                    file_change_date=time.strftime("%Y-%m-%d",time_local)
                    #若为默认值则处理所有日期的文件
                    if date=="all":
                        # 在目标目录中创建修改日期目录
                        if not os.path.exists(target_folder+"\\"+file_change_date):
                            os.mkdir(target_folder+"\\"+file_change_date)  
                        # 获取源文件绝对路径
                        source_file=os.path.dirname(entry)+"\\"+os.path.split(entry)[-1]
                        # 获取目标路径，并创建目录
                        source_split=re.split(r'[\\]',source_file.strip())
                        model_name=source_split[source_folder_length]
                        target_file=target_folder+"\\"+file_change_date+"\\"+model_name+source_file[len(source_folder):]
                        if not os.path.exists(target_file[:-len(os.path.split(entry)[-1])-1]):
                            os.makedirs(target_file[:-len(os.path.split(entry)[-1])-1])
                        # 拷贝
                        os.system("copy %s %s /y" % (source_file,target_file))
                    #若指定日期，则拷贝指定日期的文件
                    elif file_change_date==date:
                        # 在目标目录中创建修改日期目录
                        if not os.path.exists(target_folder+"\\"+file_change_date):
                            os.mkdir(target_folder+"\\"+file_change_date)  
                        # 获取源文件绝对路径
                        source_file=os.path.dirname(entry)+"\\"+os.path.split(entry)[-1]
                        # 获取目标路径，并创建目录
                        source_split=re.split(r'[\\]',source_file.strip())
                        model_name=source_split[source_folder_length]
                        target_file=target_folder+"\\"+file_change_date+"\\"+model_name+source_file[len(source_folder):]
                        if not os.path.exists(target_file[:-len(os.path.split(entry)[-1])-1]):
                            os.makedirs(target_file[:-len(os.path.split(entry)[-1])-1])
                        print(model_name)
                        print(source_file)
                        print(target_file)
                        # 拷贝
                        try:
                            os.system("copy %s %s /y" % (source_file,target_file))
                        except:
                            print("copy log has error")
                        else:
                            print("copy log OK")
                        
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
    source_folder=r"\\192.168.123.49\Temp\Charles\Test_Log"
    target_folder=r"D:\TEMP_TEST"
    date="2020-08-01"
	
    source_folder_length=len(re.split(r'[\\]',source_folder))
    core=int(get_CPU_NumberOfCores())
    source_dirs=os.listdir(source_folder)

    p = Pool(core*5)
    for i in range(len(source_dirs)):
        p.apply_async(filt, args=(source_folder+"\\"+source_dirs[i],target_folder,source_folder_length,date))
    p.close()
    p.join()
    print('All subprocesses done.')