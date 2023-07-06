#!/bin/bash

lewis-control -r 10.1.1.9:10000 device current_gas H2
lewis-control -r 10.1.1.9:10000 device current_gas_pressure 1E-7

lewis-control -r 10.1.1.9:10000 device current_gas H2O
lewis-control -r 10.1.1.9:10000 device current_gas_pressure 2E-7

lewis-control -r 10.1.1.9:10000 device current_gas CO
lewis-control -r 10.1.1.9:10000 device current_gas_pressure 1E-8

lewis-control -r 10.1.1.9:10000 device current_gas CO2
lewis-control -r 10.1.1.9:10000 device current_gas_pressure 2E-8

sleep 300

# Air leak!
lewis-control -r 10.1.1.9:10000 device current_gas O2
lewis-control -r 10.1.1.9:10000 device current_gas_pressure 2E-6
lewis-control -r 10.1.1.9:10000 device current_gas N2
lewis-control -r 10.1.1.9:10000 device current_gas_pressure 8E-6

