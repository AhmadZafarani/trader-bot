# YA FATEMEH
from csv import reader
from model.Candle import Candle
from model.Moment import Moment
import model.strategy as strategies
from controller.view_controller import control_views, check_view_essentials, view_before_trade
from scenario import scenario
from controller.logs import setup_logger, get_logger
from futures_controller import position, future_balance


dollar_balance = scenario.start_of_work_dollar_balance
bitcoin_balance = scenario.start_of_work_crypto_balance
start_of_profit_loss_period_balance = 0
this_moment = Moment(0, 0, 0)
strategy_results = []
working_strategies = []
lock_all = False  # used to locking all strategies
till_end = False


def open_extra_files(extra_files: dict) -> list:
    files = []
    for file in extra_files:
        csv_file = open(extra_files[file])
        files.append(list(reader(csv_file)))
    return files


def candle_maker(candles_data: list, i: int, files: list) -> Candle:
    fields = [f for f in candles_data[i]]
    c = Candle(i, float(fields[0]), float(fields[1]), float(
        fields[2]), float(fields[3]), float(fields[4]))
    for file in files:
        field_names = file[0]
        field_length = len(field_names)
        fields = [f for f in file[i]]

        for j in range(field_length):
            c.__setattr__(field_names[j], float(fields[j]))
    return c


def data_converter(candles_file: str, extra_candle_files: dict) -> list:
    files = open_extra_files(extra_candle_files)

    candles = []
    with open(candles_file) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        candles_data = list(csv_reader)
        candles_number = len(candles_data)
        for i in range(1, candles_number):
            c = candle_maker(candles_data, i, files)
            candles.append(c)
    return candles


def bundle_extra_fields_into_this_moment(moments_extra_files: list, moment_index: int):
    for file in moments_extra_files:
        field_names = file[0]
        field_length = len(field_names)
        fields = [f for f in file[moment_index]]

    for j in range(field_length):
        this_moment.__setattr__(field_names[j], float(fields[j]))


def analyze_each_moment(csv_reader: list, moment_index: int, moments_extra_files: list, candle: Candle, candles: list):
    time, price, volume = csv_reader[moment_index]        # volume MAY be used!
    price = float(price)
    time = int(time) // 1000

    profit_loss_percentage = profit_loss_calculator(moment_index, price)
    this_moment.update_moment(
        time, price, candle.identifier, profit_loss_percentage, moment_index)
    position.calculate_pnl(price)

    bundle_extra_fields_into_this_moment(moments_extra_files, moment_index)

    viewed = view_before_trade(this_moment, moment_index,
                               bitcoin_balance, dollar_balance)

    try_strategies(this_moment, candles)

    if not viewed:
        check_view_essentials(this_moment, moment_index,
                              bitcoin_balance, dollar_balance)


def analyze_data(candles: list, csv_file_name: str, moments_extra_files: dict):
    files = open_extra_files(moments_extra_files)
    setup_logger('log1', r'logs/cndl-mmnt.log')
    log1 = get_logger('log1')

    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        moments_data = list(csv_reader)
        moment_index = 1
        for c in candles:
            log1.info(c)
            for _ in range(scenario.number_of_moments_in_a_candle):
                analyze_each_moment(
                    moments_data, moment_index, files, c, candles)
                moment_index += 1
                log1.info(f"    {this_moment}")

            # print('Analyzing :', round(100 * c.identifier / len(candles), 2), '%')
        control_views(strategy_results)


def profit_loss_calculator(moment_index: int, this_moment_price: float) -> float:
    global start_of_profit_loss_period_balance
    x = dollar_balance + bitcoin_balance * this_moment_price
    if (moment_index - 1) % scenario.profit_loss_period_step == 0:
        start_of_profit_loss_period_balance = x
        return 0
    else:
        return round((x - start_of_profit_loss_period_balance) * 100 / start_of_profit_loss_period_balance, 4)


