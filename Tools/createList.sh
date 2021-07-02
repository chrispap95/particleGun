#!/bin/sh
# Script that creates a list of the published datasets from previous step
# Input:
#         $1: step
#         $2: energies
#         $3: particles
#         $4: geometry
#         $5: eta
#         $6: phi
#         $7: tag
#         $8: closeBy
#         $9: campaign

echo -n -e "\033[93mFetching\033[0m"
echo " data from previous step. Hold tight! "

if [ "$8" == "True" ]
then
  if [ -z $5 ]
  then
    if [ -z $6 ]
    then
      python checkStatus.py -s $1 -E $2 -p $3 -g $4 -t $7 -c $9 --closeBy | grep "Output dataset:" | \
      awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
    else
      python checkStatus.py -s $1 -E $2 -p $3 -g $4 -P $6 -t $7 -c $9 --closeBy | grep "Output dataset:" | \
      awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
    fi
  elif [ -z $6 ]
  then
    python checkStatus.py -s $1 -E $2 -p $3 -g $4 -e $5 -t $7 -c $9 --closeBy | grep "Output dataset:" | \
    awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
  else
    python checkStatus.py -s $1 -E $2 -p $3 -g $4 -e $5 -P $6 -t $7 -c $9 --closeBy | grep "Output dataset:" | \
    awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
  fi
else
  if [ -z $5 ]
  then
    if [ -z $6 ]
    then
      python checkStatus.py -s $1 -E $2 -p $3 -g $4 -t $7 -c $9 | grep "Output dataset:" | \
      awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
    else
      python checkStatus.py -s $1 -E $2 -p $3 -g $4 -P $6 -t $7 -c $9 | grep "Output dataset:" | \
      awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
    fi
  elif [ -z $6 ]
  then
    python checkStatus.py -s $1 -E $2 -p $3 -g $4 -e $5 -t $7 -c $9 | grep "Output dataset:" | \
    awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
  else
    python checkStatus.py -s $1 -E $2 -p $3 -g $4 -e $5 -P $6 -t $7 -c $9 | grep "Output dataset:" | \
    awk '{print substr($NF,0,length($NF))}' > myGeneration/list.txt
  fi
fi

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
