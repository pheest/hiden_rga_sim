@echo off
set CurrentDir=%~dp0

set LewisPath=C:\Python310\scripts\
if not "%1"=="" set LewisPath=%1

call %CurrentDir%kill_lewis.bat
%LewisPath%lewis.exe -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}" -a %CurrentDir% > lewis_emulator.log 2>&1

