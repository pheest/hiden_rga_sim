@echo on
tasklist | find /i "lewis.exe" >NUL && (
    taskkill /f /im "lewis.exe"
)
