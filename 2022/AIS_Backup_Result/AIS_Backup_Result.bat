if exist D:\python_script\AIS_Backup_Result\AIS_Backup_Result.txt del D:\python_script\AIS_Backup_Result\AIS_Backup_Result.txt
ping 127.0.0.1 -n 5
call python D:\python_script\AIS_Backup_Result\AIS_Backup_Result.py
ping 127.0.0.1 -n 5
call python D:\python_script\AIS_Backup_Result\send_mail.py