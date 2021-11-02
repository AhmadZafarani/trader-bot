#!/bin/sh
RED='\033[0;31m'
NC='\033[0m'        # No Color
GREEN='\033[0;32m'  # Green
Purple='\033[0;35m' # Purple
Cyan='\033[0;36m'   # Cyan

echo "backing up data and scenario ..."
mkdir tmp
cp -r ../data tmp/data
cp ../scenario.py tmp/scenario.py
cp ../model/strategy.py tmp/strategy.py

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"
echo "Testing Candle_and_moment_syncing ..."
echo -n "test1 : "

cp Candle_and_moment_syncing_test/test1/scenario.py ../../trader-bot/scenario.py

cp Candle_and_moment_syncing_test/test1/strategy.py ../../trader-bot/model/strategy.py

cp Candle_and_moment_syncing_test/test1/BTC-100-1h-candles.csv ../../trader-bot/data/BTC-100-1h-candles.csv
cp Candle_and_moment_syncing_test/test1/BTC-100-1h-moment.csv ../../trader-bot/data/BTC-100-1h-moment.csv

# cp Candle_and_moment_syncing_test/test1/Moment.py ../model/Moment.py

cd ../../trader-bot/

python main.py >/dev/null

cd code-test/

cmp Candle_and_moment_syncing_test/test1/cndl-mmnt.log ../../trader-bot/logs/cndl-mmnt.log

e=$?

if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi

if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../../trader-bot/data/BTC-100-1h-candles.csv

rm ../../trader-bot/data/BTC-100-1h-moment.csv

echo -n "test2 : "

cp Candle_and_moment_syncing_test/test2/scenario.py ../../trader-bot/scenario.py

cp Candle_and_moment_syncing_test/test2/strategy.py ../../trader-bot/model/strategy.py

cp Candle_and_moment_syncing_test/test2/BTC-15m-10-mmnt.csv ../../trader-bot/data/

cp Candle_and_moment_syncing_test/test2/BTC-15m-10-cndl.csv ../../trader-bot/data/

cd ../../trader-bot/

python main.py >/dev/null

cd code-test

cmp --silent Candle_and_moment_syncing_test/test2/cndl-mmnt.log ../../trader-bot/logs/cndl-mmnt.log
e=$?
if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi
if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../../trader-bot/data/BTC-15m-10-mmnt.csv
rm ../../trader-bot/data/BTC-15m-10-cndl.csv

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"

echo "Testing candles_extra_fields ..."

cp ./candles_extra_fields/BTC-100-1h-candles.csv ../data/BTC-100-1h-candles.csv
cp ./candles_extra_fields/BTC-100-1h-moment.csv ../data/BTC-100-1h-moment.csv
cp ./candles_extra_fields/BTC_100_1h_ADX.csv ../data/BTC_100_1h_ADX.csv
cp ./candles_extra_fields/BTC_100_1h_ICHI.csv ../data/BTC_100_1h_ICHI.csv
cp ./candles_extra_fields/scenario.py ../scenario.py
cp ./candles_extra_fields/strategy.py ../model/strategy.py

cd ..

python main.py >/dev/null

cd code-test

echo -n "test1 : "
cmp --silent ./candles_extra_fields/cndl-extra.log ../logs/cndl-extra.log

e=$?
if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi
if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC-100-1h-candles.csv
rm ../data/BTC-100-1h-moment.csv
rm ../data/BTC_100_1h_ADX.csv
rm ../data/BTC_100_1h_ICHI.csv
rm ../logs/cndl-extra.log

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"
echo "Testing moments_extra_fields"
cp ./moments_extra_fields/BTC-100-1h-candles.csv ../data/BTC-100-1h-candles.csv
cp ./moments_extra_fields/BTC-100-1h-moment.csv ../data/BTC-100-1h-moment.csv
cp ./moments_extra_fields/BTC_100_1h_ADX.csv ../data/BTC_100_1h_ADX.csv
cp ./moments_extra_fields/BTC_100_1h_ICHI.csv ../data/BTC_100_1h_ICHI.csv
cp ./moments_extra_fields/scenario.py ../scenario.py
cp ./moments_extra_fields/strategy.py ../model/strategy.py

cd ..

python main.py >/dev/null

cd code-test

echo -n "test1 : "
cmp --silent ./moments_extra_fields/mmnt-extra.log ../logs/mmnt-extra.log
e=$?
if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi
if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC-100-1h-candles.csv
rm ../data/BTC-100-1h-moment.csv
rm ../data/BTC_100_1h_ADX.csv
rm ../data/BTC_100_1h_ICHI.csv
rm ../logs/mmnt-extra.log

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"

