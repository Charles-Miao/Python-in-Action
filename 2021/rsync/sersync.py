import os
import logging
import queue
import threading
import time
import watchdog.observers as observers
import watchdog.events as events
from ftplib import FTP
import paramiko

logger = logging.getLogger(__name__)

SENTINEL = None

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

class MyEventHandler(events.FileSystemEventHandler):
    def on_any_event(self, event):
        super(MyEventHandler, self).on_any_event(event)
        queue.put(event)
    def __init__(self, queue):
        self.queue = queue

def process(queue):
    while True:
        event = queue.get()
        logger.info(event)
        #print(event.key)
        _current_file=(event.key)[1].replace(rsyncSrc,'/cygdrive/d/Debug_Log')
        current_file=_current_file.replace('\\','/')
        

        
        if ((event.key)[0] == "created" or (event.key)[0] == "modified") and (event.key)[2] == False:
            print(current_file)
            rsync_cmd='rsync -avz -R -d --port=873 --delete --progress "'+current_file+'" '+rsyncDes+' --password-file="/cygdrive/d/ServerCheck/rsync/pass.txt"'
            os.popen(rsync_cmd)			
        elif (event.key)[0] == "deleted":
            #print(current_file)
            #delete_cmd='ssh administrator@192.168.123.42 \'rm -rf \"/volume1/Real-time'+current_file+'\"\''
            #os.popen(delete_cmd)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname='192.168.123.42', port=22, username='administrator', password='Z900TE@Quality!!#')
            stdin, stdout, stderr = client.exec_command('rm -rf "/volume1/Real-time'+current_file+'"')
            client.close()
        elif (event.key)[0] == "moved":
            #print(current_file)
            #delete_cmd='ssh administrator@192.168.123.42 \'rm -rf \"/volume1/Real-time'+current_file+'\"\''
            #os.popen(delete_cmd)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname='192.168.123.42', port=22, username='administrator', password='Z900TE@Quality!!#')
            stdin, stdout, stderr = client.exec_command('rm -rf "/volume1/Real-time'+current_file+'"')
            client.close()

            _new_file=(event.key)[2].replace(rsyncSrc,'/cygdrive/d/Debug_Log')
            new_file=_new_file.replace('\\','/')
            #print(new_file)
            rsync_cmd='rsync -avz -R -d --port=873 --delete --progress "'+new_file+'" '+rsyncDes+' --password-file="/cygdrive/d/ServerCheck/rsync/pass.txt"'
            os.popen(rsync_cmd)	
        time.sleep(7)

if __name__ == '__main__':

    rsyncSrc=r'D:\Debug_Log'
    rsyncDes='rsync_backup@192.168.123.42::realtime'

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s %(threadName)s] %(message)s',
                        datefmt='%H:%M:%S')
    
    queue = queue.Queue()
    num_workers = int(get_CPU_NumberOfCores())
    pool = [threading.Thread(target=process, args=(queue,)) for i in range(num_workers)]
    for t in pool:
        t.daemon = True
        t.start()

    event_handler = MyEventHandler(queue)
    observer = observers.Observer()
    observer.schedule(
        event_handler,
        path=rsyncSrc,
        recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()