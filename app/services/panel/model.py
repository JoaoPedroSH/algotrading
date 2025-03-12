from app.services.db.db import get_db



def getConfigsUnique(id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id, c.user_id, account_mt5, server_mt5, password_mt5, symbol, period, status, created
            FROM config c
            JOIN user u ON c.user_id = u.id
            WHERE c.id = %s
            ORDER BY created DESC
            """,
            (id,)
        )
        config = cursor.fetchone()
        cursor.close()
        db.close()
        return config
    except Exception as e:
        print(f"Erro ao tentar buscar as configurações com id = {id}: {e}")

def getConfigs():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT c.id, c.user_id, account_mt5, server_mt5, symbol, period, status, created "
            "FROM config c JOIN user u ON c.user_id = u.id "
            "ORDER BY created DESC"
        )
        configs = cursor.fetchall()
        cursor.close()
        return configs
    except Exception as e:
        print(f"Erro ao tentar buscar as configurações: {e}")


def postNewConfig(idUser, request):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO config (user_id, account_mt5, server_mt5, password_mt5, symbol, period, status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
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
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao tentar inserir nova configuração: {e}")
        return False

