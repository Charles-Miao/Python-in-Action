@echo on
chcp 65001 >nul
setlocal enabledelayedexpansion

set server=10.197.193.15
set SERVER_custom=\\%server%\ht共享盘\ESOP\测试SOP\onekey\update_client.bat
set LOCAL_DIR=%~dp0

net use  * /delete /y 2>nul
net use \\%server% "Js@ict2024" /user:ht\esop /y

copy "%SERVER_custom%" "%LOCAL_DIR%" /y


ping -n 2 127.0.0.1 >nul 2>&1

call "%LOCAL_DIR%update_client.bat"

endlocal
pause

