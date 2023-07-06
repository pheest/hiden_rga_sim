#!/bin/bash

CurrentDir=$(dirname "$0")
export PYTHONPATH="$CurrentDir"

lewis-control -r 10.1.1.9:10000 device

