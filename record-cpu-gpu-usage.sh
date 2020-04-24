#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DATA_FILE="/data/E122_CPU_GPU.csv"

GPU_USAGE=""
LINENUM=0
while read line; do
	if [[ "$LINENUM" == "8" ]]; then
		GPU_USAGE=$(echo "$line" | cut -d "|" -f 4 | grep -E -o '[0-9]+')
		break
	fi
	((LINENUM++))
done < <(nvidia-smi)

CPU_USAGE="$(awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1); }' <(grep 'cpu ' /proc/stat) <(sleep 1;grep 'cpu ' /proc/stat))"
# echo "CPU: $CPU_USAGE"
# echo "GPU: $GPU_USAGE"

echo "$(date +"%Y-%m-%d %H:%M:%S"),$CPU_USAGE,$GPU_USAGE" >> "$DIR$DATA_FILE"