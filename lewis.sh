#!/bin/bash 
CurrentDir=$(dirname "$0") 
export PYTHONPATH=$CurrentDir
lewis -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}"
