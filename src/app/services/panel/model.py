from app.services.db.db import get_db

def postNewConfig(idUser, request):
    try:
        db = get_db()
        db.execute(
            "INSERT INTO config (user_id, account_mt5, server_mt5, password_mt5, symbol, period, status)" " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (idUser, request["account_mt5"], request["server_mt5"], request["password_mt5"], request["symbol"], request["period"], 0),
        )
        db.commit()
    except Exception as e:
        print(f"Erro ao tentar inserir nova configuração: {e}")

