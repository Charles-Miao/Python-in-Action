import os
import time
import re
import zipfile
from multiprocessing import Pool

def compress(sz,target,source):
    os.system("%s a -t7z %s %s -r -mx=5 -m0=LZMA2 -ms=10m -mf=on -mhc=on -mmt=on" % (sz,target,source))

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
    target_folder=r"D:\TEMP"
    z_target_folder=r"D:\Test_Log"
    sz=r"D:\ServerCheck\filt_compress_log\7z1900-extra\7za.exe"

    core=int(get_CPU_NumberOfCores())
    folder_list=os.listdir(target_folder)

    p = Pool(core)
    for folder in folder_list:
        target=os.path.join(z_target_folder, folder+'.7z')
        source=os.path.join(target_folder, folder+'\\*') 
        p.apply_async(compress, args=(sz,target,source,))
    p.close()
    p.join()
    print('All subprocesses done.')