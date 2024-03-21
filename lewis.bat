@echo off
set CurrentDir=%~dp0

set LewisPath=C:\Python311\scripts\
if not "%1"=="" set LewisPath=%1

call %CurrentDir%kill_lewis.bat
set logdir=/var/log/hidenPyIoc/
if not exist %logdir% set logdir=
%LewisPath%lewis.exe -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}" -a %CurrentDir% > %logdir%lewis_emulator.log 2>&1

