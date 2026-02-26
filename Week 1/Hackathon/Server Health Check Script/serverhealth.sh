#!/bin/bash
echo "hostname: $(hostname)"
echo "date: $(date)"
echo "CPU Usage:"
lscpu
echo "Memory usage:"
free -h
echo "Disk usage:"
df -h
echo "Top processes"
top -b -n 1 | head -n 10
echo "Active networks"
ss -tulpn | head -n 10
