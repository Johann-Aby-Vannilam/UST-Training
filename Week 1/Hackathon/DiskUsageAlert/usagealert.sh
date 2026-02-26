#!/bin/bash
echo "Disk usage:"
df -h
THRESHOLD=80
LOG_FILE="/var/log/disk_usage.log"
df -h | awk 'NR>1 {print $1, $5, $6}' | while read disk usage mount_point; do
    usage_percent=${usage%\%}
    if [ "$usage_percent" -ge "$THRESHOLD" ]; then
        message="ALERT: Disk usage on $mount_point ($disk) is ${usage_percent}%"
        echo "$message"
        echo "$(date) - $message" >> "$LOG_FILE"
    fi
done