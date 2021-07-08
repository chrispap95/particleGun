#!/bin/sh
# Script that creates a list of the published datasets from previous step
# Input:
#         $1: command to run

echo -n -e "\033[93mFetching\033[0m"
echo " data from previous step. Hold tight! "
cd ${CMSSW_BASE}/src/particleGun

eval $1

if [ ! -s myGeneration/list.txt ]
then
  echo -n -e "\033[91mError: \033[0m"
  echo "list file is empty or does not exist! Please check again the input values."
  exit 1
else
  echo -n "Data fetched "
  echo -n -e "\033[92msuccessfully\033[0m"
  echo "!"
  echo "Going to use the following datasets:"
  cat myGeneration/list.txt
  sleep 2
fi
