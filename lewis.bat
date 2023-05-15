SET CurrentDir=%~dp0
SET PYTHONPATH=%CurrentDir%

taskkill /IM "lewis.exe" /F
C:\Python310\scripts\lewis.exe -k hidenrga interfaces -r 10.1.1.9:10000 -p "stream: {bind_address: 10.1.1.9, port: 5025}" > lewis_emulator.log 2>&1

