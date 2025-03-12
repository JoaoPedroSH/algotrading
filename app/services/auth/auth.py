import functools
from flask import (Blueprint, g, redirect, render_template, request, session, url_for)
from app.services.auth.authRn import AuthRn

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        auth_rn = AuthRn(request)
        auth_rn.register()

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        auth_rn = AuthRn(request)
        auth_rn.login()

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    auth_rn = AuthRn()
    auth_rn.load_logged_in_user()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
