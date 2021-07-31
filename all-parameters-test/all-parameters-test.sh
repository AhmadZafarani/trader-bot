#!/bin/bash
set -x
set -e

head sed-commands.txt | while read line || [[ -n $line ]];
do
    $("$line")
    python3 main.py
    analyzed_o=','$(python3 analyzeOutput/analyze.py only-print)
    echo $analyzed_o
done
