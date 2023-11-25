import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
from app.services.socket import socket
from app.services.panel import model
import pandas as pd
import pytz


async def executeConfig(id_conf):
    socket.loadingConfig("Buscando dados da configuração")
    data_config = model.getConfigsUnique(id_conf)

    for config in data_config:
        (
            id,
            user_id,
            account_mt5,
            server_mt5,
            password_mt5,
            symbol,
            period,
            status,
            created,
        ) = config

    socket.loadingConfig("Realizando Login")
    loggedAccountMt5(account_mt5, server_mt5, password_mt5)

    socket.loadingConfig("Selecionando ativo")
    selectSymbolMt5(symbol)

    socket.loadingConfig("Pegando dados do ativo")
    infoTicksSymbol(symbol)

    socket.loadingConfig("Concluido")

    return True


def initializeMt5():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        mt5.shutdown()
        return False
    return True


def loggedAccountMt5(account, server, password):
    if not mt5.initialize(login=account, server=server, password=password):
        print("initialize and login() failed, error code =", mt5.last_error())
        mt5.shutdown()
        return False
    return True


def getSymbolsMt5():
    initializeMt5()
    year_now = datetime.now().strftime("%y")
    symbols = mt5.symbols_get(group=f"WIN*{year_now}, WDO*{year_now}")
    return symbols


def selectSymbolMt5(symbol):
    initializeMt5()
    selected = mt5.symbol_select(symbol, True)
    if not selected:
        print(f"Failed to select {symbol}, error code =", mt5.last_error())
        return False
    return True


def infoTicksSymbol(symbol):
    initializeMt5()

    current_utc_time = datetime.now(timezone.utc)
    two_days_ago = current_utc_time - timedelta(days=90)
    utc_to = current_utc_time
    utc_from = two_days_ago

    print(current_utc_time)

    ticks = mt5.copy_ticks_range(symbol, utc_from, utc_to, mt5.COPY_TICKS_ALL)
    print("Ticks received:", len(ticks))

    ticks_frame = pd.DataFrame(ticks)
    ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

    print("\nDisplay dataframe with ticks")
    print(ticks_frame.head(1))
    return True


def orderOpen():
    import time
    import MetaTrader5 as mt5

    # display data on the MetaTrader 5 package
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    # prepare the buy request structure
    symbol = "WINZ23"
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()

    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, exit", symbol)
            mt5.shutdown()
            quit()

    lot = 0.1
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print(
        "1. order_send(): by {} {} lots at {} with deviation={} points".format(
            symbol, lot, price, deviation
        )
    )
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print(
                        "       traderequest: {}={}".format(
                            tradereq_filed, traderequest_dict[tradereq_filed]
                        )
                    )
        print("shutdown() and quit")
        mt5.shutdown()
        quit()

    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))
    time.sleep(2)


orderOpen()


def orderClose():
    # create a close request
    symbol = "WINZ23"
    lot = 0.1
    position_id = result.order
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print(
        "3. close position #{}: sell {} {} lots at {} with deviation={} points".format(
            position_id, symbol, lot, price, deviation
        )
    )
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result", result)
    else:
        print("4. position #{} closed, {}".format(position_id, result))
        # request the result as a dictionary and display it element by element
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print(
                        "       traderequest: {}={}".format(
                            tradereq_filed, traderequest_dict[tradereq_filed]
                        )
                    )
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
