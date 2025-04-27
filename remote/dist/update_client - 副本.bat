@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set server=10.197.193.15
::net use  * /delete /y 2>nul
::net use \\%server% "Js@ict2024" /user:ht\esop /y


set SERVER_URL=\\%server%\ht共享盘\ESOP\测试SOP\onekey\client.exe
set LOCAL_DIR=%~dp0
set CLIENT_PROCESS=client.exe
::set ZIP_FILE=client.7z

taskkill /F /IM "%CLIENT_PROCESS%" /T >nul 2>&1
timeout /T 3


copy %SERVER_URL% %LOCAL_DIR% /y

start "" "%LOCAL_DIR%%CLIENT_PROCESS%" /B

::if exist "%LOCAL_DIR%%CLIENT_PROCESS%" (
    ::echo start client.exe...
    ::start "" "%LOCAL_DIR%%CLIENT_PROCESS%"
::) else (
   ::echo error:can not find file "%CLIENT_PROCESS%"
    ::pause
    ::exit /b 1
::)

endlocal
echo done
exit
