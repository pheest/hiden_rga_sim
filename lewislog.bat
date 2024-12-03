@echo on
set /A Instance=1
if not "%1"=="" set /A Instance=%1
set LewisPath=C:\Python311\scripts\
if not "%2"=="" set LewisPath=%2
set /A RPC_PORT=9999 + %Instance%
set /A DEVICE_PORT=5024 + %Instance%
set logdir=/var/log/hidenPyIoc/
if not exist %logdir% set logdir=../../main/epics/var/log
set CurrentDir=%~dp0
%LewisPath%lewis.exe -k hidenrga interfaces -r localhost:%RPC_PORT% -p "stream: {bind_address: localhost, port: %DEVICE_PORT%}" -a %CurrentDir% > %logdir%lewis_emulator%Instance%.log 2>&1
if %errorlevel% equ 130 time /t
