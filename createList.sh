#!/bin/sh
# Script that creates a list of the published datasets from previous step
# Input:
#         $1: step
#         $2: energies
#         $3: particles

echo "Fetching data from previous step. Hold tight!"
python checkStatus.py -s $1 -E $2 -p $3 -g $4 | grep "Output dataset:" | awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
echo "Data fetched successfully!"
echo "Going to use the following datasets:"
cat myGeneration/list.txt
sleep 2
