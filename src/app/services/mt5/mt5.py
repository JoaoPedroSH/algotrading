import MetaTrader5 as mt5

from dotenv import load_dotenv

import os

from datetime import datetime

load_dotenv()


def initializeMt5():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        mt5.shutdown()
        return False
    return True


def loggedAccountMt5():
    """login = os.getenv("login")
    server = os.getenv("server")
    passwordmt5 = os.getenv("password")"""
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        mt5.shutdown()
        return False
    return True


def getSymbolsMt5():
    initializeMt5()
    year_now = datetime.now().strftime("%y")
    symbols=mt5.symbols_get(group=f"WIN*{year_now}, WDO*{year_now}")
    return symbols


def selectSymbolMt5(symbol):
    initializeMt5()
    selected=mt5.symbol_select(symbol,True)
    if not selected:
        print("Failed to select EURCAD, error code =",mt5.last_error())
        return False
    return True


def infoTicksSymbol(symbol):
    initializeMt5()
    lasttick=mt5.symbol_info_tick(symbol)
    return lasttick
""" Falta buscar os ticks anteriores ao inves de um """
    
def execModelIA():
    initializeMt5()
    infoTicksSymbol("WINZ23")
    selectSymbolMt5("WINZ23")