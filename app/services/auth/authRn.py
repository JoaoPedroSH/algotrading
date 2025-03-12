from werkzeug.security import check_password_hash
from flask import (flash, redirect, session, url_for, g)
from app.services.auth.authDto import AuthDto


class AuthRn:
    def __init__(self, request=None):
        self.auth_dto = AuthDto()

        if request is not None:
            self.username = request.form["username"]
            self.password = request.form["password"]


    def register(self):
        error = None

        if not self.username:
            error = "Insira o nome de usuário."
        elif not self.password:
            error = "Insira a senha."

        if error is None:
            try:
                self.auth_dto.register_user(self.username, self.password)
            except Exception as e:
                error = f"Erro ao cadastrar o usuário {self.username}. {e}"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    def login(self):
        user = None
        error = None

        try:
            user = self.auth_dto.get_user(self.username)
        except Exception as e:
            error = f"Erro ao procurar o usuário {self.username}.{e}"

        if user is None:
            error = "Não foi possível encontrar o usuário informado"
        elif not check_password_hash(user["password"], self.password):
            error = "A senha informada está incorreta."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    def load_logged_in_user(self):
        id_user = session.get("user_id")

        if id_user is None:
            g.user = None
        else:
            g.user = (
                self.auth_dto.load_logged_user(id_user)
            )
