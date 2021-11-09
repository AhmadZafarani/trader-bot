# YA FATEMEH
import model.strategy as strategies
from controller.exchange_controller import *
from view.views import log_cndl_mmnt

dollar_balance = scenario.start_of_work_dollar_balance
bitcoin_balance = scenario.start_of_work_crypto_balance
start_of_profit_loss_period_balance = 0
this_moment = Moment(0, 0, 0)
strategy_results = []
working_strategies = []
lock_all = False  # used to locking all strategies


def profit_loss_calculator(moment_index: int, this_moment_price: float) -> float:
    global start_of_profit_loss_period_balance
    x = dollar_balance + bitcoin_balance * this_moment_price
    if (moment_index - 1) % scenario.profit_loss_period_step == 0:
        start_of_profit_loss_period_balance = x
        return 0
    else:
        return round((x - start_of_profit_loss_period_balance) * 100 / start_of_profit_loss_period_balance, 4)


def lock_all_strategies(working_strategies_to_lock: list, moment: Moment, logger):
    crypto = 0
    for ws in working_strategies_to_lock:
        crypto += ws.sell_volume

    price = moment.price
    for ws in working_strategies_to_lock:
        if not ws.sold:
            sell(ws.sell_volume, price)
            ws.finish_strategy(ws.finish_txt)
            if ws.lock_method == "lock_to_fin":
                strategies.lock_strategies.pop(ws.short_name)

    logger.warning(f'all({[x.id for x in working_strategies_to_lock]}) locked in {moment.get_time_string()}')
    logger.info(f'More Details for lock_all : price , Volume = {price} , {crypto}')


def try_strategies(moment: Moment, candles: list, strategy_logger):
    global working_strategies, bitcoin_balance, dollar_balance, lock_all

    for locked in list(strategies.lock_strategies):  # unlock strategies
        if strategies.lock_strategies[locked][1] != 0:
            if strategies.lock_strategies[locked][1] <= moment.timestamp:
                strategy_logger.warning(
                    f'"{strategies.lock_strategies[locked][2]}" unlocked in {moment.get_time_string()}')
                strategies.lock_strategies.pop(locked)

    # remove finished strategies from working_strategies
    working_strategies = [ws for ws in working_strategies if ws.working]

    # lock all strategy if periodical profit loss is reached
    if scenario.periodical_profit_loss_limit["enable"] and not lock_all and len(working_strategies) > 0:
        if moment.profit_loss_percentage >= scenario.periodical_profit_loss_limit['options']['profit_limit']:
            strategy_logger.warning(
                f"periodical profit limit reached in {moment.get_time_string()}")
            lock_all = True
            lock_all_strategies(working_strategies_to_lock=working_strategies, moment=moment, logger=strategy_logger)
        elif moment.profit_loss_percentage <= scenario.periodical_profit_loss_limit['options']['loss_limit']:
            strategy_logger.warning(
                f"periodical loss limit reached in {moment.get_time_string()}")
            lock_all = True
            lock_all_strategies(working_strategies_to_lock=working_strategies, moment=moment, logger=strategy_logger)

    working_strategies = [ws for ws in working_strategies if ws.working]
    for ws in working_strategies:
        strategy_logger.debug(
            f'continuing "{ws.id}" in {moment.get_time_string()}')
        ws.continue_strategy(working_strategies,
                             start_of_profit_loss_period_balance=start_of_profit_loss_period_balance,
                             dollar_balance=dollar_balance)

    if not lock_all:
        for s in strategies.strategies:  # trying to start not locked strategies
            if s not in strategies.lock_strategies:
                strategy_logger.debug(
                    f'working on "{s}" in {moment.get_time_string()}')
                strtg = strategies.strategies[s](
                    moment, bitcoin_balance, dollar_balance, candles, logger=strategy_logger, name=s)
                if strtg.working:
                    working_strategies.append(strtg)

    if lock_all and moment.moment_id % scenario.profit_loss_period_step == 0:
        strategy_logger.warning(
            f'all strategies unlocked in {moment.get_time_string()}')
        lock_all = False


