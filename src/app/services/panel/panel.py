from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.services.auth.auth import login_required
from app.services.db.db import get_db

from app.services.mt5.mt5 import getSymbolsMt5
from app.services.mt5.mt5 import initializeMt5

bp = Blueprint("panel", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    
    initMt5 = initializeMt5()
            
    return render_template("panel/index.html", posts=posts, initMt5=initMt5)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    
    if request.method == "POST":
        from app.services.panel.controller import checkformCreate
        
        check_form = checkformCreate(request.form)
        error = check_form
        
        if error is not None:
            flash(error)
        else:
            from app.services.panel.model import postNewConfig
            
            try:
                postNewConfig(g.user["id"], request)
                return redirect(url_for("panel.index"))
            except Exception as e:
                flash("Não foi possível inserir uma nova configuração. Entre em contato com o suporte!")

    symbols = getSymbolsMt5()
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
