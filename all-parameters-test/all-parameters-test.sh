#!/bin/bash 
# set -x
# set -e
echo "expected,variance" > variance_and_expected.csv
cat sed-commands.txt | while read line;
do  
    eval $line
    python3 main.py
    analyzed_o=$(python3 analyzeOutput/analyze.py only-print)
    echo $analyzed_o >> variance_and_expected.csv
done
