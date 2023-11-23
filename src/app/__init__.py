import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from .services.db import db

    db.init_app(app)

    from .services.auth import auth

    app.register_blueprint(auth.bp)

    from .services.orders import orders

    app.register_blueprint(orders.bp)
    app.add_url_rule("/", endpoint="index")

    return app


""" import pandas as pd
from datetime import datetime
import time
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os

load_dotenv()

login = os.getenv("login")
server = os.getenv("server")

if not mt5.initialize():
    print("Inicialização do MT5 falhou!")
    mt5.shutdown()

#Listando Ativos
ativos = mt5.symbols_get()
print(len(ativos))
for i in range(10):
    print(ativos[i].name)
    
#Obtendo cotações
def get_info_ativo(ativo, timeframe, n):
    ativo = mt5.copy_rates_from_pos(ativo, timeframe, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit='s')
    ativo.set_index('time', inplace=True)
    return ativo
print(get_info_ativo('WIN$', mt5.TIMEFRAME_M1, 5))

#Valor em tempo real
tempo = time.time() + 10
while time.time() < tempo:
    tick = mt5.symbol_info_tick('WIN$')._asdict()
    print(f"WIN$ - last:{tick['last']}, bid:{tick['bid']}, ask:{tick['ask']}")
    time.sleep(0.5)
    
#Enviar ordens """
