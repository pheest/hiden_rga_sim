@echo on
set CurrentDir=%~dp0


set /A Instances=1
if not "%1"=="" set Instances=%1
set LewisPath=C:\Python311\scripts\
if not "%2"=="" set LewisPath=%2

call %CurrentDir%kill_lewis.bat

set /A Instance=0
:start
set /A Instance+=1
if %Instance% EQU %Instances% goto end
start /B %CurrentDir%lewislog.bat %Instance% %LewisPath%
goto start
:end
REM See https://superuser.com/questions/1705792/how-to-suppress-windows-batch-job-termination-confirmation
echo N | cmd /C %CurrentDir%lewislog.bat %Instance% %LewisPath%
if %errorlevel% equ 130 time /t
