@echo off

set program_name=XXX.exe
set restart_delay=10

:start
tasklist | find /i "%program_name%" > nul
if %errorlevel% equ 0 (
    echo %program_name% is running.
    choice /t 3600 /d y /n>nul
) else (
    echo %program_name% has stopped. Restarting...
    start "X:\XXX.exe" "%program_name%"
    timeout /t %restart_delay%
)

goto start
