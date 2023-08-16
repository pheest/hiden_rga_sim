#!/bin/bash

# This scripts sets simulated vaccum pressures in Pascal units
lewis-control device current_gas H2
lewis-control device current_gas_pressure 1E-5

lewis-control device current_gas H2O
lewis-control device current_gas_pressure 2E-5

lewis-control device current_gas CO
lewis-control device current_gas_pressure 1E-6

lewis-control device current_gas CO2
lewis-control device current_gas_pressure 2E-6

sleep 30

# Air leak!
lewis-control device current_gas O2
lewis-control device current_gas_pressure 2E-4
lewis-control device current_gas N2
lewis-control device current_gas_pressure 8E-4

while true
do
    sleep 10
    # Helium leak checking

    lewis-control device current_gas O2
    lewis-control device current_gas_pressure 1.92E-4
    lewis-control device current_gas N2
    lewis-control device current_gas_pressure 7.68E-4

    lewis-control device current_gas He
    lewis-control device current_gas_pressure 4E-5

    sleep 10

    lewis-control device current_gas O2
    lewis-control device current_gas_pressure 1.84E-4
    lewis-control device current_gas N2
    lewis-control device current_gas_pressure 7.36E-4

    lewis-control device current_gas He
    lewis-control device current_gas_pressure 8E-5
done
