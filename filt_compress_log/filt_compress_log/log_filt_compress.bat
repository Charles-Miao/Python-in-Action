echo on
::initialization
d:
cd %~dp0
inifile.exe config.ini [config] log_path > log_path.bat
call log_path.bat
::check temp folder is empty
python empty_folder.py
::filt and compress test log
python log_filt_compress_1.3.py > %log_path%
::check the result
python check_logging.py
