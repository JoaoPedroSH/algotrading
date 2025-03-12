def checkformCreate(request):
    account_mt5 = request["account_mt5"]
    server_mt5 = request["server_mt5"]
    password_mt5 = request["password_mt5"]
    symbol = request["symbol"]
    period = request["period"]

    error = None
    
    if not account_mt5:
        error = "Conta obrigatória!"
        return {True}
    if not server_mt5:
        error = "Servidor obrigatório!"
    if not password_mt5:
        error = "Senha obrigatória!"
    if not symbol:
        error = "Ativo obrigatório!"
    if not period:
        error = "Período obrigatório!"
        
    return error