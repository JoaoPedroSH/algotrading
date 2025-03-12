from app.services.db.db import get_db


def getConfigsUnique(id):
    try:
        db = get_db()
        configs = db.execute(
            "SELECT c.id, c.user_id, account_mt5, server_mt5, password_mt5, symbol, period, status, created"
            " FROM config c JOIN user u ON c.user_id = u.id"
            " WHERE c.id = :id"
            " ORDER BY created DESC",
            {"id": id}
        ).fetchall()
        return configs
    except Exception as e:
        print(f"Erro ao tentar buscar as configurações com id = {id}: {e}")

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
            "INSERT INTO config (user_id, account_mt5, server_mt5, password_mt5, symbol, period, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                idUser,
                request.form["account_mt5"],
                request.form["server_mt5"],
                request.form["password_mt5"],
                request.form["symbol"],
                request.form["period"],
                0,
            ),
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao tentar inserir nova configuração: {e}")
        return False

