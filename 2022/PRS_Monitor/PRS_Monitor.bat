call python D:\python_script\PRS_Monitor\PRS_Log.py
::call python D:\python_script\PRS_Monitor\send_mail.py

if exist Z:\Temp\Charles\PRS\prs.csv del Z:\Temp\Charles\PRS\prs.csv
copy D:\python_script\PRS_Monitor\prs.csv Z:\Temp\Charles\PRS\prs.csv /y