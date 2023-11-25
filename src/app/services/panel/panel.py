from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort

from app.services.auth.auth import login_required
from app.services.db.db import get_db

from app.services.mt5 import mt5
from app.services.panel import model
from app.services.panel import controller

bp = Blueprint("panel", __name__)


@bp.route("/")
def index():
    configs = model.getConfigs()
    initMt5 = mt5.initializeMt5()
    if not configs:
        flash("Nenhum configuração criada!")
    return render_template("panel/index.html", configs=configs, initMt5=initMt5)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        check_form = controller.checkformCreate(request.form)
        error = check_form

        if error is not None:
            flash(error)
        else:
            try:
                model.postNewConfig(g.user["id"], request)
                return redirect(url_for("panel.index"))
            except Exception as e:
                flash(
                    f"Não foi possível inserir uma nova configuração. Entre em contato com o suporte! {e}"
                )

    symbols = mt5.getSymbolsMt5()
    return render_template("panel/create_config.html", symbols=symbols)


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("panel.index"))

    return render_template("panel/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("panel.index"))

import asyncio
@bp.route("/<int:id>/execute")
@login_required
def execute(id):
    exec = asyncio.run(mt5.executeConfig(id))
    if not exec:
        flash(
            f"Erro ao tentar executar a configuração. Entre em contato com o suporte!"
        )
    return redirect(url_for("panel.index"))


