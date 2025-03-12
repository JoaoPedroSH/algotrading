from flask import Flask, Blueprint, render_template, url_for

bp = Blueprint("landingPage", __name__)

@bp.route("/")
def index():
    return render_template("landingPage/index.html")

@bp.route("/login")
def login():
    return render_template("auth/login.html")

@bp.route("/register")
def register():
    return render_template("auth/register.html")