@echo off
tasklist | find /i "lewis.exe" >NUL && (
    taskkill /f /im "lewis.exe"
)
