#!/bin/bash

declare -i Instance
Instance=${1:-1}
declare -i RPC_PORT
RPC_PORT=9999+$Instance
declare -i DEVICE_PORT
DEVICE_PORT=5024+$Instance

CurrentDir=$(dirname "$0")
export PYTHONPATH=$CurrentDir

LogDir='/var/log/hidenPyIoc/'
if [ ! -d $LogDir ] || [ ! -w $LogDir ]; then
    # Can't write to global log dir. File directory is src/test/lewis_emulators, we want src/main/epics/var/log
    LogDir=$(dirname $(dirname $CurrentDir))'/main/epics/var/log/'
fi

lewis -k hidenrga interfaces -r localhost:$RPC_PORT -p "stream: {bind_address: localhost, port: $DEVICE_PORT}" > "$logdir"lewis_emulator$Instance.log 2>&1
