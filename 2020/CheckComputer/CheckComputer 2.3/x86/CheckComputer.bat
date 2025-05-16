@echo off

:check_Tool
tasklist | find /i "CheckComputer_2.0.exe"
if errorlevel 1 (
start /B CheckComputer_2.0.exe
call :kill_main
)

exit

:kill_main
set count=0
:retry
if @%count%==@600 goto kill_start
tasklist | find /i "CheckComputer_2.0.exe"
if errorlevel 1 goto kill_end
set /a count=%count%+1
ping -n 3 127.0.0.1
goto retry
:kill_start
taskkill /F /IM "CheckComputer_2.0.exe"
:kill_end
goto :EOF