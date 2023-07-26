SET CurrentDir=%~dp0
SET PYTHONPATH=%CurrentDir%

taskkill /IM "lewis.exe" /F
C:\Python310\scripts\lewis.exe -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}" > lewis_emulator.log 2>&1

