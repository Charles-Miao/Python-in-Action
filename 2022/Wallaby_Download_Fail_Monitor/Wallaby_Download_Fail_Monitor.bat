call python D:\python_script\Wallaby_Download_Fail_Monitor\Wallaby_Download_Fail_Monitor.py
::call python D:\python_script\PRS_Monitor\send_mail.py

if exist Z:\Temp\Charles\Wallaby_DL_Monitor\*.csv del Z:\Temp\Charles\Wallaby_DL_Monitor\*.csv
copy D:\python_script\Wallaby_Download_Fail_Monitor\csv Z:\Temp\Charles\Wallaby_DL_Monitor /y