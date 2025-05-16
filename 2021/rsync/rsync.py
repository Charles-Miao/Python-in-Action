#-*- coding: utf-8 -*-
import subprocess
import os
import time
import re

rsyncSrc=r'D:\Debug_Log'
rsyncDes='rsync_backup@192.168.123.42::realtime'
listen=r'inotifywait -mrq --format "%%e@%%w\%%f" "D:\Debug_Log"'
popen=subprocess.Popen(listen,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

while True:
    line=popen.stdout.readline().strip()
    #print(line)
    lineArr=line.decode().split('@')
    oper=lineArr[0]
	
    file=lineArr[1]
    touched=False
    delete=False
    #print(file.strip())
    if file.index(rsyncSrc)==0:
        if (oper=='DELETE') or  (oper=='MOVED_FROM'):
            _cureent_file=file.replace(rsyncSrc,'/cygdrive/d/Debug_Log')
            cureent_file=_cureent_file.replace('\\','/')
            print(cureent_file)
            delete_cmd='ssh administrator@192.168.123.42 \'rm -rf \"/volume1/Real-time'+cureent_file+'\"\''
            #modify_time_cmd='ssh administrator@192.168.123.42 \'stat \"/volume1/Real-time'+cureent_file+'\"\''
            #print(delete_cmd)
            delete=True
        if (oper=='MOVED_TO') or (oper=='CREATE') or (oper=='MODIFY'):
            _cureent_file=file.replace(rsyncSrc,'/cygdrive/d/Debug_Log')
            #print(_cureent_file)
            cureent_file=_cureent_file.replace('\\','/')
            print(cureent_file)
            #rsync_cmd='set CYGWIN=nodosfilewarning && cd /d '+rsyncSrc+' && '+'start /b rsync -avz -R -d --port=873 --delete --progress '+cureent_file+' '+rsyncDes+' --password-file="/cygdrive/d/ServerCheck/rsync/pass.txt" 2>D:\ServerCheck\rsync\error.log'
            rsync_cmd='rsync -avz -R -d --port=873 --delete --progress "'+cureent_file+'" '+rsyncDes+' --password-file="/cygdrive/d/ServerCheck/rsync/pass.txt"'
            touched=True
    if delete:
        #print(delete_cmd)
        #print(modify_time_cmd)
        #conent=os.popen(modify_time_cmd).readlines()
        #print(conent)
        #modify_date=""
        #for index in range(len(conent)):
        #    if "Modify" in conent[index]:
        #        modify_date=re.split(r'[: ]',conent[index])[2].strip()	
        #        #print(re.split(r'[: ]',conent[index]))	
        #if modify_date==time.strftime("%Y-%m-%d", time.localtime()):
        #    os.popen(delete_cmd)
        os.popen(delete_cmd)
    if touched:
        #print(rsync_cmd)
        rsyncAction=os.popen(rsync_cmd)
        rsyncStat=rsyncAction.read()
        if "speedup is" in rsyncStat:
            print(file+' rsynced!')
            print(rsyncStat)
        else:
            print(file+' rsync failed!')
            print(rsyncStat)