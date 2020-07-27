import os
import time
import re
from multiprocessing import Pool

from log_filt import get_CPU_NumberOfCores
from log_filt import filt
from log_compress import compress

if __name__ == "__main__":
    source_folder=r"W:\TEST_LOG"
    target_folder=r"Y:\TEMP"
    z_target_folder=r"C:\Users\Charles\Desktop\TE_Test_Data"
    sz=r"C:\Users\Charles\Desktop\7z1900-extra\7za.exe"
        
    core=int(get_CPU_NumberOfCores())
    #filt log
    source_dirs=os.listdir(source_folder)
    p = Pool(core)
    for i in range(len(source_dirs)):
        p.apply_async(filt, args=(source_folder+"\\"+source_dirs[i],target_folder,))
    p.close()
    p.join()
    print('filt log was done.')
    #compress log
    folder_list=os.listdir(target_folder)
    p = Pool(core)
    for folder in folder_list:
        target=os.path.join(z_target_folder, folder+'.7z')
        source=os.path.join(target_folder, folder+'\\*') 
        p.apply_async(compress, args=(sz,target,source,))
    p.close()
    p.join()
    print('compress log was done.')