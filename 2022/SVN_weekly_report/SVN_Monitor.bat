D:
cd \python_script\SVN_weekly_report
call python D:\python_script\SVN_weekly_report\get_info.py
::call python D:\python_script\PRS_Monitor\send_mail.py

if exist Z:\Temp\Charles\SVN\SVN.xlsx del Z:\Temp\Charles\SVN\SVN.xlsx
copy D:\python_script\SVN_weekly_report\SVN.xlsx Z:\Temp\Charles\SVN\SVN.xlsx /y

