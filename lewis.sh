#!/bin/bash

killall lewis 2>/dev/null

declare -i Instances
Instances=${1:-1}

CurrentDir=$(dirname "$0")

for ((Instance=1; Instance < $Instances; Instance++))
do
    $CurrentDir/lewislog.sh $Instance &
done

$CurrentDir/lewislog.sh $Instances
