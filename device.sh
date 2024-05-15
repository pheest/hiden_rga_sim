#!/bin/bash

CurrentDir=$(dirname "$0")
export PYTHONPATH="$CurrentDir"

lewis-control -r localhost:10000 device

