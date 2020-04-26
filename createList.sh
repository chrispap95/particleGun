#!/bin/sh
# Script that creates a list of the published datasets from previous step
# Input:
#         $1: step
#         $2: energies
#         $3: particles
#         $4: geometry
#         $5: eta
#         $6: phi

tput setaf 3
echo -n "Fetching"
tput sgr0
echo " data from previous step. Hold tight! "

if [ -z $5 ]
then
  if [ -z $6 ]
  then
    python checkStatus.py -s $1 -E $2 -p $3 -g $4 | grep "Output dataset:" | \
    awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
  else
    python checkStatus.py -s $1 -E $2 -p $3 -g $4 -P $6 | grep "Output dataset:" | \
    awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
  fi
elif [ -z $6 ]
then
  python checkStatus.py -s $1 -E $2 -p $3 -g $4 -e $5 | grep "Output dataset:" | \
  awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
else
  python checkStatus.py -s $1 -E $2 -p $3 -g $4 -e $5 -P $6 | grep "Output dataset:" | \
  awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
fi

if [ -s myGeneration/list.txt ] || [ ! -f myGeneration/list.txt ]
then
  tput setaf 1
  echo -n "Error: "
  tput sgr0
  echo "list file is empty or does not exist! Please check again the input values."
  exit 1
else
  echo -n "Data fetched "
  tput setaf 2
  echo -n "successfully"
  tput sgr0
  echo "!"
  echo "Going to use the following datasets:"
  cat myGeneration/list.txt
  sleep 2
fi
