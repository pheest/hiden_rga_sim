#!/bin/bash 
CurrentDir=$(dirname "$0") 
#export PYTHONPATH=$CurrentDir 
export PYTHONPATH=$(pwd) 
echo $PYTHONPATH 
#pkill -f "lewis.exe" 
#lewis -k hidenrga.interfaces stream_interface -r 10.1.1.9:10000 -p "stream: {bind_address: 10.1.1.9, port: 5025}" > lewis_emulator.log 2>&1 
lewis -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}"