echo "Testing lock_mechanism ..."
cp ./lock_mechanism/lock_to_fin/BTC_2021_15m_cndl.csv ../data/BTC_2021_15m_cndl.csv
cp ./lock_mechanism/lock_to_fin/BTC_2021_1m_mmnt.csv ../data/BTC_2021_1m_mmnt.csv
cp ./lock_mechanism/lock_to_fin/scenario.py ../scenario.py
cp ./lock_mechanism/lock_to_fin/strategy.py ../model/strategy.py
cd ..
python main.py >/dev/null
cd code-test
echo -n "lock_to_fin: "
cmp --silent ./lock_mechanism/lock_to_fin/strategy_results.txt ../strategy_results.txt
e=$?
if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi
if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC_2021_15m_cndl.csv
rm ../data/BTC_2021_1m_mmnt.csv
rm ../strategy_results.txt

echo -n "lock_to_cndl:"
cp ./lock_mechanism/lock_to_hour/BTC_2021_15m_cndl.csv ../data/BTC_2021_15m_cndl.csv
cp ./lock_mechanism/lock_to_hour/BTC_2021_1m_mmnt.csv ../data/BTC_2021_1m_mmnt.csv
cp ./lock_mechanism/lock_to_hour/scenario.py ../scenario.py
cp ./lock_mechanism/lock_to_hour/strategy.py ../model/strategy.py
cd ..
python main.py >/dev/null
cd code-test
cmp --silent ./lock_mechanism/lock_to_hour/strategy_results.txt ../strategy_results.txt
e=$?
if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi
if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC_2021_15m_cndl.csv
rm ../data/BTC_2021_1m_mmnt.csv
rm ../strategy_results.txt

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"
echo "Testing periodical profit loss log"
cp ./periodical_profit_loss_log/test1/BTC_2021_15m_cndl.csv ../data/BTC_2021_15m_cndl.csv
cp ./periodical_profit_loss_log/test1/BTC_2021_1m_mmnt.csv ../data/BTC_2021_1m_mmnt.csv
cp ./periodical_profit_loss_log/test1/scenario.py ../scenario.py
cp ./periodical_profit_loss_log/test1/strategy.py ../model/strategy.py

cd ..

python main.py >/dev/null
echo -n "test1: "
cd code-test
cmp --silent ./periodical_profit_loss_log/test1/periodical_report.csv ../periodical_report.csv

e=$?

if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi

if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC_2021_15m_cndl.csv
rm ../data/BTC_2021_1m_mmnt.csv
rm ../periodical_report.csv
echo -n "test2: "
cp ./periodical_profit_loss_log/test2/BTC_2021_15m_cndl.csv ../data/BTC_2021_15m_cndl.csv
cp ./periodical_profit_loss_log/test2/BTC_2021_1m_mmnt.csv ../data/BTC_2021_1m_mmnt.csv
cp ./periodical_profit_loss_log/test2/scenario.py ../scenario.py
cp ./periodical_profit_loss_log/test2/strategy.py ../model/strategy.py

cd ..
python main.py >/dev/null
cd code-test
cmp --silent ./periodical_profit_loss_log/test2/periodical_report.csv ../periodical_report.csv
e=$?

if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi

if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC_2021_15m_cndl.csv
rm ../data/BTC_2021_1m_mmnt.csv
rm ../periodical_report.csv

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"
echo "Testing balance log ... "

cp ./balance_log/BTC_2021_15m_cndl.csv ../data/BTC_2021_15m_cndl.csv
cp ./balance_log/BTC_2021_1m_mmnt.csv ../data/BTC_2021_1m_mmnt.csv
cp ./balance_log/scenario.py ../scenario.py
cp ./balance_log/strategy.py ../model/strategy.py

cd ..
python main.py >/dev/null
cd code-test

echo -n "test1: "
cmp --silent ./balance_log/balance_report.csv ../balance_report.csv
e=$?

if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi

if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC_2021_15m_cndl.csv
rm ../data/BTC_2021_1m_mmnt.csv
rm ../balance_report.csv

echo -e "${Cyan}++++++++++++++++++++++++++++++++++++++++++++++++${NC}"
echo "Testing momental periodical profit loss "
cp ./momental_pediodical_profit/BTC_2021_15m_cndl.csv ../data/BTC_2021_15m_cndl.csv
cp ./momental_pediodical_profit/BTC_2021_1m_mmnt.csv ../data/BTC_2021_1m_mmnt.csv
cp ./momental_pediodical_profit/scenario.py ../scenario.py
cp ./momental_pediodical_profit/strategy.py ../model/strategy.py
cd ..
python main.py >/dev/null
cd code-test
echo -n "test1:"

cmp --silent ./momental_pediodical_profit/cndl-mmnt.log ../logs/cndl-mmnt.log

e=$?

if [ $e -eq 1 ]; then
    echo -e "${RED}Failed!${NC}"
fi

if [ $e -eq 0 ]; then
    echo -e "${GREEN}Done!${NC}"
fi

rm ../data/BTC_2021_15m_cndl.csv
rm ../data/BTC_2021_1m_mmnt.csv
rm ../logs/cndl-mmnt.log

################################################################################################
echo "restoring data"
cp -r tmp/data ../
cp tmp/scenario.py ../scenario.py
cp tmp/strategy.py ../model/strategy.py

rm -r tmp/
