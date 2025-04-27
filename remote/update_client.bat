@echo on
chcp 65001 >nul
setlocal enabledelayedexpansion

set server=10.197.193.15
::net use  * /delete /y 2>nul
::net use \\%server% "Js@ict2024" /user:ht\esop /y


set SERVER_URL=\\%server%\ht共享盘\ESOP\测试SOP\onekey\client.exe
set LOCAL_DIR=%~dp0
set CLIENT_PROCESS=client.exe
::set ZIP_FILE=client.7z

taskkill /F /IM "%CLIENT_PROCESS%" >nul
ping -n 2 127.0.0.1 >nul 2>&1


copy %SERVER_URL% %LOCAL_DIR% /y

ping -n 3 127.0.0.1 >nul 2>&1

start "" "%LOCAL_DIR%%CLIENT_PROCESS%"



endlocal
echo done
