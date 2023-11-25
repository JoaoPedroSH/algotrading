from app.services.db.db import get_db

def getConfigs():
    try:
        db = get_db()
        configs = db.execute(
            "SELECT c.id, c.user_id, account_mt5, server_mt5, symbol, period, status, created"
            " FROM config c JOIN user u ON c.user_id = u.id"
            " ORDER BY created DESC"
        ).fetchall()
        return configs
    except Exception as e:
        print(f"Erro ao tentar buscar as configurações: {e}")

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