def buy(bitcoin: int, price: int):
    if scenario.live_trading_mode:
        exchange_buy(bitcoin, price)
    #     return

    global bitcoin_balance, dollar_balance
    bitcoin = round(bitcoin, 4)
    bitcoin_balance += bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    dollar_balance -= (bitcoin * price * (1 + scenario.fee))
    dollar_balance = round(dollar_balance, 4)
    if dollar_balance < 0:
        raise RuntimeError('dollar balance is negative')


def sell(bitcoin: int, price: int):
    if scenario.live_trading_mode:
        exchange_sell(bitcoin, price)
    #     return

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


def calculate_indicators_and_bundle_into_candles(candles: list):
    log_debug("constructed candles are:")
    for i in range(len(candles)):
        for func in scenario.live_candle_indicators:
            indic = func(i, candles)
            for k in indic:
                candles[i].__setattr__(k, indic[k])
        log_debug(f"\t{candles[i]}")


def set_this_moment(moment: Moment):
    global this_moment
    this_moment = moment


def analyze_live_data(exchange: ccxt.Exchange, candles: list):
    global this_moment
    this_moment: Moment
    moment_index = 0

    loggers = analyze_first_moment(candles)
    while True:
        log_info(f"working strategies are: {working_strategies}")
        sleep_till_end_of_moment()
        moment_index += 1

        ret = sync_bot_data_with_exchange(exchange, candles, moment_index)
        if ret == SERVER_SIDE_ERROR:
            log_error("moment process failed! => sync_bot_data_with_exchange")
            moment_index -= 1
            this_moment.decrease_moment_id()
            continue

        # this part is for viewing previous moment
        control_live_view(loggers, candles, this_moment, moment_index,
                          bitcoin_balance, dollar_balance, strategy_results)
        try_strategies(this_moment, candles, strategy_logger=loggers[1])


def analyze_first_moment(candles):
    global this_moment
    this_moment: Moment

    calculate_indicators_and_bundle_into_this_moment()
    this_moment.set_profit_loss_percentage(profit_loss_calculator(1, this_moment.price))
    loggers = control_start_live_view()
    log_cndl_mmnt(loggers[0], this_moment, candles)
    try_strategies(this_moment, candles, strategy_logger=loggers[1])
    return loggers


def sleep_till_end_of_moment():
    print(
        f"moment index: {this_moment.moment_id} => sleeping {scenario.live_sleep_between_each_moment} seconds.")
    sleep(scenario.live_sleep_between_each_moment)


def sync_bot_data_with_exchange(exchange: ccxt.Exchange, candles: list, moment_index: int):
    while True:
        ret = sync_last_candles(exchange, candles)
        if ret == SERVER_SIDE_ERROR:
            return SERVER_SIDE_ERROR

        t, p = get_current_data_from_exchange(exchange)
        if t == SERVER_SIDE_ERROR and p == SERVER_SIDE_ERROR:
            return SERVER_SIDE_ERROR

        this_moment.update_moment(
            t / 1000.0, p, candles[-1].identifier, profit_loss_calculator(moment_index + 1, p), moment_index)
        calculate_indicators_and_bundle_into_this_moment()
        return


def calculate_indicators_and_bundle_into_this_moment():
    # TODO: fill here!
    global this_moment
    log_debug(f"constructed this_moment: {this_moment}")


def sync_last_candles(exchange: ccxt.Exchange, candles: list):
    new_candles = get_n_past_candles(
        exchange, scenario.live_start_of_work_needed_candles, 1, handle_failure=False)
    if new_candles == SERVER_SIDE_ERROR:
        return SERVER_SIDE_ERROR

    candles.clear()
    for c in new_candles:
        candles.append(c)
    calculate_indicators_and_bundle_into_candles(candles)
