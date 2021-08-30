#!/bin/bash 
# set -x
# set -e

echo "expected,variance" > all-parameters-test/test-variance-and-expected-$1.csv
cat all-parameters-test/sed-commands-$1.txt | while read line;
do
    eval $line
    python3 main.py
    analyzed_o=$(python3 analyze-output/analyze.py only-print)
    echo $analyzed_o >> all-parameters-test/test-variance-and-expected-$1.csv
done
