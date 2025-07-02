@echo off

d:
cd D:\ServerJobs\GitCheckOut

  ShowConsole.exe MINIMIZED
  set dst=D:\Honey
  setlocal ENABLEDELAYEDEXPANSION
:CheckOut
    for /f "tokens=1,2" %%I in (GitCheckout.ini) do (
      echo [%date% %time%]  http://10.150.64.3:3000/Admin/%%I.git -- ^> %dst%\%%J
      cd %dst%\%%J
      git reset --hard HEAD
      git pull origin main
      )
:End
EXIT  
