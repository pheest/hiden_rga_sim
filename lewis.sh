#!/bin/bash

killall lewis 2>/dev/null
CurrentDir=$(dirname "$0") 
export PYTHONPATH=$CurrentDir
logdir='/var/log/hidenPyIoc/'
if [[ ! -w logdir ]]; then
    logdir=''
fi
lewis -k hidenrga interfaces -r localhost:10000 -p "stream: {bind_address: localhost, port: 5025}" > "$logdir"lewis_emulator.log 2>&1

