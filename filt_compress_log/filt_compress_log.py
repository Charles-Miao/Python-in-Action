import os
import time
import zipfile

class filt_compress:
    def __init__(self,source_folder,target_folder,sz,date="all"):
        self.source_folder=source_folder
        self.target_folder=target_folder
        self.sz=sz
        self.date=date
    
    def filt(self):
        for files in os.walk(self.source_folder):
            with os.scandir(files[0]) as entries:
                for entry in entries:
                    if os.path.isfile(entry):
                        # 获取文件修改日期
                        info = entry.stat()
                        time_local=time.localtime(info.st_mtime)
                        file_change_date=time.strftime("%Y-%m-%d",time_local)
                        #若为默认值则处理所有日期的文件
                        if self.date=="all":
                            # 在目标目录中创建修改日期目录
                            if not os.path.exists(self.target_folder+"\\"+file_change_date):
                                os.mkdir(self.target_folder+"\\"+file_change_date)  
                            # 获取源文件绝对路径
                            source_file=os.path.dirname(entry)+"\\"+os.path.split(entry)[-1]
                            # 获取目标路径，并创建目录
                            target_file=self.target_folder+"\\"+file_change_date+source_file[len(self.source_folder):]
                            if not os.path.exists(target_file[:-len(os.path.split(entry)[-1])-1]):
                                os.makedirs(target_file[:-len(os.path.split(entry)[-1])-1])
                            # 拷贝
                            os.system("copy %s %s /y" % (source_file,target_file))
                        #若指定日期，则拷贝指定日期的文件
                        elif file_change_date==self.date:
                            # 在目标目录中创建修改日期目录
                            if not os.path.exists(self.target_folder+"\\"+file_change_date):
                                os.mkdir(self.target_folder+"\\"+file_change_date)  
                            # 获取源文件绝对路径
                            source_file=os.path.dirname(entry)+"\\"+os.path.split(entry)[-1]
                            # 获取目标路径，并创建目录
                            target_file=self.target_folder+"\\"+file_change_date+source_file[len(self.source_folder):]
                            if not os.path.exists(target_file[:-len(os.path.split(entry)[-1])-1]):
                                os.makedirs(target_file[:-len(os.path.split(entry)[-1])-1])
                            # 拷贝
                            os.system("copy %s %s /y" % (source_file,target_file))
    
    def compress(self):
        folder_list=os.listdir(self.target_folder)
        for folder in folder_list:
            target=os.path.join(self.target_folder, folder+'.7z')
            source=os.path.join(self.target_folder, folder+'\\*') 
            if os.path.isdir(os.path.join(self.target_folder, folder)):
                os.system("%s a -t7z %s %s -r -mx=5 -m0=LZMA2 -ms=10m -mf=on -mhc=on -mmt=on" % (self.sz,target,source))
            

if __name__ == "__main__":
    source_folder=r"C:\Users\Charles\Desktop\Test_Log"
    target_folder=r"C:\Users\Charles\Desktop\RF_PCBA_Data_Backup"
    sz=r"C:\Users\Charles\Desktop\7z1900-extra\7za.exe"
    filt_compress=filt_compress(source_folder,target_folder,sz)
    filt_compress.filt()
    filt_compress.compress()