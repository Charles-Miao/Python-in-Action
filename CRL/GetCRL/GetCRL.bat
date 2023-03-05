@echo on
::initialization
d:
cd \CRL\GetCRL

if exist crl*.pem del crl*.pem
if exist LVR5-crl.crl del LVR5-crl.crl

::set parameters
ping 172.168.48.11 -n 1
if not errorlevel 1 set server_ip=172.168.48.11
ping 172.168.48.12 -n 1
if not errorlevel 1 set server_ip=172.168.48.12
echo %server_ip%

for /f %%i in ('datex -f yyyy-mm-dd') do set end_date=%%i
for /f %%i in ('datex -f hh:nn:ss') do set end_time=%%i
set end_date_time=%end_date%T%end_time%Z
echo %end_date_time%

set start_date_time=2023-01-01T00:00:00Z

set expiry_hours=960

::get CRL
https_client.exe -ip %server_ip%:8888 -action getCRL -crl_begin %start_date_time% -crl_end %end_date_time% -crl_expiry %expiry_hours%

::renmae CRL
copy crl*.pem LVR5-crl.crl /y

::transfer to ftp server
echo open 192.168.123.71>tmp_ftp.txt
echo crl>>tmp_ftp.txt
echo crl>>tmp_ftp.txt
echo put LVR5-crl.crl>>tmp_ftp.txt
echo bye>>tmp_ftp.txt

ftp -s:tmp_ftp.txt

