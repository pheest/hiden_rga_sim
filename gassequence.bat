REM This scripts sets simulated vaccum pressures in Pascal units

C:\Python310\scripts\lewis-control.exe device current_gas H2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 1E-5

C:\Python310\scripts\lewis-control.exe device current_gas D2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 4E-5

C:\Python310\scripts\lewis-control.exe device current_gas H2O
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 2E-5

C:\Python310\scripts\lewis-control.exe device current_gas CO
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 1E-6

C:\Python310\scripts\lewis-control.exe device current_gas CO2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 2E-6

timeout 30

REM Air leak!
C:\Python310\scripts\lewis-control.exe device current_gas O2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 2E-4
C:\Python310\scripts\lewis-control.exe device current_gas N2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 8E-4

:startleakckecking
timeout 10
REM Helium leak checking

C:\Python310\scripts\lewis-control.exe device current_gas O2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 1.92E-4
C:\Python310\scripts\lewis-control.exe device current_gas N2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 7.68E-4

C:\Python310\scripts\lewis-control.exe device current_gas He
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 4E-5

timeout 10

C:\Python310\scripts\lewis-control.exe device current_gas O2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 1.84E-4
C:\Python310\scripts\lewis-control.exe device current_gas N2
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 7.36E-4

C:\Python310\scripts\lewis-control.exe device current_gas He
C:\Python310\scripts\lewis-control.exe device current_gas_pressure 8E-5

goto startleakckecking
