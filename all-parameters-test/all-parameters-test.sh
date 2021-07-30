#!/bin/bash
# set -x
set -e

cat sed-commands.txt | while read line || [[ -n $line ]];
do
    $("$line")
    # sed -i "s/(volume_buy = ).*/120/" scenario.py;sed -i "s/(lock_method = ).*/1"lock_to_fin"/" scenario.py;sed -i "s/(lock_hour = ).*/13/" scenario.py;sed -i "s/(profit_limit = ).*/12/" scenario.py;sed -i "s/(loss_limit = ).*/1-1/" scenario.py;sed -i "s/(opening_intractions = ).*/1[0, 0, 0, 0]/" scenario.py;sed -i "s/(close_intraction = ).*/1[0, 0, 0, 0, 0]/" scenario.py;
    python3 main.py

    analyzed_o=','$(python3 analyzeOutput/analyze.py only-print)
    echo $analyzed_o

done
