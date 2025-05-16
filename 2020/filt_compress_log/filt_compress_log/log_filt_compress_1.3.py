import os
import time
import re
from multiprocessing import Pool
from datetime import date, timedelta
import configparser

from log_filt_1 import get_CPU_NumberOfCores
from log_filt_1 import filt
from log_compress import compress

if __name__ == "__main__":
    config=configparser.ConfigParser()
    config_file=os.getcwd()+"\config.ini"
    config.read(config_file)
	
    source_folder=config.get("config","source_folder")
    temp_folder=config.get("config","temp_folder")
    z_target_folder=config.get("config","z_target_folder")
    sz=config.get("config","sz")
    source_folder_length=len(re.split(r'[\\]',source_folder))
    da=[]
    da.append(str(date.today()-timedelta(7)))
    da.append(str(date.today()-timedelta(8)))
    da.append(str(date.today()-timedelta(9)))
    da.append(str(date.today()-timedelta(10)))
    da.append(str(date.today()-timedelta(11)))
    da.append(str(date.today()-timedelta(12)))
    da.append(str(date.today()-timedelta(13)))

    core=int(get_CPU_NumberOfCores())
    #filt log
    source_dirs=os.listdir(source_folder)
    p = Pool(core)
    for i in range(len(source_dirs)):
        p.apply_async(filt, args=(source_folder+"\\"+source_dirs[i],temp_folder,source_folder_length,da))
    p.close()
    p.join()
    print('filt log was done.')
    #compress log
    folder_list=os.listdir(temp_folder)
    p = Pool(core)
    for folder in folder_list:
        target=os.path.join(z_target_folder, folder+'.7z')
        source=os.path.join(temp_folder, folder+'\\*') 
        p.apply_async(compress, args=(sz,target,source,))
    p.close()
    p.join()
    print('compress log was done.')