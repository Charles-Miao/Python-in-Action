@echo off
chcp 65001 >nul
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set ip=%%a
    set ip=%ip: =%
    ::echo 本地IP地址是: %ip% > ip.txt

    vncviewer %ip%:80 -password pwd.txt
    if errorlevel 1 (
        echo 远程连接失败，请检查网络和配置。
    ) else (
        echo 成功发起远程连接。
    )
    pause
    exit /b
)
echo 未找到有效的 IPv4 地址。
)
pause