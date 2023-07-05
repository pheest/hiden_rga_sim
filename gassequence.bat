
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas H2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 1E-7

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas H2O
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 2E-7

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas CO
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 1E-8

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas CO2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 2E-8

timeout 30

REM Air leak!
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas O2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 2E-6
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas N2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 8E-6

:startleakckecking
timeout 10
REM Helium leak checking

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas O2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 1.92E-6
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas N2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 7.68E-6

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas He
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 4E-7

timeout 10

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas O2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 1.84E-6
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas N2
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 7.36E-6

C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas He
C:\Python310\scripts\lewis-control.exe -r 10.1.1.9:10000 device current_gas_pressure 8E-7

goto startleakckecking
