REM This scripts sets simulated vaccum pressures in Pascal units

set /A Instance=1
if not "%1"=="" set /A Instance=%1
set /A RPC_PORT=9999+%Instance%

set LewisPath=C:\Python311\scripts\
if not "%2"=="" set LewisPath=%2

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas H2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 1E-5

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas D2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 4E-5

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas H2O
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 2E-5

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas CO
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 1E-6

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas CO2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 2E-6

timeout 30

REM Air leak!
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas O2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 2E-4
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas N2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 8E-4

:startleakckecking
timeout 10
REM Helium leak checking

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas O2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 1.92E-4
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas N2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 7.68E-4

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas He
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 4E-5

timeout 10

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas O2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 1.84E-4
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas N2
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 7.36E-4

%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas He
%LewisPath%\lewis-control.exe -r localhost:%RPC_PORT% device current_gas_pressure 8E-5

goto startleakckecking
