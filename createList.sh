#!/bin/sh
# Script that creates a list of the published datasets from previous step

echo "Fetching data from previous step. Hold tight!"
python checkStatus.py | grep "Output dataset:" | awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
echo "Data fetched successfully!"
sleep 2
