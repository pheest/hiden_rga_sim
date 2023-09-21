@echo off
set CurrentDir=%~dp0
set Device = hidenrga
if not "%1"=="" set Device=%1

set LewisPath=C:\Python310\scripts\
if not "%2"=="" set LewisPath=%2

call %CurrentDir%kill_lewis.bat
%LewisPath%lewis.exe -k %Device% interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}" -a %CurrentDir% > lewis_emulator.log 2>&1