def lock_all_strategies(working_strategies: list, moment: Moment, start_of_profit_loss_period_balance: int, dollar: int, profit_loss: int):
    crypto1 = 0
    for ws in working_strategies:
        crypto1 += ws.sell_volume
    price = ((start_of_profit_loss_period_balance *
              (1 + profit_loss/100)) - dollar) / crypto1

    for ws in working_strategies:
        if not ws.sold:
            sell(ws.sell_volume, price)
            ws.finish_strategy(ws.finish_txt)
            if ws.lock_method == "lock_to_fin":
                strategies.lock_strategies.pop(ws.short_name)


def get_global_profit_loss(price):
    global bitcoin_balance, dollar_balance
    money = dollar_balance + bitcoin_balance*price
    return round(100*(money - scenario.start_of_work_dollar_balance) / scenario.start_of_work_dollar_balance, 3)


def try_strategies(moment: Moment, candles: list):
    global working_strategies, bitcoin_balance, dollar_balance, lock_all, till_end, position, future_balance

    if till_end:
        return
    for locked in list(strategies.lock_strategies):       # unlock strategies
        if strategies.lock_strategies[locked][1] != 0:
            if strategies.lock_strategies[locked][1] == moment.candle_id:
                strategies.lock_strategies.pop(locked)

    # remove finished strategies from working_strategies
    if scenario.global_limit:
        if get_global_profit_loss(moment.price) >= scenario.global_profit_limit:
            till_end = True
            lock_all_strategies(
                working_strategies=working_strategies, moment=moment, start_of_profit_loss_period_balance=scenario.start_of_work_dollar_balance, dollar=dollar_balance, profit_loss=scenario.global_profit_limit)
            return
        if get_global_profit_loss(moment.price) <= scenario.global_loss_limit:
            till_end = True
            lock_all_strategies(
                working_strategies=working_strategies, moment=moment, start_of_profit_loss_period_balance=scenario.start_of_work_dollar_balance, dollar=dollar_balance, profit_loss=scenario.global_loss_limit)

    working_strategies = [ws for ws in working_strategies if ws.working]
    # lock all strategy if periodical profit loss is reached

    if scenario.periodical_profit_loss_limit["enable"] and not lock_all and len(working_strategies) > 0:
        if moment.profit_loss_percentage >= scenario.periodical_profit_loss_limit['options']['profit_limit']:
            lock_all = True
            lock_all_strategies(
                working_strategies=working_strategies, moment=moment, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar=dollar_balance, profit_loss=scenario.periodical_profit_loss_limit['options']['profit_limit'])
        elif moment.profit_loss_percentage <= scenario.periodical_profit_loss_limit['options']['loss_limit']:
            lock_all = True
            lock_all_strategies(
                working_strategies=working_strategies, moment=moment, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar=dollar_balance, profit_loss=scenario.periodical_profit_loss_limit['options']['loss_limit'])

    working_strategies = [ws for ws in working_strategies if ws.working]
    for ws in working_strategies:
        ws.continue_strategy(
            working_strategies, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar_balance=dollar_balance)

    if not lock_all:
        for s in strategies.strategies:     # trying to start not locked strategies
            if not s in strategies.lock_strategies:
                strtg = strategies.strategies[s](
                    moment, bitcoin_balance, dollar_balance, candles, future_balance)
                if strtg.working:
                    working_strategies.append(strtg)

    if lock_all and moment.moment_id % scenario.profit_loss_period_step == 0:
        lock_all = False


def buy(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin = round(bitcoin, 4)
    bitcoin_balance += bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    dollar_balance -= (bitcoin * price * (1 + scenario.fee))
    dollar_balance = round(dollar_balance, 4)
    if dollar_balance < 0:
        raise RuntimeError('dollar balance is negative')


def sell(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin = round(bitcoin, 4)
    bitcoin_balance -= bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    if bitcoin_balance < 0:
        raise RuntimeError('bitcoin balance is negative')
    dollar_balance += (bitcoin * price * (1 - scenario.fee))
    dollar_balance = round(dollar_balance, 4)


def get_this_moment() -> Moment:
    return this_moment


def set_report(r: str):
    strategy_results.append(r)
