@echo off
SET CurrentDir=%~dp0
SET PYTHONPATH=%CurrentDir%

call %CurrentDir%kill_lewis.bat
C:\Python310\scripts\lewis.exe -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}" > lewis_emulator.log 2>&1

