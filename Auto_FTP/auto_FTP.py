#https://blog.csdn.net/qq_33195791/article/details/103824448
import os
import re
import sys
import datetime,time
from ftplib import FTP
import traceback
import logging
 
FTP_PERFECT_BUFF_SIZE = 8192
 
def is_same_size(ftp, local_file, remote_file):
    try:
        remote_file_size = ftp.size(remote_file)
    except Exception as err:
        logging.debug("get remote file_size failed, Err:%s" % err)
        remote_file_size = -1
 
    try:
        local_file_size = os.path.getsize(local_file)
    except Exception as err:
        logging.debug("get local file_size failed, Err:%s" % err)
        local_file_size = -1

    result = True if(remote_file_size == local_file_size) else False
 
    return (result, remote_file_size, local_file_size)
 
def upload_file(local_file, remote_file, ftp):
    if not os.path.exists(local_file):
        logging.debug('no such file or directory %s.' (local_file))
        return False
 
    result = False
    remote_file_size = local_file_size = -1
 
    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
    if True != result:
        print('remote_file %s is not exist, now trying to upload...' %(remote_file))
        logging.debug('remote_file %s is not exist, now trying to upload...' %(remote_file))  
        global FTP_PERFECT_BUFF_SIZE
        bufsize = FTP_PERFECT_BUFF_SIZE
        try:
            with open(local_file, 'rb') as file_handler :           
                if ftp.storbinary('STOR ' + remote_file, file_handler, bufsize):
                    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
        except Exception as err:
            logging.debug('some error happend in storbinary file :%s. Err:%s' %(local_file, traceback.format_exc()))
            result = False
 
    logging.debug('Upload ?%s? %s , remote_file_size = %d, local_file_size = %d.' \
    %(remote_file, 'success' if (result == True) else 'failed', remote_file_size, local_file_size))
    print('Upload ?%s? %s , remote_file_size = %d, local_file_size = %d.' \
    %(remote_file, 'success' if (result == True) else 'failed', remote_file_size, local_file_size))
 
def upload_file_tree(local_path, remote_path, ftp, IsRecursively):
    print("remote_path:", remote_path)
 
    try:
        ftp.cwd(remote_path)
    except Exception as e:
        print('Except INFO:', e)
        base_dir, part_path = ftp.pwd(), remote_path.split('/')
        for subpath in part_path:
            if '' == subpath:
                continue
            base_dir = os.path.join(base_dir, subpath) 
            try:
                ftp.cwd(base_dir) 
            except Exception as e:
                print('Except INFO:', e)
                print('remote not exist directory %s , create it.' %(base_dir))
                ftp.mkd(base_dir) 
                continue

    try:
        file_list = os.listdir(local_path)
        for file_name in file_list:
            if os.path.isdir(os.path.join(local_path, file_name) ):
                print('%s is a directory...' %(file_name))
                if IsRecursively: 
                    try:
                        cwd = ftp.pwd()
                        ftp.cwd(file_name)  
                        ftp.cwd(cwd)
                    except Exception as e:
                        print('check remote directory %s not eixst, now trying to create it! Except INFO:%s.' %(file_name, e))
                        ftp.mkd(file_name)
                    
                    print('trying to upload directory %s --> %s ...' %(file_name, remote_path))
                    logging.debug('trying to upload directory %s --> %s ...' %(file_name, remote_path))
                    p_local_path = os.path.join(local_path, file_name)
                    p_remote_path = os.path.join(ftp.pwd(), file_name)
                    upload_file_tree(p_local_path, p_remote_path, ftp, IsRecursively)
                    ftp.cwd("..")
                else:
                    logging.debug('translate mode is UnRecursively, %s is a directory, continue ...' %(file_name))
                    continue
            else:
                local_file = os.path.join(local_path, file_name) 
                remote_file = os.path.join(remote_path, file_name)
                if upload_file(local_file, remote_file, ftp):
                    pass
    except:
        logging.debug('some error happend in upload file :%s. Err:%s' %(file_name, traceback.format_exc()))
    return
 
 
if __name__ == '__main__':  
    current_time = time.time()
    str_time = time.strftime('%Y%m%d%H%M%S',time.localtime(current_time ))
    log_file_name = 'ftpput' + str_time  + '.log'
 
    LOG_FORMAT = "%(message)s" #"%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a ' 
    LOG_PATH = os.path.join(os.getcwd(), log_file_name)
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt = DATE_FORMAT ,
                        filemode='w', 
                        filename=LOG_PATH 
                        )
 
 
    host = '10.45.41.143'
    port = 21
    username = 'QCN'
    password = 'qcn'
    ftp = FTP()
    ftp.connect(host,port)
    ftp.login(username, password)
 
    local_path = r'X:\QCN_20230117'
    remote_path = 'QCN_20230117'
    #local_file =None
    #remote_file = None
    IsRecursively = True
    upload_file_tree(local_path, remote_path, ftp, IsRecursively)
    #upload_file(local_file, remote_file, ftp)
