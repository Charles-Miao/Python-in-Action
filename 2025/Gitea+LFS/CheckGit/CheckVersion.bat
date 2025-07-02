@echo off

set sendfile=D:\ServerJobs\CheckGit\git_send.txt
if exist %sendfile% del %sendfile%

d:
cd D:\ServerJobs\CheckGit

for /f "tokens=1,2 delims=," %%i in (Config.ini) do (
call :CheckGit %%i %%j
)

goto send

echo ***************************************Check Git Function************************************************
:CheckGit
set ProgramPath=%1
set VerFile=%2

:: 获取最新提交哈希
for /f %%h in ('git -C %ProgramPath% log -1 --pretty^=format:"%%H"') do set "current_hash=%%h"

:: 读取上次记录的哈希
if exist %VerFile% (
    set /p last_hash=<%VerFile%
) else (
    set last_hash=
)

:: 判断版本是否有变化
if "%current_hash%"=="%last_hash%" goto CheckGit_END

:: 获取修改者
for /f %%a in ('git -C %ProgramPath% log -1 --pretty^=format:"%%an"') do set "author=%%a"

:: 获取修改时间
for /f "delims=" %%d in ('git -C %ProgramPath% log -1 --pretty^=format:"%%ad" --date^=local') do set "commit_date=%%d"

:: 获取远程仓库名
for /f "tokens=*" %%a in ('git -C %ProgramPath% remote get-url origin 2^>nul') do set "url=%%a"

echo ---------------------Author/ Commit Date/ Current Ver------------------- >> %sendfile%
echo Author: %author% >> %sendfile%
echo Commit date: %commit_date% >> %sendfile%
echo Current Version:  %current_hash% >> %sendfile%
echo Remote URL: %url% >> %sendfile%
echo. >> %sendfile%

:: 记录提交描述
echo ---------------------Commit messages------------------------------------ >> %sendfile%
git -C %ProgramPath% log -1 --pretty=format:"%%B" >> %sendfile%
echo. >> %sendfile%

:: 记录详细信息
echo ---------------------Full diff HEAD vs HEAD~1--------------------------- >> %sendfile%
git -C %ProgramPath% diff HEAD~1 HEAD >> %sendfile%

:: 更新版本文件
echo %current_hash%> %VerFile%

:CheckGit_END
goto :EOF
echo ***************************************Check Git Function************************************************

:send
@REM send mail to TE
if exist %sendfile% (
    python send_mail.py
)
:end