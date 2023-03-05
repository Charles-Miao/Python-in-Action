from ctypes import *
import os
import sys
import ftplib
 
 
class myFtp:
    ftp = ftplib.FTP()
 
    def __init__(self, host, port=21):
        self.ftp.connect(host, port)
 
    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)
 
    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')
        print(file_handler)
        # self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)#接收服务器上文件并写入本地文件
        self.ftp.retrbinary('RETR ' + RemoteFile, file_handler.write)
        file_handler.close()
        return True
 
    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print("remoteDir:", RemoteDir)
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print(self.ftp.nlst(file))
            if file.find(".") == -1:
                if not os.path.exists(Local):
                    os.makedirs(Local)
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return
    
    def CheckFolderisEmpty(self,RemoteDir):
        self.ftp.cwd(RemoteDir)
        if len(self.ftp.nlst())==0:
            return("Empty")
        else:
            return("Not Empty")
    
    def DeleteFiles(self,RemoteDir): #删除ftp上指定的文件
        self.ftp.cwd(RemoteDir)   # 要登录的ftp目录
        files=self.ftp.nlst()#获取当前目录下的所有文件
        for filename in files:
            self.ftp.delete(filename)  # 删除ftp服务器上的文件

    def uploadFile(self,LocalDir,RemoteDir):
        self.ftp.cwd(RemoteDir)
        file_handle=open(LocalDir,'rb')
        filename=os.path.split(LocalDir)[-1]
        self.ftp.storbinary('STOR %s' %filename, file_handle, blocksize=1024)
        self.ftp.set_debuglevel(0)
        file_handle.close()

    def close(self):
        self.ftp.quit()
 
 
if __name__ == "__main__":
    ftp = myFtp('192.168.66.38')
    ftp.Login('WKS_TE_CRL', '8K21g93w')
    ftpfolder='/Revoke'
    localfolder=r'D:\python_script\get_CRL\revoke_file'

    if ftp.CheckFolderisEmpty(ftpfolder) == "Empty":
        print("Folder is Empty")
    elif ftp.CheckFolderisEmpty(ftpfolder) == "Not Empty":
        print("Folder is not Empty")
        ftp.DownLoadFileTree(localfolder, ftpfolder)  # 从目标目录下载到本地目录
        ftp.DeleteFiles(ftpfolder)
    ftp.close()
    print("ok!")
