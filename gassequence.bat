
C:\Python310\scripts\lewis-control.exe device current_gas H2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 1E-7

C:\Python310\scripts\lewis-control.exe device current_gas H2O
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 2E-7

C:\Python310\scripts\lewis-control.exe device current_gas CO
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 1E-8

C:\Python310\scripts\lewis-control.exe device current_gas CO2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 2E-8

timeout 300

REM Air leak!
C:\Python310\scripts\lewis-control.exe device current_gas O2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 2E-6
C:\Python310\scripts\lewis-control.exe device current_gas N2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 8E-6
