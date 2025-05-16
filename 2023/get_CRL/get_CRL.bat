echo on

d:
cd \python_script\get_CRL

python get_CRL.py
if exist D:\python_script\get_CRL\CRL\LVR5-crl.crl del D:\python_script\get_CRL\CRL\LVR5-crl.crl
