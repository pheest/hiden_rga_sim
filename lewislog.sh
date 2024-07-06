declare -i Instance
Instance=${1:-1}
declare -i RPC_PORT
RPC_PORT=9999+$Instance
declare -i DEVICE_PORT
DEVICE_PORT=5024+$Instance

CurrentDir=$(dirname "$0")
export PYTHONPATH=$CurrentDir

logdir='/var/log/hidenPyIoc/'
if [[ ! -w $logdir ]]; then
    # Can't write to global log dir. Running in test/lewis_emulators.
    logdir = '../../main/epics/var/log/'
fi

lewis -k hidenrga interfaces -r localhost:$RPC_PORT -p "stream: {bind_address: localhost, port: $DEVICE_PORT}" > "$logdir"lewis_emulator$Instance.log 2>&1
