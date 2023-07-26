#!/bin/bash

lewis-control device current_gas H2
lewis-control device current_gas_pressure 1E-7

lewis-control device current_gas H2O
lewis-control device current_gas_pressure 2E-7

lewis-control device current_gas CO
lewis-control device current_gas_pressure 1E-8

lewis-control device current_gas CO2
lewis-control device current_gas_pressure 2E-8

sleep 30

# Air leak!
lewis-control device current_gas O2
lewis-control device current_gas_pressure 2E-6
lewis-control device current_gas N2
lewis-control device current_gas_pressure 8E-6

while true
do
    sleep 10
    # Helium leak checking

    lewis-control device current_gas O2
    lewis-control device current_gas_pressure 1.92E-6
    lewis-control device current_gas N2
    lewis-control device current_gas_pressure 7.68E-6

    lewis-control device current_gas He
    lewis-control device current_gas_pressure 4E-7

    sleep 10

    lewis-control device current_gas O2
    lewis-control device current_gas_pressure 1.84E-6
    lewis-control device current_gas N2
    lewis-control device current_gas_pressure 7.36E-6

    lewis-control device current_gas He
    lewis-control device current_gas_pressure 8E-7
done
